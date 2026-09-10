"""Interactive Mockingbird flow: record window → transcribe → review → send.

The window is deliberately low-tech and robust: a rich ``Live`` panel redrawn
from the main thread while ``select()`` watches stdin for whole lines. No
raw/cbreak mode, no second stdin listener — the core app enforces exactly one
cbreak reader, and we are not it. Keys therefore need Enter (``p``, ``s``,
``q`` + Enter), which also keeps paste-safety and cooked-mode terminal state
trivially correct.

The review loop is the "pause, edit, adapt" part of the ask: after
transcribing you can send, edit in ``$VISUAL``/``$EDITOR``, or re-record —
with the current draft pinned in the recording window so you can *record
against it*.
"""

from __future__ import annotations

import os
import select
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .recorder import MicRecorder, RecorderError
from .transcriber import TranscriberError, transcribe

_WINDOW_POLL_SECONDS = 0.15
_DRAFT_PREVIEW_CHARS = 220


def _fmt_elapsed(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def _fmt_bytes(nbytes: int) -> str:
    return f"{nbytes / (1024 * 1024):.1f} MB"


def _render_window(recorder: MicRecorder, draft: Optional[str]) -> Panel:
    if recorder.paused:
        state, state_style = "⏸ PAUSED", "yellow"
    else:
        state, state_style = " REC", "red"
    status = (
        f"[{state_style}]{state}[/{state_style}]  "
        f"[b]{_fmt_elapsed(recorder.elapsed)}[/b]  ·  "
        f"{_fmt_bytes(recorder.captured_bytes)}  ·  "
        f"takes: {len(recorder._segments)}"  # noqa: SLF001 — same-package view
    )
    body = Text.from_markup(status + "\n\n")
    body.append(
        "[p] pause/resume    [s] stop & transcribe    [q] cancel\n", style="dim"
    )
    if draft:
        preview = draft[:_DRAFT_PREVIEW_CHARS].replace("\n", " ")
        if len(draft) > _DRAFT_PREVIEW_CHARS:
            preview += "…"
        body.append("\nrecording against draft:\n", style="bold dim")
        body.append(preview, style="italic")
    return Panel(body, title="Mockingbird", border_style="cyan")


def run_recording_window(
    recorder: MicRecorder, draft: Optional[str], console: Console
) -> str:
    """Show the live window until the user stops or cancels.

    Returns ``"stop"`` or ``"cancel"``. Ctrl+C counts as cancel.
    """
    recorder.start()
    with Live_wrapper(console) as live:
        try:
            while True:
                ready, _, _ = select.select([sys.stdin], [], [], _WINDOW_POLL_SECONDS)
                if ready:
                    # readline() needs a newline; partial typing simply waits —
                    # recording keeps running meanwhile, nothing is lost.
                    line = sys.stdin.readline().strip().lower()
                    key = line[:1]
                    if key == "p":
                        if recorder.paused:
                            recorder.resume()
                        else:
                            recorder.pause()
                    elif key == "s":
                        recorder.pause()
                        return "stop"
                    elif key == "q":
                        return "cancel"
                    else:
                        # Reprint the legend so stray keys self-explain.
                        live.update(_render_window(recorder, draft))
                live.update(_render_window(recorder, draft))
        except KeyboardInterrupt:
            return "cancel"


class Live_wrapper:
    """Tiny context wrapper so the window code reads flat."""

    def __init__(self, console: Console) -> None:
        self._console = console

    def __enter__(self):
        from rich.live import Live

        self._live = Live(console=self._console, refresh_per_second=8, transient=True)
        self._live.__enter__()
        return self._live

    def __exit__(self, *exc):
        return self._live.__exit__(*exc)


def _resolve_editor() -> list[str]:
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "vi"
    return shlex.split(editor)


def edit_text(text: str, work_dir: Path) -> str:
    """Open *text* in the user's editor; return the (possibly unchanged) text."""
    edit_path = Path(work_dir) / "transcript_editable.md"
    edit_path.write_text(text + "\n", encoding="utf-8")
    try:
        subprocess.call(_resolve_editor() + [str(edit_path)])
    except OSError as exc:
        Console().print(f"[yellow]Could not open editor: {exc}[/yellow]")
        return text
    edited = edit_path.read_text(encoding="utf-8", errors="replace").strip()
    return edited or text


def _ask(prompt: str, console: Console) -> str:
    try:
        return console.input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "q"


def capture_and_review(session_dir: Path, console: Console) -> Optional[str]:
    """Full Mockingbird cycle. Returns the approved prompt text, or None.

    Outer loop = takes (re-records keep the previous transcript as the draft
    pinned in the window); inner loop = review of one take.
    """
    session_dir = Path(session_dir)
    draft: Optional[str] = None

    while True:  # one iteration per take
        recorder = MicRecorder(session_dir)
        try:
            action = run_recording_window(recorder, draft, console)
        except RecorderError as exc:
            console.print(f"[red] {exc}[/red]")
            return None
        if action == "cancel":
            recorder.cancel()
            return None

        try:
            master = recorder.stop()
        except RecorderError as exc:
            console.print(f"[yellow] {exc} — let's take another.[/yellow]")
            continue

        with console.status("[cyan] Mockingbird is listening back…[/cyan]"):
            try:
                text = transcribe(master, session_dir)
            except TranscriberError as exc:
                console.print(f"[yellow] {exc}[/yellow]")
                again = _ask("Re-record? [Y/n] > ", console)
                if again in ("", "y", "yes"):
                    draft = draft  # keep prior draft, if any
                    continue
                return None

        while True:  # review of the current take
            console.print(
                Panel(
                    Text(text, style="white"),
                    title=" Transcript",
                    border_style="green",
                )
            )
            choice = _ask(
                "[b][s][/b]end as prompt  ·  [b][e][/b]dit  ·  "
                "[b][r][/b]e-record  ·  [b][q][/b]uit > ",
                console,
            )
            if choice in ("s", "send", ""):
                return text
            if choice in ("e", "edit"):
                text = edit_text(text, session_dir)
                continue
            if choice in ("r", "re", "re-record", "record"):
                draft = text  # next take records *against* this draft
                break
            if choice in ("q", "quit", "cancel"):
                return None
            console.print("[dim]s / e / r / q[/dim]")


def new_session_dir() -> Path:
    """Timestamped session folder under ~/.spruce_grove/mockingbird/."""
    base = Path.home() / ".spruce_grove" / "mockingbird"
    session = base / time.strftime("%Y%m%d-%H%M%S")
    session.mkdir(parents=True, exist_ok=True)
    _prune_sessions(base)
    return session


def _prune_sessions(base: Path, keep: int = 20) -> None:
    sessions = sorted(p for p in base.iterdir() if p.is_dir())
    for stale in sessions[:-keep]:
        for child in stale.iterdir():
            child.unlink(missing_ok=True)
        stale.rmdir()
