"""The inherited harness, behind the seam.

This adapter implements the grove ``Harness`` protocol by delegating to the
existing ``ModelFactory`` machinery — behavior is preserved exactly because
the delegation is a pass-through, not a reimplementation. When the grove's
own implementation matures (SOVEREIGNTY.md Phase 3), it lives in its own
module behind the same protocol and this file becomes one selectable
option among many — then, eventually, deletable.
"""

from __future__ import annotations

from collections.abc import Mapping
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

    def load_models_config(self) -> dict[str, Any]:
        """Delegate verbatim to ``ModelFactory.load_config``.

        The import and the attribute lookup both happen at call time: the
        heavy module stays off the boot path, and patches aimed at
        ``spruce_grove.model_factory`` keep working through the seam
        unchanged.
        """
        from spruce_grove import model_factory

        return model_factory.ModelFactory.load_config()

    def make_model_settings(
        self,
        model_name: str,
        max_tokens: int | None = None,
        overrides: Mapping[str, Any] | None = None,
    ) -> Any:
        """Delegate verbatim to ``model_factory.make_model_settings``.

        Same late-import discipline as the other surfaces; the call-time
        attribute lookup preserves the inherited test seam.
        """
        from spruce_grove import model_factory

        return model_factory.make_model_settings(
            model_name,
            max_tokens=max_tokens,
            overrides=overrides,
        )

    def tool_context_type(self) -> type:
        """Return the inherited context class call sites annotate with.

        Same late-import discipline as the other surfaces: the heavy
        framework stays off the boot path until a tool module actually asks
        for the annotation. The inherited framework detects the context
        parameter by type *identity*, so this must be the exact class it
        injects — see ``_is_run_context`` in the inherited
        ``_function_schema``.
        """
        from pydantic_ai import RunContext

        return RunContext


# Structural check: an instance satisfies the grove protocol.
_instance: PydanticHarness = PydanticHarness()
assert isinstance(_instance, Harness)
