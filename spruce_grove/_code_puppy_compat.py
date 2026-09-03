"""Legacy ``code_puppy`` import compatibility shim.

Spruce Grove OS is a distribution inspired by and built from Code Puppy; the
core package was renamed ``code_puppy`` -> ``spruce_grove``. External plugin
packages (notably the ``code-puppy-core-plugins`` bundle) still import the
core under its original dotted name, e.g. ``from code_puppy.callbacks import
...``. This module installs a meta-path finder that resolves any import of
``code_puppy`` or ``code_puppy.*`` to the corresponding ``spruce_grove``
module, keeping the external plugin ecosystem working unchanged.

Design notes:

- The finder is *prepended* to ``sys.meta_path``. It must come before
  ``PathFinder`` because the legacy parent package gets aliased to the real
  ``spruce_grove`` package, whose ``__path__`` would otherwise let
  ``PathFinder`` load ``code_puppy.<submodule>`` as a *second, divergent*
  module object from the same file.
- If a genuinely installed ``code_puppy`` distribution is on ``sys.path``
  (detected via ``PathFinder`` before our hook goes in), the shim stays out
  of the way entirely and the real package wins.
"""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import sys

_LEGACY = "code_puppy"
_TARGET = "spruce_grove"


class _CodePuppyAliasLoader(importlib.abc.Loader):
    """Loads a legacy-named module by delegating to its spruce_grove twin."""

    def __init__(self, target_name: str) -> None:
        self._target_name = target_name

    def create_module(self, spec):  # noqa: D102 - importlib protocol
        return importlib.import_module(self._target_name)

    def exec_module(self, module) -> None:  # noqa: D102 - importlib protocol
        # Alias the dotted legacy name straight at the canonical module so
        # ``code_puppy.x is spruce_grove.x`` holds True everywhere.
        sys.modules[self._legacy_name(self._target_name)] = sys.modules[
            self._target_name
        ]

    @staticmethod
    def _legacy_name(target_name: str) -> str:
        if target_name == _TARGET:
            return _LEGACY
        return _LEGACY + target_name[len(_TARGET) :]


class _CodePuppyAliasFinder(importlib.abc.MetaPathFinder):
    """Maps ``code_puppy[.*]`` lookups onto ``spruce_grove[.*]``."""

    def find_spec(self, fullname, path=None, target=None):
        if fullname == _LEGACY:
            target_name = _TARGET
        elif fullname.startswith(_LEGACY + "."):
            target_name = _TARGET + fullname[len(_LEGACY) :]
        else:
            return None

        spec = importlib.util.find_spec(target_name)
        if spec is None:
            return None
        return importlib.util.spec_from_loader(
            fullname, _CodePuppyAliasLoader(target_name)
        )


def _real_legacy_package_exists() -> bool:
    """True if a real ``code_puppy`` distribution is importable via sys.path."""
    spec = importlib.machinery.PathFinder.find_spec(_LEGACY, None)
    return spec is not None


def install() -> None:
    """Install the alias finder once (idempotent).

    Skipped entirely when a real legacy package exists on disk - correctness
    for external plugins matters, but an actual co-installed ``code_puppy``
    must always win.
    """
    if any(isinstance(f, _CodePuppyAliasFinder) for f in sys.meta_path):
        return
    if _real_legacy_package_exists():
        return
    sys.meta_path.insert(0, _CodePuppyAliasFinder())
