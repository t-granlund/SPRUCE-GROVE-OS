"""Full coverage tests for spruce_grove/command_line/config_commands.py."""

import json
from unittest.mock import MagicMock, mock_open, patch


class TestGetCommandsHelp:
    def test_lazy_import(self):
        from spruce_grove.command_line.config_commands import get_commands_help

        with patch(
            "spruce_grove.command_line.command_handler.get_commands_help",
            return_value="help text",
        ):
            assert get_commands_help() == "help text"


class TestGetJsonAgentsPinnedToModel:
    def test_returns_pinned(self, tmp_path):
        from spruce_grove.command_line.config_commands import (
            _get_json_agents_pinned_to_model,
        )

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"model": "gpt-5"}))
        with patch(
            "spruce_grove.agents.json_agent.discover_json_agents",
            return_value={"test": str(agent_file)},
        ):
            result = _get_json_agents_pinned_to_model("gpt-5")
            assert "test" in result

    def test_skips_errors(self, tmp_path):
        from spruce_grove.command_line.config_commands import (
            _get_json_agents_pinned_to_model,
        )

        with patch(
            "spruce_grove.agents.json_agent.discover_json_agents",
            return_value={"bad": "/nonexistent/path.json"},
        ):
            result = _get_json_agents_pinned_to_model("gpt-5")
            assert result == []


class TestHandlePinModelCommand:
    def _make_patches(self, **overrides):
        defaults = {
            "discover_json_agents": {},
            "load_model_names": ["gpt-5", "claude"],
            "get_agent_descriptions": {"spruce-grove": "Default agent"},
        }
        defaults.update(overrides)
        return [
            patch(
                "spruce_grove.agents.json_agent.discover_json_agents",
                return_value=defaults["discover_json_agents"],
            ),
            patch(
                "spruce_grove.command_line.model_picker_completion.load_model_names",
                return_value=defaults["load_model_names"],
            ),
            patch(
                "spruce_grove.agents.agent_manager.get_agent_descriptions",
                return_value=defaults["get_agent_descriptions"],
            ),
        ]

    def test_agent_not_found(self):
        from spruce_grove.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("spruce_grove.messaging.emit_error"),
            patch("spruce_grove.messaging.emit_info"),
        ):
            assert handle_pin_model_command("/pin_model unknown gpt-5") is True

    def test_pin_builtin_agent(self):
        from spruce_grove.command_line.config_commands import handle_pin_model_command

        mock_agent = MagicMock()
        mock_agent.name = "spruce-grove"
        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("spruce_grove.config.set_agent_pinned_model"),
            patch("spruce_grove.messaging.emit_success"),
            patch("spruce_grove.messaging.emit_info"),
            patch("spruce_grove.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_pin_model_command("/pin_model spruce-grove gpt-5") is True

    def test_unpin_delegation(self):
        from spruce_grove.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch(
                "spruce_grove.command_line.config_commands.handle_unpin_command",
                return_value=True,
            ) as unpin,
        ):
            assert handle_pin_model_command("/pin_model agent (unpin)") is True
            unpin.assert_called_once()


