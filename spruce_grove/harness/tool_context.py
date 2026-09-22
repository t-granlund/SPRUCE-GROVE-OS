"""Grove-owned tool-context vocabulary.

Tools opt into context injection by annotating their first parameter with
``ToolContext``. The class is *obtained from the running harness* rather
than imported from the framework directly, and this module carries no
external-framework import at all — the one framework reference lives where
it belongs, in the adapter (``pydantic_harness.py``).

Why the indirection matters: the inherited framework detects the context
parameter by type *identity* (``annotation is RunContext``). So grove
vocabulary must be the exact class the running harness injects. Binding it
here gives the whole grove one import site for that class; the day the
grove's own harness lands (Phase 3), the binding follows it and no tool
module changes.
"""

from __future__ import annotations

from spruce_grove.harness.selector import get_harness

__all__ = ["ToolContext"]

# Bound once at import: one process runs one harness, so the annotation
# class is fixed for the lifetime of the process.
ToolContext: type = get_harness().tool_context_type()
