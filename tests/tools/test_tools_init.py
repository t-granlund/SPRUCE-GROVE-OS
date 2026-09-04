"""Tests for spruce_grove/tools/__init__.py - 100% coverage."""

from unittest.mock import MagicMock, patch


class TestLoadPluginTools:
    def test_no_plugin_does_not_expose_skill_tools(self):
        from spruce_grove.tools import TOOL_REGISTRY, _load_plugin_tools

        names = ("activate_skill", "list_or_search_skills")
        previous = {name: TOOL_REGISTRY.pop(name, None) for name in names}
        try:
            with patch("spruce_grove.tools.on_register_tools", return_value=[]):
                _load_plugin_tools()
            assert all(name not in TOOL_REGISTRY for name in names)
        finally:
            TOOL_REGISTRY.update(
                {name: func for name, func in previous.items() if func is not None}
            )

    def test_loads_tools(self):
        from spruce_grove.tools import TOOL_REGISTRY, _load_plugin_tools

        with patch("spruce_grove.tools.on_register_tools") as mock_cb:
            mock_cb.return_value = [
                [{"name": "test_tool", "register_func": lambda a: None}]
            ]
            _load_plugin_tools()
            assert "test_tool" in TOOL_REGISTRY
            del TOOL_REGISTRY["test_tool"]

    def test_none_results(self):
        from spruce_grove.tools import _load_plugin_tools

        with patch("spruce_grove.tools.on_register_tools") as mock_cb:
            mock_cb.return_value = [None]
            _load_plugin_tools()  # should not raise

    def test_single_dict_result(self):
        from spruce_grove.tools import TOOL_REGISTRY, _load_plugin_tools

        with patch("spruce_grove.tools.on_register_tools") as mock_cb:
            mock_cb.return_value = [
                {"name": "single_tool", "register_func": lambda a: None}
            ]
            _load_plugin_tools()
            assert "single_tool" in TOOL_REGISTRY
            del TOOL_REGISTRY["single_tool"]

    def test_invalid_tool_def(self):
        from spruce_grove.tools import _load_plugin_tools

        with patch("spruce_grove.tools.on_register_tools") as mock_cb:
            mock_cb.return_value = [[{"name": "no_func"}]]  # missing register_func
            _load_plugin_tools()  # should not raise

    def test_non_callable(self):
        from spruce_grove.tools import _load_plugin_tools

        with patch("spruce_grove.tools.on_register_tools") as mock_cb:
            mock_cb.return_value = [[{"name": "x", "register_func": "not_callable"}]]
            _load_plugin_tools()  # should not add

    def test_exception_swallowed(self):
        from spruce_grove.tools import _load_plugin_tools

        with patch(
            "spruce_grove.tools.on_register_tools", side_effect=Exception("boom")
        ):
            _load_plugin_tools()  # should not raise


class TestHasExtendedThinkingActive:
    @patch("spruce_grove.config.get_global_model_name", return_value=None)
    def test_no_model(self, mock_model):
        from spruce_grove.tools import has_extended_thinking_active

        assert not has_extended_thinking_active()

    def test_non_claude(self):
        from spruce_grove.tools import has_extended_thinking_active

        assert not has_extended_thinking_active("gpt-4")

    @patch("spruce_grove.config.get_effective_model_settings", return_value={})
    @patch("spruce_grove.model_utils.get_default_extended_thinking", return_value=False)
    def test_claude_disabled(self, mock_default, mock_settings):
        from spruce_grove.tools import has_extended_thinking_active

        assert not has_extended_thinking_active("claude-3")

    @patch(
        "spruce_grove.config.get_effective_model_settings",
        return_value={"extended_thinking": True},
    )
    @patch("spruce_grove.model_utils.get_default_extended_thinking", return_value=False)
    def test_claude_legacy_true(self, mock_default, mock_settings):
        from spruce_grove.tools import has_extended_thinking_active

        assert has_extended_thinking_active("claude-3")

    @patch(
        "spruce_grove.config.get_effective_model_settings",
        return_value={"extended_thinking": "enabled"},
    )
    @patch("spruce_grove.model_utils.get_default_extended_thinking", return_value=False)
    def test_claude_enabled(self, mock_default, mock_settings):
        from spruce_grove.tools import has_extended_thinking_active

        assert has_extended_thinking_active("claude-3")

    @patch(
        "spruce_grove.config.get_effective_model_settings",
        return_value={"extended_thinking": "adaptive"},
    )
    @patch("spruce_grove.model_utils.get_default_extended_thinking", return_value=False)
    def test_claude_adaptive(self, mock_default, mock_settings):
        from spruce_grove.tools import has_extended_thinking_active

        assert has_extended_thinking_active("anthropic-model")


