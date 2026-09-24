"""Transcription via the local Mockingbird whisper-cpp rig.

Mirrors the pipeline Mockingbird itself uses (ffmpeg → whisper-cli) with the
``whisper-large-v3-turbo-q5_0`` ggml model from ``~/dev/mockingbird/models/``.

Resolution order (env vars win so CI/other machines can redirect):

* binary: ``$SPRUCE_MOCKINGBIRD_WHISPER`` → ``whisper-cli`` on PATH →
  ``/opt/homebrew/bin/whisper-cli``
* model:  ``$SPRUCE_MOCKINGBIRD_MODEL`` → the turbo q5_0 in
  ``~/dev/mockingbird/models`` → first ``.bin`` found there
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from .recorder import ffmpeg_binary

#: How long whisper may chew on one recording before we give up.
TRANSCRIBE_TIMEOUT = 600.0

#: Peak level (dBFS) below which a recording is treated as no meaningful
#: speech. Measured 2026-09-23: digital silence sits at ~-91 dB, normal room
#: speech peaks near -2 dB, so -50 leaves an enormous margin while still
#: catching a mic that captured nothing.
_SILENCE_PEAK_DBFS = -50.0

#: Whisper was trained on YouTube captions and *hallucinates* on non-speech —
#: the canonical artifacts are "Thank you.", "Thanks for watching!", and
#: bare "you" / "." fragments. The reported live bug was the token *repeated*
#: ("thank you, thank you, thank you"), across lines as often as within one,
#: so this matches a single stock token and :func:`_is_stock_artifact` strips
#: every occurrence to decide whether anything of the user actually remained.
#: Real speech that merely *contains* "thank you" leaves residue behind and is
#: therefore never dropped.
_STOCK_TOKEN = re.compile(
    r"""(?:
        thank\s+you(?:\s+(?:very\s+)?much)?
      | thanks?(?:\s+(?:for|a\s+lot))?(?:\s+watching)?
      | you
      | (?:bye|goodbye)
      | please\s+subscribe
      | (?:subtitles?|captions?)(?:\s+by)?
    )""",
    re.IGNORECASE | re.VERBOSE,
)


def _peak_dbfs(wav_path: Path) -> float:
    """Peak loudness of *wav_path* in dBFS (e.g. -91 = silence, -2 = speech)."""
    cmd = [
        ffmpeg_binary(),
        "-hide_banner",
        "-i",
        str(wav_path),
        "-af",
        "volumedetect",
        "-f",
        "null",
        "-",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired as exc:
        raise TranscriberError("Audio level check timed out") from exc
    match = re.search(r"max_volume:\s*(-?[\d.]+)\s*dB", proc.stderr or "")
    if not match:
        # Unreadable level: don't invent a verdict — let whisper try.
        return float("inf")
    return float(match.group(1))


def _assert_has_speech(wav_path: Path) -> None:
    """Refuse to transcribe a take that captured no audible speech.

    This is the fix for the "thank you, thank you, thank you" report: at
    normal mic levels silence transcribes as a Whisper hallucination, so the
    honest move is to detect the empty take *before* whisper and say so.
    """
    peak = _peak_dbfs(wav_path)
    if peak < _SILENCE_PEAK_DBFS:
        raise TranscriberError(
            f"Nothing audible was captured (peak {peak:.0f} dB). "
            "Check the microphone and speak a little closer, then try again."
        )


#: A take is "long" once it runs past this many seconds; below it the density
#: signal is too noisy to judge (a real 0.8 s "Thanks." is honest speech).
_LONG_TAKE_SECONDS = 3.0

#: Below this length a one-word transcript is plausible real speech (“Thanks.”,
#: “Yes.”) and must NOT be mistaken for an artifact. At or above it, a
#: one-word result over that much audio is the hallucination signature.
_MIN_ARTIFACT_SECONDS = 1.5

#: Characters per second OF SPEECH (pauses excluded) below which a long take
#: reads as non-speech. Measured 2026-09-24 over real takes in
#: ~/.spruce_grove/mockingbird/: continuous speech runs 14-19 chars/sec; a
#: pause-heavy take (17.3 s of speech inside 25.8 s) still holds 4.3; a loud
#: 440 Hz tone yields 0.15. 2.0 sits between the noise floor and the lowest
#: honest speech, with room for very riff-y takes.
#:
#: History: this was 4.0 measured against TOTAL duration, which wrongly
#: rejected pause-heavy real speech ("Testing, testing. Is this thing
#: working?") as a hallucination -- the exact failure that made /rec look
#: broken to the person using it.
_MIN_CHARS_PER_SECOND = 2.0

#: Silence detection for the density check: below this level for at least this
#: long counts as a pause rather than speech.
_SILENCE_NOISE_DB = -30.0
_SILENCE_MIN_SECONDS = 0.5


def _duration_seconds(wav_path: Path) -> float:
    """Duration of *wav_path* in seconds, or 0.0 when it can't be read."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "csv=p=0",
        str(wav_path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float((proc.stdout or "").strip() or 0.0)
    except (subprocess.TimeoutExpired, ValueError):
        return 0.0


def _is_stock_artifact(text: str) -> bool:
    """True when *text* is nothing but repeated stock Whisper tokens.

    Strip every recognized token plus surrounding punctuation/whitespace; if
    the whole transcript disappears, the user said none of it. This is what
    catches "Thank you.\\nThank you.\\nThank you." -- the reported bug -- which
    a single-line anchored pattern missed.
    """
    residue = _STOCK_TOKEN.sub(" ", text)
    return not re.sub(r"[\s.!?…,\-]+", "", residue)


def _speech_seconds(wav_path: Path, total_seconds: float) -> float:
    """Seconds of *wav_path* that actually contain sound (pauses excluded).

    /rec is explicitly a pause-and-resume tool, so a take's total length is a
    poor denominator for "how much speech is here": 8 s of silence in the
    middle must not count as 8 s that failed to produce words. Falls back to
    the total duration whenever silence can't be measured, so the check can
    only ever be as strict as before, never stricter.
    """
    cmd = [
        ffmpeg_binary(),
        "-hide_banner",
        "-i",
        str(wav_path),
        "-af",
        f"silencedetect=noise={_SILENCE_NOISE_DB}dB:d={_SILENCE_MIN_SECONDS}",
        "-f",
        "null",
        "-",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return total_seconds
    silences = re.findall(r"silence_duration:\s*([\d.]+)", proc.stderr or "")
    if not silences:
        return total_seconds
    return max(total_seconds - sum(float(s) for s in silences), 0.0)


def _looks_like_hallucination(
    text: str, duration: float, speech: float | None = None
) -> bool:
    """True when whisper 'heard' something other than speech.

    Two independent tells, either is enough:

    * **Density** — a long take that yielded only a few characters *per second
      of speech* is non-speech. Real speech here runs 14-19 chars/sec even
      when pause-heavy; hallucinations and tones land near 0. Dividing by
      speech (not total) time is what keeps a paused, honest take from being
      mistaken for an artifact.
    * **Known artifact** — the transcript is *only* a stock Whisper token
      ("Thank you.", "you", "."). Anchored to the whole line, so real speech
      that merely contains those words is never touched.
    """
    stripped = text.strip()
    if speech is None:
        speech = duration
    if duration >= _LONG_TAKE_SECONDS:
        chars = len(re.sub(r"\s+", "", stripped))
        if speech > 0 and chars / speech < _MIN_CHARS_PER_SECOND:
            return True
    if duration >= _MIN_ARTIFACT_SECONDS:
        return _is_stock_artifact(stripped)
    return False


_DEFAULT_MODEL_DIR = Path.home() / "dev" / "mockingbird" / "models"
_PREFERRED_MODEL = "whisper-large-v3-turbo-q5_0.bin"
_HOMEBREW_WHISPER = "/opt/homebrew/bin/whisper-cli"


class TranscriberError(RuntimeError):
    """Raised when transcription cannot run or produces no text."""


def resolve_whisper_binary() -> str:
    candidate = os.environ.get("SPRUCE_MOCKINGBIRD_WHISPER", "")
    for path in (candidate, shutil.which("whisper-cli") or "", _HOMEBREW_WHISPER):
        if path and Path(path).exists():
            return path
    raise TranscriberError(
        "whisper-cli not found. Install with: brew install whisper-cpp "
        "(or set $SPRUCE_MOCKINGBIRD_WHISPER)"
    )


def resolve_model() -> Path:
    candidate = os.environ.get("SPRUCE_MOCKINGBIRD_MODEL", "")
    if candidate:
        path = Path(candidate).expanduser()
        if path.exists():
            return path
        raise TranscriberError(f"$SPRUCE_MOCKINGBIRD_MODEL not found: {path}")

    if _DEFAULT_MODEL_DIR.is_dir():
        preferred = _DEFAULT_MODEL_DIR / _PREFERRED_MODEL
        if preferred.exists():
            return preferred
        for model in sorted(_DEFAULT_MODEL_DIR.glob("*.bin")):
            return model  # first available model beats none

    raise TranscriberError(
        f"No whisper model found in {_DEFAULT_MODEL_DIR}. "
        "Run Mockingbird's download-models script or set $SPRUCE_MOCKINGBIRD_MODEL"
    )


def transcribe(wav_path: Path, work_dir: Path) -> str:
    """Transcribe *wav_path* and return the plain-text transcript.

    Output artifacts (``transcript.txt``) land in *work_dir* so every
    session keeps its own trail.
    """
    wav_path = Path(wav_path)
    work_dir = Path(work_dir)
    if not wav_path.exists():
        raise TranscriberError(f"Audio file missing: {wav_path}")

    _assert_has_speech(wav_path)

    prefix = work_dir / "transcript"
    cmd = [
        resolve_whisper_binary(),
        "-m",
        str(resolve_model()),
        "-f",
        str(wav_path),
        "-otxt",
        "-of",
        str(prefix),
        "-np",
    ]
    lang = os.environ.get("SPRUCE_MOCKINGBIRD_LANG", "").strip()
    if lang:
        cmd += ["-l", lang]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TRANSCRIBE_TIMEOUT,
            cwd=str(work_dir),
        )
    except subprocess.TimeoutExpired as exc:
        raise TranscriberError("Transcription timed out") from exc

    txt_path = Path(f"{prefix}.txt")
    if proc.returncode != 0:
        raise TranscriberError(
            f"whisper-cli failed: {(proc.stderr or proc.stdout).strip()[-400:]}"
        )
    if not txt_path.exists():
        raise TranscriberError("whisper-cli produced no transcript file")

    text = txt_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        raise TranscriberError(
            "Transcript came back empty — the recording may be too quiet."
        )
    duration = _duration_seconds(wav_path)
    speech = _speech_seconds(wav_path, duration)
    if _looks_like_hallucination(text, duration, speech):
        raise TranscriberError(
            "Only non-speech came through (whisper hallucinated "
            f"{text!r}). No usable speech in this recording."
        )
    return text


def describe_rig() -> str:
    """One-line summary of the resolved rig, for preflight output."""
    return f"whisper-cli: {resolve_whisper_binary()}  ·  model: {resolve_model().name}"
