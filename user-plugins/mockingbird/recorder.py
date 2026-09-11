"""Microphone capture via ffmpeg/avfoundation, with pause/resume.

The Mockingbird flow needs an iterative recorder: record, pause, resume,
re-record. ffmpeg cannot pause a live capture, so pause is modeled as
*segmented capture* — every resume starts a new PCM segment file and the
segments are concatenated (losslessly, PCM → PCM) on stop.

Design notes:

* Only one ffmpeg process exists at a time; graceful shutdown is done by
  writing ``q`` to its stdin so the WAV muxer finalizes the header. A
  terminate/kill ladder backs that up.
* Capture format is fixed at 16 kHz mono s16le — exactly what whisper-cpp
  wants — so no resampling surprises at transcription time.
* Devices are discovered by parsing ``ffmpeg -list_devices``; the choice can
  be forced with ``SPRUCE_MOCKINGBIRD_MIC`` (name substring or index).

All failures raise :class:`RecorderError` with a human-readable message;
the UI layer decides how to present them.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path
from typing import List, Optional

#: Capture format shared by every segment and the final master WAV.
SAMPLE_RATE = 16000
CHANNELS = 1

_GRACEFUL_STOP_WAIT = 5.0  # seconds to wait for ffmpeg to finalize a segment
_MIN_SEG_SECONDS = 0.3  # below this a segment is considered empty

_FFMPEG_DEVICE_TIMEOUT = 10.0


class RecorderError(RuntimeError):
    """Raised for any microphone-capture failure the user should see."""


def ffmpeg_binary() -> str:
    ffmpeg = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    if not Path(ffmpeg).exists():
        raise RecorderError("ffmpeg not found. Install it with: brew install ffmpeg")
    return ffmpeg


def list_audio_devices() -> List[str]:
    """Return readable names of available macOS audio input devices."""
    cmd = [
        ffmpeg_binary(),
        "-hide_banner",
        "-f",
        "avfoundation",
        "-list_devices",
        "true",
        "-i",
        "",
    ]
    # ffmpeg exits non-zero for -list_devices; the device table is on stderr.
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=_FFMPEG_DEVICE_TIMEOUT
    )
    devices: List[str] = []
    in_audio = False
    for line in proc.stderr.splitlines():
        if "AVFoundation audio devices" in line:
            in_audio = True
            continue
        if "AVFoundation video devices" in line:
            in_audio = False
            continue
        if in_audio:
            match = re.search(r"\[(\d+)\]\s+(.+)$", line)
            if match:
                devices.append(match.group(2).strip())
    return devices


def resolve_mic_index() -> int:
    """Pick an avfoundation audio device index.

    Honors ``SPRUCE_MOCKINGBIRD_MIC``: an integer is used as the raw
    avfoundation index; any other value is matched (case-insensitively)
    against device names as a substring. Defaults to the first device.
    """
    devices = list_audio_devices()
    preference = os.environ.get("SPRUCE_MOCKINGBIRD_MIC", "").strip()

    if preference:
        if preference.isdigit() and int(preference) < 64:
            return int(preference)
        for idx, name in enumerate(devices):
            if preference.lower() in name.lower():
                return idx
        raise RecorderError(
            f"No audio device matching {preference!r}. "
            f"Found: {devices or '(none — check microphone permission)'}"
        )

    if not devices:
        raise RecorderError(
            "No audio input devices found. Check macOS "
            "System Settings → Privacy & Security → Microphone."
        )
    return 0


class MicRecorder:
    """Segmented microphone recorder.

    Usage::

        rec = MicRecorder(session_dir)
        rec.start()
        rec.pause()      # optional, any number of times
        rec.resume()
        master = rec.stop()      # -> path to one 16 kHz mono WAV
        # or: rec.cancel()
    """

    def __init__(self, session_dir: Path) -> None:
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self._proc: Optional[subprocess.Popen] = None
        self._segments: List[Path] = []
        self._seg_started: Optional[float] = None
        self._accumulated = 0.0  # seconds captured before the current segment
        self._paused = False

    # -- state ------------------------------------------------------------

    @property
    def paused(self) -> bool:
        return self._paused

    @property
    def elapsed(self) -> float:
        """Seconds of usable audio captured so far."""
        if self._seg_started is not None:
            return self._accumulated + (time.monotonic() - self._seg_started)
        return self._accumulated

    @property
    def captured_bytes(self) -> int:
        total = 0
        for seg in self._segments:
            try:
                total += seg.stat().st_size
            except OSError:
                continue
        return total

    # -- control ----------------------------------------------------------

    def start(self) -> None:
        """Begin capturing the first segment."""
        if self._proc is not None:
            raise RecorderError("Recorder already running")
        self._start_segment()

    def pause(self) -> None:
        """Finalize the current segment and stop capturing."""
        if self._proc is None or self._paused:
            return
        self._finish_segment()
        self._paused = True

    def resume(self) -> None:
        """Start a new segment after a pause."""
        if self._proc is not None or not self._paused:
            return
        self._paused = False
        self._start_segment()

    def stop(self) -> Path:
        """Finish capture and return the master WAV path."""
        if self._proc is not None:
            self._finish_segment()
        self._paused = False
        if not self._segments:
            raise RecorderError("Nothing was recorded")
        if self.elapsed < _MIN_SEG_SECONDS:
            raise RecorderError("Recording was too short to be usable")
        return self._concat()

    def cancel(self) -> None:
        """Abort capture, kill any live process, delete segments."""
        self._kill_current()
        for seg in self._segments:
            seg.unlink(missing_ok=True)
        self._segments.clear()
        self._accumulated = 0.0
        self._seg_started = None

    # -- internals ---------------------------------------------------------

    def _start_segment(self) -> None:
        seg_path = self.session_dir / f"segment_{len(self._segments):03d}.wav"
        cmd = [
            ffmpeg_binary(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "avfoundation",
            "-i",
            f":{resolve_mic_index()}",
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            str(CHANNELS),
            "-y",
            str(seg_path),
        ]
        try:
            self._proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise RecorderError(f"Could not start ffmpeg: {exc}") from exc
        self._seg_started = time.monotonic()
        self._segments.append(seg_path)

    def _finish_segment(self) -> None:
        """Gracefully stop the live ffmpeg so the WAV header is finalized."""
        proc, self._proc = self._proc, None
        if proc is None:
            return
        try:
            if proc.stdin:
                proc.stdin.write(b"q\n")
                proc.stdin.flush()
                proc.stdin.close()
        except OSError:
            pass
        try:
            proc.wait(timeout=_GRACEFUL_STOP_WAIT)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                proc.kill()
        if self._seg_started is not None:
            self._accumulated += time.monotonic() - self._seg_started
            self._seg_started = None

    def _kill_current(self) -> None:
        if self._proc is None:
            return
        proc, self._proc = self._proc, None
        proc.send_signal(signal.SIGKILL)

    def _concat(self) -> Path:
        """Concatenate segments (PCM → PCM is lossless) into master.wav."""
        master = self.session_dir / "master.wav"
        if len(self._segments) == 1:
            shutil.copyfile(self._segments[0], master)
            return master

        list_file = self.session_dir / "segments.txt"
        list_file.write_text(
            "".join(f"file '{seg.name}'\n" for seg in self._segments),
            encoding="utf-8",
        )
        cmd = [
            ffmpeg_binary(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            str(CHANNELS),
            "-c:a",
            "pcm_s16le",
            "-y",
            str(master),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode != 0 or not master.exists():
            raise RecorderError(
                f"Could not stitch recording segments: {proc.stderr.strip()}"
            )
        return master
