"""Discover the grove sessions running on this machine right now.

A "live session" is what the user means by it: an **open terminal** that has a
``uvx spruce-grove`` process in it and has not been closed out. Closed windows
are the interesting edge -- the process can linger after its terminal is gone,
so presence in ``ps`` alone is not liveness. We confirm the TTY device still
exists, which is the honest signal.

This module is deliberately **pure**: no TUI, no desktop knowledge, no network,
no writes. It reads four local sources and returns plain dataclasses so that
both consumers -- the ``/console`` TUI and the desktop shell, via
``--console --json`` -- share one implementation instead of drifting into two.

Sources, and what each one is authoritative for:

* ``ps`` output ................................. which processes exist, TTY, age
* ``/dev/ttysNNN`` existence .................... whether that terminal is still open
* ``~/.spruce_grove/tty_sessions/*.txt`` ........ TTY -> autosave session name
* ``~/.spruce_grove/autosaves/*_meta.json`` ..... title, agent-facing richness, last save
* ``~/.spruce_grove/terminal_sessions.json`` .... session name -> agent name

Every enrichment degrades to ``None`` rather than raising: ``ps`` column layout
varies by platform, and a session with an unreadable metadata file is still a
session worth showing.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from spruce_grove.config import AUTOSAVE_DIR, CACHE_DIR, STATE_DIR

#: How long to wait for ``ps``. It is a local process listing; if it stalls,
#: something is deeply wrong and returning "no sessions" beats hanging a UI.
_PS_TIMEOUT_SECONDS = 5.0

#: A grove process, by executable path or by the uvx argument.
_GROVE_MARKERS = ("spruce-grove", "spruce_grove")


@dataclass(frozen=True)
class LiveSession:
    """One running grove session, as seen from outside the process."""

    pid: int
    ppid: int
    #: TTY device name as ``ps`` reports it (``ttys000``), or None if piped.
    tty: Optional[str]
    #: True when ``/dev/<tty>`` still exists -- the terminal was not closed.
    terminal_open: bool
    #: ``terminal`` for a real TTY, ``embedded`` for a piped child (desktop).
    kind: str
    session_name: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    agent_name: Optional[str] = None
    cwd: Optional[str] = None
    message_count: Optional[int] = None
    total_tokens: Optional[int] = None
    last_autosave: Optional[str] = None
    uptime_seconds: Optional[int] = None

    @property
    def is_live(self) -> bool:
        """A session the user would call "open"."""
        return self.terminal_open or self.kind == "embedded"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["is_live"] = self.is_live
        return data


#: ``ps`` truncates etime by magnitude: ``MM:SS`` under an hour, ``HH:MM:SS``
#: under a day, ``D-HH:MM:SS`` beyond. All three must parse, or every
#: sub-hour session reports its age as unknown.
_ELAPSED_RE = re.compile(
    r"^(?:(?P<days>\d+)-)?(?:(?P<hours>\d+):)?(?P<minutes>\d+):(?P<seconds>\d+)$"
)


def _parse_elapsed(raw: str) -> Optional[int]:
    """Turn ``ps`` etime (``50:55``, ``19:30:31``, ``1-02:03:04``) into seconds."""
    match = _ELAPSED_RE.match(raw.strip())
    if not match:
        return None
    return (
        int(match.group("days") or 0) * 86400
        + int(match.group("hours") or 0) * 3600
        + int(match.group("minutes")) * 60
        + int(match.group("seconds"))
    )


def _grove_processes() -> List[Dict[str, Any]]:
    """List local processes that look like a running grove CLI.

    Columns are requested with ``=`` suffixes so ``ps`` emits them without
    headers and with stable spacing.
    """
    try:
        completed = subprocess.run(
            ["ps", "-Ao", "pid=,ppid=,tty=,etime=,stat=,command="],
            capture_output=True,
            text=True,
            timeout=_PS_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []

    found: List[Dict[str, Any]] = []
    for line in completed.stdout.splitlines():
        parts = line.split(None, 5)
        if len(parts) < 6:
            continue
        pid_raw, ppid_raw, tty_raw, etime_raw, _stat, command = parts
        if not any(marker in command for marker in _GROVE_MARKERS):
            continue
        # Only session owners count; the uvx wrapper is a parent, not a session.
        if not _is_session_owner(command):
            continue
        # Skip our own listing process and any grep that matched the pattern.
        if "ps -Ao" in command or command.lstrip().startswith("grep "):
            continue
        try:
            pid, ppid = int(pid_raw), int(ppid_raw)
        except ValueError:
            continue
        found.append(
            {
                "pid": pid,
                "ppid": ppid,
                "tty": None if tty_raw in ("??", "-") else tty_raw,
                "uptime_seconds": _parse_elapsed(etime_raw),
                "command": command,
            }
        )
    return found


#: The ``uvx`` launcher, e.g. ``/opt/homebrew/bin/uv tool uvx spruce-grove``.
#: It is a parent of the CLI, never the session itself.
_UVX_WRAPPER_MARKERS = ("uv tool uvx", "uvx spruce-grove")


def _is_the_cli_entrypoint(command: str) -> bool:
    """True when this process is the CLI itself, not the ``uvx`` wrapper.

    ``uvx spruce-grove`` spawns a child interpreter; we want the child, whose
    command names the tool's own entry-point script. The entry point is the
    only process that owns a session, so matching it is what identifies a
    session at all -- matching the wrapper would double-count every one.
    """
    return "bin/spruce-grove" in command


def _is_session_owner(command: str) -> bool:
    """True when this process could own a grove session.

    The interpreter that runs the entry point qualifies (its ``command`` is
    ``.../bin/python3 .../bin/spruce-grove``); the ``uvx`` wrapper does not.
    """
    if any(marker in command for marker in _UVX_WRAPPER_MARKERS):
        return False
    return _is_the_cli_entrypoint(command)


def _collapse_to_one_per_tty(processes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Keep a single process per TTY, preferring the CLI over its wrapper.

    Without a TTY (a piped child) each PID stands alone.
    """
    by_key: Dict[str, Dict[str, Any]] = {}
    for proc in processes:
        key = proc["tty"] or f"pid:{proc['pid']}"
        current = by_key.get(key)
        if current is None:
            by_key[key] = proc
            continue
        # Prefer the entry point; break ties by highest PID (the younger,
        # more specific process).
        if _is_the_cli_entrypoint(proc["command"]) and not _is_the_cli_entrypoint(
            current["command"]
        ):
            by_key[key] = proc
        elif _is_the_cli_entrypoint(proc["command"]) == _is_the_cli_entrypoint(
            current["command"]
        ):
            if proc["pid"] > current["pid"]:
                by_key[key] = proc
    return sorted(by_key.values(), key=lambda p: p["pid"])


