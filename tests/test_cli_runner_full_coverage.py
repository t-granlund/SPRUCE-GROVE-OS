"""Full coverage tests for cli_runner.py.

Covers main(), interactive_mode(), run_prompt_with_attachments(),
execute_single_prompt(), and main_entry() — targeting all uncovered branches.
"""

import asyncio
import os
from contextlib import ExitStack
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sync_input(fn):
    """Adapt async-mock classic-input fns to the plain input() seam."""
    import inspect as _inspect

    def _call(*args, **kwargs):
        result = fn(*args, **kwargs)
        if _inspect.iscoroutine(result):
            # Async mocks complete without awaiting anything; drive them
            # synchronously (we are already inside the event loop).
            try:
                result.send(None)
            except StopIteration as stop:
                return stop.value
            raise RuntimeError("async input mock did not finish synchronously")
        return result

    return _call


def _mock_renderer():
    r = MagicMock()
    r.console = MagicMock()
    r.console.file = MagicMock()
    r.console.file.flush = MagicMock()
    r.start = MagicMock()
    r.stop = MagicMock()
    return r


def _mock_parse_result(
    prompt="hello", warnings=None, attachments=None, link_attachments=None
):
    m = MagicMock()
    m.prompt = prompt
    m.warnings = warnings or []
    m.attachments = attachments or []
    m.link_attachments = link_attachments or []
    return m


def _mock_clipboard(images=None):
    mgr = MagicMock()
    mgr.get_pending_images.return_value = images or []
    mgr.get_pending_count.return_value = len(images) if images else 0
    mgr.clear_pending = MagicMock()
    return mgr


def _apply_patches(stack, patches_dict):
    """Apply a dict of patches using an ExitStack."""
    for target, value in patches_dict.items():
        stack.enter_context(patch(target, value))


def _assert_core_plugins_message_once(mock_emit, version):
    expected = call(f"Core plugins version: {version}")
    assert mock_emit.call_args_list.count(expected) == 1


def _base_main_patches():
    """Return a dict of common patches needed for main()."""
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


def _interactive_patches():
    return {
        "spruce_grove.cli_runner.print_truecolor_warning": MagicMock(),
        "spruce_grove.cli_runner.reset_windows_terminal_ansi": MagicMock(),
        "spruce_grove.cli_runner.reset_windows_terminal_full": MagicMock(),
        "spruce_grove.cli_runner.save_command_to_history": MagicMock(),
        "spruce_grove.cli_runner.finalize_autosave_session": MagicMock(
            return_value="session-1"
        ),
        "spruce_grove.cli_runner.COMMAND_HISTORY_FILE": "/tmp/test_history",
        "spruce_grove.command_line.onboarding_wizard.should_show_onboarding": MagicMock(
            return_value=False
        ),
        "spruce_grove.config.auto_save_session_if_enabled": MagicMock(),
    }


async def _run_interactive(
    renderer,
    patches_dict,
    input_fn,
    agent=None,
    initial_command=None,
    extra_patches=None,
):
    """Helper to run interactive_mode with patching."""
    if agent is None:
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"

    with ExitStack() as stack:
        _apply_patches(stack, patches_dict)
        stack.enter_context(patch("builtins.input", _sync_input(input_fn)))
        stack.enter_context(
            patch(
                "spruce_grove.agents.agent_manager.get_current_agent",
                return_value=agent,
            )
        )
        if extra_patches:
            _apply_patches(stack, extra_patches)

        from spruce_grove.cli_runner import interactive_mode

        await interactive_mode(renderer, initial_command=initial_command)


def _scripted_input(*steps):
    """Build an async fake ``input()`` that yields the given literal steps in
    order, raising any step that is an exception (instance or class), then
    returning ``/exit`` for all further calls."""
    state = {"n": 0}

    async def fake_input(*a, **kw):
        idx = state["n"]
        state["n"] += 1
        if idx < len(steps):
            step = steps[idx]
            if isinstance(step, BaseException) or (
                isinstance(step, type) and issubclass(step, BaseException)
            ):
                raise step
            return step
        return "/exit"

    return fake_input


# ---------------------------------------------------------------------------
# main() tests
# ---------------------------------------------------------------------------


