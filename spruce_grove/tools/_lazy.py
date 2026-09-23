"""Resolve tool implementations only when an agent registers them.

Lazy resolution is what keeps boot light and what lets an agent carry only
the tools it actually uses. It also means the import happens *mid-session*,
whenever an agent first needs a tool — so this is the seam where a tool can
fail to import long after startup.

That matters for one specific reason: an install upgraded underneath a
running process replaces code on disk while the process still holds the old
module table, and the next lazy import then fails confusingly. The wrapper
below names that cause instead of surfacing a bare, baffling ImportError.
"""

import logging
from importlib import import_module

logger = logging.getLogger(__name__)


def _stale_install_hint(module: str, exc: BaseException) -> str:
    """Describe a lazy-import failure in terms the user can act on.

    The overwhelmingly likely cause of a mid-session import failure is a
    stale in-process module: the CLI is upgraded on disk while it runs
    (self-update), so the running process's module table no longer matches
    the files. Say so, and give the fix.
    """
    return (
        f"tool module {module!r} could not be imported "
        f"({type(exc).__name__}: {exc}). The installed code may have been "
        "upgraded underneath a running process — restart the CLI so its "
        "modules are re-imported."
    )


def lazy_registration(module: str, name: str):
    """Return a register callable that imports ``module.name`` on first use.

    A failure is raised as an ImportError carrying an actionable message; the
    caller (``register_tools_for_agent``) treats it as a skipped tool rather
    than a fatal error, so one broken tool can never take down an agent run.
    """

    def register(*args, **kwargs):
        try:
            return getattr(import_module(module), name)(*args, **kwargs)
        except ImportError as exc:
            # Only re-frame a genuinely stale/missing import. An error raised
            # from *inside* a successfully-loaded tool's registration is that
            # tool's own bug and should surface unchanged.
            if _is_missing_symbol(module, name, exc):
                message = _stale_install_hint(module, exc)
                logger.warning(message)
                raise ImportError(message) from exc
            raise

    register.__name__ = name
    register.__qualname__ = name
    return register


def _is_missing_symbol(module: str, name: str, exc: ImportError) -> bool:
    """True when ``module`` or ``name`` failed to resolve.

    Distinguishes "this symbol/module isn't importable" (worth re-framing)
    from "the tool's own registration raised ImportError" (not our business).
    """
    target = f"{module}.{name}"
    message = str(exc)
    return (
        target in message
        or module in message
        or name in message
        or "cannot import name" in message
    )
