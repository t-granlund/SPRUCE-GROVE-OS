"""Changelog feed generator for the Code Puppy field guide.

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

import subprocess
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


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
                "subject": subject,
                "author": author,
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
        "commits": [{k: c[k] for k in ("hash", "short_hash", "subject", "author", "date")} for c in commits],
    }