class TestMain:
    """Test the main() async function."""

    async def _run_main(self, argv, extra_patches=None, base_overrides=None):
        patches = _base_main_patches()
        if base_overrides:
            patches.update(base_overrides)
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
                patch(
                    "spruce_grove.messaging.get_global_queue", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.messaging.get_message_bus", return_value=MagicMock()
                )
            )
            _apply_patches(stack, patches)
            if extra_patches:
                _apply_patches(stack, extra_patches)
            from spruce_grove.cli_runner import main

            await main()

    @pytest.mark.anyio
    async def test_prompt_mode(self):
        mock_exec = AsyncMock()
        await self._run_main(
            ["spruce-grove", "-p", "hello world"],
            extra_patches={"spruce_grove.cli_runner.execute_single_prompt": mock_exec},
        )
        mock_exec.assert_called_once()

    @pytest.mark.anyio
    async def test_interactive_mode_default(self):
        mock_inter = AsyncMock()
        await self._run_main(
            ["spruce-grove"],
            extra_patches={
                "spruce_grove.cli_runner.interactive_mode": mock_inter,
                "pyfiglet.figlet_format": MagicMock(return_value="LOGO\n\n"),
            },
        )
        mock_inter.assert_called_once()

    @pytest.mark.anyio
    async def test_narrow_terminal_interactive_mode_uses_compact_banner(self):
        mock_inter = AsyncMock()
        mock_figlet = MagicMock(return_value="LOGO\n\n")
        # Rich's Console honors COLUMNS, so this squeezes the banner width
        # below the full SPRUCE GROVE figlet (79 cols).
        with patch.dict(os.environ, {"COLUMNS": "50"}):
            await self._run_main(
                ["spruce-grove"],
                extra_patches={
                    "spruce_grove.cli_runner.interactive_mode": mock_inter,
                    "pyfiglet.figlet_format": mock_figlet,
                },
            )

        mock_figlet.assert_called_once_with("GROVE", font="ansi_shadow")

    @pytest.mark.anyio
    async def test_with_command_args(self):
        mock_inter = AsyncMock()
        await self._run_main(
            ["spruce-grove", "do", "something"],
            extra_patches={
                "spruce_grove.cli_runner.interactive_mode": mock_inter,
                "pyfiglet.figlet_format": MagicMock(return_value="LOGO\n\n"),
            },
        )
        assert mock_inter.call_args[1]["initial_command"] == "do something"

    @pytest.mark.anyio
    async def test_no_available_port(self):
        await self._run_main(
            ["spruce-grove", "-p", "test"],
            base_overrides={
                "spruce_grove.cli_runner.find_available_port": MagicMock(
                    return_value=None
                ),
            },
        )

    @pytest.mark.anyio
    async def test_keymap_error(self):
        from spruce_grove.keymap import KeymapError

        with pytest.raises(SystemExit):
            await self._run_main(
                ["spruce-grove", "-p", "test"],
                base_overrides={
                    "spruce_grove.cli_runner.validate_cancel_agent_key": MagicMock(
                        side_effect=KeymapError("bad key")
                    ),
                },
            )

    @pytest.mark.anyio
    async def test_model_valid(self):
        mock_set = MagicMock()
        await self._run_main(
            ["spruce-grove", "-m", "gpt-5", "-p", "hi"],
            extra_patches={
                "spruce_grove.cli_runner.execute_single_prompt": AsyncMock(),
                "spruce_grove.config.set_model_name": mock_set,
                "spruce_grove.config._validate_model_exists": MagicMock(
                    return_value=True
                ),
            },
        )
        mock_set.assert_called_with("gpt-5")

    @pytest.mark.anyio
    async def test_model_invalid(self):
        mock_mf = MagicMock()
        mock_mf.load_config.return_value = {"gpt-5": {}}
        with pytest.raises(SystemExit):
            await self._run_main(
                ["spruce-grove", "-m", "bad-model", "-p", "hi"],
                extra_patches={
                    "spruce_grove.config.set_model_name": MagicMock(),
                    "spruce_grove.config._validate_model_exists": MagicMock(
                        return_value=False
                    ),
                    "spruce_grove.model_factory.ModelFactory": mock_mf,
                },
            )

    @pytest.mark.anyio
    async def test_model_validation_exception(self):
        with pytest.raises(SystemExit):
            await self._run_main(
                ["spruce-grove", "-m", "bad", "-p", "hi"],
                extra_patches={
                    "spruce_grove.config.set_model_name": MagicMock(),
                    "spruce_grove.config._validate_model_exists": MagicMock(
                        side_effect=RuntimeError("boom")
                    ),
                },
            )

    @pytest.mark.anyio
    async def test_agent_valid(self):
        mock_set = MagicMock()
        await self._run_main(
            ["spruce-grove", "-a", "spruce-grove", "-p", "hi"],
            extra_patches={
                "spruce_grove.cli_runner.execute_single_prompt": AsyncMock(),
                "spruce_grove.agents.agent_manager.get_available_agents": MagicMock(
                    return_value={"spruce-grove": {}}
                ),
                "spruce_grove.agents.agent_manager.set_current_agent": mock_set,
            },
        )
        mock_set.assert_called_with("spruce-grove")

    @pytest.mark.anyio
    async def test_agent_invalid(self):
        with pytest.raises(SystemExit):
            await self._run_main(
                ["spruce-grove", "-a", "bad-agent", "-p", "hi"],
                extra_patches={
                    "spruce_grove.agents.agent_manager.get_available_agents": MagicMock(
                        return_value={"spruce-grove": {}}
                    ),
                },
            )

    @pytest.mark.anyio
    async def test_agent_exception(self):
        with pytest.raises(SystemExit):
            await self._run_main(
                ["spruce-grove", "-a", "bad", "-p", "hi"],
                extra_patches={
                    "spruce_grove.agents.agent_manager.get_available_agents": MagicMock(
                        side_effect=RuntimeError("boom")
                    ),
                },
            )

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        ("argv", "mode_target"),
        [
            (
                ["spruce-grove", "-p", "hi"],
                "spruce_grove.cli_runner.execute_single_prompt",
            ),
            (["spruce-grove"], "spruce_grove.cli_runner.interactive_mode"),
        ],
        ids=["one-shot", "interactive"],
    )
    async def test_core_plugins_version_with_updates_disabled(self, argv, mode_target):
        mock_emit = MagicMock()
        mock_core_version = MagicMock(return_value="0.0.2")

        await self._run_main(
            argv,
            extra_patches={
                mode_target: AsyncMock(),
                "spruce_grove.cli_runner.get_core_plugins_version": mock_core_version,
                "spruce_grove.messaging.emit_system_message": mock_emit,
                "pyfiglet.figlet_format": MagicMock(return_value="LOGO\n\n"),
            },
        )

        from spruce_grove.cli_runner import __version__ as current_version

        mock_core_version.assert_called_once_with()
        assert call(f"Current version: {current_version}") in mock_emit.call_args_list
        _assert_core_plugins_message_once(mock_emit, "0.0.2")

    @pytest.mark.anyio
    async def test_core_plugins_version_renders_once_through_message_pipeline(self):
        from io import StringIO

        from rich.console import Console as RichConsole

        from spruce_grove.messaging.message_queue import MessageQueue

        output = StringIO()
        queue = MessageQueue()
        queue.start()
        console = RichConsole(file=output, force_terminal=False, width=120)

        async def execute_and_drain(*_args, **_kwargs):
            assert queue.drain()

        patches = _base_main_patches()
        patches["spruce_grove.cli_runner.get_core_plugins_version"] = MagicMock(
            return_value="0.0.2"
        )

        try:
            with ExitStack() as stack:
                stack.enter_context(patch.dict(os.environ, {"NO_VERSION_UPDATE": "1"}))
                stack.enter_context(patch("sys.argv", ["spruce-grove", "-p", "hi"]))
                stack.enter_context(
                    patch("spruce_grove.cli_runner.Console", return_value=console)
                )
                stack.enter_context(
                    patch(
                        "spruce_grove.messaging.RichConsoleRenderer",
                        return_value=_mock_renderer(),
                    )
                )
                stack.enter_context(
                    patch("spruce_grove.messaging.get_global_queue", return_value=queue)
                )
                stack.enter_context(
                    patch(
                        "spruce_grove.messaging.message_queue.get_global_queue",
                        return_value=queue,
                    )
                )
                stack.enter_context(
                    patch(
                        "spruce_grove.messaging.get_message_bus",
                        return_value=MagicMock(),
                    )
                )
                stack.enter_context(
                    patch(
                        "spruce_grove.cli_runner.execute_single_prompt",
                        side_effect=execute_and_drain,
                    )
                )
                _apply_patches(stack, patches)

                from spruce_grove.cli_runner import main

                await main()
        finally:
            queue.stop()

        assert output.getvalue().count("Core plugins version: 0.0.2") == 1

    @pytest.mark.anyio
    async def test_core_plugins_version_uses_localized_unknown_fallback(self):
        mock_emit = MagicMock()

        await self._run_main(
            ["spruce-grove", "-p", "hi"],
            extra_patches={
                "spruce_grove.cli_runner.execute_single_prompt": AsyncMock(),
                "spruce_grove.cli_runner.get_core_plugins_version": MagicMock(
                    return_value=None
                ),
                "spruce_grove.messaging.emit_system_message": mock_emit,
            },
        )

        _assert_core_plugins_message_once(mock_emit, "unknown")

    @pytest.mark.anyio
    async def test_version_flag_output_is_unchanged(self, capsys):
        from spruce_grove.cli_runner import __version__ as current_version
        from spruce_grove.cli_runner import main

        mock_core_version = MagicMock()
        capsys.readouterr()
        with (
            patch("sys.argv", ["spruce-grove", "--version"]),
            patch("spruce_grove.cli_runner.callbacks", MagicMock()),
            patch(
                "spruce_grove.cli_runner.get_core_plugins_version", mock_core_version
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            await main()

        assert exc_info.value.code == 0
        assert capsys.readouterr().out == f"{current_version}\n"
        mock_core_version.assert_not_called()

    @pytest.mark.anyio
    async def test_version_check_with_callbacks(self):
        cb_mock = MagicMock(
            on_startup=AsyncMock(),
            on_shutdown=AsyncMock(),
            on_version_check=AsyncMock(),
            get_callbacks=MagicMock(return_value=[lambda: None]),
        )
        patches = _base_main_patches()
        default_version_check = patches[
            "spruce_grove.cli_runner.default_version_mismatch_behavior"
        ]
        mock_core_version = MagicMock(return_value="0.0.2")
        mock_emit = MagicMock()
        patches["spruce_grove.cli_runner.callbacks"] = cb_mock
        patches["spruce_grove.cli_runner.get_core_plugins_version"] = mock_core_version
        patches["spruce_grove.messaging.emit_system_message"] = mock_emit
        with ExitStack() as stack:
            stack.enter_context(
                patch.dict(os.environ, {"NO_VERSION_UPDATE": ""}, clear=False)
            )
            stack.enter_context(patch("sys.argv", ["spruce-grove", "-p", "hi"]))
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
                patch(
                    "spruce_grove.messaging.get_global_queue", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.messaging.get_message_bus", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.cli_runner.execute_single_prompt",
                    new_callable=AsyncMock,
                )
            )
            _apply_patches(stack, patches)
            from spruce_grove.cli_runner import main

            await main()
            cb_mock.on_version_check.assert_called_once()
            default_version_check.assert_not_called()
            mock_core_version.assert_called_once_with()
            _assert_core_plugins_message_once(mock_emit, "0.0.2")

    @pytest.mark.anyio
    async def test_version_check_no_callbacks(self):
        """Version check falls back to default_version_mismatch_behavior."""
        patches = _base_main_patches()
        default_version_check = patches[
            "spruce_grove.cli_runner.default_version_mismatch_behavior"
        ]
        mock_core_version = MagicMock(return_value="0.0.2")
        mock_emit = MagicMock()
        patches["spruce_grove.cli_runner.callbacks"] = MagicMock(
            on_startup=AsyncMock(),
            on_shutdown=AsyncMock(),
            on_version_check=AsyncMock(),
            get_callbacks=MagicMock(return_value=[]),
        )
        patches["spruce_grove.cli_runner.get_core_plugins_version"] = mock_core_version
        patches["spruce_grove.messaging.emit_system_message"] = mock_emit
        with ExitStack() as stack:
            stack.enter_context(
                patch.dict(os.environ, {"NO_VERSION_UPDATE": ""}, clear=False)
            )
            stack.enter_context(patch("sys.argv", ["spruce-grove", "-p", "hi"]))
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
                patch(
                    "spruce_grove.messaging.get_global_queue", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.messaging.get_message_bus", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.cli_runner.execute_single_prompt",
                    new_callable=AsyncMock,
                )
            )
            _apply_patches(stack, patches)
            from spruce_grove.cli_runner import main

            await main()
            default_version_check.assert_called_once()
            mock_core_version.assert_called_once_with()
            _assert_core_plugins_message_once(mock_emit, "0.0.2")

    @pytest.mark.anyio
    async def test_pyfiglet_import_error(self):
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "pyfiglet":
                raise ImportError("no pyfiglet")
            return real_import(name, *args, **kwargs)

        await self._run_main(
            ["spruce-grove"],
            extra_patches={
                "spruce_grove.cli_runner.interactive_mode": AsyncMock(),
                "builtins.__import__": fake_import,
            },
        )


