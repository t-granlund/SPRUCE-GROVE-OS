"""Keep the anonymity pivot's policy true (commit bcc846c).

The policy is: **public surfaces show seats, not names -- persons generalized,
stories kept; business names stay.** An audit of every tracked file on
2026-09-23 found 320 lines across 74 files, which is far more than the pivot
reached. See ``docs/ANONYMITY-EXIT.md`` for the ranked findings and the plan.

Why a denylist rather than a strict allowlist: 74 files cannot be cleaned in
one pass without inventing policy about the long tail. So this test hard-fails
on the surfaces whose exposure is *verified and serious* -- packaging metadata,
the shipped model prompt, the copyright line, an actively-enforced
``CODEOWNERS``, and any private working doc that is tracked -- and reports the
rest as a shrinking backlog. Add globs to ``STRICT`` as surfaces get cleaned.

Placement matters: ``.github/workflows/publish.yml`` runs the full test suite
before it bumps the version, so a regression here **blocks the release**.
"""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

#: The individual voice the pivot generalizes.
#:
#: ``Pfaffenberger`` is DELIBERATELY absent: upstream Code Puppy attribution is
#: required, not exposure. Business names are absent per policy. Matching his
#: name here would make the guardrail wrong, not the code.
#:
#: ``t-granlund`` is the GitHub ACCOUNT handle -- the remote URL, the
#: CODEOWNERS reviewer. It cannot change without renaming the account or
#: transferring the repo to an organisation, and flagging every URL would drown
#: the signal from the actual personal NAME. So the surname is only counted
#: when it is NOT part of that handle. A bare ``(?<!-)`` is insufficient: in
#: ``github.com/t-granlund/X`` the character before ``granlund`` is ``/``, so
#: the lookbehind never fires. ``(?<![-\w])`` is what actually excludes it.
DENY = re.compile(
    r"(?i)\btyler\b"
    r"|(?<![-\w])granlund\b"
    r"|tylergranlund\.com"
    r"|hello@tylergranlund\.com"
)

#: Files that legitimately contain the name, because their JOB is to handle it.
ALLOW = {
    # Must know the name in order to redact it from the field guide.
    "docs/field_guide_changelog.py",
    # Exercises that redaction, so it asserts the name is recognized.
    "tests/test_site_generators.py",
    # This file.
    "tests/test_anonymity_audit.py",
    # The plan document quotes the findings it describes.
    "docs/ANONYMITY-EXIT.md",
}

#: Cleaned surfaces. A hit in any of these is a hard failure -- these are the
#: places where the name is both public and consequential.
#:
#: Most were fixed in the commit that added this file. The shipped prompt, the
#: copyright line, the trademark contact and the packaging metadata are all
#: free text: they can name a seat instead of a person with no loss of meaning.
STRICT = [
    "pyproject.toml",
    "NOTICE",
    "TRADEMARKS.md",
    "spruce_grove/**/*.py",
]

#: Surfaces still to clean, with their 2026-09-23 counts. The test reports
#: these instead of failing, so progress is visible without blocking work.
#: Cleaned 2026-09-23: `SESSION-HANDOFF.md` (20 hits) -- untracked, gitignored,
#: replaced by the name-free `docs/SESSION-START.md`.
BACKLOG = {
    "BUILD-LOG.md": 16,
    "pages-hub/dashboard.html": 14,
    "mission-control.html": 13,
    "docs/SOVEREIGNTY-EXECUTION.md": 10,
    "SOURCITY.md": 8,
    "LIVING-UPDATES.md": 6,
    "docs/LICENSE-ANALYSIS.md": 6,
    "BRAND.md": 5,
}


def _tracked_files() -> list[str]:
    """Every file git tracks -- i.e. every file that is public."""
    result = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def _is_scannable(rel: str) -> bool:
    return Path(rel).suffix.lower() not in {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".whl",
        ".gz",
        ".woff",
        ".woff2",
        ".zip",
        ".pdf",
    }


def _lines_with_name(rel: str) -> list[tuple[int, str]]:
    path = REPO / rel
    if not path.is_file() or not _is_scannable(rel):
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    return [
        (number, line.strip())
        for number, line in enumerate(text.splitlines(), start=1)
        if DENY.search(line)
    ]


def _matches_any(rel: str, globs: list[str]) -> bool:
    return any(Path(rel).match(pattern) for pattern in globs)


class TestStrictSurfaces:
    """These must be clean. A failure here is a release blocker."""

    @pytest.mark.parametrize("pattern", STRICT)
    def test_no_personal_identity(self, pattern):
        offenders = []
        for rel in _tracked_files():
            if rel in ALLOW or not _matches_any(rel, [pattern]):
                continue
            offenders.extend(f"{rel}:{n}: {line}" for n, line in _lines_with_name(rel))
        assert not offenders, (
            f"personal identity on a public surface matching {pattern!r}:\n"
            + "\n".join(offenders)
        )


