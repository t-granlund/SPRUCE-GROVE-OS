"""Spruce Grove -- Leather Apron Club starter plugin.

L3 first brick: the smallest possible grove surface that ships through the
plugin seam instead of core. Registers ``/junto``, a boot-camp plaque of the
club credo the grove builds under. User tier (loads for every project,
trust-free) because the credo belongs to the person, not the repo.

The Junto: Benjamin Franklin's mutual-improvement club, founded 1727.
Tradespeople meeting to ask better questions of each other's work. The
grove's digital version keeps the same rule: improvements march in pairs.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from spruce_grove.callbacks import register_callback

_COMMANDS = {"junto", "grove"}

_CREDO_LINES = (
    "Ask better questions than the ones you are given.",
    "Improve each other honestly; accountability, never blame.",
    "Build for the town first. The barbershop, the artisan, the drone pilot.",
    "Leave it better than we found it.",
)


def _grove_credo(command: str, name: str):
    """Handle /junto (alias /grove); pass anything else through untouched.

    Hook contract: True when handled or a string to feed back as input;
    None means "not mine" so the next plugin or the CLI can continue.
    """
    if name not in _COMMANDS:
        return None

    console = Console()
    body = "\n".join(f"[#98B79E]{line}[/#98B79E]" for line in _CREDO_LINES)
    parlor = (
        "\n\n[dim]gran\N{DOT OPERATOR}lund \N{DOT OPERATOR} sv. \N{DOT OPERATOR} spruce grove "
        "\N{DOT OPERATOR} together we are better, always.[/dim]"
    )
    console.print(
        Panel(
            body + parlor,
            title="[#D2A069]The Leather Apron Club (Junto)[/#D2A069]",
            subtitle="[dim]est. 1727 \N{DOT OPERATOR} rebooted for the grove[/dim]",
            border_style="#588F5E",
            padding=(1, 2),
        )
    )
    return True


def _grove_help():
    """Advertise the command on the /help menu."""
    return [("/junto", "Leather Apron Club credo -- why the grove builds")]


register_callback("custom_command", _grove_credo)
register_callback("custom_command_help", _grove_help)