class TestHandleShowCommand:
    def _show_patches(self, effective_temp=0.7, global_temp=0.7, yolo=True):
        """Return a context manager patching all lazy imports in handle_show_command."""
        mock_agent = MagicMock()
        mock_agent.display_name = "Test Agent"
        return [
            patch("spruce_grove.agents.get_current_agent", return_value=mock_agent),
            patch(
                "spruce_grove.command_line.model_picker_completion.get_active_model",
                return_value="gpt-5",
            ),
            patch("spruce_grove.config.get_grove_name", return_value="Pup"),
            patch("spruce_grove.config.get_owner_name", return_value="Owner"),
            patch("spruce_grove.config.get_yolo_mode", return_value=yolo),
            patch("spruce_grove.config.get_auto_save_session", return_value=True),
            patch("spruce_grove.config.get_protected_token_count", return_value=50000),
            patch("spruce_grove.config.get_compaction_threshold", return_value=0.85),
            patch(
                "spruce_grove.config.get_compaction_strategy", return_value="truncation"
            ),
            patch("spruce_grove.config.get_temperature", return_value=global_temp),
            patch(
                "spruce_grove.config.get_effective_temperature",
                return_value=effective_temp,
            ),
            patch("spruce_grove.config.get_default_agent", return_value="spruce-grove"),
            patch("spruce_grove.config.get_resume_message_count", return_value=50),
            patch(
                "spruce_grove.config.get_effective_model_settings",
                return_value={"reasoning_effort": "medium", "verbosity": "medium"},
            ),
            patch("spruce_grove.config.get_value"),
            patch(
                "spruce_grove.keymap.get_cancel_agent_display_name", return_value="ctrl+c"
            ),
            patch("spruce_grove.messaging.emit_info"),
        ]

    def test_show_command(self):
        from spruce_grove.command_line.config_commands import handle_show_command

        patches = self._show_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patches[3],
            patches[4],
            patches[5],
            patches[6],
            patches[7],
            patches[8],
            patches[9],
            patches[10],
            patches[11],
            patches[12],
            patches[13],
            patches[14],
            patches[15],
            patches[16],
        ):
            assert handle_show_command("/show") is True


class TestHandleUnpinCommand:
    def test_no_args_with_pinned(self):
        from spruce_grove.command_line.config_commands import handle_unpin_command

        agent_file_content = json.dumps({"model": "gpt-5"})
        with (
            patch(
                "spruce_grove.agents.json_agent.discover_json_agents",
                return_value={"j": "/f.json"},
            ),
            patch(
                "spruce_grove.agents.agent_manager.get_agent_descriptions",
                return_value={"a": "desc"},
            ),
            patch("spruce_grove.config.get_agent_pinned_model", return_value="gpt-5"),
            patch("builtins.open", mock_open(read_data=agent_file_content)),
            patch("spruce_grove.messaging.emit_warning"),
            patch("spruce_grove.messaging.emit_info"),
        ):
            assert handle_unpin_command("/unpin") is True

    def test_unpin_builtin(self):
        from spruce_grove.command_line.config_commands import handle_unpin_command

        mock_agent = MagicMock()
        mock_agent.name = "spruce-grove"
        with (
            patch("spruce_grove.agents.json_agent.discover_json_agents", return_value={}),
            patch(
                "spruce_grove.agents.agent_manager.get_agent_descriptions",
                return_value={"spruce-grove": "desc"},
            ),
            patch("spruce_grove.config.clear_agent_pinned_model"),
            patch("spruce_grove.messaging.emit_success"),
            patch("spruce_grove.agents.get_current_agent", return_value=mock_agent),
            patch("spruce_grove.messaging.emit_info"),
        ):
            assert handle_unpin_command("/unpin spruce-grove") is True

    def test_unpin_current_agent_reload_failure(self, tmp_path):
        from spruce_grove.command_line.config_commands import handle_unpin_command

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"name": "test", "model": "gpt-5"}))
        mock_agent = MagicMock()
        mock_agent.name = "test"
        mock_agent.reload_code_generation_agent.side_effect = Exception("boom")
        with (
            patch(
                "spruce_grove.agents.json_agent.discover_json_agents",
                return_value={"test": str(agent_file)},
            ),
            patch(
                "spruce_grove.agents.agent_manager.get_agent_descriptions",
                return_value={},
            ),
            patch("spruce_grove.messaging.emit_success"),
            patch("spruce_grove.messaging.emit_warning"),
            patch("spruce_grove.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_unpin_command("/unpin test") is True

    def test_unpin_exception(self):
        from spruce_grove.command_line.config_commands import handle_unpin_command

        with (
            patch(
                "spruce_grove.agents.json_agent.discover_json_agents",
                return_value={"test": "/bad.json"},
            ),
            patch(
                "spruce_grove.agents.agent_manager.get_agent_descriptions",
                return_value={},
            ),
            patch("spruce_grove.messaging.emit_error"),
        ):
            assert handle_unpin_command("/unpin test") is True
