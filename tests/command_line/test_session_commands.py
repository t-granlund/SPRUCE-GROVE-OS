"""Tests for session_commands.py to achieve 100% coverage."""

from unittest.mock import MagicMock, patch

import pytest


class TestGetCommandsHelp:
    def test_lazy_import(self):
        from spruce_grove.command_line.session_commands import get_commands_help

        with patch(
            "spruce_grove.command_line.command_handler.get_commands_help",
            return_value="help text",
        ):
            result = get_commands_help()
            assert result == "help text"


class TestHandleSessionCommand:
    def _run(self, command):
        from spruce_grove.command_line.session_commands import handle_session_command

        return handle_session_command(command)

    def test_session_show_id(self):
        with (
            patch(
                "spruce_grove.config.get_current_session_name",
                return_value="auto_session_abc123",
            ),
            patch("spruce_grove.messaging.emit_info") as mock_info,
        ):
            result = self._run("/session")
            assert result is True
            mock_info.assert_called_once()
            # Both the session-line and the prefix-path show the full name
            # verbatim (no id/name duality post-unification).
            assert "auto_session_abc123" in mock_info.call_args[0][0]

    def test_session_id_subcommand(self):
        with (
            patch(
                "spruce_grove.config.get_current_session_name",
                return_value="auto_session_xyz",
            ),
            patch("spruce_grove.messaging.emit_info"),
        ):
            assert self._run("/session id") is True

    def test_session_show_user_named(self):
        """User-named session displays the full name verbatim, no auto_ prefix."""
        with (
            patch(
                "spruce_grove.config.get_current_session_name",
                return_value="mywork",
            ),
            patch("spruce_grove.messaging.emit_info") as mock_info,
        ):
            assert self._run("/session") is True
            rendered = mock_info.call_args[0][0]
            assert "mywork" in rendered
            # Regression guard: must NOT re-synthesize auto_session_mywork
            assert "auto_session_mywork" not in rendered

    def test_session_new(self):
        with (
            patch(
                "spruce_grove.config.rotate_session_name",
                return_value="auto_session_new123",
            ),
            patch("spruce_grove.messaging.emit_success") as mock_s,
        ):
            assert self._run("/session new") is True
            # Post-LEAN-Phase-2 emits the full name (not the bare id).
            assert "auto_session_new123" in mock_s.call_args[0][0]

    def test_session_invalid(self):
        with patch("spruce_grove.messaging.emit_warning") as mock_w:
            assert self._run("/session bad") is True
            mock_w.assert_called_once()


