"""Mockingbird plugin — voice prompts for Spruce Grove OS.

Registers ``/rec`` (alias ``/r``): opens a live recording window, captures
the microphone via ffmpeg, transcribes with the local Mockingbird whisper
rig, then walks a review loop (send / edit in $EDITOR / re-record against
the draft). Sending returns the transcript as the user prompt, so it is
dissected and applied against the directory you are working in.

Configuration (all optional, via environment):

* ``SPRUCE_MOCKINGBIRD_MODEL``   — path to a whisper-cpp ggml model
* ``SPRUCE_MOCKINGBIRD_WHISPER`` — path to the whisper-cli binary
* ``SPRUCE_MOCKINGBIRD_MIC``     — mic name substring or avfoundation index
* ``SPRUCE_MOCKINGBIRD_LANG``    — language hint passed to whisper (e.g. ``en``)
"""

from __future__ import annotations

import sys

from spruce_grove.callbacks import CustomCommandResult, register_callback

_COMMAND_NAMES = {"rec", "r", "record"}

_HELP_ENTRY = (
    "rec",
    "Record voice -> Mockingbird transcribes -> review/edit -> send as "
    "prompt (alias: /r)",
)


def _custom_help():
    return [_HELP_ENTRY]


def _preflight(console) -> bool:
    """Verify the rig before touching the mic; explain exactly what's missing."""
    from .recorder import resolve_mic_index  # cheap; also validates a mic exists
    from .transcriber import resolve_model, resolve_whisper_binary

    try:
        resolve_mic_index()
        resolve_whisper_binary()
        model = resolve_model()
    except Exception as exc:  # RecorderError/TranscriberError both subclass RE
        console.print(f"[red]Mockingbird preflight failed:[/red] {exc}")
        return False
    console.print(f"[dim]Mockingbird rig ready · model: {model.name}[/dim]")
    return True


def _run_rec_flow():
    from rich.console import Console

    from .review import capture_and_review, new_session_dir
    from .recorder import RecorderError

    console = Console()
    if not _preflight(console):
        return True
    session_dir = new_session_dir()
    try:
        prompt_text = capture_and_review(session_dir, console)
    except RecorderError as exc:
        console.print(f"[red]Mockingbird recording failed:[/red] {exc}")
        return True
    if prompt_text:
        from spruce_grove.messaging import emit_info

        emit_info("Transcript approved — sending it through as your prompt.")
        return CustomCommandResult(prompt_text)
    return True


def _handle_custom_command(command: str, name: str):
    if name not in _COMMAND_NAMES:
        return None

    if not sys.stdin.isatty():
        from spruce_grove.messaging import emit_warning

        emit_warning("/rec needs an interactive terminal (stdin is not a TTY here).")
        return True

    if not sys.platform.startswith("darwin"):
        from spruce_grove.messaging import emit_warning

        emit_warning(
            "/rec currently records via macOS avfoundation. "
            "On other platforms, transcribe an existing file instead."
        )
        return True

    try:
        return _run_rec_flow()
    except KeyboardInterrupt:
        from spruce_grove.messaging import emit_info

        emit_info("Recording cancelled.")
        return True
    except Exception as exc:  # never crash the app (plugin rule #4)
        from spruce_grove.messaging import emit_error

        emit_error(f"Mockingbird plugin error: {exc}")
        return True


register_callback("custom_command_help", _custom_help)
register_callback("custom_command", _handle_custom_command)
