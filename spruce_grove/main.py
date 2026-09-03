"""Main entry point for Spruce Grove CLI.

This module re-exports the main_entry function from cli_runner for backwards
compatibility. All the actual logic lives in cli_runner.py.

The neon splash starts BEFORE the cli_runner import below: that import pulls
in pydantic-ai, prompt_toolkit, rich, and friends (~seconds of cold start),
which is exactly the window the shimmer covers. ``spruce_grove.splash`` is
stdlib-only by design -- keep it that way, and keep it first.
"""

from spruce_grove.splash import start_splash

_splash = start_splash()
try:
    from spruce_grove.cli_runner import main_entry
finally:
    _splash.stop()

__all__ = ["main_entry"]

if __name__ == "__main__":
    main_entry()
