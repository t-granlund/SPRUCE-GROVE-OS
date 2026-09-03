"""Tests for opt-in Logfire wiring (spruce_grove/observability.py)."""

import sys
import types
from contextlib import nullcontext
from unittest.mock import patch

from spruce_grove import observability
from spruce_grove.config import get_enable_logfire


class TestGetEnableLogfire:
    def test_defaults_to_false(self):
        with patch("spruce_grove.config.get_value", return_value=None):
            assert get_enable_logfire() is False

    def test_truthy_values(self):
        for val in ("1", "true", "Yes", "ON"):
            with patch("spruce_grove.config.get_value", return_value=val):
                assert get_enable_logfire() is True, val

    def test_falsy_values(self):
        for val in ("0", "false", "no", "off", "banana"):
            with patch("spruce_grove.config.get_value", return_value=val):
                assert get_enable_logfire() is False, val


class TestLogfireOptedIn:
    def test_env_var_wins(self, monkeypatch):
        monkeypatch.setenv("SPRUCE_GROVE_ENABLE_LOGFIRE", "1")
        with patch("spruce_grove.observability.get_enable_logfire", return_value=False):
            assert observability.logfire_opted_in() is True

    def test_falls_back_to_config(self, monkeypatch):
        monkeypatch.delenv("SPRUCE_GROVE_ENABLE_LOGFIRE", raising=False)
        with patch("spruce_grove.observability.get_enable_logfire", return_value=True):
            assert observability.logfire_opted_in() is True

    def test_default_is_opted_out(self, monkeypatch):
        monkeypatch.delenv("SPRUCE_GROVE_ENABLE_LOGFIRE", raising=False)
        with patch("spruce_grove.observability.get_enable_logfire", return_value=False):
            assert observability.logfire_opted_in() is False


class TestConfigureLogfire:
    def test_noop_when_opted_out(self):
        with patch("spruce_grove.observability.logfire_opted_in", return_value=False):
            assert observability.configure_logfire() is False

    def test_missing_package_warns_and_fails_soft(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "logfire", None)  # import -> ImportError
        with (
            patch("spruce_grove.observability.logfire_opted_in", return_value=True),
            patch("spruce_grove.messaging.emit_warning") as warn,
        ):
            assert observability.configure_logfire() is False
        warn.assert_called_once()

    def test_configures_and_instruments(self, monkeypatch):
        fake = types.SimpleNamespace(configure=None, instrument_pydantic_ai=None)
        calls = {}
        fake.configure = lambda **kw: calls.setdefault("configure", kw)
        fake.instrument_pydantic_ai = lambda: calls.setdefault("instrumented", True)
        monkeypatch.setitem(sys.modules, "logfire", fake)
        with (
            patch("spruce_grove.observability.logfire_opted_in", return_value=True),
            patch("spruce_grove.messaging.emit_system_message"),
        ):
            assert observability.configure_logfire() is True
        assert calls["configure"]["send_to_logfire"] == "if-token-present"
        assert calls["configure"]["service_name"] == "spruce-grove"
        assert calls["instrumented"] is True

    def test_configure_error_warns_and_fails_soft(self, monkeypatch):
        def boom(**_kw):
            raise RuntimeError("bad token")

        fake = types.SimpleNamespace(
            configure=boom, instrument_pydantic_ai=lambda: None
        )
        monkeypatch.setitem(sys.modules, "logfire", fake)
        with (
            patch("spruce_grove.observability.logfire_opted_in", return_value=True),
            patch("spruce_grove.messaging.emit_warning") as warn,
        ):
            assert observability.configure_logfire() is False
        warn.assert_called_once()


class TestEmitCancellation:
    def test_noop_when_logfire_is_inactive(self, monkeypatch):
        fake = types.SimpleNamespace(warning=lambda *_args, **_kwargs: None)
        monkeypatch.setitem(sys.modules, "logfire", fake)
        monkeypatch.setattr(observability, "_logfire_active", False)

        with patch.object(fake, "warning") as warning:
            observability.emit_cancellation("group-1")

        warning.assert_not_called()

    def test_emits_event_when_logfire_is_active(self, monkeypatch):
        fake = types.SimpleNamespace(warning=lambda *_args, **_kwargs: None)
        monkeypatch.setitem(sys.modules, "logfire", fake)
        monkeypatch.setattr(observability, "_logfire_active", True)

        with patch.object(fake, "warning") as warning:
            observability.emit_cancellation("group-1")

        warning.assert_called_once_with("Agent run cancelled", group_id="group-1")

    def test_emits_as_child_of_captured_agent_context(self, monkeypatch):
        context = {"traceparent": "00-trace-span-01"}
        fake = types.SimpleNamespace(
            get_context=lambda: context,
            attach_context=lambda carrier: nullcontext(carrier),
            warning=lambda *_args, **_kwargs: None,
        )
        monkeypatch.setitem(sys.modules, "logfire", fake)
        monkeypatch.setattr(observability, "_logfire_active", True)
        monkeypatch.setattr(observability, "_agent_contexts", {})

        observability.capture_agent_context("group-1")
        with (
            patch.object(fake, "attach_context", wraps=fake.attach_context) as attach,
            patch.object(fake, "warning") as warning,
        ):
            observability.emit_cancellation("group-1")

        attach.assert_called_once_with(context)
        warning.assert_called_once_with("Agent run cancelled", group_id="group-1")
        assert "group-1" not in observability._agent_contexts

    def test_clear_agent_context(self, monkeypatch):
        monkeypatch.setattr(
            observability, "_agent_contexts", {"group-1": {"traceparent": "value"}}
        )

        observability.clear_agent_context("group-1")

        assert observability._agent_contexts == {}

    def test_logfire_error_fails_soft(self, monkeypatch):
        def boom(*_args, **_kwargs):
            raise RuntimeError("collector exploded")

        monkeypatch.setitem(sys.modules, "logfire", types.SimpleNamespace(warning=boom))
        monkeypatch.setattr(observability, "_logfire_active", True)

        observability.emit_cancellation("group-1")