class TestPackagingMetadata:
    """What PyPI will publish, once corrected, must name no person."""

    def test_authors_and_urls_carry_no_individual(self):
        project = tomllib.loads((REPO / "pyproject.toml").read_text())["project"]
        blob = f"{project.get('authors')} {project.get('maintainers')} {project.get('urls')}"
        assert not DENY.search(blob), (
            "pyproject authors/maintainers/urls still publish a personal identity"
        )

    def test_upstream_attribution_is_preserved(self):
        """The fix must not over-correct: Pfaffenberger's credit is required."""
        project = tomllib.loads((REPO / "pyproject.toml").read_text())["project"]
        names = " ".join(entry.get("name", "") for entry in project.get("authors", []))
        assert "Pfaffenberger" in names, (
            "upstream Code Puppy attribution was dropped while de-personalizing"
        )

    def test_author_email_is_real_or_absent_never_invented(self):
        """A bouncing address in permanent metadata is worse than none."""
        project = tomllib.loads((REPO / "pyproject.toml").read_text())["project"]
        for entry in project.get("authors", []):
            email = entry.get("email", "")
            if email:
                assert not email.endswith("@sprucegrove.io"), (
                    "sprucegrove.io has no MX records (verified 2026-09-23), so a "
                    "role address there would bounce; stand up a mailbox first"
                )


class TestFunctionalIdentities:
    """Some exposures are handles, not names -- and removal breaks function.

    ``.github/CODEOWNERS`` names ``@t-granlund`` as the required reviewer. That
    is a GitHub ACCOUNT handle: it must resolve to a real account or the review
    gate silently stops working, and it cannot change without renaming the
    account or transferring the repo to an organisation. The honest shape of
    that is a *documented pending migration*, not a fake pass and not a
    permanently-red test.
    """

    #: Real account handles permitted to appear in functional config. Distinct
    #: from a personal NAME, which must never appear.
    ALLOWED_HANDLES = {"@t-granlund", "t-granlund"}

    def test_codeowners_uses_only_allowed_handles(self):
        text = (REPO / ".github/CODEOWNERS").read_text()
        handles = set(re.findall(r"@[A-Za-z0-9_.-]+", text))
        assert handles <= self.ALLOWED_HANDLES, (
            "CODEOWNERS names a handle outside the allowlist: "
            f"{handles - self.ALLOWED_HANDLES}"
        )

    def test_codeowners_names_no_personal_name(self):
        """The rule that still applies: seats in config, never names."""
        offenders = [
            f"{n}: {line}" for n, line in _lines_with_name(".github/CODEOWNERS")
        ]
        assert not offenders, (
            "CODEOWNERS contains a personal name (handles belong, names do not):\n"
            + "\n".join(offenders)
        )

    def test_the_org_transfer_is_recorded_as_pending(self):
        """An unrecorded limitation becomes a permanent one."""
        doc = (REPO / "docs" / "ANONYMITY-EXIT.md").read_text()
        assert "CODEOWNERS" in doc, "the pending org migration is undocumented"
        assert "t-granlund" in doc, "the handle's pending migration is undocumented"


class TestPrivateWorkingDocsStayPrivate:
    """Working docs are not public surfaces. This is the feasibility half."""

    def test_session_handoff_is_not_tracked(self):
        assert "SESSION-HANDOFF.md" not in _tracked_files(), (
            "the session handoff is a private working doc; it must not be tracked"
        )

    def test_the_public_pointer_exists_once_the_handoff_moves(self):
        """Deleting the handoff must leave a name-free entry point behind."""
        if "SESSION-HANDOFF.md" in _tracked_files():
            pytest.skip("handoff not yet removed; nothing to point from")
        pointer = REPO / "docs" / "SESSION-START.md"
        assert pointer.is_file(), "handoff removed with no replacement pointer"


class TestBacklogIsTrackedHonestly:
    """The long tail is not fixed yet; make that a visible number, not a guess."""

    #: Measured 2026-09-23. Lower it as files are cleaned; never raise it.
    MAX_FILES_WITH_NAME = 73

    def test_backlog_count_does_not_regress(self):
        """New leaks raise the count; cleaned files lower it."""
        measured = sum(
            1 for rel in _tracked_files() if rel not in ALLOW and _lines_with_name(rel)
        )
        assert measured <= self.MAX_FILES_WITH_NAME, (
            f"{measured} tracked files carry the personal name "
            f"(ceiling {self.MAX_FILES_WITH_NAME}). The cleanup is going backwards."
        )

    def test_scan_is_actually_looking_at_files(self):
        """Guard the guard: a broken git call would make every check vacuous."""
        tracked = _tracked_files()
        assert len(tracked) > 100
        assert "pyproject.toml" in tracked


class TestRedactionAllowlistStaysWhole:
    """The documented #1 regression: a divergent copy of the author list."""

    def test_grove_authors_cover_every_known_alias(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_fgc_for_audit", REPO / "docs" / "field_guide_changelog.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert {"tyler granlund", "t-granlund", "tyler", "tyler.granlund"} <= (
            module.GROVE_AUTHORS
        )
        assert module.GROVE_DISPLAY_NAME == "the grove"
