"""The live-session scanner must be right, because a console acts on its output.

These tests pin the four behaviours that were actually wrong on first draft:
``ps`` elapses under an hour are ``MM:SS`` (not ``HH:MM:SS``); the ``uvx``
wrapper is a parent, not a session; a saved session is identified by the PID
embedded in its name, with the per-TTY pointer as fallback; and every
enrichment degrades to ``None`` instead of raising.

Nothing here touches the real machine state: ``ps`` output, the TTY check and
every directory are injected.
"""

import json
import subprocess
from pathlib import Path

import pytest

from spruce_grove import live_sessions as ls

# --- ps output -------------------------------------------------------------

#: A realistic listing: the uvx wrapper AND its child for one terminal, so any
#: failure to exclude the wrapper shows up as a duplicate session.
PS_OUTPUT = """\
  1529  1521 ttys001 19:30:31 S+   /Users/t/.local/share/uv/tools/spruce-grove/bin/python3 /Users/t/.local/share/uv/tools/spruce-grove/bin/spruce-grove
  1528  1520 ttys001 19:30:32 S+   /opt/homebrew/bin/uv tool uvx spruce-grove
 53729 53728 ttys003    52:55 S+   /Users/t/.local/share/uv/tools/spruce-grove/bin/python3 /Users/t/.local/share/uv/tools/spruce-grove/bin/spruce-grove
 53728 53727 ttys003    52:55 S+   /opt/homebrew/bin/uv tool uvx spruce-grove
 54067 54066 ttys004 51:10.00 S+   /Users/t/.local/share/uv/tools/spruce-grove/bin/python3 /Users/t/.local/share/uv/tools/spruce-grove/bin/spruce-grove
 99999     1 ttys009  1-02:03:04 S  /Users/t/.local/share/uv/tools/spruce-grove/bin/spruce-grove
   777   776 ??       10:00 S    /Users/t/.local/share/uv/tools/spruce-grove/bin/spruce-grove --console --json
"""


def _fake_ps(monkeypatch, output=PS_OUTPUT):
    monkeypatch.setattr(
        ls.subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(a, 0, output, ""),
    )


@pytest.fixture
def grove_dirs(tmp_path, monkeypatch):
    """Point every data directory at tmp_path and open all TTYs by default."""
    cache, state = tmp_path / "cache", tmp_path / "state"
    autosaves = cache / "autosaves"
    (cache / "tty_sessions").mkdir(parents=True)
    state.mkdir(parents=True)
    autosaves.mkdir(parents=True)
    monkeypatch.setattr(ls, "CACHE_DIR", str(cache))
    monkeypatch.setattr(ls, "STATE_DIR", str(state))
    monkeypatch.setattr(ls, "AUTOSAVE_DIR", str(autosaves))
    monkeypatch.setattr(ls, "_terminal_is_open", lambda tty: True)
    _fake_ps(monkeypatch)
    return {"cache": cache, "state": state, "autosaves": autosaves}


def _write_meta(autosaves: Path, name: str, **fields) -> None:
    payload = {"session_name": name, **fields}
    (autosaves / f"{name}_meta.json").write_text(json.dumps(payload), encoding="utf-8")


# --- elapsed parsing -------------------------------------------------------


class TestElapsedParsing:
    """``ps`` elapses three shapes; the first draft only understood one."""

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("52:55", 52 * 60 + 55),  # under an hour -- MM:SS
            ("19:30:31", 19 * 3600 + 30 * 60 + 31),  # under a day -- HH:MM:SS
            ("1-02:03:04", 86400 + 2 * 3600 + 3 * 60 + 4),  # over a day
            ("00:00", 0),
        ],
    )
    def test_all_ps_shapes_parse(self, raw, expected):
        assert ls._parse_elapsed(raw) == expected

    def test_unparseable_is_none_not_an_exception(self):
        assert ls._parse_elapsed("garbage") is None
        assert ls._parse_elapsed("") is None


# --- session identification ------------------------------------------------


