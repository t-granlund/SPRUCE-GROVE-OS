"""Dedicated onboarding for Synthetic.new subscribers.

``/onboard-synthetic`` walks a subscriber through everything needed to run the
grove exactly the way the maintainer runs it: the rotation-safe ``syn:`` alias
family for text and vision, the pinned fallback models, the API key stored in
the shared credential store, and the main model pointed at the driving seat.

Why aliases: pinned upstream model ids rotate and 404. The ``syn:`` aliases
survive rotation, so they are the right things to bake into config. The pinned
entries ship anyway (clearly labelled with their quota-burn risk) for the days
an alias is having a bad afternoon.

Everything is idempotent: re-running refreshes the alias definitions, prunes
pins the catalog has rotated out (``STALE_MODELS``), and keeps any user-added
models already present in ``extra_models.json``.

``/onboard-synthetic check`` goes beyond the key: it diffs the live
``/openai/v1/models`` catalog against the installed set (catching rotation
drift), reads the free ``/v2/quotas`` endpoint, and pings the quota-free
embeddings endpoint. Synthetic also speaks Anthropic
(``https://api.synthetic.new/anthropic/v1``) and offers a native
zero-data-retention web search (``https://api.synthetic.new/v2/search``);
the grove itself drives everything through the OpenAI-compatible endpoint.

Lineup refreshed 2026-09 against the live catalog + docs: ``syn:large:text``
now fronts ``hf:deepseek-ai/DeepSeek-V4.1-Flash`` (Beta, multimodal input) and
``hf:zai-org/GLM-5.2`` has been rotated out. Kimi-K3 is the rate-limit
baseline (one call = one request); the GLM Flash aliases stretch quota
furthest (~0.1 requests per call per the rate-limits docs).
"""

from __future__ import annotations

import getpass
import json
import os
import urllib.error
import urllib.request

from spruce_grove.command_line.command_registry import register_command
from spruce_grove.config import CONFIG_DIR, CONFIG_FILE, get_api_key, set_api_key
from spruce_grove.config_file import mutate_config

ENDPOINT = "https://api.synthetic.new/openai/v1"
KEY_NAME = "SYNTHETIC_API_KEY"
EXTRA_MODELS_PATH = os.path.join(CONFIG_DIR, "extra_models.json")

# Synthetic also speaks Anthropic (messages + count_tokens) and ships two
# native, quota-free endpoints: live subscription quotas and a zero-data-
# retention web search. Documented here for tooling; the grove drives all of
# its own traffic through the OpenAI-compatible endpoint above.
ANTHROPIC_ENDPOINT = "https://api.synthetic.new/anthropic/v1"
QUOTAS_URL = "https://api.synthetic.new/v2/quotas"
SEARCH_URL = "https://api.synthetic.new/v2/search"

# Embedding models are subscription-included and never count against rate
# limits, but they are API-only (no chat), so onboarding verifies rather than
# installs them — a chat-model entry in extra_models.json would be dead weight.
EMBEDDINGS_URL = f"{ENDPOINT}/embeddings"
EMBEDDINGS_MODEL = "hf:nomic-ai/nomic-embed-text-v1.5"

# Upstream ids the live catalog has rotated out. apply_onboarding prunes
# exactly these — and nothing else — so retired pins stop haunting the picker
# while user-added models stay untouched.
STALE_MODELS = frozenset({"hf:zai-org/GLM-5.2"})

_ENDPOINT_BLOCK = {
    "url": ENDPOINT,
    "api_key": f"${KEY_NAME}",
    "timeout": 1800,
}


def _model(name: str, context_length: int, description: str, **extra) -> dict:
    cfg = {
        "type": "custom_openai",
        "provider": "synthetic",
        "name": name,
        "custom_endpoint": dict(_ENDPOINT_BLOCK),
        "context_length": context_length,
        # Live catalog reports max_output_length 65536 across the whole
        # lineup; pinning it here skips the 15%-of-context heuristic.
        "max_output_tokens": 65536,
        "supported_settings": ["temperature", "seed", "top_p"],
        "description": description,
    }
    cfg.update(extra)
    return cfg


