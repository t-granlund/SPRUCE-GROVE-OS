"""Dedicated onboarding for Synthetic.new subscribers.

``/onboard-synthetic`` walks a subscriber through everything needed to run the
grove exactly the way the maintainer runs it: the rotation-safe ``syn:`` alias
family for text and vision, the pinned fallback models, the API key stored in
the shared credential store, and the main model pointed at the driving seat.

Why aliases: pinned upstream model ids rotate and 404. The ``syn:`` aliases
survive rotation, so they are the right things to bake into config. The pinned
entries ship anyway (clearly labelled with their quota-burn risk) for the days
an alias is having a bad afternoon.

Everything is idempotent: re-running refreshes the alias definitions and keeps
any user-added models already present in ``extra_models.json``.
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
        "Synthetic alias (rotation-safe) -> hf:zai-org/GLM-5.3-Flash. "
        "1.0x driving-seat reasoning.",
    ),
    "syn:small:text": _model(
        "syn:small:text",
        196608,
        "Synthetic alias (rotation-safe) -> hf:zai-org/GLM-4.7-Flash. "
        "0.1x fan-out + mechanical gates.",
    ),
    "syn:large:vision": _model(
        "syn:large:vision",
        524288,
        "Synthetic alias (rotation-safe) -> hf:moonshotai/Kimi-K3. Large vision.",
        supports_vision=True,
    ),
    "syn:small:vision": _model(
        "syn:small:vision",
        262144,
        "Synthetic alias (rotation-safe) -> hf:Qwen/Qwen3.8-27B. Small vision.",
        supports_vision=True,
    ),
}

# Pinned upstream ids — rotation 404 risk, so always prefer the syn: aliases.
PINNED_MODELS = {
    "hf:zai-org/GLM-5.2": _model(
        "hf:zai-org/GLM-5.2",
        524288,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:large:text). Always-on included.",
    ),
    "hf:zai-org/GLM-4.7-Flash": _model(
        "hf:zai-org/GLM-4.7-Flash",
        196608,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:small:text). Always-on included.",
    ),
    "hf:moonshotai/Kimi-K3": _model(
        "hf:moonshotai/Kimi-K3",
        524288,
        "Pinned Synthetic model (3.0x quota burn; prefer syn:large:vision). Always-on included.",
    ),
    "hf:Qwen/Qwen3.8-27B": _model(
        "hf:Qwen/Qwen3.8-27B",
        262144,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:small:vision). Always-on included.",
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
    "hf:zai-org/GLM-5.3-Flash": _model(
        "hf:zai-org/GLM-5.3-Flash",
        524288,
        "Pinned Synthetic model (rotation 404 risk; prefer syn:large:text). "
        "Always-on included. Current syn:large:text upstream.",
        max_output_tokens=65536,
    ),
}

DRIVING_SEAT = "syn:large:text"


def build_synthetic_models() -> dict:
    """The full model set this onboarding installs (aliases + pinned)."""
    models = dict(ALIAS_MODELS)
    models.update(PINNED_MODELS)
    return models


def probe_endpoint(api_key: str, timeout: int = 20) -> tuple[bool, str]:
    """Live check against the Synthetic endpoint. Returns (ok, detail)."""
    req = urllib.request.Request(
        f"{ENDPOINT}/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
            ids = body.get("data") or []
            return True, f"endpoint answered, {len(ids)} models visible"
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "key rejected (401/403) — check the key on synthetic.new"
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # network unreachable, DNS, timeout …
        return False, f"could not reach endpoint: {exc}"


def apply_onboarding(api_key: str) -> None:
    """Store the key, install the model set, point the main model at the alias."""
    set_api_key(KEY_NAME, api_key)

    from spruce_grove.atomic_json import mutate_json

    def _merge(existing):
        merged = dict(existing or {})
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
        "driving seat). Vision is optimised automatically: the vision aliases\n"
        "carry supports_vision so image work routes to them.\n\n"
        "  /onboard-synthetic          interactive onboarding\n"
        "  /onboard-synthetic check    verify key + endpoint without changing anything\n"
    ),
)
def handle_onboard_synthetic_command(command: str) -> bool:
    """Interactive onboarding for Synthetic.new subscribers."""
    from spruce_grove.messaging import emit_error, emit_info, emit_success

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
        ok, detail = probe_endpoint(api_key)
        if ok:
            emit_success(f"synthetic.new: {detail}")
        else:
            emit_error(f"synthetic.new: {detail}")
        emit_info(
            "models installed in extra_models.json: "
            + ", ".join(sorted(build_synthetic_models()))
        )
        return True

    emit_info("Synthetic.new onboarding - what this sets up:")
    emit_info("  1. Your API key, stored in the shared credential store")
    emit_info("  2. The rotation-safe alias family: syn:large:text (driving seat, 1.0x),")
    emit_info("     syn:small:text (fan-out, 0.1x), syn:large:vision (Kimi-K3),")
    emit_info("     syn:small:vision (Qwen3.8-27B) - vision models tagged for image work")
    emit_info("  3. The pinned fallbacks (labelled with their rotation/quota risk)")
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
    emit_info("vision routed to the syn:* vision aliases (supports_vision tagged)")
    emit_info("Quota wisdom, earned the hard way:")
    emit_info("  prefer the syn: aliases - pinned upstream ids rotate and 404")
    emit_info("  Kimi-K3 burns 3.0x quota - keep it behind syn:large:vision")
    emit_info("  syn:small:text is your 0.1x workhorse for fan-out and gates")
    emit_info("Verify any time with /onboard-synthetic check")
    return True


__all__ = [
    "ALIAS_MODELS",
    "PINNED_MODELS",
    "DRIVING_SEAT",
    "KEY_NAME",
    "EXTRA_MODELS_PATH",
    "build_synthetic_models",
    "probe_endpoint",
    "apply_onboarding",
    "handle_onboard_synthetic_command",
]