class TestRegisterToolsForAgent:
    @patch("spruce_grove.tools._load_plugin_tools")
    @patch("spruce_grove.tools.has_extended_thinking_active", return_value=False)
    def test_register_known_tool(self, mock_ext, mock_load):
        from spruce_grove.tools import TOOL_REGISTRY, register_tools_for_agent

        agent = MagicMock()
        mock_fn = MagicMock()
        TOOL_REGISTRY["__test_tool"] = mock_fn
        try:
            register_tools_for_agent(agent, ["__test_tool"])
            mock_fn.assert_called_once_with(agent)
        finally:
            del TOOL_REGISTRY["__test_tool"]

    @patch("spruce_grove.tools._load_plugin_tools")
    @patch("spruce_grove.tools.has_extended_thinking_active", return_value=False)
    @patch("spruce_grove.tools.emit_warning")
    def test_unknown_tool(self, mock_warn, mock_ext, mock_load):
        from spruce_grove.tools import register_tools_for_agent

        agent = MagicMock()
        register_tools_for_agent(agent, ["__nonexistent_tool"])
        mock_warn.assert_called()

    @patch("spruce_grove.tools._load_plugin_tools")
    @patch("spruce_grove.tools.has_extended_thinking_active", return_value=False)
    def test_register_legacy_reasoning_tool(self, mock_ext, mock_load):
        from spruce_grove.tools import register_tools_for_agent

        agent = MagicMock()
        register_tools_for_agent(agent, ["agent_share_your_reasoning"])
        agent.tool.assert_called()

    @patch("spruce_grove.tools._load_plugin_tools")
    @patch("spruce_grove.tools.has_extended_thinking_active", return_value=False)
    @patch("spruce_grove.config.get_universal_constructor_enabled", return_value=False)
    def test_skip_uc_disabled(self, mock_uc, mock_ext, mock_load):
        from spruce_grove.tools import TOOL_REGISTRY, register_tools_for_agent

        mock_fn = MagicMock()
        original = TOOL_REGISTRY.get("universal_constructor")
        TOOL_REGISTRY["universal_constructor"] = mock_fn
        try:
            agent = MagicMock()
            register_tools_for_agent(agent, ["universal_constructor"])
            mock_fn.assert_not_called()
        finally:
            if original:
                TOOL_REGISTRY["universal_constructor"] = original

    @patch("spruce_grove.tools._load_plugin_tools")
    @patch("spruce_grove.tools.has_extended_thinking_active", return_value=False)
    @patch("spruce_grove.config.get_universal_constructor_enabled", return_value=False)
    def test_skip_uc_prefixed_disabled(self, mock_uc, mock_ext, mock_load):
        from spruce_grove.tools import register_tools_for_agent

        agent = MagicMock()
        register_tools_for_agent(agent, ["uc:api.weather"])
        # Should skip silently

    @patch("spruce_grove.tools._load_plugin_tools")
    @patch("spruce_grove.tools.has_extended_thinking_active", return_value=False)
    @patch("spruce_grove.config.get_universal_constructor_enabled", return_value=True)
    @patch("spruce_grove.tools._register_uc_tool_wrapper")
    def test_uc_prefixed_enabled(self, mock_uc_reg, mock_uc, mock_ext, mock_load):
        from spruce_grove.tools import register_tools_for_agent

        agent = MagicMock()
        register_tools_for_agent(agent, ["uc:api.weather"])
        mock_uc_reg.assert_called_once_with(agent, "api.weather")


class TestRegisterUcToolWrapper:
    @patch("code_puppy_core_plugins.universal_constructor.registry.get_registry")
    @patch("spruce_grove.tools.emit_warning")
    def test_tool_not_found(self, mock_warn, mock_reg):
        from spruce_grove.tools import _register_uc_tool_wrapper

        mock_reg.return_value.get_tool.return_value = None
        _register_uc_tool_wrapper(MagicMock(), "bad")
        mock_warn.assert_called()

    @patch("code_puppy_core_plugins.universal_constructor.registry.get_registry")
    @patch("spruce_grove.tools.emit_warning")
    def test_func_not_found(self, mock_warn, mock_reg):
        from spruce_grove.tools import _register_uc_tool_wrapper

        tool = MagicMock()
        tool.meta.description = "d"
        tool.docstring = "doc"
        mock_reg.return_value.get_tool.return_value = tool
        mock_reg.return_value.get_tool_function.return_value = None
        _register_uc_tool_wrapper(MagicMock(), "t")
        mock_warn.assert_called()

    @patch("code_puppy_core_plugins.universal_constructor.registry.get_registry")
    def test_success(self, mock_reg):
        from spruce_grove.tools import _register_uc_tool_wrapper

        tool = MagicMock()
        tool.meta.description = "d"
        tool.docstring = "doc"
        mock_reg.return_value.get_tool.return_value = tool

        def my_func(x: int = 1) -> int:
            return x

        mock_reg.return_value.get_tool_function.return_value = my_func
        agent = MagicMock()
        _register_uc_tool_wrapper(agent, "my.tool")
        agent.tool.assert_called_once()

    @patch(
        "code_puppy_core_plugins.universal_constructor.registry.get_registry",
        side_effect=Exception("boom"),
    )
    @patch("spruce_grove.tools.emit_warning")
    def test_exception(self, mock_warn, mock_reg):
        from spruce_grove.tools import _register_uc_tool_wrapper

        _register_uc_tool_wrapper(MagicMock(), "t")
        mock_warn.assert_called()

    @patch("code_puppy_core_plugins.universal_constructor.registry.get_registry")
    @patch("spruce_grove.tools.emit_warning")
    def test_register_fails(self, mock_warn, mock_reg):
        from spruce_grove.tools import _register_uc_tool_wrapper

        tool = MagicMock()
        tool.meta.description = "d"
        tool.docstring = None
        mock_reg.return_value.get_tool.return_value = tool
        mock_reg.return_value.get_tool_function.return_value = lambda: None
        agent = MagicMock()
        agent.tool.side_effect = Exception("fail")
        _register_uc_tool_wrapper(agent, "t")
        mock_warn.assert_called()


class TestRegisterAllToolsAndGetNames:
    @patch("spruce_grove.tools.register_tools_for_agent")
    def test_register_all(self, mock_reg):
        from spruce_grove.tools import register_all_tools

        agent = MagicMock()
        register_all_tools(agent, model_name="test")
        mock_reg.assert_called_once()

    @patch("spruce_grove.tools._load_plugin_tools")
    def test_get_names(self, mock_load):
        from spruce_grove.tools import get_available_tool_names

        names = get_available_tool_names()
        assert isinstance(names, list)
        assert len(names) > 0
