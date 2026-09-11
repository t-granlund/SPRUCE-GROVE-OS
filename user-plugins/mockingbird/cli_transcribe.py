"""Headless ``--transcribe`` verb: the plugin's rig as a CLI service.

Registered via the ``register_cli_args`` / ``handle_cli_args`` hooks (plugins
load before ``parse_args`` — see cli_runner.py), so other surfaces — the
desktop shell, scripts, pipelines — can transcribe audio without
re-implementing whisper-rig resolution. Zero core edits, per the golden rule.

Contract::

    spruce-grove --transcribe <audiofile>    # transcript on stdout, exit 0

Accepts anything ffmpeg can read (m4a, mp3, webm/opus from the desktop
MediaRecorder, wav, ...); converts to 16 kHz mono PCM in a temp dir, then
runs the standard transcriber. Output is plain text — no rich markup — so it
pipes cleanly into editors, clipboards, and Tauri commands.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from .recorder import ffmpeg_binary
from .transcriber import transcribe

#: ffmpeg conversion ceiling; a broken/huge input must not wedge the CLI.
_CONVERT_TIMEOUT = 300.0

_EXIT_OK = {"handled": True, "exit_code": 0}
_EXIT_ERR = {"handled": True, "exit_code": 1}


def add_args(parser) -> None:
    """Register ``--transcribe AUDIOFILE`` on the CLI parser."""
    parser.add_argument(
        "--transcribe",
        metavar="AUDIOFILE",
        default=None,
        help="transcribe an audio file with the local Mockingbird rig and exit",
    )


def handle(args) -> dict | None:
    """Run the verb when requested; stay out of the way otherwise."""
    path = getattr(args, "transcribe", None)
    if not path:
        return None  # not our command — let other handlers / the CLI proceed
    try:
        print(_transcribe_file(Path(path)))
    except Exception as exc:  # noqa: BLE001 — the verb IS the error boundary
        print(f"transcribe failed: {exc}", file=sys.stderr)
        return _EXIT_ERR
    return _EXIT_OK


def _transcribe_file(src: Path) -> str:
    """Convert *src* to whisper's preferred PCM and transcribe it."""
    src = src.expanduser()
    if not src.exists():
        raise FileNotFoundError(f"no such file: {src}")

    work = Path(tempfile.mkdtemp(prefix="mockingbird-cli-"))
    wav = work / "input.wav"
    cmd = [
        ffmpeg_binary(),
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(src),
        "-ar",
        "16000",
        "-ac",
        "1",
        "-c:a",
        "pcm_s16le",
        "-y",
        str(wav),
    ]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=_CONVERT_TIMEOUT
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("ffmpeg conversion timed out") from exc
    if proc.returncode != 0 or not wav.exists():
        detail = (proc.stderr or proc.stdout).strip()[-300:]
        raise RuntimeError(f"ffmpeg convert failed: {detail}")

    return transcribe(wav, work)