class TestHandleCompactCommand:
    @pytest.fixture(autouse=True)
    def _mock_autosave(self):
        with patch("spruce_grove.config.auto_save_session_if_enabled") as autosave:
            self.autosave = autosave
            yield

    def _run(self, cmd="/compact"):
        from spruce_grove.command_line.session_commands import handle_compact_command

        return handle_compact_command(cmd)

    def test_mid_run_queues_compaction_for_next_model_call(self):
        controller = MagicMock()
        with (
            patch("spruce_grove.messaging.run_ui.is_run_active", return_value=True),
            patch(
                "spruce_grove.messaging.pause_controller.get_pause_controller",
                return_value=controller,
            ),
            patch("spruce_grove.messaging.emit_info") as emit_info,
        ):
            assert self._run() is True

        controller.request_compaction.assert_called_once_with()
        assert "next model call" in emit_info.call_args[0][0]

    def test_no_history(self):
        agent = MagicMock()
        agent.get_message_history.return_value = []
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.messaging.emit_warning") as mw,
        ):
            assert self._run() is True
            mw.assert_called_once()

    def test_truncation_strategy(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1", "m2", "m3"]
        agent.estimate_tokens_for_message.return_value = 100
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.config.get_compaction_strategy",
                return_value="truncation",
            ),
            patch("spruce_grove.agents._compaction.build_compaction_strategy"),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=["m3"],
            ) as rcs,
            patch("spruce_grove.messaging.emit_info"),
            patch("spruce_grove.messaging.emit_success") as ms,
        ):
            assert self._run() is True
            rcs.assert_called_once()
            self.autosave.assert_called_once_with(force=True)
            ms.assert_called_once()
            assert "truncation" in ms.call_args[0][0]

    def test_summarization_strategy(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1", "m2"]
        agent.estimate_tokens_for_message.return_value = 100
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.config.get_compaction_strategy",
                return_value="summarization",
            ),
            patch("spruce_grove.agents._compaction.build_compaction_strategy"),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=["summary", "m2"],
            ),
            patch("spruce_grove.messaging.emit_info"),
            patch("spruce_grove.messaging.emit_success") as ms,
        ):
            assert self._run() is True
            self.autosave.assert_called_once_with(force=True)
            ms.assert_called_once()

    def test_save_failure_does_not_report_compaction_success(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1", "m2"]
        agent.estimate_tokens_for_message.return_value = 100
        self.autosave.return_value = False
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.config.get_compaction_strategy",
                return_value="summarization",
            ),
            patch("spruce_grove.agents._compaction.build_compaction_strategy"),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=["summary"],
            ),
            patch("spruce_grove.messaging.emit_info"),
            patch("spruce_grove.messaging.emit_success") as ms,
        ):
            assert self._run() is True

        self.autosave.assert_called_once_with(force=True)
        ms.assert_not_called()

    def test_compaction_fails(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1"]
        agent.estimate_tokens_for_message.return_value = 100
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.config.get_compaction_strategy",
                return_value="summarization",
            ),
            patch("spruce_grove.agents._compaction.build_compaction_strategy"),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=[],
            ),
            patch("spruce_grove.messaging.emit_info"),
            patch("spruce_grove.messaging.emit_error") as me,
        ):
            assert self._run() is True
            self.autosave.assert_not_called()
            me.assert_called_once()

    def test_exception(self):
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                side_effect=Exception("boom"),
            ),
            patch("spruce_grove.messaging.emit_error") as me,
        ):
            assert self._run() is True
            assert "boom" in me.call_args[0][0]

    def test_zero_before_tokens(self):
        """Cover the before_tokens == 0 branch for reduction_pct."""
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1"]
        agent.estimate_tokens_for_message.return_value = 0
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.config.get_compaction_strategy",
                return_value="summarization",
            ),
            patch("spruce_grove.agents._compaction.build_compaction_strategy"),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=["s"],
            ),
            patch("spruce_grove.messaging.emit_info"),
            patch("spruce_grove.messaging.emit_success"),
        ):
            assert self._run() is True


class TestHandleTruncateCommand:
    def _run(self, cmd):
        from spruce_grove.command_line.session_commands import handle_truncate_command

        return handle_truncate_command(cmd)

    @pytest.mark.parametrize(
        "cmd",
        ["/truncate", "/truncate abc", "/truncate -1", "/truncate 1 2"],
        ids=["missing_arg", "invalid_n", "negative_n", "too_many_args"],
    )
    def test_invalid_args_return_true(self, cmd):
        with patch("spruce_grove.messaging.emit_error"):
            assert self._run(cmd) is True

    def test_no_history(self):
        agent = MagicMock()
        agent.get_message_history.return_value = []
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.messaging.emit_warning"),
        ):
            assert self._run("/truncate 5") is True

    def test_already_small(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["a", "b"]
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.messaging.emit_info"),
        ):
            assert self._run("/truncate 5") is True

    def test_success(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["sys", "a", "b", "c", "d"]
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=["sys", "c", "d"],
            ) as rcs,
            patch("spruce_grove.messaging.emit_success"),
        ):
            assert self._run("/truncate 3") is True
            # The sliding window is asked for N-1 recent messages (+ first).
            assert rcs.call_args[0][0].keep_messages == 2
            hist = agent.set_message_history.call_args[0][0]
            assert len(hist) == 3
            assert hist[0] == "sys"

    def test_n_equals_1(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["sys", "a", "b"]
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.agents._compaction.resolve_agent_model"),
            patch(
                "spruce_grove.agents._compaction.run_compaction_sync",
                return_value=["sys"],
            ) as rcs,
            patch("spruce_grove.messaging.emit_success"),
        ):
            assert self._run("/truncate 1") is True
            assert rcs.call_args[0][0].keep_messages == 1
            assert agent.set_message_history.call_args[0][0] == ["sys"]