class TestProcessSelection:
    def test_uvx_wrapper_is_not_a_session(self, grove_dirs):
        """Matching the wrapper would double-count every session."""
        sessions = ls.list_live_sessions()
        ttys = [s.tty for s in sessions]
        assert ttys.count("ttys001") == 1
        assert 1528 not in [s.pid for s in sessions]  # the wrapper
        assert 1529 in [s.pid for s in sessions]  # the CLI entry point

    def test_each_terminal_yields_exactly_one_session(self, grove_dirs):
        sessions = ls.list_live_sessions()
        terminals = [s for s in sessions if s.kind == "terminal"]
        assert {s.tty for s in terminals} == {
            "ttys001",
            "ttys003",
            "ttys004",
            "ttys009",
        }
        assert len(terminals) == 4  # one per terminal, never the wrapper too

    def test_piped_process_is_embedded(self, grove_dirs):
        embedded = [s for s in ls.list_live_sessions() if s.kind == "embedded"]
        assert [s.pid for s in embedded] == [777]
        assert embedded[0].tty is None
        assert embedded[0].is_live is True  # no TTY to lose


class TestSessionIdentity:
    def test_pid_suffix_in_the_session_name_is_the_link(self, grove_dirs):
        _write_meta(
            grove_dirs["autosaves"],
            "auto_session_20260922_160139_419602_1529",
            title="Desktop App QA Round Two",
            scope_key="/Users/t/desktop",
            message_count=362,
        )
        session = next(s for s in ls.list_live_sessions() if s.pid == 1529)
        assert session.session_name == "auto_session_20260922_160139_419602_1529"
        assert session.title == "Desktop App QA Round Two"
        assert session.cwd == "/Users/t/desktop"
        assert session.message_count == 362

    def test_newest_wins_when_a_pid_recycled(self, grove_dirs):
        _write_meta(
            grove_dirs["autosaves"],
            "auto_session_20260101_000000_000000_1529",
            title="Old",
            timestamp="2026-01-01T00:00:00",
        )
        _write_meta(
            grove_dirs["autosaves"],
            "auto_session_20260922_160139_419602_1529",
            title="New",
            timestamp="2026-09-22T16:01:39",
        )
        session = next(s for s in ls.list_live_sessions() if s.pid == 1529)
        assert session.title == "New"

    def test_tty_pointer_is_the_fallback(self, grove_dirs):
        """A session whose name carries a dead PID is still found via its TTY."""
        _write_meta(
            grove_dirs["autosaves"],
            "auto_session_20260922_180513_178375_1666",
            title="Complete Gratsy IT Ops application",
        )
        (grove_dirs["cache"] / "tty_sessions" / "dev_ttys004.txt").write_text(
            "auto_session_20260922_180513_178375_1666", encoding="utf-8"
        )
        session = next(s for s in ls.list_live_sessions() if s.pid == 54067)
        assert session.title == "Complete Gratsy IT Ops application"

    def test_unmatched_session_fields_are_none(self, grove_dirs):
        session = next(s for s in ls.list_live_sessions() if s.pid == 53729)
        assert session.session_name is None
        assert session.title is None
        assert session.is_live is True  # still reported, just unexplained


# --- liveness --------------------------------------------------------------


class TestLiveness:
    def test_closed_terminal_marks_orphan_and_is_hidden_by_default(
        self, grove_dirs, monkeypatch
    ):
        monkeypatch.setattr(ls, "_terminal_is_open", lambda tty: tty != "ttys009")
        assert 99999 not in [s.pid for s in ls.list_live_sessions()]

        orphan = next(
            s for s in ls.list_live_sessions(include_closed=True) if s.pid == 99999
        )
        assert orphan.terminal_open is False
        assert orphan.is_live is False

    def test_all_open_terminals_are_live(self, grove_dirs):
        assert all(s.is_live for s in ls.list_live_sessions())


# --- degradation -----------------------------------------------------------


class TestDegradation:
    """A UI must never die because one file was unreadable."""

    def test_corrupt_meta_does_not_raise(self, grove_dirs):
        (grove_dirs["autosaves"] / "auto_session_x_1529_meta.json").write_text(
            "{not json", encoding="utf-8"
        )
        assert ls.list_live_sessions()  # still returns sessions

    def test_missing_directories_do_not_raise(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ls, "CACHE_DIR", str(tmp_path / "nope"))
        monkeypatch.setattr(ls, "STATE_DIR", str(tmp_path / "nope2"))
        monkeypatch.setattr(ls, "AUTOSAVE_DIR", str(tmp_path / "nope3"))
        monkeypatch.setattr(ls, "_terminal_is_open", lambda tty: True)
        _fake_ps(monkeypatch)
        assert len(ls.list_live_sessions()) == 5  # all processes, no metadata

    def test_ps_failure_yields_no_sessions(self, monkeypatch):
        def boom(*a, **k):
            raise OSError("ps is gone")

        monkeypatch.setattr(ls.subprocess, "run", boom)
        assert ls.list_live_sessions() == []

    def test_corrupt_terminal_sessions_json_is_ignored(self, grove_dirs):
        (grove_dirs["state"] / "terminal_sessions.json").write_text(
            "not json at all", encoding="utf-8"
        )
        assert ls._read_session_agents() == {}


