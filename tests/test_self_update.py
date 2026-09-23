"""Tests for the self-update (self-heal) module."""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from spruce_grove.self_update import (
    auto_update_disabled,
    mark_pending_update,
    pending_update,
    perform_self_update,
    run_deferred_update,
    self_update_supported,
    update_at_exit_disabled,
)


@pytest.fixture(autouse=True)
def _clear_pending_update():
    """The deferred stash lives in os.environ -- never let it leak a test."""
    keys = ("_SPRUCE_GROVE_PENDING_UPDATE", "_SPRUCE_GROVE_PENDING_UPDATE_TIMEOUT")
    for key in keys:
        os.environ.pop(key, None)
    yield
    for key in keys:
        os.environ.pop(key, None)


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
        monkeypatch.setattr("spruce_grove.self_update.shutil.which", lambda name: None)
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
        with patch("spruce_grove.self_update._running_from_uv_tool", return_value=True):
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
        with patch("spruce_grove.self_update.subprocess.run", return_value=completed):
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
        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
            assert perform_self_update("1.0.3", "1.0.36") is False
        mock_run.assert_not_called()
        _fake_messaging["info"].assert_called_once()

    def test_unsupported_install_short_circuits(self, _fake_messaging, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: False
        )
        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
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


class TestDeferredUpdate:
    """Actuation must never run mid-session -- it waits for exit.

    Regression: upgrading while the process can still lazily import tool
    modules swapped the code on disk under a live session, and the next lazy
    import half-mixed two versions. Deferral is the fix.
    """

    def test_defer_owns_console_schedules_instead_of_running(
        self, _fake_messaging, monkeypatch
    ):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        # stdin is a real TTY -> this process owns the console.
        fake_stdin = MagicMock()
        fake_stdin.isatty.return_value = True
        monkeypatch.setattr("sys.stdin", fake_stdin)

        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
            assert perform_self_update("1.0.3", "1.0.36", defer_to_exit=True) is True

        mock_run.assert_not_called()  # nothing ran now
        assert pending_update() == ("1.0.3", "1.0.36")

    def test_defer_without_console_leaves_it_to_the_parent(
        self, _fake_messaging, monkeypatch
    ):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        # stdin is a pipe -> a parent (the desktop shell) owns this process.
        fake_stdin = MagicMock()
        fake_stdin.isatty.return_value = False
        monkeypatch.setattr("sys.stdin", fake_stdin)

        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
            assert perform_self_update("1.0.3", "1.0.36", defer_to_exit=True) is False

        mock_run.assert_not_called()
        assert pending_update() is None  # nothing stashed for us to run
        _fake_messaging["info"].assert_called_once()

    def test_defer_still_respects_guards(self, _fake_messaging, monkeypatch):
        """A guard failure must not schedule work that cannot run."""
        monkeypatch.setenv("NO_AUTO_UPDATE", "1")
        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
            assert perform_self_update("1.0.3", "1.0.36", defer_to_exit=True) is False
        mock_run.assert_not_called()
        assert pending_update() is None

    def test_run_deferred_is_a_noop_when_nothing_pending(self, monkeypatch):
        monkeypatch.delenv("_SPRUCE_GROVE_PENDING_UPDATE", raising=False)
        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
            assert run_deferred_update() is False
        mock_run.assert_not_called()

    def test_run_deferred_actuates_a_stashed_update(self, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.delenv("SPRUCE_GROVE_UPDATE_AT_EXIT", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        mark_pending_update("1.0.3", "1.0.36", timeout=5.0)

        completed = MagicMock(returncode=0, stdout="ok", stderr="")
        with patch(
            "spruce_grove.self_update.subprocess.run", return_value=completed
        ) as mock_run:
            assert run_deferred_update() is True

        assert mock_run.call_args.args[0] == ["uv", "tool", "upgrade", "spruce-grove"]
        # The stash is cleared, so a second exit path cannot double-run it.
        assert pending_update() is None

    def test_run_deferred_clears_the_stash_even_on_failure(self, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        mark_pending_update("1.0.3", "1.0.36", timeout=5.0)

        completed = MagicMock(returncode=1, stdout="", stderr="nope")
        with patch("spruce_grove.self_update.subprocess.run", return_value=completed):
            assert run_deferred_update() is False

        assert pending_update() is None

    def test_run_deferred_never_raises(self, monkeypatch):
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        monkeypatch.setattr(
            "spruce_grove.self_update.self_update_supported", lambda: True
        )
        mark_pending_update("1.0.3", "1.0.36", timeout=5.0)
        with patch(
            "spruce_grove.self_update.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="uv", timeout=5),
        ):
            assert run_deferred_update() is False
        assert pending_update() is None

    def test_exit_optout_is_respected(self, monkeypatch):
        monkeypatch.setenv("SPRUCE_GROVE_UPDATE_AT_EXIT", "0")
        assert update_at_exit_disabled() is True
        monkeypatch.setenv("SPRUCE_GROVE_UPDATE_AT_EXIT", "1")
        assert update_at_exit_disabled() is False

    def test_env_optout_blocks_actuation(self, monkeypatch):
        monkeypatch.setenv("SPRUCE_GROVE_UPDATE_AT_EXIT", "0")
        monkeypatch.delenv("NO_AUTO_UPDATE", raising=False)
        mark_pending_update("1.0.3", "1.0.36", timeout=5.0)
        with patch("spruce_grove.self_update.subprocess.run") as mock_run:
            assert run_deferred_update() is False
        mock_run.assert_not_called()

    def test_mark_pending_is_idempotent(self, monkeypatch):
        monkeypatch.delenv("_SPRUCE_GROVE_PENDING_UPDATE", raising=False)
        mark_pending_update("1.0.3", "1.0.36", timeout=5.0)
        mark_pending_update("1.0.3", "1.0.37", timeout=9.0)
        assert pending_update() == ("1.0.3", "1.0.37")