class TestHandleAutosaveLoadCommand:
    def test_returns_marker(self):
        from spruce_grove.command_line.session_commands import (
            handle_autosave_load_command,
        )

        assert handle_autosave_load_command("/autosave_load") == "__AUTOSAVE_LOAD__"


class TestHandleDumpContextCommand:
    def _run(self, cmd):
        from spruce_grove.command_line.session_commands import (
            handle_dump_context_command,
        )

        return handle_dump_context_command(cmd)

    def test_missing_name(self):
        with patch("spruce_grove.messaging.emit_warning"):
            assert self._run("/dump_context") is True

    def test_no_history(self):
        agent = MagicMock()
        agent.get_message_history.return_value = []
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.messaging.emit_warning"),
        ):
            assert self._run("/dump_context mysession") is True

    def test_success(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1", "m2"]
        meta = MagicMock(
            message_count=2,
            total_tokens=200,
            pickle_path="a.pkl",
            metadata_path="a.json",
        )
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.session_lifecycle.persist_named_session",
                return_value=meta,
            ),
            patch("spruce_grove.messaging.emit_success"),
        ):
            assert self._run("/dump_context mysession") is True

    def test_exception(self):
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1"]
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.session_lifecycle.persist_named_session",
                side_effect=Exception("disk full"),
            ),
            patch("spruce_grove.messaging.emit_error") as me,
        ):
            assert self._run("/dump_context mysession") is True
            assert "disk full" in me.call_args[0][0]

    def test_reserved_prefix_rejected(self):
        """User cannot squat on the auto_session_ namespace via /dump_context.

        Pre-unification, /dump_context bypassed every validator and would
        happily write ``contexts/auto_session_anything.pkl``, polluting the
        autosave namespace. The new contract routes through
        persist_named_session and validates input first.
        """
        agent = MagicMock()
        agent.get_message_history.return_value = ["m1"]
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch("spruce_grove.messaging.emit_error") as me,
        ):
            assert self._run("/dump_context auto_session_squat") is True
            assert "reserved" in me.call_args[0][0].lower()


class TestHandleLoadContextCommand:
    def _run(self, cmd):
        from spruce_grove.command_line.session_commands import (
            handle_load_context_command,
        )

        return handle_load_context_command(cmd)

    def test_missing_name(self):
        with patch("spruce_grove.messaging.emit_warning"):
            assert self._run("/load_context") is True

    @pytest.mark.parametrize(
        "sessions,called",
        [(["s1"], True), ([], False)],
        ids=["with_available", "no_available"],
    )
    def test_file_not_found(self, sessions, called):
        with (
            patch(
                "spruce_grove.command_line.session_commands.load_session",
                side_effect=FileNotFoundError(),
            ),
            patch(
                "spruce_grove.command_line.session_commands.list_sessions",
                return_value=sessions,
            ),
            patch("spruce_grove.messaging.emit_error"),
            patch("spruce_grove.messaging.emit_info") as mi,
        ):
            assert self._run("/load_context missing") is True
            if called:
                mi.assert_called_once()
            else:
                mi.assert_not_called()

    def test_generic_exception(self):
        with (
            patch(
                "spruce_grove.command_line.session_commands.load_session",
                side_effect=Exception("corrupt"),
            ),
            patch("spruce_grove.messaging.emit_error") as me,
        ):
            assert self._run("/load_context bad") is True
            assert "corrupt" in me.call_args[0][0]

    def test_success(self):
        """/load_context NAME rotates the singleton (does NOT pin).

        This is the deliberate, original ``/load_context`` semantic from
        commit ``cc04629b`` (Mike Pfaffenberger, 2025-10-11):
        ``/dump_context`` + ``/load_context`` are a snapshot pair (like
        ``pg_dump`` / ``pg_restore``, save games, git stash). Loading a
        named snapshot must NOT cause subsequent autosaves to overwrite
        that snapshot -- the rotate forks future writes to a fresh
        ``auto_session_<TS>`` file so the loaded reference point stays
        frozen on disk. The ``-r NAME`` continuation path pins (and saves
        back in place); the asymmetry between the two verbs is
        intentional and load-bearing. Do NOT "unify" them.
        """
        agent = MagicMock()
        agent.estimate_tokens_for_message.return_value = 50
        with (
            patch(
                "spruce_grove.command_line.session_commands.load_session",
                return_value=["m1", "m2"],
            ),
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.config.rotate_session_name",
                return_value="auto_session_20260101_120000",
            ) as mock_rotate,
            patch("spruce_grove.messaging.emit_success") as mock_success,
            patch("spruce_grove.command_line.autosave_menu.display_resumed_history"),
        ):
            assert self._run("/load_context mysession") is True
            mock_rotate.assert_called_once_with()
            # Success line surfaces the new autosave id so the user is
            # never surprised about where their next saves are landing.
            success_text = mock_success.call_args[0][0]
            assert "auto_session_20260101_120000" in success_text