# --- agent names -----------------------------------------------------------


class TestAgentNames:
    def test_agent_resolved_by_parent_pid(self, grove_dirs):
        """terminal_sessions.json is keyed by PPID, a separate identity space."""
        (grove_dirs["state"] / "terminal_sessions.json").write_text(
            json.dumps({"1521": "solutions-architect"}), encoding="utf-8"
        )
        session = next(s for s in ls.list_live_sessions() if s.pid == 1529)
        assert session.agent_name == "solutions-architect"


# --- rendering -------------------------------------------------------------


class TestRendering:
    def test_table_lists_every_session(self, grove_dirs):
        _write_meta(
            grove_dirs["autosaves"],
            "auto_session_20260922_160139_419602_1529",
            title="Desktop App QA Round Two",
        )
        sessions = ls.list_live_sessions()
        table = ls.format_table(sessions)
        assert "Desktop App QA Round Two" in table
        assert "ttys001" in table
        # header + rule + one row per session
        assert table.count("\n") == 1 + len(sessions)
        # ...and nothing was dropped in rendering.
        assert all(str(s.pid) in table for s in sessions)

    def test_empty_message(self):
        assert ls.format_table([]) == "No live grove sessions."

    def test_orphan_state_is_visible(self):
        orphan = ls.LiveSession(
            pid=1, ppid=0, tty="ttys099", terminal_open=False, kind="terminal"
        )
        assert "ORPHAN" in ls.format_table([orphan])

    def test_dict_payload_exposes_is_live(self):
        session = ls.LiveSession(
            pid=1, ppid=0, tty="ttys000", terminal_open=True, kind="terminal"
        )
        assert session.to_dict()["is_live"] is True


# --- CLI verb (--console) --------------------------------------------------


class TestConsoleVerb:
    """`--console` must be a fast, headless read -- no agent, no API keys."""

    def _run(self, argv, monkeypatch):
        import asyncio
        import sys

        from spruce_grove.cli_runner import main

        monkeypatch.setattr(sys, "argv", ["spruce-grove", *argv])
        return asyncio.run(main())

    def test_human_table_exits_zero(self, grove_dirs, monkeypatch, capsys):
        assert self._run(["--console"], monkeypatch) == 0
        out = capsys.readouterr().out
        assert "ttys001" in out

    def test_json_flag_emits_the_contract(self, grove_dirs, monkeypatch, capsys):
        assert self._run(["--console", "--json"], monkeypatch) == 0
        payload = json.loads(capsys.readouterr().out)
        assert isinstance(payload, list) and payload
        # The documented keys are a contract for the desktop shell.
        assert {"pid", "tty", "is_live", "title", "session_name"} <= set(payload[0])

    def test_default_hides_orphans_and_all_reveals_them(
        self, grove_dirs, monkeypatch, capsys
    ):
        monkeypatch.setattr(ls, "_terminal_is_open", lambda tty: tty != "ttys009")
        assert self._run(["--console", "--json"], monkeypatch) == 0
        assert 99999 not in [s["pid"] for s in json.loads(capsys.readouterr().out)]

        assert self._run(["--console", "--json", "--all"], monkeypatch) == 0
        orphans = [s for s in json.loads(capsys.readouterr().out) if s["pid"] == 99999]
        assert orphans and orphans[0]["is_live"] is False

    def test_console_is_reachable_without_api_keys(self, grove_dirs, monkeypatch):
        """Proves it short-circuits before the agent/model stack loads."""
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(key, raising=False)
        monkeypatch.setattr(
            "spruce_grove.config.get_api_key",
            lambda *a, **k: (_ for _ in ()).throw(
                AssertionError("--console must not resolve credentials")
            ),
        )
        assert self._run(["--console"], monkeypatch) == 0
