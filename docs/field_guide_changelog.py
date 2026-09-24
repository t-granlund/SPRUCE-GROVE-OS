"""Changelog feed generator for the Spruce Grove field guide.

Produces the `changelog_data` dict the HTML renderer consumes: a summary of
recent commits on main and a simple set of monthly release buckets.

Shape returned by `_get_recent_commits`:
    {
        "total_commits": int,           # commits in the last ~2 months on main
        "releases": [                   # one entry per calendar month bucket
            {"month": "2026-08", "commit_count": 42, "commits": [...]}
        ],
        "commits": [                    # subset of recent commits as dicts
            {"hash", "short_hash", "subject", "author", "date"}
        ],
    }
"""

import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Public pages show seats, not names (MANIFESTO, "Not tied to a single
# person"). The grove's own commits render as "the grove"; upstream
# contributors and bots keep their names — credit, not exposure.
#
# This is the CANONICAL grove-author set. Anything that classifies commit
# authorship for a public surface (e.g. pages-hub/generate-updates.py's
# provenance chips) must import it from here — a second, divergent copy is
# exactly how an anonymity regression ships.
GROVE_AUTHORS = {"tyler granlund", "t-granlund", "tyler", "tyler.granlund"}

# The public display form `_display_author` emits for every grove author.
# Provenance classifiers must treat this value as grove-grown too, or the
# anonymized feeds mislabel their own commits as upstream.
GROVE_DISPLAY_NAME = "the grove"


def _display_author(author: str) -> str:
    """Anonymize the grove's own commit author for public rendering."""
    return GROVE_DISPLAY_NAME if author.strip().lower() in GROVE_AUTHORS else author


#: Personal identity that can appear inside a commit SUBJECT, not just its
#: author. Redacting `%an` alone was not enough: seven subjects on the live
#: site named the person or their domain, because the words were typed into the
#: message rather than the author field.
#:
#: `t-granlund` is deliberately NOT matched here -- it is the account handle in
#: URLs and remotes, it cannot change without an org transfer, and replacing it
#: inside a pasted URL would produce a broken link rather than a private one.
#: `(?<![-\w])` is load-bearing, not decoration: without it the generic
#: surname rule rewrites the `t-granlund` HANDLE into `t-the grove` and breaks
#: every URL that contains it. Order also matters -- the specific patterns run
#: before the generic one, so a domain is described rather than half-replaced.
_PERSONAL_IN_SUBJECT = (
    (re.compile(r"\btylergranlund\.com\b", re.I), "the grove site"),
    (re.compile(r"\btyler\s+granlund\b", re.I), GROVE_DISPLAY_NAME),
    (re.compile(r"\bgranlund-grove\b", re.I), "grove"),
    (re.compile(r"(?<![-\w])granlund\b", re.I), GROVE_DISPLAY_NAME),
    (re.compile(r"\btyler\b", re.I), GROVE_DISPLAY_NAME),
)


def _display_subject(subject: str) -> str:
    """Anonymize the grove's own commit subject for public rendering.

    Same policy as :func:`_display_author`, applied to the message text. Keeps
    the sentence and its meaning; only the person leaves.
    """
    for pattern, replacement in _PERSONAL_IN_SUBJECT:
        subject = pattern.sub(replacement, subject)
    return subject


def _get_recent_commits(_run, repo_root: Path) -> dict:
    """Return a changelog summary dict consumed by `generate-field-guide.py`."""
    try:
        output = _run(
            [
                "git",
                "log",
                "main",
                "--since=2 months ago",
                "--pretty=format:%H|%h|%s|%an|%aI",
                "--name-only",
            ],
            cwd=repo_root,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, TypeError):
        return {"total_commits": 0, "releases": [], "commits": []}

    commits: list[dict] = []
    current: dict | None = None
    for line in output.splitlines():
        if "|" in line:
            if current is not None:
                commits.append(current)
            full_hash, short_hash, subject, author, timestamp = line.split("|", 4)
            try:
                dt = datetime.fromisoformat(timestamp)
                date_str = dt.strftime("%Y-%m-%d")
                month_str = dt.strftime("%Y-%m")
            except ValueError:
                date_str = timestamp.split("T")[0] if "T" in timestamp else timestamp
                month_str = date_str[:7]
            current = {
                "hash": full_hash,
                "short_hash": short_hash,
                "subject": _display_subject(subject),
                "author": _display_author(author),
                "date": date_str,
                "month": month_str,
            }
        elif current is not None and line.strip():
            # files touched — we don't surface them, but tracking keeps parsing aligned
            pass

    if current is not None:
        commits.append(current)

    # Bucket by calendar month (releases == one entry per month with commits)
    month_buckets: dict[str, list[dict]] = defaultdict(list)
    for c in commits:
        month_buckets[c["month"]].append(c)

    releases = [
        {"month": month, "commit_count": len(bucket), "commits": bucket[:10]}
        for month, bucket in sorted(month_buckets.items(), reverse=True)
    ]

    return {
        "total_commits": len(commits),
        "releases": releases,
        "commits": [
            {k: c[k] for k in ("hash", "short_hash", "subject", "author", "date")}
            for c in commits
        ],
    }
