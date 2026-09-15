"""Tests for the self-update (self-heal) module."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from spruce_grove.self_update import (
    auto_update_disabled,
    perform_self_update,
    self_update_supported,
)


@pytest.fixture(autouse=True)
def _fake_messaging():
    """Keep message-bus emissions inert and observable."""
    with (
        patch("spruce_grove.self_update.emit_info") as mock_info,
        patch("spruce_grove.self_update.emit_success") as mock_success,
        patch("spruce_grove.self_update.emit_warning") as mock_warning,
    ):
        yield {
            "info": mock_info,
            "success": mock_success,
            "warning": mock_warning,
        }


class TestAutoUpdateDisabled:
    def test_env_unset_means_enabled(self, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        assert auto_update_disabled() is False

    @pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes", "on", "On"])
    def test_truthy_values_disable(self, monkeypatch, value):
        monkeypatch.setenv("NO_AUTO_UPDATE", value)
        assert auto_update_disabled() is True

    @pytest.mark.parametrize("value", ["", "0", "false", "off", "no"])
    def test_falsy_values_do_not_disable(self, monkeypatch, value):
        monkeypatch.setenv("NO_AUTO_UPDATE", value)
        assert auto_update_disabled() is False


class TestSelfUpdateSupported:
    def test_requires_uv_binary(self, monkeypatch):
        monkeypatch.setattr(
            "spruce_grove.self_update.shutil.which", lambda name: None
        )
        assert self_update_supported() is False

    def test_requires_uv_managed_install(self, monkeypatch):
        monkeypatch.setattr(
            "spruce_grove.self_update.shutil.which", lambda name: "/usr/bin/uv"
        )
        with patch(
            "spruce_grove.self_update._running_from_uv_tool",
            return_value=False,
        ):
            assert self_update_supported() is False

    def test_supported_when_uv_and_tool_env(self, monkeypatch):
        monkeypatch.setattr(
            "spruce_grove.self_update.shutil.which", lambda name: "/usr/bin/uv"
        )
        with patch(
            "spruce_grove.self_update._running_from_uv_tool", return_value=True
        ):
            assert self_update_supported() is True


class TestPerformSelfUpdate:
    def test_success_runs_uv_upgrade(self, _fake_messaging, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        completed = MagicMock(returncode=0, stdout="ok", stderr="")
        with patch(
            "spruce_grove.self_update.subprocess.run", return_value=completed
        ) as mock_run:
            assert perform_self_update("1.0.3", "1.0.36") is True

        mock_run.assert_called_once()
        args = mock_run.call_args.args[0]
        assert args == ["uv", "tool", "upgrade", "spruce-grove"]
        _fake_messaging["success"].assert_called_once()

    def test_nonzero_exit_reports_failure(self, _fake_messaging, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        completed = MagicMock(returncode=2, stdout="", stderr="boom")
        with patch(
            "spruce_grove.self_update.subprocess.run", return_value=completed
        ):
            assert perform_self_update("1.0.3", "1.0.36") is False
        _fake_messaging["success"].assert_not_called()
        _fake_messaging["warning"].assert_called_once()

    def test_timeout_reports_failure(self, _fake_messaging, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        with patch(
            "spruce_grove.self_update.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="uv", timeout=180),
        ):
            assert perform_self_update("1.0.3", "1.0.36") is False
        _fake_messaging["warning"].assert_called_once()

    def test_disabled_env_short_circuits(self, _fake_messaging, monkeypatch):
        monkeypatch.setenv("NO_AUTO_UPDATE", "1")
        with patch(
            "spruce_grove.self_update.subprocess.run"
        ) as mock_run:
            assert perform_self_update("1.0.3", "1.0.36") is False
        mock_run.assert_not_called()
        _fake_messaging["info"].assert_called_once()

    def test_unsupported_install_short_circuits(self, _fake_messaging, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: False
        )
        with patch(
            "spruce_grove.self_update.subprocess.run"
        ) as mock_run:
            assert perform_self_update("1.0.3", "1.0.36") is False
        mock_run.assert_not_called()
        _fake_messaging["warning"].assert_called_once()

    def test_never_raises_on_unexpected_error(self, _fake_messaging, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        with patch(
            "spruce_grove.self_update.self_update_supported",
            side_effect=RuntimeError("surprise"),
        ):
            assert perform_self_update("1.0.3", "1.0.36") is False
        _fake_messaging["warning"].assert_called_once()