# The rotation-safe alias family — the right things to bake into config.
ALIAS_MODELS = {
    "syn:large:text": _model(
        "syn:large:text",
        524288,
        "Synthetic alias (rotation-safe) -> hf:deepseek-ai/DeepSeek-V4.1-Flash "
        "(Beta). Driving-seat reasoning AND the default vision target — it "
        "takes images at ~0.2 requests/call vs the Kimi-K3 baseline; heavy "
        "vision stays on syn:large:vision.",
        supports_vision=True,
    ),
    "syn:small:text": _model(
        "syn:small:text",
        196608,
        "Synthetic alias (rotation-safe) -> hf:zai-org/GLM-4.7-Flash. "
        "0.1x-class fan-out + mechanical gates; stretches quota furthest.",
    ),
    "syn:large:vision": _model(
        "syn:large:vision",
        524288,
        "Synthetic alias (rotation-safe) -> hf:moonshotai/Kimi-K3. Large "
        "vision; the rate-limit baseline (1 request = 1 request).",
        supports_vision=True,
    ),
    "syn:small:vision": _model(
        "syn:small:vision",
        262144,
        "Synthetic alias (rotation-safe) -> hf:Qwen/Qwen3.8-27B. Small vision "
        "at a fraction of the baseline cost.",
        supports_vision=True,
    ),
}

# Pinned upstream ids — rotation 404 risk, so always prefer the syn: aliases.
PINNED_MODELS = {
    "hf:zai-org/GLM-5.3-Flash": _model(
        "hf:zai-org/GLM-5.3-Flash",
        524288,
        "Pinned Synthetic model (rotation 404 risk). Always-on included. "
        "Cheapest reasoning class (~0.1 requests/call per the rate-limits "
        "docs); no longer the syn:large:text target.",
        supports_vision=True,
    ),
    "hf:deepseek-ai/DeepSeek-V4.1-Flash": _model(
        "hf:deepseek-ai/DeepSeek-V4.1-Flash",
        524288,
        "Pinned Synthetic model (Beta; rotation 404 risk; prefer "
        "syn:large:text). Always-on included. Current syn:large:text upstream.",
        supports_vision=True,
    ),
    "hf:zai-org/GLM-4.7-Flash": _model(
        "hf:zai-org/GLM-4.7-Flash",
        196608,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:small:text). "
        "Always-on included.",
    ),
    "hf:moonshotai/Kimi-K3": _model(
        "hf:moonshotai/Kimi-K3",
        524288,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:large:vision). "
        "Always-on included. Rate-limit baseline: 1 call = 1 request.",
        supports_vision=True,
    ),
    "hf:Qwen/Qwen3.8-27B": _model(
        "hf:Qwen/Qwen3.8-27B",
        262144,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:small:vision). "
        "Always-on included.",
        supports_vision=True,
    ),
    "hf:nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4": _model(
        "hf:nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4",
        262144,
        "Pinned Synthetic model. Always-on included.",
    ),
    "hf:openai/gpt-oss-120b": _model(
        "hf:openai/gpt-oss-120b",
        131072,
        "Pinned Synthetic model. Always-on included.",
    ),
}

DRIVING_SEAT = "syn:large:text"


def build_synthetic_models() -> dict:
    """The full model set this onboarding installs (aliases + pinned)."""
    models = dict(ALIAS_MODELS)
    models.update(PINNED_MODELS)
    return models