def _terminal_is_open(tty: str) -> bool:
    """True when the TTY device still exists (terminal not closed)."""
    try:
        return os.path.exists(f"/dev/{tty}")
    except OSError:
        return False


def tty_session_key(tty: str) -> str:
    """Reproduce ``config._tty_session_path``'s key for a ``ps`` TTY name.

    ``config`` builds it from ``/dev/ttys000`` via ``replace("/", "_")`` then
    ``lstrip("_")``, so ``ttys000`` -> ``dev_ttys000``.
    """
    return tty.replace("/", "_").lstrip("_") if tty.startswith("/") else f"dev_{tty}"


def _read_tty_sessions() -> Dict[str, str]:
    """Map TTY device name (``ttys000``) -> autosave session name."""
    mapping: Dict[str, str] = {}
    directory = Path(CACHE_DIR) / "tty_sessions"
    try:
        entries = list(directory.glob("*.txt"))
    except OSError:
        return mapping
    for entry in entries:
        try:
            name = entry.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if not name:
            continue
        # dev_ttys000.txt -> ttys000
        mapping[entry.stem.removeprefix("dev_")] = name
    return mapping


def _read_session_agents() -> Dict[str, str]:
    """Map terminal-session id -> agent name.

    Keys are the *parent PID* of the terminal (see
    ``agent_manager.get_terminal_session_id``), a different identity space
    from TTYs and autosave names -- hence the separate lookup table.
    """
    path = Path(STATE_DIR) / "terminal_sessions.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def _pid_from_session_name(name: Optional[str]) -> Optional[int]:
    """Extract the PID suffix from an auto session name.

    Names are minted as ``auto_session_<date>_<time>_<us>_<pid>``, so the
    trailing field is the PID of the process that created the session. That is
    the *only* dependable link between a live process and its saved session:
    the ``tty_sessions`` pointer is best-effort and only refreshed on save,
    while the name carries its creator's identity permanently.
    """
    if not name:
        return None
    tail = name.rsplit("_", 1)[-1]
    return int(tail) if tail.isdigit() else None


