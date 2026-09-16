"""Baked banner art - the grove's boot lettering, owned outright.

Generated once from pyfiglet's ``ansi_shadow`` font (at pyfiglet's default
80-column wrap, byte-identical to what the call sites rendered) and committed
as constants, so the boot path never needs the library again. Dependency-exit
rung 5, docs/DEPENDENCY-EXIT.md. The gradient in ``cli_runner`` still paints
these line-by-line; only the letter source changed.
"""

from __future__ import annotations

__all__ = [
    "SPRUCE_GROVE_BANNER",
    "GROVE_BANNER",
    "art_for_label",
    "SPRUCE_GROVE_NATURAL_WIDTH",
]

# Rendered exactly as the call sites did: figlet_format(label, font="ansi_shadow")
# at pyfiglet's default 80-column wrap.
SPRUCE_GROVE_BANNER = "███████╗██████╗ ██████╗ ██╗   ██╗ ██████╗███████╗\n██╔════╝██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝\n███████╗██████╔╝██████╔╝██║   ██║██║     █████╗  \n╚════██║██╔═══╝ ██╔══██╗██║   ██║██║     ██╔══╝  \n███████║██║     ██║  ██║╚██████╔╝╚██████╗███████╗\n╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝\n                                                 \n ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗\n██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔════╝\n██║  ███╗██████╔╝██║   ██║██║   ██║█████╗  \n██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝██╔══╝  \n╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝ ███████╗\n ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝\n                                           "

GROVE_BANNER = " ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗\n██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔════╝\n██║  ███╗██████╔╝██║   ██║██║   ██║█████╗  \n██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝██╔══╝  \n╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝ ███████╗\n ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝\n                                           "

# The unwrapped width of "SPRUCE GROVE" (measured at width=300 at bake time).
# platform_utils._FULL_BANNER_WIDTH pins the label-selection threshold to this.
SPRUCE_GROVE_NATURAL_WIDTH = 96


def art_for_label(label: str) -> str:
    """Return the baked ansi-shadow art for a ``startup_banner_text`` label.

    ``SPRUCE GROVE`` gets the full render; anything else gets the compact
    GROVE art.
    """
    return SPRUCE_GROVE_BANNER if label == "SPRUCE GROVE" else GROVE_BANNER
