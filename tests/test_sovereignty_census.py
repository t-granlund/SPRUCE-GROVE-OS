"""Keep the pydantic-ai exit census honest.

SOVEREIGNTY.md quotes how many files still reach for pydantic-ai, and that
number has already drifted once: the 2026-09-22 figure counted only top-level
``pydantic_ai`` imports and missed ten files that reach the framework through
``model_factory`` or a nested import. A documented number nobody checks is a
number that rots, so the ceiling is pinned here.

This is deliberately a *ceiling*, not an equality: it must fail when the exit
regresses (new pydantic-ai reach), and it should be lowered as the replacement
lands. It must never block progress by demanding an exact match.
"""

import re
from pathlib import Path

import pytest

GROVE = Path(__file__).resolve().parent.parent / "spruce_grove"

#: Measured 2026-09-23. Lower these as the replacement lands; never raise them
#: without a written reason -- raising them means the exit went backwards.
MAX_FILES = 57
MAX_IMPORTS = 92

#: ``from pydantic_ai...`` / ``import pydantic_ai...`` at any indentation, plus
#: ``model_factory`` (grove's own module, but it re-exports the framework).
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+pydantic_ai", re.MULTILINE)


def _python_files():
    return sorted(GROVE.rglob("*.py"))


def _files_reaching_the_framework():
    """Files that touch pydantic-ai directly or through grove's model_factory."""
    return [
        p
        for p in _python_files()
        if "pydantic_ai" in p.read_text(encoding="utf-8")
        or "model_factory" in p.read_text(encoding="utf-8")
    ]


def _import_statement_count():
    return sum(
        len(IMPORT_RE.findall(p.read_text(encoding="utf-8"))) for p in _python_files()
    )


class TestCensus:
    def test_file_count_does_not_regress(self):
        found = len(_files_reaching_the_framework())
        assert found <= MAX_FILES, (
            f"{found} files reach pydantic-ai, ceiling is {MAX_FILES}. "
            "The sovereignty exit went backwards -- new code should use the "
            "harness seam, not the framework."
        )

    def test_import_count_does_not_regress(self):
        found = _import_statement_count()
        assert found <= MAX_IMPORTS, (
            f"{found} pydantic_ai import statements, ceiling is {MAX_IMPORTS}."
        )

    def test_the_counts_are_worth_checking(self):
        """Guard the guard: a broken glob would make both checks vacuous."""
        assert len(_python_files()) > 200
        assert _import_statement_count() > 0


class TestSeamIsTheIntendedPath:
    def test_the_seam_imports_no_framework(self):
        """protocol.py is the contract; it must stay dependency-free."""
        protocol = GROVE / "harness" / "protocol.py"
        assert "pydantic_ai" not in protocol.read_text(encoding="utf-8")

    def test_harness_is_import_light(self):
        """Naming the seam must not drag the framework in.

        Subprocess is the honest test: a module already imported by the test
        session would mask an eager import.
        """
        import subprocess
        import sys

        code = (
            "import sys; import spruce_grove.harness; "
            "assert not any(m.startswith('pydantic_ai') for m in sys.modules), "
            "[m for m in sys.modules if m.startswith('pydantic_ai')]"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, timeout=60
        )
        assert completed.returncode == 0, completed.stderr

    @pytest.mark.parametrize(
        "name",
        [
            "resolve_model",
            "load_models_config",
            "make_model_settings",
            "tool_context_type",
        ],
    )
    def test_the_protocol_still_exposes_the_vocabulary(self, name):
        """These four are what step 2 delivered; losing one is a regression."""
        from spruce_grove.harness.protocol import Harness

        assert hasattr(Harness, name)