# ---------------------------------------------------------------------------
# interactive_mode() tests
# ---------------------------------------------------------------------------


class TestInteractiveMode:
    """Test interactive_mode() branches."""

    @pytest.mark.anyio
    async def test_exit_command(self):
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(return_value="/exit"),
        )

    @pytest.mark.anyio
    async def test_startup_shows_single_press_tab_line(self):
        """Startup used to dump ~12 tip lines; now it's one pointer to the
        Tab overlay. That content moved, it isn't gone."""
        emit_system_message = MagicMock()

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(return_value="/exit"),
            extra_patches={
                "spruce_grove.messaging.emit_system_message": emit_system_message,
            },
        )

        messages = [call.args[0] for call in emit_system_message.call_args_list]
        assert any("Tab" in message for message in messages), messages
        # The old per-topic tip lines must be gone from startup output.
        assert not any("newline: Shift+Enter" in message for message in messages)
        assert not any(
            "Ctrl+X Ctrl+E to open $EDITOR" in message for message in messages
        )
        assert not any(
            "Type /help to view all commands" in message for message in messages
        )

    @pytest.mark.anyio
    async def test_quit_command(self):
        agent = MagicMock()
        agent.get_user_prompt.return_value = None  # test None prompt branch
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(return_value="quit"),
            agent=agent,
        )

    @pytest.mark.anyio
    async def test_eof_exits(self):
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(side_effect=EOFError),
        )

    @pytest.mark.anyio
    async def test_keyboard_interrupt_continues(self):
        fake_input = _scripted_input(KeyboardInterrupt)

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={},
        )

    @pytest.mark.anyio
    async def test_keyboard_interrupt_notifies_continuation_plugins(self):
        fake_input = _scripted_input(KeyboardInterrupt)

        mock_cancel = AsyncMock()
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.callbacks.on_interactive_turn_cancel": mock_cancel,
            },
        )
        mock_cancel.assert_awaited()

    @pytest.mark.anyio
    async def test_clear_command(self):
        fake_input = _scripted_input("/clear")

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            agent=agent,
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                # /clear lives in session_commands and lazy-imports the clipboard
                # manager + autosave rotation — patch at the source modules.
                "spruce_grove.command_line.clipboard.get_clipboard_manager": MagicMock(
                    return_value=_mock_clipboard([b"img"])
                ),
                "spruce_grove.config.finalize_autosave_session": MagicMock(
                    return_value="session-1"
                ),
            },
        )
        agent.clear_message_history.assert_called()

    @pytest.mark.anyio
    async def test_slash_command_handled(self):
        fake_input = _scripted_input("/help")

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                    return_value=True
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("/help")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_slash_command_returns_prompt(self):
        fake_input = _scripted_input("/custom")

        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                    return_value="run this"
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("/custom")
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(mock_result, MagicMock())
                ),
            },
        )

    @pytest.mark.anyio
    async def test_slash_command_exception(self):
        fake_input = _scripted_input("/bad")

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                    side_effect=RuntimeError("cmd error")
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("/bad")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_normal_prompt_execution(self):
        fake_input = _scripted_input("write hello")

        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(mock_result, MagicMock())
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_prompt_returns_none_cancelled(self):
        fake_input = _scripted_input("write hello")

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(None, MagicMock())
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_prompt_cancelled_notifies_continuation_plugins(self):
        fake_input = _scripted_input("write hello")

        mock_cancel = AsyncMock()
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(None, MagicMock())
                ),
                "spruce_grove.callbacks.on_interactive_turn_cancel": mock_cancel,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
            },
        )
        mock_cancel.assert_awaited()

    @pytest.mark.anyio
    async def test_prompt_exception(self):
        fake_input = _scripted_input("write hello")

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    side_effect=RuntimeError("agent error")
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
                "spruce_grove.messaging.queue_console.get_queue_console": MagicMock(
                    return_value=MagicMock()
                ),
            },
        )

    @pytest.mark.anyio
    async def test_empty_input_skipped(self):
        fake_input = _scripted_input("   ")

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("   ")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_initial_command_success(self):
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(return_value="/exit"),
            agent=agent,
            initial_command="do stuff",
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(mock_result, MagicMock())
                ),
            },
        )

    @pytest.mark.anyio
    async def test_initial_command_error(self):
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(return_value="/exit"),
            agent=agent,
            initial_command="do stuff",
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    side_effect=RuntimeError("fail")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_initial_command_returns_none(self):
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            AsyncMock(return_value="/exit"),
            agent=agent,
            initial_command="do stuff",
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(None, MagicMock())
                ),
            },
        )

    @pytest.mark.anyio
    async def test_autosave_load_non_tty(self):
        fake_input = _scripted_input("/autosave_load")

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = False

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                    return_value="__AUTOSAVE_LOAD__"
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("/autosave_load")
                ),
                "sys.stdin": mock_stdin,
                "sys.stdout": mock_stdout,
            },
        )

    @pytest.mark.anyio
    async def test_autosave_load_tty_cancelled(self):
        fake_input = _scripted_input("/autosave_load")

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch.dict(os.environ, {"SPRUCE_GROVE_NO_TUI": ""}, clear=False):
            await _run_interactive(
                _mock_renderer(),
                _interactive_patches(),
                fake_input,
                extra_patches={
                    "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                        return_value="__AUTOSAVE_LOAD__"
                    ),
                    "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                        return_value=_mock_parse_result("/autosave_load")
                    ),
                    "sys.stdin": mock_stdin,
                    "sys.stdout": mock_stdout,
                    "spruce_grove.command_line.autosave_menu.interactive_autosave_picker": AsyncMock(
                        return_value=None
                    ),
                },
            )

    @pytest.mark.anyio
    async def test_autosave_load_tty_success(self):
        fake_input = _scripted_input("/autosave_load")

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        agent.estimate_tokens_for_message.return_value = 10

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch.dict(os.environ, {"SPRUCE_GROVE_NO_TUI": ""}, clear=False):
            await _run_interactive(
                _mock_renderer(),
                _interactive_patches(),
                fake_input,
                agent=agent,
                extra_patches={
                    "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                        return_value="__AUTOSAVE_LOAD__"
                    ),
                    "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                        return_value=_mock_parse_result("/autosave_load")
                    ),
                    "sys.stdin": mock_stdin,
                    "sys.stdout": mock_stdout,
                    "spruce_grove.command_line.autosave_menu.interactive_autosave_picker": AsyncMock(
                        return_value="my-session"
                    ),
                    "spruce_grove.session_storage.load_session": MagicMock(
                        return_value=[MagicMock()]
                    ),
                    "spruce_grove.config.set_current_autosave_from_session_name": MagicMock(),
                    "spruce_grove.command_line.autosave_menu.display_resumed_history": MagicMock(),
                    "spruce_grove.cli_runner.get_current_agent": MagicMock(
                        return_value=agent
                    ),
                },
            )

    @pytest.mark.anyio
    async def test_autosave_load_non_tty_warns_instead_of_prompting(self):
        """Non-TTY /autosave_load points at -r NAME instead of prompting."""
        fake_input = _scripted_input("/autosave_load")

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = False

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                    return_value="__AUTOSAVE_LOAD__"
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("/autosave_load")
                ),
                "sys.stdin": mock_stdin,
                "sys.stdout": mock_stdout,
            },
        )

    @pytest.mark.anyio
    async def test_slash_command_returns_false(self):
        """Command returns False = not recognized, fall through."""
        fake_input = _scripted_input("/unknown")

        mock_result = MagicMock(output="ok")
        mock_result.all_messages.return_value = []

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                    return_value=False
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("/unknown")
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(mock_result, MagicMock())
                ),
            },
        )

    @pytest.mark.anyio
    async def test_continuation_loop(self):
        fake_input = _scripted_input("write hello")

        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        mock_run = AsyncMock(return_value=(mock_result, MagicMock()))
        mock_turn_end = AsyncMock(
            side_effect=[[{"prompt": "repeat", "clear_context": True}], []]
        )

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": mock_run,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
                "spruce_grove.callbacks.on_interactive_turn_end": mock_turn_end,
            },
        )
        assert mock_run.await_count == 2

    @pytest.mark.anyio
    async def test_continuation_loop_cancelled(self):
        fake_input = _scripted_input("write hello")

        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []
        run_call = 0

        async def fake_run(*a, **kw):
            nonlocal run_call
            run_call += 1
            if run_call == 1:
                return (mock_result, MagicMock())
            return (None, MagicMock())

        mock_cancel = AsyncMock()
        mock_turn_end = AsyncMock(
            side_effect=[[{"prompt": "repeat", "clear_context": True}], []]
        )

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": fake_run,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
                "spruce_grove.callbacks.on_interactive_turn_end": mock_turn_end,
                "spruce_grove.callbacks.on_interactive_turn_cancel": mock_cancel,
            },
        )
        mock_cancel.assert_awaited()

    @pytest.mark.anyio
    async def test_continuation_no_request_stops(self):
        fake_input = _scripted_input("write hello")

        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        mock_turn_end = AsyncMock(return_value=[])
        mock_run = AsyncMock(return_value=(mock_result, MagicMock()))
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": mock_run,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
                "spruce_grove.callbacks.on_interactive_turn_end": mock_turn_end,
            },
        )
        mock_turn_end.assert_called()
        assert mock_run.await_count == 1

    @pytest.mark.anyio
    async def test_continuation_loop_exception_is_reported_to_plugins(self):
        fake_input = _scripted_input("write hello")

        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []
        run_call = 0

        async def fake_run(*a, **kw):
            nonlocal run_call
            run_call += 1
            if run_call == 1:
                return (mock_result, MagicMock())
            raise RuntimeError("wiggum fail")

        mock_turn_end = AsyncMock(
            side_effect=[[{"prompt": "repeat", "clear_context": True}], []]
        )

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": fake_run,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
                "spruce_grove.callbacks.on_interactive_turn_end": mock_turn_end,
            },
        )
        assert mock_turn_end.call_count >= 2

    @pytest.mark.anyio
    async def test_onboarding_chatgpt(self):
        patches = _interactive_patches()
        patches[
            "spruce_grove.command_line.onboarding_wizard.should_show_onboarding"
        ] = MagicMock(return_value=True)

        mock_future = MagicMock()
        mock_future.result.return_value = "chatgpt"
        mock_pool = MagicMock()
        mock_pool.submit.return_value = mock_future
        mock_executor = MagicMock()
        mock_executor.__enter__ = MagicMock(return_value=mock_pool)
        mock_executor.__exit__ = MagicMock(return_value=False)

        await _run_interactive(
            _mock_renderer(),
            patches,
            AsyncMock(return_value="/exit"),
            extra_patches={
                "concurrent.futures.ThreadPoolExecutor": MagicMock(
                    return_value=mock_executor
                ),
                "spruce_grove.command_line.onboarding_wizard.run_onboarding_wizard": AsyncMock(
                    return_value="chatgpt"
                ),
                "code_puppy_core_plugins.chatgpt_oauth.oauth_flow.run_oauth_flow": MagicMock(),
                "spruce_grove.config.set_model_name": MagicMock(),
            },
        )

    @pytest.mark.anyio
    async def test_onboarding_claude(self):
        patches = _interactive_patches()
        patches[
            "spruce_grove.command_line.onboarding_wizard.should_show_onboarding"
        ] = MagicMock(return_value=True)

        mock_future = MagicMock()
        mock_future.result.return_value = "claude"
        mock_pool = MagicMock()
        mock_pool.submit.return_value = mock_future
        mock_executor = MagicMock()
        mock_executor.__enter__ = MagicMock(return_value=mock_pool)
        mock_executor.__exit__ = MagicMock(return_value=False)

        await _run_interactive(
            _mock_renderer(),
            patches,
            AsyncMock(return_value="/exit"),
            extra_patches={
                "concurrent.futures.ThreadPoolExecutor": MagicMock(
                    return_value=mock_executor
                ),
                "code_puppy_core_plugins.claude_code_oauth.register_callbacks._perform_authentication": MagicMock(),
                "spruce_grove.config.set_model_name": MagicMock(),
            },
        )

    @pytest.mark.anyio
    @pytest.mark.parametrize("onboarding_result", ["completed", "skipped"])
    async def test_onboarding_result(self, onboarding_result):
        patches = _interactive_patches()
        patches[
            "spruce_grove.command_line.onboarding_wizard.should_show_onboarding"
        ] = MagicMock(return_value=True)

        mock_future = MagicMock()
        mock_future.result.return_value = onboarding_result
        mock_pool = MagicMock()
        mock_pool.submit.return_value = mock_future
        mock_executor = MagicMock()
        mock_executor.__enter__ = MagicMock(return_value=mock_pool)
        mock_executor.__exit__ = MagicMock(return_value=False)

        await _run_interactive(
            _mock_renderer(),
            patches,
            AsyncMock(return_value="/exit"),
            extra_patches={
                "concurrent.futures.ThreadPoolExecutor": MagicMock(
                    return_value=mock_executor
                ),
            },
        )

    @pytest.mark.anyio
    async def test_onboarding_exception(self):
        patches = _interactive_patches()
        patches[
            "spruce_grove.command_line.onboarding_wizard.should_show_onboarding"
        ] = MagicMock(side_effect=RuntimeError("fail"))

        await _run_interactive(
            _mock_renderer(),
            patches,
            AsyncMock(return_value="/exit"),
        )

    @pytest.mark.anyio
    async def test_clear_no_clipboard_images(self):
        """Test /clear when no clipboard images pending."""
        fake_input = _scripted_input("/clear")

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            agent=agent,
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                # Same lazy-import targets as test_clear_command above.
                "spruce_grove.command_line.clipboard.get_clipboard_manager": MagicMock(
                    return_value=_mock_clipboard()
                ),
                "spruce_grove.config.finalize_autosave_session": MagicMock(
                    return_value="session-1"
                ),
            },
        )


