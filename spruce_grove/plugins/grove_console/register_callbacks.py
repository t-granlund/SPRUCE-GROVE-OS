"""Register `/console`, the live-session panel."""

from __future__ import annotations

from spruce_grove.callbacks import register_callback

HELP = ("console", "See and tend the grove sessions running on this machine")


def _custom_help():
    return [HELP]


def _run_panel() -> None:
    """Open the interactive panel until the user quits.

    Imported lazily so a session that never runs `/console` pays nothing for
    a TUI stack it will not use.
    """
    from code_puppy_core_plugins.termflow_tui import FragmentTUI

    from spruce_grove.plugins.grove_console import panel as p
    from spruce_grove.plugins.grove_console.model import ConsoleModel

    model = ConsoleModel()
    armed = {"kill": False}

    def render() -> list:
        width, height = _size()
        return p.compose(model, width=width, height=height, armed=armed["kill"])

    def handle(key: str) -> bool:
        return p.on_key(
            key,
            model,
            armed=armed["kill"],
            arm=lambda: armed.__setitem__("kill", True),
            disarm=lambda: armed.__setitem__("kill", False),
        )

    def tick() -> bool:
        # A panel left open should keep telling the truth about the machine.
        return model.refresh()

    FragmentTUI(render, handle, on_tick=tick).run()


def _size() -> tuple:
    from termflow.tui.terminal import terminal_size

    return terminal_size()


def _handle_custom_command(command: str, name: str):
    """Handle `/console`. Returns None for anything we do not own."""
    if name != "console":
        return None
    from spruce_grove.messaging import emit_error

    try:
        _run_panel()
    except Exception as exc:  # never let a TUI crash the session
        emit_error(f"console failed: {exc}")
    return True


register_callback("custom_command", _handle_custom_command)
register_callback("custom_command_help", _custom_help)
