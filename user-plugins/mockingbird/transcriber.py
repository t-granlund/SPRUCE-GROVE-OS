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
import shutil
import subprocess
from pathlib import Path

#: How long whisper may chew on one recording before we give up.
TRANSCRIBE_TIMEOUT = 600.0

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
    return text


def describe_rig() -> str:
    """One-line summary of the resolved rig, for preflight output."""
    return f"whisper-cli: {resolve_whisper_binary()}  ·  model: {resolve_model().name}"
