"""Regression tests: ``-r NAME`` re-renders recent history on interactive resume.

The ``-r``/``--resume`` startup path used to load the saved session into the
agent's context but never paint it, leaving a blank screen after e.g. a
reboot-driven relaunch (tmux-resurrect). Every *other* resume path (``/load``,
``/load_context``, and the interactive autosave picker) calls
``display_resumed_history``; ``-r`` now does too -- but only in interactive
mode (a real TTY and not headless ``-p``) so scripted/piped runs stay quiet.

These tests drive ``cli_runner.main()`` with a fully mocked resume so we assert
purely on whether ``display_resumed_history`` is invoked.
"""

import os
import pathlib
from contextlib import ExitStack
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _mock_renderer():
    r = MagicMock()
    r.console = MagicMock()
    r.console.file = MagicMock()
    r.console.file.flush = MagicMock()
    r.start = MagicMock()
    r.stop = MagicMock()
    return r


def _base_main_patches():
    """Common patches so main() can run without touching the real system."""
    return {
        "spruce_grove.cli_runner.find_available_port": MagicMock(return_value=8090),
        "spruce_grove.cli_runner.ensure_config_exists": MagicMock(),
        "spruce_grove.cli_runner.validate_cancel_agent_key": MagicMock(),
        "spruce_grove.cli_runner.initialize_command_history_file": MagicMock(),
        "spruce_grove.cli_runner.default_version_mismatch_behavior": MagicMock(),
        "spruce_grove.cli_runner.print_truecolor_warning": MagicMock(),
        "spruce_grove.cli_runner.reset_unix_terminal": MagicMock(),
        "spruce_grove.cli_runner.reset_windows_terminal_ansi": MagicMock(),
        "spruce_grove.cli_runner.reset_windows_terminal_full": MagicMock(),
        "spruce_grove.cli_runner.callbacks": MagicMock(
            on_startup=AsyncMock(),
            on_shutdown=AsyncMock(),
            on_version_check=AsyncMock(),
            get_callbacks=MagicMock(return_value=[]),
        ),
        "spruce_grove.cli_runner.plugins": MagicMock(),
        "spruce_grove.config.load_api_keys_to_environment": MagicMock(),
    }


def _resume_patches(mock_display, agent):
    """Patches that make the -r resume block resolve + load a fake session."""
    return {
        "spruce_grove.session_lifecycle.resolve_or_create_resume_target": MagicMock(
            return_value=("my-session", pathlib.Path("/tmp/autosaves"), False)
        ),
        "spruce_grove.session_storage.load_session": MagicMock(
            return_value=[MagicMock(), MagicMock()]
        ),
        "spruce_grove.config.pin_current_session_name": MagicMock(),
        "spruce_grove.agents.agent_manager.get_current_agent": MagicMock(
            return_value=agent
        ),
        "spruce_grove.command_line.autosave_menu.display_resumed_history": mock_display,
    }


async def _run_main(argv, extra_patches):
    patches = _base_main_patches()
    patches.update(extra_patches)
    with ExitStack() as stack:
        stack.enter_context(patch.dict(os.environ, {"NO_VERSION_UPDATE": "1"}))
        stack.enter_context(patch("sys.argv", argv))
        stack.enter_context(
            patch(
                "spruce_grove.messaging.SynchronousInteractiveRenderer",
                return_value=_mock_renderer(),
            )
        )
        stack.enter_context(
            patch(
                "spruce_grove.messaging.RichConsoleRenderer",
                return_value=_mock_renderer(),
            )
        )
        stack.enter_context(
            patch("spruce_grove.messaging.get_global_queue", return_value=MagicMock())
        )
        stack.enter_context(
            patch("spruce_grove.messaging.get_message_bus", return_value=MagicMock())
        )
        for target, value in patches.items():
            stack.enter_context(patch(target, value))
        from spruce_grove.cli_runner import main

        await main()


@pytest.mark.anyio
async def test_resume_interactive_renders_history():
    """-r NAME on an interactive TTY re-renders the recent conversation."""
    mock_inter = AsyncMock()
    mock_display = MagicMock()
    agent = MagicMock()
    agent.estimate_tokens_for_message.return_value = 1
    mock_stdout = MagicMock()
    mock_stdout.isatty.return_value = True

    extra = {
        "spruce_grove.cli_runner.interactive_mode": mock_inter,
        "spruce_grove.banner_art.art_for_label": MagicMock(return_value="LOGO\n\n"),
        "sys.stdout": mock_stdout,
    }
    extra.update(_resume_patches(mock_display, agent))

    await _run_main(["spruce-grove", "-r", "my-session"], extra)

    mock_display.assert_called_once()


@pytest.mark.anyio
async def test_resume_headless_skips_history():
    """-r NAME with -p (headless) must NOT dump history to stdout."""
    mock_exec = AsyncMock()
    mock_display = MagicMock()
    agent = MagicMock()
    agent.estimate_tokens_for_message.return_value = 1
    mock_stdout = MagicMock()
    mock_stdout.isatty.return_value = True  # even on a TTY, -p suppresses it

    extra = {
        "spruce_grove.cli_runner.execute_single_prompt": mock_exec,
        "sys.stdout": mock_stdout,
    }
    extra.update(_resume_patches(mock_display, agent))

    await _run_main(["spruce-grove", "-r", "my-session", "-p", "hi"], extra)

    mock_display.assert_not_called()