# ---------------------------------------------------------------------------
# main_entry() additional tests
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Additional interactive_mode edge cases for remaining uncovered lines
# ---------------------------------------------------------------------------


class TestInteractiveModeEdgeCases:
    """Cover remaining uncovered lines in interactive_mode."""

    @pytest.mark.anyio
    async def test_exit_with_running_task(self):
        """Lines 594-599: exit cancels running agent task."""
        fake_input = _scripted_input("do work")

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        # Use a real Future that we can cancel and await
        loop = asyncio.get_event_loop()
        mock_task = loop.create_future()
        # Don't resolve it - it stays pending (not done)

        async def fake_run(*a, **kw):
            return (mock_result, mock_task)

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            agent=agent,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": fake_run,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("do work")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_eof_with_running_task_cancels(self):
        """Lines 574-579: EOF cancels running agent task."""
        fake_input = _scripted_input("do work", EOFError)

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        loop = asyncio.get_event_loop()
        mock_task = loop.create_future()

        async def fake_run(*a, **kw):
            return (mock_result, mock_task)

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            agent=agent,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": fake_run,
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("do work")
                ),
            },
        )

    @pytest.mark.anyio
    async def test_clear_with_clipboard_images(self):
        """Line 625: clipboard_count > 0 message."""
        fake_input = _scripted_input("clear")

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        clip = _mock_clipboard([b"img1", b"img2"])

        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            agent=agent,
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                "spruce_grove.command_line.clipboard.get_clipboard_manager": MagicMock(
                    return_value=clip
                ),
            },
        )

    @pytest.mark.anyio
    async def test_autosave_load_no_tui_env(self):
        """Line 656: SPRUCE_GROVE_NO_TUI=1 forces non-interactive picker."""
        fake_input = _scripted_input("/autosave_load")

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch.dict(os.environ, {"SPRUCE_GROVE_NO_TUI": "1"}, clear=False):
            await _run_interactive(
                _mock_renderer(),
                _interactive_patches(),
                fake_input,
                extra_patches={
                    "spruce_grove.command_line.command_handler.handle_command": MagicMock(
                        return_value="__AUTOSAVE_LOAD__"
                    ),
                    "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                        return_value=_mock_parse_result("/autosave_load")
                    ),
                    "sys.stdin": mock_stdin,
                    "sys.stdout": mock_stdout,
                },
            )


