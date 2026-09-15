"""The inherited harness, behind the seam.

This adapter implements the grove ``Harness`` protocol by delegating to the
existing ``ModelFactory`` machinery — behavior is preserved exactly because
the delegation is a pass-through, not a reimplementation. When the grove's
own implementation matures (SOVEREIGNTY.md Phase 3), it lives in its own
module behind the same protocol and this file becomes one selectable
option among many — then, eventually, deletable.
"""

from __future__ import annotations

from typing import Any

from spruce_grove.harness.protocol import Harness, HarnessInfo

__all__ = ["PydanticHarness"]


class PydanticHarness:
    """Adapter: the inherited agent framework, seen through grove eyes."""

    def __init__(self) -> None:
        self.info = HarnessInfo(
            name="pydantic",
            description="inherited agent framework (delegating adapter)",
        )

    def resolve_model(self, model_name: str, config: dict[str, Any]) -> Any:
        """Delegate verbatim to ``ModelFactory.get_model``.

        Kept as a late import inside the method so that merely *selecting*
        or inspecting the harness never pulls the heavy framework — the
        same lazy discipline the rest of the boot path uses.
        """
        from spruce_grove.model_factory import ModelFactory

        return ModelFactory.get_model(model_name, config)


# Structural check: an instance satisfies the grove protocol.
_instance: PydanticHarness = PydanticHarness()
assert isinstance(_instance, Harness)
