"""Selection state and actions for the live-session console.

Kept free of rendering and of the TUI event loop so the interesting
behaviour -- what happens when you restart a session -- is testable without
a terminal. The panel layer (:mod:`panel`) owns presentation only.

The action design follows one rule: **restart, don't kill.** Grove autosaves
on its shutdown path, so SIGTERM lets a session put its work away before it
goes; SIGKILL can drop everything since the last save. Restarting is
therefore the default and killing is the explicit, confirmed escalation.
"""

from __future__ import annotations

import os
import signal
import time
from dataclasses import dataclass
from typing import Callable, List, Optional

from spruce_grove.live_sessions import LiveSession, list_live_sessions

#: Re-scanning `ps` and the metadata files is not free; a console left open
#: should refresh often enough to look live, not once per keystroke.
REFRESH_INTERVAL_SECONDS = 2.0


@dataclass(frozen=True)
class ActionResult:
    """What happened when we tried to act on a session."""

    ok: bool
    message: str
    pid: Optional[int] = None
    #: A command the user can run to bring the session back, when relevant.
    resume_hint: Optional[str] = None


def _default_sender(pid: int, sig: int) -> None:
    os.kill(pid, sig)


class ConsoleModel:
    """The console's view of the machine, plus the actions it can take.

    Args:
        scanner: injectable session source (defaults to the real scanner).
        sender: injectable signal delivery, for tests.
        self_pid: the console's own process, which it must never signal.
    """

    def __init__(
        self,
        *,
        scanner: Callable[..., List[LiveSession]] = list_live_sessions,
        sender: Callable[[int, int], None] = _default_sender,
        self_pid: Optional[int] = None,
    ) -> None:
        self._scanner = scanner
        self._sender = sender
        self._self_pid = os.getpid() if self_pid is None else self_pid
        self.sessions: List[LiveSession] = []
        self.selected = 0
        self.show_orphans = False
        self.last_refresh: float = 0.0
        self.status: str = ""
        self.refresh(force=True)

    # --- reading ----------------------------------------------------------

    def refresh(self, *, force: bool = False, now: Optional[float] = None) -> bool:
        """Re-scan sessions. Returns True when the view changed.

        Throttled so the render loop can call it on every tick.
        """
        now = time.monotonic() if now is None else now
        if not force and (now - self.last_refresh) < REFRESH_INTERVAL_SECONDS:
            return False

        previous = [(s.pid, s.title) for s in self.sessions]
        self.sessions = self._scanner(include_closed=self.show_orphans)
        self.last_refresh = now

        # Keep the cursor on something real. Prefer the session that was
        # selected before; when it is gone, clamp instead of raising.
        if self.selected >= len(self.sessions):
            self.selected = max(0, len(self.sessions) - 1)
        self.selected = max(0, min(self.selected, max(0, len(self.sessions) - 1)))
        return previous != [(s.pid, s.title) for s in self.sessions]

    @property
    def current(self) -> Optional[LiveSession]:
        if not self.sessions:
            return None
        # Clamp defensively: a refresh could shrink the list between calls.
        self.selected = max(0, min(self.selected, len(self.sessions) - 1))
        return self.sessions[self.selected]

    def toggle_orphans(self) -> None:
        self.show_orphans = not self.show_orphans
        self.refresh(force=True)

    # --- navigation -------------------------------------------------------

    def move(self, delta: int) -> None:
        if not self.sessions:
            return
        last = len(self.sessions) - 1
        # Clamp rather than wrap, matching the plugins-menu convention.
        self.selected = max(0, min(self.selected + delta, last))

    def jump_first(self) -> None:
        self.selected = 0

    def jump_last(self) -> None:
        self.selected = max(0, len(self.sessions) - 1)

    # --- acting -----------------------------------------------------------

    def restart(self) -> ActionResult:
        """Ask a session to exit cleanly, so it autosaves on the way out."""
        return self._signal(
            signal.SIGTERM,
            verb="Restart requested",
            note="it saves state as it exits",
        )

    def kill(self) -> ActionResult:
        """Force a session down. Only ever called after explicit confirmation."""
        return self._signal(
            signal.SIGKILL,
            verb="Force-killed",
            note="unsaved work since the last autosave is gone",
        )

    def _signal(self, sig: int, *, verb: str, note: str) -> ActionResult:
        session = self.current
        if session is None:
            return ActionResult(False, "No session selected.")

        if session.pid == self._self_pid:
            return ActionResult(
                False,
                "That is this session. Exit it the normal way instead.",
                pid=session.pid,
            )
        if session.pid <= 1:
            return ActionResult(False, "Refusing to signal a system process.")

        try:
            self._sender(session.pid, sig)
        except ProcessLookupError:
            return ActionResult(
                False, f"PID {session.pid} is already gone.", pid=session.pid
            )
        except PermissionError:
            return ActionResult(
                False, f"Not permitted to signal PID {session.pid}.", pid=session.pid
            )
        except OSError as exc:
            return ActionResult(False, f"Could not signal {session.pid}: {exc}")

        self.status = (
            f"{verb}: {session.title or session.session_name or session.pid} ({note})"
        )
        return ActionResult(
            True,
            self.status,
            pid=session.pid,
            resume_hint=resume_command(session),
        )


def resume_command(session: LiveSession) -> Optional[str]:
    """The command that brings a session back where it was.

    ``--cwd`` scopes the resume to the session's own directory, which is what
    makes this a *restart* rather than a new session in the wrong place.
    """
    name = session.session_name
    if not name:
        return None
    if session.cwd:
        return f"spruce-grove --resume {name} --cwd"
    return f"spruce-grove --resume {name}"
