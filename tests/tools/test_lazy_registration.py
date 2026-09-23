"""Keep tool discovery cheap without changing registration behavior."""

import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from spruce_grove.tools._lazy import lazy_registration


def test_registration_defers_import_and_forwards_arguments(monkeypatch):
    implementation = Mock(return_value="registered")
    importer = Mock(return_value=SimpleNamespace(register_example=implementation))
    monkeypatch.setattr("spruce_grove.tools._lazy.import_module", importer)
    register = lazy_registration("example.tools", "register_example")
    importer.assert_not_called()
    assert register.__name__ == "register_example"
    agent = object()
    assert register(agent, option=True) == "registered"
    importer.assert_called_once_with("example.tools")
    implementation.assert_called_once_with(agent, option=True)


def test_listing_tools_does_not_import_browser_implementations():
    # A fresh process avoids modules preloaded by pytest/conftest masking
    # an accidental eager import. No fragile wall-clock threshold.
    subprocess.run(
        [
            sys.executable,
            "-c",
            """
import sys
from spruce_grove.tools import TOOL_REGISTRY
assert 'browser_initialize' in TOOL_REGISTRY
assert all(callable(value) for value in TOOL_REGISTRY.values())
assert 'spruce_grove.tools.browser.browser_manager' not in sys.modules
assert 'playwright.async_api' not in sys.modules
""",
        ],
        check=True,
        timeout=30,
    )


def test_all_lazy_registrations_resolve():
    from importlib import import_module

    from spruce_grove.tools import TOOL_REGISTRY

    for register in TOOL_REGISTRY.values():
        if register.__module__ != "spruce_grove.tools._lazy":
            continue
        closed = dict(zip(register.__code__.co_freevars, register.__closure__))
        module = import_module(closed["module"].cell_contents)
        assert callable(getattr(module, closed["name"].cell_contents))


class TestStaleImportDiagnostics:
    """A mid-session import failure must name its likely cause.

    Regression: a long-lived process kept a stale module table after an
    on-disk upgrade, so a lazy tool import failed with a bare ImportError
    that gave no hint what had happened.
    """

    def test_missing_symbol_is_reframed_with_the_restart_hint(self, monkeypatch):
        def boom(_module):
            raise ImportError(
                "cannot import name 'ToolContext' from 'spruce_grove.harness'"
            )

        monkeypatch.setattr("spruce_grove.tools._lazy.import_module", boom)
        register = lazy_registration(
            "spruce_grove.tools.browser.browser_control", "register_browser_initialize"
        )
        with pytest.raises(ImportError) as excinfo:
            register(object())

        message = str(excinfo.value)
        assert "restart" in message.lower()
        assert "upgraded" in message.lower()
        # The original failure is preserved as the cause.
        assert isinstance(excinfo.value.__cause__, ImportError)

    def test_a_tools_own_import_error_surfaces_unchanged(self, monkeypatch):
        """If the module loads but the tool itself raises ImportError,
        that is the tool's own bug -- do not blame the install."""

        def raises_inside(agent):
            raise ImportError("some internal optional dependency is missing")

        importer = Mock(return_value=SimpleNamespace(register_thing=raises_inside))
        monkeypatch.setattr("spruce_grove.tools._lazy.import_module", importer)
        register = lazy_registration("example.tools", "register_thing")

        with pytest.raises(ImportError) as excinfo:
            register(object())
        assert "restart the CLI" not in str(excinfo.value)

    def test_missing_module_is_reframed(self, monkeypatch):
        def boom(_module):
            raise ImportError("No module named 'spruce_grove.tools.gone'")

        monkeypatch.setattr("spruce_grove.tools._lazy.import_module", boom)
        register = lazy_registration("spruce_grove.tools.gone", "register_gone")
        with pytest.raises(ImportError) as excinfo:
            register(object())
        assert "restart" in str(excinfo.value).lower()

    def test_success_path_is_untouched(self, monkeypatch):
        impl = Mock(return_value="ok")
        importer = Mock(return_value=SimpleNamespace(register_x=impl))
        monkeypatch.setattr("spruce_grove.tools._lazy.import_module", importer)
        register = lazy_registration("example.tools", "register_x")
        assert register("agent") == "ok"
