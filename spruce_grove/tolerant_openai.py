"""Tolerant OpenAI chat-completions model for non-conforming gateways.

pydantic-ai's ``OpenAIChatModel`` re-validates every response against the
strict SDK ``ChatCompletion`` schema (see ``OpenAIChatModel._validate_completion``,
whose docstring explicitly invites subclass overrides). Some third-party
OpenAI-compatible gateways attach informational ``metadata`` fields whose
values are not strings -- the observed offender is Synthetic.new, which
returns ``metadata.weight_versions`` as a *list* of span objects. The strict
schema (``metadata: dict[str, str]``) then rejects an otherwise perfectly
usable completion, pydantic-ai raises ``UnexpectedModelBehavior``, and
callers such as the wiggum goal judges convert that into abstentions.

``TolerantOpenAIChatModel`` keeps strict validation as the default path and,
only when it fails, retries once with non-string ``metadata`` values
JSON-encoded. Unrelated validation failures still propagate unchanged.
First-party OpenAI traffic keeps the stock strict model; this wrapper is
wired only into the ``custom_openai`` factory branch, which by definition
serves third-party endpoints.
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError
from pydantic_ai.models import openai as _openai_models
from pydantic_ai.models.openai import OpenAIChatModel


def _scrub_non_string_metadata(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Return a copy of ``payload`` with non-string metadata values encoded.

    Returns ``None`` when there is nothing to scrub, so callers can
    distinguish "metadata was fine, failure is elsewhere" from "metadata
    needed surgery".
    """
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return None
    if all(isinstance(value, str) for value in metadata.values()):
        return None
    scrubbed = dict(payload)
    scrubbed["metadata"] = {
        key: value if isinstance(value, str) else json.dumps(value)
        for key, value in metadata.items()
    }
    return scrubbed


class TolerantOpenAIChatModel(OpenAIChatModel):
    """``OpenAIChatModel`` that survives provider-junk ``metadata`` fields.

    Uses the documented ``_validate_completion`` subclass hook: try strict
    validation first; on ``ValidationError``, retry once after JSON-encoding
    any non-string ``metadata`` values. Lossless for the fields that matter
    (choices, usage, tool calls); only the informational metadata map is
    normalized.
    """

    def _validate_completion(self, response: Any) -> Any:
        try:
            return super()._validate_completion(response)
        except ValidationError:
            validator = getattr(_openai_models, "_ChatCompletion", None)
            if validator is None:
                # pydantic-ai internals moved; no scrub path available.
                raise
            scrubbed = _scrub_non_string_metadata(response.model_dump())
            if scrubbed is None:
                # Metadata was already conforming; the failure is unrelated.
                raise
            return validator.model_validate(scrubbed)