def fetch_model_ids(api_key: str, timeout: int = 20) -> tuple[bool, str, list]:
    """Live GET /openai/v1/models. Returns (ok, detail, sorted model ids)."""
    req = urllib.request.Request(
        f"{ENDPOINT}/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
            ids = sorted(
                str(m.get("id")) for m in (body.get("data") or []) if m.get("id")
            )
            return True, f"endpoint answered, {len(ids)} models visible", ids
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "key rejected (401/403) — check the key on synthetic.new", []
        return False, f"HTTP {exc.code}", []
    except Exception as exc:  # network unreachable, DNS, timeout …
        return False, f"could not reach endpoint: {exc}", []


def probe_endpoint(api_key: str, timeout: int = 20) -> tuple[bool, str]:
    """Live check against the Synthetic endpoint. Returns (ok, detail)."""
    ok, detail, _ = fetch_model_ids(api_key, timeout=timeout)
    return ok, detail


def check_catalog_drift(live_ids: list) -> tuple[list, list]:
    """Diff the live catalog against the onboarding model set.

    Returns ``(rotated_out, unpinned)``: pinned ids that vanished from the
    live catalog (404s waiting to happen — re-onboard), and live ids the
    onboarding set doesn't install (on-demand models may legitimately show
    up here; purely informational).
    """
    live = set(live_ids)
    rotated = sorted(model_id for model_id in PINNED_MODELS if model_id not in live)
    known = set(build_synthetic_models())
    unpinned = sorted(model_id for model_id in live if model_id not in known)
    return rotated, unpinned


def probe_quotas(api_key: str, timeout: int = 15) -> tuple[bool, str]:
    """Live read of the native /v2/quotas endpoint.

    Free by design: Synthetic documents that /quotas requests never count
    against subscription limits.
    """
    req = urllib.request.Request(
        QUOTAS_URL,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "key rejected (401/403)"
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # network unreachable, DNS, timeout …
        return False, f"could not reach endpoint: {exc}"

    weekly = body.get("weeklyTokenLimit") or {}
    five_hour = body.get("rollingFiveHourLimit") or {}
    subscription = body.get("subscription") or {}
    parts = []
    if weekly.get("remainingCredits") is not None:
        percent = weekly.get("percentRemaining")
        percent_txt = f", {percent:.0f}%" if isinstance(percent, (int, float)) else ""
        parts.append(
            f"weekly credits {weekly['remainingCredits']} of "
            f"{weekly.get('maxCredits', '?')}{percent_txt}"
        )
    if five_hour.get("remaining") is not None:
        parts.append(
            f"5-hour requests {five_hour['remaining']:g} of {five_hour.get('max', '?'):g}"
        )
    if five_hour.get("limited"):
        parts.append("5-hour pool exhausted — waits for the next regen tick")
    if subscription.get("requests") is not None and subscription.get("limit"):
        parts.append(
            f"{subscription['requests']}/{subscription['limit']} requests this window"
        )
    if not parts:
        return True, "quota endpoint answered (no known fields in payload)"
    return True, "; ".join(parts)


def probe_embeddings(api_key: str, timeout: int = 15) -> tuple[bool, str]:
    """Ping POST /openai/v1/embeddings with the included embedding model.

    Free by design: Synthetic documents that embeddings requests never count
    against subscription limits, so this check burns no quota.
    """
    req = urllib.request.Request(
        EMBEDDINGS_URL,
        data=json.dumps({"model": EMBEDDINGS_MODEL, "input": "ping"}).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
        first = (body.get("data") or [{}])[0]
        dims = len(first.get("embedding") or [])
        return True, f"{EMBEDDINGS_MODEL} answered ({dims}-dim vector, quota-free)"
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "key rejected (401/403)"
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # network unreachable, DNS, timeout …
        return False, f"could not reach endpoint: {exc}"


def verify_model_routing() -> dict:
    """Audit the model routing config: does every target actually resolve?

    Pure-local (no network, no quota burn). This is the guardrail for the
    failure mode that actually happened (2026-09-22): pins sat in a config
    section no reader touched, under agent names that no longer existed,
    while every agent silently rode the global default. Each check here
    would have caught that drift loudly instead.

    Returns a report dict:
        global      the global default model (or None)
        pins        [{"agent", "model"}] for every configured pin
        summarizer  the compaction summarizer model (or None)
        problems    human-readable, actionable problems (empty when healthy)
    """
    from spruce_grove.config import (
        get_all_agent_pinned_models,
        get_global_model_name,
        get_summarization_model_name,
    )
    from spruce_grove.model_factory import ModelFactory

    report: dict = {"global": None, "pins": [], "summarizer": None, "problems": []}

    try:
        catalog = ModelFactory.load_config()
    except Exception as exc:
        report["problems"].append(f"could not load the model catalog: {exc}")
        return report

    global_model = get_global_model_name()
    report["global"] = global_model
    if not global_model:
        report["problems"].append("no global model configured - run /onboard-synthetic")
    elif global_model not in catalog:
        report["problems"].append(
            f"global model {global_model!r} is not in the catalog - it will "
            "fall through to the first available model at startup"
        )

    try:
        from spruce_grove.agents.agent_manager import get_available_agents

        agents = get_available_agents()
        agent_names = (
            set(agents) if isinstance(agents, dict) else {a.name for a in agents}
        )
    except Exception as exc:  # pragma: no cover - defensive: enumeration env issues
        agent_names = None
        report["problems"].append(f"could not enumerate agents: {exc}")

    for agent_name, model in sorted(get_all_agent_pinned_models().items()):
        report["pins"].append({"agent": agent_name, "model": model})
        if agent_names is not None and agent_name not in agent_names:
            report["problems"].append(
                f"pin agent_model_{agent_name}: no such agent (stale name?) - "
                f"real names: {', '.join(sorted(agent_names))}"
            )
        if model not in catalog:
            report["problems"].append(
                f"pin agent_model_{agent_name}: model {model!r} is not in the "
                "catalog (rotated out? never installed?)"
            )

    summarizer = get_summarization_model_name()
    report["summarizer"] = summarizer
    if summarizer and summarizer not in catalog:
        report["problems"].append(
            f"summarization_model {summarizer!r} is not in the catalog - "
            "compaction degrades to the sliding-window fallback"
        )

    return report


def apply_onboarding(api_key: str) -> None:
    """Store the key, install the model set, point the main model at the alias."""
    set_api_key(KEY_NAME, api_key)

    from spruce_grove.atomic_json import mutate_json

    def _merge(existing):
        merged = dict(existing or {})
        for stale in STALE_MODELS:
            merged.pop(stale, None)
        merged.update(build_synthetic_models())
        return merged

    mutate_json(EXTRA_MODELS_PATH, _merge, default={})

    def _apply(cfg):
        cfg["DEFAULT"]["model"] = DRIVING_SEAT

    mutate_config(CONFIG_FILE, _apply)


@register_command(
    "onboard-synthetic",
    "Onboard a Synthetic.new subscription: rotation-safe text/vision alias models, API key, and the driving seat",
    usage="/onboard-synthetic [check]",
    aliases=["synthetic-onboard"],
    category="setup",
    detailed_help=(
        "Dedicated onboarding for Synthetic.new subscribers.\n\n"
        "Installs the rotation-safe syn: alias family (large/small text and\n"
        "vision), the pinned fallback models, stores your API key in the shared\n"
        "credential store, and points the main model at syn:large:text (the\n"
        "driving seat). Vision is optimised automatically: syn:large:text\n"
        "carries supports_vision (DeepSeek-V4.1-Flash takes images) so image\n"
        "work routes to the cheapest multimodal alias; heavy vision stays on\n"
        "syn:large:vision (Kimi-K3). Rotated-out pins\n"
        "(e.g. hf:zai-org/GLM-5.2) are pruned; user-added models are kept.\n\n"
        "  /onboard-synthetic          interactive onboarding\n"
        "  /onboard-synthetic check    verify key + live model catalog (rotation\n"
        "                              drift), free quota readout (/v2/quotas),\n"
        "                              the quota-free embeddings endpoint, and\n"
        "                              the routing audit (every agent pin must\n"
        "                              name a real agent and a live model)\n"
    ),
)
def handle_onboard_synthetic_command(command: str) -> bool:
    """Interactive onboarding for Synthetic.new subscribers."""
    from spruce_grove.messaging import (
        emit_error,
        emit_info,
        emit_success,
        emit_warning,
    )

    mode = command.replace("/onboard-synthetic", "", 1).strip().lower()
    if mode.startswith("check"):
        mode = "check"

    api_key = get_api_key(KEY_NAME)
    have_key = bool(api_key)

    if mode == "check":
        if not have_key:
            emit_error(
                f"[{KEY_NAME}] is not set - run /onboard-synthetic to configure it."
            )
            return True
        ok, detail, live_ids = fetch_model_ids(api_key)
        if ok:
            emit_success(f"synthetic.new: {detail}")
        else:
            emit_error(f"synthetic.new: {detail}")
        if ok:
            rotated, unpinned = check_catalog_drift(live_ids)
            if rotated:
                emit_warning(
                    "pinned models no longer on the subscription: "
                    + ", ".join(rotated)
                    + " - re-run /onboard-synthetic to refresh and prune"
                )
            if unpinned:
                emit_info(
                    "new on the subscription (not installed): " + ", ".join(unpinned)
                )
        ok_q, quota_detail = probe_quotas(api_key)
        if ok_q:
            emit_success(f"quotas: {quota_detail}")
        else:
            emit_warning(f"quotas: {quota_detail}")
        ok_e, embed_detail = probe_embeddings(api_key)
        if ok_e:
            emit_success(f"embeddings: {embed_detail}")
        else:
            emit_warning(f"embeddings: {embed_detail}")
        emit_info(
            "also available: Anthropic-compat "
            + ANTHROPIC_ENDPOINT
            + " (messages), "
            + SEARCH_URL
            + " (quota-free web search)"
        )
        emit_info(
            "models installed in extra_models.json: "
            + ", ".join(sorted(build_synthetic_models()))
        )
        routing = verify_model_routing()
        emit_info(f"routing: global model -> {routing['global']}")
        emit_info(f"routing: summarizer -> {routing['summarizer']}")
        for pin in routing["pins"]:
            emit_info(f"routing: {pin['agent']} -> {pin['model']}")
        if routing["problems"]:
            for problem in routing["problems"]:
                emit_warning(f"routing: {problem}")
        else:
            emit_success(
                "routing: every pin targets a live catalog model and a real agent"
            )
        return True

    emit_info("Synthetic.new onboarding - what this sets up:")
    emit_info("  1. Your API key, stored in the shared credential store")
    emit_info("  2. The rotation-safe alias family: syn:large:text (driving seat,")
    emit_info("     currently DeepSeek-V4.1-Flash), syn:small:text (0.1x-class")
    emit_info("     fan-out), syn:large:vision (Kimi-K3), syn:small:vision")
    emit_info("     (Qwen3.8-27B) - vision models tagged for image work")
    emit_info("  3. The pinned fallbacks (labelled with their rotation/quota risk),")
    emit_info("     minus anything the catalog has rotated out (pruned automatically)")
    emit_info("  4. Main model -> syn:large:text")

    if have_key:
        emit_success(f"[{KEY_NAME}] is already configured - reusing it.")
    else:
        key = getpass.getpass(f"Paste your {KEY_NAME} (input hidden): ").strip()
        if not key:
            emit_error("No key entered - onboarding cancelled. Nothing was changed.")
            return True
        set_api_key(KEY_NAME, key)
        api_key = key
        emit_success("Key stored in the shared credential store.")

    ok, detail = probe_endpoint(api_key)
    if ok:
        emit_success(f"endpoint check passed: {detail}")
    else:
        emit_error(
            f"endpoint check failed: {detail}. The key is stored; fix the endpoint "
            "issue and re-run /onboard-synthetic check. Models are NOT installed "
            "until the check passes."
        )
        return True

    apply_onboarding(api_key)
    emit_success("alias family + pinned models written to extra_models.json")
    emit_info(f"main model -> {DRIVING_SEAT}")
    emit_info(
        "image work routes to syn:large:text (cheapest multimodal); "
        "heavy vision -> syn:large:vision"
    )
    emit_info("Quota wisdom, per the current rate-limits docs:")
    emit_info("  prefer the syn: aliases - pinned upstream ids rotate and 404")
    emit_info("  Kimi-K3 is the baseline: one call counts as one request")
    emit_info("  GLM Flash aliases stretch quota furthest (~0.1 requests per call)")
    emit_info("  embeddings (" + EMBEDDINGS_MODEL + ") are free - index away")
    emit_info("Verify any time with /onboard-synthetic check")
    return True


__all__ = [
    "ALIAS_MODELS",
    "PINNED_MODELS",
    "DRIVING_SEAT",
    "KEY_NAME",
    "EXTRA_MODELS_PATH",
    "ENDPOINT",
    "ANTHROPIC_ENDPOINT",
    "QUOTAS_URL",
    "SEARCH_URL",
    "EMBEDDINGS_URL",
    "EMBEDDINGS_MODEL",
    "STALE_MODELS",
    "build_synthetic_models",
    "fetch_model_ids",
    "check_catalog_drift",
    "probe_endpoint",
    "probe_quotas",
    "probe_embeddings",
    "apply_onboarding",
    "handle_onboard_synthetic_command",
]
