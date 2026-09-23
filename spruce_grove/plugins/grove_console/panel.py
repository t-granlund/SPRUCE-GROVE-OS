"""The two-pane live-session console panel.

Presentation only: it renders a :class:`~.model.ConsoleModel` to termflow
fragments and maps keys onto the model's actions. Navigation follows the
plugins-menu convention (``j``/``k`` + arrows move clamped, ``g``/``G`` jump,
``q``/``esc``/``ctrl-c`` bail) so the muscle memory carries over.

Destructive actions are two-step on purpose. ``r`` restarts (a clean SIGTERM
the session autosaves through); ``x`` *arms* a force-kill and a second ``x``
confirms it. A console should never be one stray keypress away from dropping
someone's work.
"""

from __future__ import annotations

from typing import Callable, List, Tuple

from spruce_grove.live_sessions import LiveSession
from spruce_grove.plugins.grove_console.model import ConsoleModel

Fragments = list  # list[tuple[str, str]]

#: How many lines of the session's log tail to show in the detail pane.
LOG_TAIL_LINES = 12


def _age(session: LiveSession) -> str:
    seconds = session.uptime_seconds
    if seconds is None:
        return "?"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def _state_style(session: LiveSession) -> Tuple[str, str]:
    if not session.is_live:
        return ("class:tui.warning", "orphan")
    return ("class:tui.success", "live")


def render_list(model: ConsoleModel, *, width: int) -> Fragments:
    """The left pane: one line per session, selection marked."""
    out: Fragments = [("class:tui.title", "Live grove sessions"), ("", "\n")]
    if not model.sessions:
        out.append(("class:tui.muted", "  none found"))
        out.append(("", "\n"))
        return out

    for index, session in enumerate(model.sessions):
        selected = index == model.selected
        cursor = "▸ " if selected else "  "
        style = "class:tui.selected" if selected else "class:tui.body"
        state_style, state = _state_style(session)

        label = session.title or session.session_name or "(unidentified)"
        room = max(8, width - len(cursor) - 16)
        if len(label) > room:
            label = label[: room - 1] + "…"

        out.append((style, f"{cursor}{label}"))
        out.append(("", "\n"))
        out.append(
            (
                "class:tui.muted",
                f"    pid {session.pid} · {session.tty or 'piped'} · {_age(session)} · ",
            )
        )
        out.append((state_style, state))
        out.append(("", "\n"))
    return out


def render_detail(model: ConsoleModel, *, width: int) -> Fragments:
    """The right pane: everything known about the selected session."""
    session = model.current
    out: Fragments = [("class:tui.title", "Session detail"), ("", "\n")]
    if session is None:
        out.append(("class:tui.muted", "  nothing selected"))
        out.append(("", "\n"))
        return out

    rows = [
        ("pid", str(session.pid)),
        ("tty", session.tty or "(piped -- embedded)"),
        ("age", _age(session)),
        ("agent", session.agent_name or "-"),
        ("cwd", session.cwd or "-"),
        ("title", session.title or "-"),
        ("subtitle", session.subtitle or "-"),
        ("messages", str(session.message_count) if session.message_count else "-"),
        ("tokens", str(session.total_tokens) if session.total_tokens else "-"),
        ("last save", session.last_autosave or "-"),
        ("session", session.session_name or "(unidentified)"),
    ]
    for key, value in rows:
        text = value if len(value) <= width - 12 else value[: width - 13] + "…"
        out.append(("class:tui.label", f"{key:>10}  "))
        out.append(("class:tui.body", text))
        out.append(("", "\n"))

    if model.status:
        out.append(("", "\n"))
        out.append(("class:tui.success", model.status))
        out.append(("", "\n"))
    return out


def render_footer(model: ConsoleModel, *, armed: bool) -> Fragments:
    """Key hints, plus the armed-kill warning when it is armed."""
    out: Fragments = [("", "\n")]
    if armed:
        out.append(
            (
                "class:tui.danger",
                "    force-kill armed -- press x again to confirm, any other key cancels",
            )
        )
        out.append(("", "\n"))
    hints = [
        ("j/k", "move"),
        ("enter", "detail"),
        ("r", "restart"),
        ("x", "force-kill"),
        ("o", "orphans"),
        ("q", "quit"),
    ]
    for key, label in hints:
        out.append(("class:tui.help_key", f"  {key}"))
        out.append(("class:tui.help", f" {label}"))
    out.append(("", "\n"))
    return out


def compose(model: ConsoleModel, *, width: int, height: int, armed: bool) -> List[str]:
    """Build the full frame as ANSI lines for :class:`FragmentTUI`."""
    from code_puppy_core_plugins.termflow_tui import two_pane

    list_width = max(24, min(40, width // 2))
    body = list(render_list(model, width=list_width))
    body += render_footer(model, armed=armed)
    right = list(render_detail(model, width=width - list_width - 2))

    lines = two_pane(body, right, width=width, list_width=list_width)
    # The layout collapses on narrow terminals; keep the detail reachable.
    return lines


def on_key(
    key: str,
    model: ConsoleModel,
    *,
    armed: bool,
    arm: Callable[[], None],
    disarm: Callable[[], None],
) -> bool:
    """Dispatch one key. Returns True when the console should exit.

    ``arm``/``disarm`` let the caller own the armed-kill flag so a stray key
    can clear it.
    """
    if key in ("q", "Q", "\x1b", "\x03"):
        return True

    if armed:
        if key in ("x", "X"):
            model.kill()
            model.refresh(force=True)
        else:
            model.status = "force-kill cancelled."
        disarm()
        return False

    if key in ("j", "down"):
        model.move(1)
    elif key in ("k", "up"):
        model.move(-1)
    elif key in ("g", "home"):
        model.jump_first()
    elif key in ("G", "end"):
        model.jump_last()
    elif key in ("o", "O"):
        model.toggle_orphans()
    elif key in ("r", "R"):
        result = model.restart()
        if result.resume_hint:
            model.status += f"  ·  resume with: {result.resume_hint}"
        model.refresh(force=True)
    elif key in ("x", "X"):
        arm()
    elif key in ("\r", "\n"):
        # Detail is always visible in the wide layout; the key exists for
        # muscle-memory parity with the other pickers.
        pass
    else:
        model.refresh()

    return False