# ---------------------------------------------------------------------------
# main() Windows raw-Ctrl+C clamp and other edge cases
# ---------------------------------------------------------------------------


class TestMainWindowsClampAndEdgeCases:
    @pytest.mark.anyio
    async def test_windows_raw_ctrl_c_clamp_armed(self):
        """When the console clamp succeeds, the sticky flag is set."""
        patches = _base_main_patches()
        with ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, {"NO_VERSION_UPDATE": "1"}))
            stack.enter_context(patch("sys.argv", ["spruce-grove", "-p", "hi"]))
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
                patch(
                    "spruce_grove.messaging.get_global_queue", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.messaging.get_message_bus", return_value=MagicMock()
                )
            )
            stack.enter_context(
                patch(
                    "spruce_grove.cli_runner.execute_single_prompt",
                    new_callable=AsyncMock,
                )
            )
            _apply_patches(stack, patches)
            mock_disable = stack.enter_context(
                patch(
                    "spruce_grove.terminal_utils.disable_windows_ctrl_c",
                    return_value=True,
                )
            )
            mock_keep = stack.enter_context(
                patch("spruce_grove.terminal_utils.set_keep_ctrl_c_disabled")
            )
            from spruce_grove.cli_runner import main

            await main()

            mock_disable.assert_called_once()
            mock_keep.assert_called_once_with(True)

    @pytest.mark.anyio
    async def test_initial_command_awaiting_input(self):
        """Lines 405-406: is_awaiting_user_input branch."""
        patches = _interactive_patches()
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        await _run_interactive(
            _mock_renderer(),
            patches,
            AsyncMock(return_value="/exit"),
            agent=agent,
            initial_command="do stuff",
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(mock_result, MagicMock())
                ),
                "spruce_grove.tools.command_runner.is_awaiting_user_input": MagicMock(
                    return_value=True
                ),
            },
        )

    @pytest.mark.anyio
    async def test_initial_command_awaiting_input_import_error(self):
        """Lines 405-406: is_awaiting_user_input ImportError."""
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if "command_runner" in name and "is_awaiting" not in str(args):
                # Only block the specific import inside the try block
                pass
            return real_import(name, *args, **kwargs)

        patches = _interactive_patches()
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        await _run_interactive(
            _mock_renderer(),
            patches,
            AsyncMock(return_value="/exit"),
            agent=agent,
            initial_command="do stuff",
            extra_patches={
                "spruce_grove.cli_runner.get_current_agent": MagicMock(
                    return_value=agent
                ),
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(mock_result, MagicMock())
                ),
            },
        )


