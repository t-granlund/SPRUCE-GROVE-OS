"""The grove-owned harness seam — the sovereignty boundary.

This package is the ONLY sanctioned way for grove code to talk to whatever
agent harness executes underneath it. Today that harness is the inherited
external framework (see ``SOVEREIGNTY.md``); tomorrow it is the grove's own
implementation. The point of this seam is that consumers never know (or
care) which one is running — they speak grove vocabulary, and the harness
behind it can be swapped, run side-by-side, or removed without touching
them.

Phase 2 of the sovereignty exit (see ``SOVEREIGNTY.md``):

- ``protocol``          grove-owned vocabulary and the ``Harness`` protocol
- ``pydantic_harness``  adapter delegating to the inherited implementation
- ``selector``          selection point (``SPRUCE_GROVE_HARNESS`` env var)

Rules of the seam (they mirror the Leather Apron Gate):

- Nothing in ``protocol.py`` may import the external harness. The
  vocabulary is grove-owned; a structural test enforces this.
- Migrations land one call site at a time, tests green at each landing.
- The adapter must preserve behavior exactly. Parity is proven by tests,
  not asserted in comments.
"""

from spruce_grove.harness.protocol import Harness, HarnessInfo
from spruce_grove.harness.selector import get_harness

__all__ = ["Harness", "HarnessInfo", "get_harness", "ToolContext"]


def __getattr__(name: str):
    """Expose the tool-context vocabulary lazily.

    ``ToolContext`` is bound via the running harness, which for the
    inherited adapter imports the heavy framework. Resolving it lazily
    keeps ``import spruce_grove.harness`` itself import-light — boot-path
    code can select a harness without pulling the framework just to name
    the seam.
    """
    if name == "ToolContext":
        from spruce_grove.harness.tool_context import ToolContext

        return ToolContext
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