def _read_autosave_meta() -> Dict[str, Dict[str, Any]]:
    """Map session name -> its ``_meta.json`` payload."""
    metas: Dict[str, Dict[str, Any]] = {}
    directory = Path(AUTOSAVE_DIR)
    try:
        entries = list(directory.glob("*_meta.json"))
    except OSError:
        return metas
    for entry in entries:
        try:
            data = json.loads(entry.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        name = data.get("session_name") or entry.name.removesuffix("_meta.json")
        metas[str(name)] = data
    return metas


def _newest_session_for_pid(
    pid: int, metas: Dict[str, Dict[str, Any]]
) -> Optional[str]:
    """Return the most recently saved session whose name claims ``pid``."""
    newest_name: Optional[str] = None
    newest_stamp = ""
    for name, meta in metas.items():
        if _pid_from_session_name(name) != pid:
            continue
        stamp = str(meta.get("timestamp") or "")
        if newest_name is None or stamp > newest_stamp:
            newest_name, newest_stamp = name, stamp
    return newest_name


def list_live_sessions(*, include_closed: bool = False) -> List[LiveSession]:
    """Return the grove sessions running on this machine.

    Args:
        include_closed: when False (default) only sessions whose terminal is
            still open (or that run embedded) are returned. True also yields
            orphans -- processes left behind by a closed window.
    """
    processes = _collapse_to_one_per_tty(_grove_processes())
    tty_sessions = _read_tty_sessions()
    agents = _read_session_agents()
    metas = _read_autosave_meta()

    sessions: List[LiveSession] = []
    for proc in processes:
        pid = proc["pid"]
        tty = proc["tty"]
        terminal_open = _terminal_is_open(tty) if tty else False
        kind = "terminal" if tty else "embedded"
        if kind == "embedded":
            # No TTY device to check; a live parent is the best available proof.
            terminal_open = True

        # Identify the session. PID embedded in the session name is the
        # dependable link; the per-TTY pointer is best-effort and only
        # refreshed when a session is saved, so it is the fallback.
        name = _newest_session_for_pid(pid, metas)
        if name is None and tty:
            candidate = tty_sessions.get(tty)
            if candidate in metas:
                name = candidate

        meta = metas.get(name) if name else None
        sessions.append(
            LiveSession(
                pid=pid,
                ppid=proc["ppid"],
                tty=tty,
                terminal_open=terminal_open,
                kind=kind,
                session_name=name,
                title=(meta or {}).get("title"),
                subtitle=(meta or {}).get("subtitle"),
                cwd=(meta or {}).get("scope_key"),
                message_count=(meta or {}).get("message_count"),
                total_tokens=(meta or {}).get("total_tokens"),
                last_autosave=(meta or {}).get("timestamp"),
                agent_name=agents.get(str(proc["ppid"])),
                uptime_seconds=proc["uptime_seconds"],
            )
        )

    kept = [s for s in sessions if include_closed or s.is_live]
    return sorted(kept, key=lambda s: s.pid)


def format_table(sessions: List[LiveSession]) -> str:
    """Render sessions as a fixed-width table for a terminal."""
    if not sessions:
        return "No live grove sessions."

    headers = ("PID", "TTY", "AGE", "STATE", "AGENT", "TITLE")
    rows: List[tuple] = []
    for s in sessions:
        age = _human_age(s.uptime_seconds)
        state = "live" if s.is_live else "ORPHAN"
        rows.append(
            (
                str(s.pid),
                s.tty or "(piped)",
                age,
                state,
                s.agent_name or "-",
                (s.title or s.session_name or "-")[:44],
            )
        )

    widths = [
        max(len(headers[i]), *(len(r[i]) for r in rows)) for i in range(len(headers))
    ]
    lines = [
        "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)).rstrip(),
        "  ".join("-" * widths[i] for i in range(len(headers))),
    ]
    lines += [
        "  ".join(r[i].ljust(widths[i]) for i in range(len(headers))).rstrip()
        for r in rows
    ]
    return "\n".join(lines)


def _human_age(seconds: Optional[int]) -> str:
    """Compact age: ``43m``, ``19h``, ``2d``."""
    if seconds is None:
        return "?"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"