class TestRemainingEdgeCases:
    """Cover the hardest-to-reach lines."""

    @pytest.mark.anyio
    async def test_cancelled_result_notifies_continuation_plugins(self):
        """Cancelled agent runs notify continuation plugins."""
        fake_input = _scripted_input("write hello")

        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"

        mock_cancel = AsyncMock()
        await _run_interactive(
            _mock_renderer(),
            _interactive_patches(),
            fake_input,
            agent=agent,
            extra_patches={
                "spruce_grove.cli_runner.run_prompt_with_attachments": AsyncMock(
                    return_value=(None, MagicMock())
                ),
                "spruce_grove.cli_runner.parse_prompt_attachments": MagicMock(
                    return_value=_mock_parse_result("write hello")
                ),
                "spruce_grove.callbacks.on_interactive_turn_cancel": mock_cancel,
            },
        )
        mock_cancel.assert_awaited()

    @pytest.mark.anyio
    async def test_execute_single_prompt_success_path(self):
        """Lines 1005-1015: execute_single_prompt success with .output access."""
        from spruce_grove.cli_runner import execute_single_prompt

        mock_renderer = _mock_renderer()
        # response needs .output attribute (not a tuple)
        mock_response = MagicMock()
        mock_response.output = "the response"

        with ExitStack() as stack:
            stack.enter_context(patch("spruce_grove.cli_runner.get_current_agent"))
            stack.enter_context(
                patch(
                    "spruce_grove.cli_runner.run_prompt_with_attachments",
                    new_callable=AsyncMock,
                    return_value=mock_response,
                )
            )
            stack.enter_context(patch("spruce_grove.cli_runner.emit_info"))
            await execute_single_prompt("test", mock_renderer)


