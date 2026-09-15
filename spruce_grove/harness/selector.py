"""Harness selection — how the grove picks the implementation behind the seam.

Phase 2 selection is deliberately tiny: the ``SPRUCE_GROVE_HARNESS``
environment variable names the implementation (default ``"pydantic"`` — the
inherited framework). When the grove's own implementation exists (Phase 3),
its selector name lands here and grove.cfg gains the setting; nothing else
changes. Unknown names never crash the boot — the grove fails soft, logs
loudly, and falls back to the inherited implementation.
"""

from __future__ import annotations

import logging
import os

from spruce_grove.harness.protocol import Harness, HarnessInfo

__all__ = ["get_harness", "available_harnesses", "DEFAULT_HARNESS"]

logger = logging.getLogger(__name__)

DEFAULT_HARNESS = "pydantic"

_REGISTRY: dict[str, HarnessInfo] = {
    "pydantic": HarnessInfo(
        name="pydantic",
        description="inherited agent framework (delegating adapter)",
    ),
}


def available_harnesses() -> dict[str, HarnessInfo]:
    """Registry of selectable implementations (for diagnostics/roadmap)."""
    return dict(_REGISTRY)


def get_harness() -> Harness:
    """Return the configured harness implementation. Never raises."""
    wanted = (
        os.environ.get("SPRUCE_GROVE_HARNESS", "").strip().lower()
        or DEFAULT_HARNESS
    )
    if wanted not in _REGISTRY:
        logger.error(
            "SPRUCE_GROVE_HARNESS=%r is not an available harness (%s); "
            "falling back to %r",
            wanted,
            ", ".join(sorted(_REGISTRY)),
            DEFAULT_HARNESS,
        )
        wanted = DEFAULT_HARNESS

    if wanted == "pydantic":
        from spruce_grove.harness.pydantic_harness import PydanticHarness

        return PydanticHarness()

    # Unreachable while the registry has one entry; kept as the explicit
    # extension point so adding an implementation cannot forget selection.
    raise AssertionError(f"harness {wanted!r} registered but not wired")
