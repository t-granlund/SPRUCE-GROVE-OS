"""The console can signal other people's work, so its actions must be right.

The rendering is checked lightly (it is presentation); the weight is on the
model -- signalling the wrong process, or a hard kill standing in for a clean
restart, is the kind of bug that costs someone a session.
"""

import signal
from typing import List, Optional

import pytest

from spruce_grove.live_sessions import LiveSession
from spruce_grove.plugins.grove_console import panel
from spruce_grove.plugins.grove_console.model import ConsoleModel, resume_command


def _session(pid: int, **kw) -> LiveSession:
    base = dict(
        pid=pid,
        ppid=pid - 1,
        tty=f"ttys{pid:03d}",
        terminal_open=True,
        kind="terminal",
        session_name=f"auto_session_20260922_180404_125317_{pid}",
        uptime_seconds=600,
    )
    base.update(kw)
    return LiveSession(**base)


class _Spy:
    """Records signals instead of delivering them."""

    def __init__(self, exc: Optional[Exception] = None):
        self.calls: List[tuple] = []
        self._exc = exc

    def __call__(self, pid: int, sig: int) -> None:
        self.calls.append((pid, sig))
        if self._exc:
            raise self._exc


@pytest.fixture
def sessions():
    return [_session(100), _session(200, title="Second"), _session(300)]


def _model(sessions, spy, monkeypatch, self_pid=9999):
    """Build a model whose session source is injected.

    Injection is required, not stylistic: ``scanner`` is a default argument,
    so it is bound at import time and monkeypatching the module attribute
    would not reach it.
    """
    return ConsoleModel(
        scanner=lambda **kw: list(sessions), sender=spy, self_pid=self_pid
    )


class TestSafety:
    """The console must never be a footgun against itself."""

    def test_refuses_to_signal_itself(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch, self_pid=100)
        model.selected = 0  # that is the console's own pid
        result = model.restart()
        assert result.ok is False
        assert spy.calls == []  # nothing was delivered
        assert "this session" in result.message.lower()

    def test_refuses_system_pids(self, monkeypatch):
        spy = _Spy()
        model = _model([_session(1)], spy, monkeypatch)
        assert model.restart().ok is False
        assert spy.calls == []

    def test_no_session_selected_is_graceful(self, monkeypatch):
        spy = _Spy()
        model = _model([], spy, monkeypatch)
        result = model.restart()
        assert result.ok is False
        assert spy.calls == []