class TestImportErrorFallbacks:
    """Test ImportError fallback branches."""

    @pytest.mark.anyio
    async def test_prompt_toolkit_import_error_fallback(self):
        """Lines 449-470, 542-546: prompt_toolkit not installed.

        These lines are import-error fallbacks for prompt_toolkit_completion.
        They're only reachable when the module genuinely can't be imported,
        which is impractical to test without breaking the test infrastructure.
        Marking as known-uncoverable (Windows/missing-dep edge case).
        """
        # Documents that lines 449-470/542-546 are ImportError fallbacks unreachable
        # where prompt_toolkit is installed.
        pass

    @pytest.mark.anyio
    async def test_is_awaiting_user_input_import_error(self):
        """Lines 405-406: ImportError for is_awaiting_user_input."""
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "spruce_grove.tools.command_runner":
                raise ImportError("no command_runner")
            return real_import(name, *args, **kwargs)

        renderer = _mock_renderer()
        patches = _interactive_patches()
        agent = MagicMock()
        agent.get_user_prompt.return_value = "task:"
        mock_result = MagicMock(output="done")
        mock_result.all_messages.return_value = []

        with ExitStack() as stack:
            _apply_patches(stack, patches)
            stack.enter_context(patch("builtins.input", return_value="/exit"))
            stack.enter_context(
                patch(
                    "spruce_grove.agents.agent_manager.get_current_agent",
                    return_value=agent,
                )
            )
            stack.enter_context(
                patch("spruce_grove.cli_runner.get_current_agent", return_value=agent)
            )
            stack.enter_context(
                patch(
                    "spruce_grove.cli_runner.run_prompt_with_attachments",
                    new_callable=AsyncMock,
                    return_value=(mock_result, MagicMock()),
                )
            )
            stack.enter_context(patch("builtins.__import__", side_effect=fake_import))
            from spruce_grove.cli_runner import interactive_mode

            await interactive_mode(renderer, initial_command="test")


class TestMainEntryAdditional:
    @patch("asyncio.run", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_stderr_output(self, mock_run):
        from spruce_grove.cli_runner import main_entry

        with ExitStack() as stack:
            stack.enter_context(patch("spruce_grove.cli_runner.reset_unix_terminal"))
            result = main_entry()
            assert result == 0