class TestHandleClearCommand:
    """Tests for the /clear command handler.

    Lives in session_commands so it shows up in /help (single source of truth).
    """

    def _run(self, command="/clear"):
        from spruce_grove.command_line.session_commands import handle_clear_command

        return handle_clear_command(command)

    def test_clear_wipes_history_and_rotates_session(self):
        agent = MagicMock()
        clipboard = MagicMock()
        clipboard.get_pending_count.return_value = 0
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.command_line.clipboard.get_clipboard_manager",
                return_value=clipboard,
            ),
            patch(
                "spruce_grove.config.finalize_autosave_session",
                return_value="new-session-id",
            ),
            patch("spruce_grove.messaging.emit_warning") as mock_warn,
            patch("spruce_grove.messaging.emit_system_message"),
            patch("spruce_grove.messaging.emit_info") as mock_info,
        ):
            assert self._run() is True
            agent.clear_message_history.assert_called_once()
            clipboard.clear_pending.assert_called_once()
            mock_warn.assert_called_once()
            # Info called once for the session-rotated message; no clipboard msg
            assert mock_info.call_count == 1

    def test_clear_reports_dropped_clipboard_images(self):
        agent = MagicMock()
        clipboard = MagicMock()
        clipboard.get_pending_count.return_value = 3
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.command_line.clipboard.get_clipboard_manager",
                return_value=clipboard,
            ),
            patch(
                "spruce_grove.config.finalize_autosave_session",
                return_value="sid",
            ),
            patch("spruce_grove.messaging.emit_warning"),
            patch("spruce_grove.messaging.emit_system_message"),
            patch("spruce_grove.messaging.emit_info") as mock_info,
        ):
            assert self._run() is True
            # One info for session rotation, one for the dropped clipboard count
            assert mock_info.call_count == 2
            assert any("3" in str(c) for c in mock_info.call_args_list)

    def test_clear_is_registered_and_appears_in_help(self):
        """Regression: /clear must show up in /help (was previously hidden)."""
        # Trigger registration via import side-effects
        import spruce_grove.command_line.session_commands  # noqa: F401
        from spruce_grove.command_line.command_registry import get_unique_commands

        names = {c.name for c in get_unique_commands()}
        assert "clear" in names

    def test_clear_resets_model_fallback_warnings(self):
        """A fresh conversation should re-arm any silenced pinned-model
        fallback warning rather than leaving it suppressed forever."""
        agent = MagicMock()
        clipboard = MagicMock()
        clipboard.get_pending_count.return_value = 0
        with (
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            ),
            patch(
                "spruce_grove.command_line.clipboard.get_clipboard_manager",
                return_value=clipboard,
            ),
            patch(
                "spruce_grove.config.finalize_autosave_session",
                return_value="sid",
            ),
            patch("spruce_grove.messaging.emit_warning"),
            patch("spruce_grove.messaging.emit_system_message"),
            patch("spruce_grove.messaging.emit_info"),
            patch(
                "spruce_grove.agents._builder.reset_model_fallback_warnings"
            ) as mock_reset,
        ):
            assert self._run() is True
            mock_reset.assert_called_once_with()

    def test_clear_description_documents_the_bare_word_shortcut(self):
        """The overlay renders the registry description verbatim, so the
        bare-word `clear` shortcut has to be mentioned there or it's
        undiscoverable."""
        import spruce_grove.command_line.session_commands  # noqa: F401
        from spruce_grove.command_line.command_registry import get_command

        cmd = get_command("clear")
        assert cmd is not None
        assert "clear" in cmd.description.lower()
        assert "bare word" in cmd.description.lower()