class TestRestartIsTheGentlePath:
    def test_restart_sends_sigterm_not_sigkill(self, sessions, monkeypatch):
        """SIGTERM lets the session autosave on its way out."""
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        result = model.restart()
        assert result.ok is True
        assert spy.calls == [(100, signal.SIGTERM)]
        assert signal.SIGKILL not in [sig for _, sig in spy.calls]

    def test_restart_offers_a_resume_command(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        result = model.restart()
        assert result.resume_hint == (
            "spruce-grove --resume auto_session_20260922_180404_125317_100"
        )

    def test_kill_sends_sigkill(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        assert model.kill().ok is True
        assert spy.calls == [(100, signal.SIGKILL)]

    def test_dead_pid_is_reported_not_raised(self, sessions, monkeypatch):
        spy = _Spy(exc=ProcessLookupError())
        model = _model(sessions, spy, monkeypatch)
        result = model.restart()
        assert result.ok is False
        assert "already gone" in result.message

    def test_permission_error_is_reported_not_raised(self, sessions, monkeypatch):
        spy = _Spy(exc=PermissionError())
        model = _model(sessions, spy, monkeypatch)
        result = model.restart()
        assert result.ok is False
        assert "permitted" in result.message


class TestResumeCommand:
    def test_cwd_scopes_the_resume(self):
        """--cwd is what makes it a restart in the right place, not a new session."""
        cmd = resume_command(_session(1, cwd="/Users/t/proj"))
        assert cmd.endswith("--cwd")

    def test_no_cwd_means_no_flag(self):
        assert not resume_command(_session(1)).endswith("--cwd")

    def test_unidentified_session_has_no_resume(self):
        assert resume_command(_session(1, session_name=None)) is None


class TestNavigation:
    def test_moves_are_clamped_not_wrapped(self, sessions, monkeypatch):
        model = _model(sessions, _Spy(), monkeypatch)
        model.move(-1)
        assert model.selected == 0  # clamped at the top
        model.jump_last()
        assert model.selected == len(sessions) - 1
        model.move(1)
        assert model.selected == len(sessions) - 1  # clamped at the bottom

    def test_jump_first_and_last(self, sessions, monkeypatch):
        model = _model(sessions, _Spy(), monkeypatch)
        model.jump_last()
        assert model.selected == 2
        model.jump_first()
        assert model.selected == 0

    def test_selection_clamps_when_the_list_shrinks(self, sessions, monkeypatch):
        """A session closing under the cursor must not index out of range."""
        live = list(sessions)
        model = ConsoleModel(
            scanner=lambda **kw: list(live), sender=_Spy(), self_pid=9999
        )
        model.jump_last()
        live.pop()
        live.pop()  # two sessions closed under the cursor
        model.refresh(force=True)
        assert model.selected == 0
        assert model.current is not None

    def test_empty_list_has_no_current(self, monkeypatch):
        model = _model([], _Spy(), monkeypatch)
        assert model.current is None
        model.move(1)  # must not raise
        assert model.selected == 0


class TestRefresh:
    def test_throttled_unless_forced(self, sessions):
        calls = []

        def scanner(**kw):
            calls.append(kw)
            return list(sessions)

        model = ConsoleModel(scanner=scanner, sender=_Spy())
        before = len(calls)
        assert model.refresh(now=model.last_refresh + 0.1) is False
        assert len(calls) == before  # throttled: no rescan
        model.refresh(force=True)
        assert len(calls) == before + 1

    def test_reports_when_the_view_changed(self, sessions):
        live = list(sessions)
        model = ConsoleModel(scanner=lambda **kw: list(live), sender=_Spy())
        assert model.refresh(force=True) is False  # unchanged
        live.pop()
        assert model.refresh(force=True) is True

    def test_toggle_orphans_rescans_immediately(self, sessions):
        seen = []

        def scanner(**kw):
            seen.append(kw.get("include_closed"))
            return list(sessions)

        model = ConsoleModel(scanner=scanner, sender=_Spy())
        model.toggle_orphans()
        assert model.show_orphans is True
        assert seen[-1] is True


class TestKeyDispatch:
    """Two-step kill is the whole point -- one stray key must not kill."""

    def _dispatch(self, key, model, armed):
        state = {"armed": armed}
        exit_now = panel.on_key(
            key,
            model,
            armed=armed,
            arm=lambda: state.__setitem__("armed", True),
            disarm=lambda: state.__setitem__("armed", False),
        )
        return exit_now, state["armed"]

    def test_quit_keys_exit(self, sessions, monkeypatch):
        model = _model(sessions, _Spy(), monkeypatch)
        for key in ("q", "Q", "\x1b", "\x03"):
            assert self._dispatch(key, model, False)[0] is True

    def test_x_arms_rather_than_kills(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        exit_now, armed = self._dispatch("x", model, False)
        assert exit_now is False
        assert armed is True
        assert spy.calls == []  # nothing killed yet -- that is the safety

    def test_second_x_confirms_the_kill(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        self._dispatch("x", model, False)
        self._dispatch("x", model, True)
        assert spy.calls == [(100, signal.SIGKILL)]

    def test_any_other_key_cancels_the_armed_kill(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        exit_now, armed = self._dispatch("j", model, True)
        assert armed is False
        assert spy.calls == []
        assert "cancelled" in model.status

    def test_r_restarts(self, sessions, monkeypatch):
        spy = _Spy()
        model = _model(sessions, spy, monkeypatch)
        self._dispatch("r", model, False)
        assert spy.calls == [(100, signal.SIGTERM)]

    def test_navigation_keys(self, sessions, monkeypatch):
        model = _model(sessions, _Spy(), monkeypatch)
        self._dispatch("j", model, False)
        assert model.selected == 1
        self._dispatch("G", model, False)
        assert model.selected == 2
        self._dispatch("g", model, False)
        assert model.selected == 0


class TestRendering:
    def test_shows_every_session_and_the_detail(self, monkeypatch):
        long_title = "Desktop App QA Round Two"
        model = _model(
            [_session(100, title=long_title, cwd="/Users/t/desktop")],
            _Spy(),
            monkeypatch,
        )
        text = "\n".join(panel.compose(model, width=140, height=30, armed=False))
        assert long_title in text
        assert "/Users/t/desktop" in text
        assert "pid" in text

    def test_armed_footer_warns(self, sessions, monkeypatch):
        model = _model(sessions, _Spy(), monkeypatch)
        text = "\n".join(panel.compose(model, width=100, height=30, armed=True))
        assert "force-kill armed" in text
        # It is rendered in the left pane, which has no columns to spare, so
        # the warning is split across the pane width -- check the whole frame.
        assert "confirm" in text

    def test_empty_state_is_honest(self, monkeypatch):
        model = _model([], _Spy(), monkeypatch)
        text = "\n".join(panel.compose(model, width=100, height=30, armed=False))
        assert "none found" in text

    def test_narrow_terminal_does_not_crash(self, sessions, monkeypatch):
        model = _model(sessions, _Spy(), monkeypatch)
        for width in (10, 20, 40, 60):
            assert panel.compose(model, width=width, height=20, armed=False)


class TestPluginRegistration:
    """The plugin must be discoverable, and must own only its own command."""

    def test_help_entry_describes_the_command(self):
        from spruce_grove.plugins.grove_console.register_callbacks import _custom_help

        assert _custom_help() == [
            ("console", "See and tend the grove sessions running on this machine")
        ]

    def test_callback_is_registered_under_both_hooks(self):
        from spruce_grove.callbacks import get_callbacks

        # Importing the module is what registers it; discovery does this on
        # startup, so import explicitly here.
        import spruce_grove.plugins.grove_console.register_callbacks  # noqa: F401

        for hook in ("custom_command", "custom_command_help"):
            assert get_callbacks(hook), f"nothing registered for {hook}"

    def test_returns_none_for_other_commands(self):
        from spruce_grove.plugins.grove_console.register_callbacks import (
            _handle_custom_command,
        )

        assert _handle_custom_command("/whatever", "whatever") is None

    def test_returns_none_for_empty_name(self):
        from spruce_grove.plugins.grove_console.register_callbacks import (
            _handle_custom_command,
        )

        assert _handle_custom_command("/", "") is None

    def test_plugin_is_discovered_by_the_loader(self):
        """A plugin the loader cannot find is a plugin nobody can use."""
        from pathlib import Path

        from spruce_grove.plugins import _scan_plugin_names

        assert "grove_console" in _scan_plugin_names(Path("spruce_grove/plugins"))
