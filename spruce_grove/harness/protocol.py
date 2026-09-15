"""Grove-owned harness vocabulary and protocol.

This module is deliberately **free of external-harness imports**. It speaks
only grove vocabulary, so the day the external framework is removed, this
file does not change by a single byte — only the implementation behind it
does. A structural test (``tests/test_harness.py``) enforces the import
ban, because the whole point of a sovereignty seam is that the boundary
cannot quietly dissolve.

Phase 2 scope (honest, no invented APIs):

- ``HarnessInfo``      identity/metadata for diagnostics and the banner
- ``Harness``          the protocol; today it covers model resolution,
                       which is the first migrated surface. The agent loop,
                       streaming, and tool-context surfaces will be added
                       to this protocol *as their call sites migrate* —
                       each addition lands with tests green. We do not
                       invent loop/stream APIs from imagination; we shape
                       them from the inventory in ``SOVEREIGNTY.md``.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

__all__ = ["Harness", "HarnessInfo"]


class HarnessInfo:
    """Identity of the harness implementation behind the seam."""

    name: str
    """Stable selector name (e.g. ``"pydantic"``). Matches the
    ``SPRUCE_GROVE_HARNESS`` selector value that chooses it."""

    description: str
    """One-line human description for diagnostics."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"HarnessInfo(name={self.name!r})"


@runtime_checkable
class Harness(Protocol):
    """The grove's contract with whatever executes agents underneath.

    Implementations MUST preserve behavior exactly against the inherited
    implementation (parity is proven by tests at each landing) and MUST
    never raise from selection-time paths that the inherited implementation
    would not raise from.
    """

    info: HarnessInfo

    def resolve_model(self, model_name: str, config: dict[str, Any]) -> Any:
        """Resolve a configured model name into a live model handle.

        Semantics are inherited verbatim from the first migrated call
        sites (``ModelFactory.get_model``):

        - unknown ``model_name`` → ``ValueError``
        - missing provider credentials → ``None`` (with a user-facing
          warning already emitted by the implementation)
        - otherwise → the harness's model handle (opaque to callers)

        The return type is deliberately ``Any``: callers treat the handle
        as opaque, which is what makes the harness swappable.
        """
        ...
