"""The grove spinner art must be sound, and the install must not overreach.

Two classes of bug matter here. First, bad art: a duplicate frame stalls the
animation for a tick, and an over-wide frame is truncated by the plugin and
looks broken. Second, a destructive install: this plugin writes into a file the
user owns and share with a third-party plugin, so it must never clobber an
existing entry, never clobber an unparseable file, and never overwrite a
spinner the user explicitly chose.

Every test runs against a throwaway config dir -- none touches the real
``~/.spruce_grove``.
"""

import json
from pathlib import Path

import pytest
from rich.cells import cell_len

from spruce_grove import spinner_art


class TestArt:
    def test_every_spinner_is_valid(self):
        assert spinner_art.validate_all() == {}

    def test_frames_are_braille(self):
        """Sporting ordinary text here would defeat the whole point."""
        for name, spec in spinner_art.SPINNERS.items():
            for frame in spec["frames"]:
                assert all(0x2800 <= ord(ch) <= 0x28FF for ch in frame), (
                    f"{name} has a non-braille frame: {frame!r}"
                )

    def test_no_duplicate_frames(self):
        """A repeated frame reads as a stall, not a beat."""
        for name, spec in spinner_art.SPINNERS.items():
            frames = spec["frames"]
            assert len(set(frames)) == len(frames), f"{name} repeats a frame"

    def test_frames_fit_the_plugins_width_cap(self):
        for name, spec in spinner_art.SPINNERS.items():
            for frame in spec["frames"]:
                assert cell_len(frame) <= spinner_art.MAX_FRAME_LEN, name

    def test_frames_are_one_width_within_a_spinner(self):
        """Uniform width keeps the text after the spinner from jittering."""
        for name, spec in spinner_art.SPINNERS.items():
            widths = {cell_len(f) for f in spec["frames"]}
            assert len(widths) == 1, f"{name} mixes widths {widths}"

    def test_sequences_are_animations(self):
        for name, spec in spinner_art.SPINNERS.items():
            assert len(spec["frames"]) >= 4, name

    def test_the_default_exists(self):
        assert spinner_art.DEFAULT_GROVE_SPINNER in spinner_art.SPINNERS

    def test_payload_shape_matches_the_plugin_contract(self):
        """The plugin reads frames/interval/description, and nothing else."""
        for name, spec in spinner_art.SPINNERS.items():
            assert set(spec) == {"frames", "interval", "description"}, name
            assert isinstance(spec["frames"], list)
            assert isinstance(spec["interval"], float)
            assert isinstance(spec["description"], str) and spec["description"]

    def test_validate_catches_a_stalled_sequence(self):
        """Guard the guard: validate must actually reject a bad sequence."""
        broken = list(spinner_art.GROVE_WAVE)
        broken[1] = broken[0]  # duplicate the first frame
        original = spinner_art.SPINNERS["grove"]["frames"]
        spinner_art.SPINNERS["grove"]["frames"] = broken
        try:
            problems = spinner_art.validate("grove")
            assert any("duplicate" in p for p in problems)
        finally:
            spinner_art.SPINNERS["grove"]["frames"] = original

    def test_validate_catches_an_overwide_frame(self):
        original = spinner_art.SPINNERS["groveGrowth"]["frames"]
        spinner_art.SPINNERS["groveGrowth"]["frames"] = ["\u2801" * 41, "\u2802"]
        try:
            assert any("max" in p for p in spinner_art.validate("groveGrowth"))
        finally:
            spinner_art.SPINNERS["groveGrowth"]["frames"] = original

    def test_validate_reports_unknown_names(self):
        assert spinner_art.validate("nope") == ["unknown spinner: nope"]


class TestCellConstruction:
    def test_blank_cell_is_u2800(self):
        assert spinner_art.cell() == "\u2800"

    def test_left_column_uses_dots_1237(self):
        assert [spinner_art.cell(r) for r in range(4)] == [
            "\u2801",
            "\u2802",
            "\u2804",
            "\u2840",
        ]

    def test_right_column_uses_dots_4568(self):
        assert [spinner_art.cell(None, r) for r in range(4)] == [
            "\u2808",
            "\u2810",
            "\u2820",
            "\u2880",
        ]

    def test_both_columns_combine(self):
        assert spinner_art.cell(0, 0) == "\u2809"


@pytest.fixture
def grove_home(tmp_path, monkeypatch):
    """Point the grove config dir at a temp path for the whole install."""
    monkeypatch.setattr("spruce_grove.config.CONFIG_DIR", str(tmp_path))
    monkeypatch.setattr("spruce_grove.config.CONFIG_FILE", str(tmp_path / "grove.cfg"))
    # get_value reads a cached parser; clear it so tmp_path takes effect.
    monkeypatch.setattr("spruce_grove.config._load_config", lambda: _EmptyConfig())
    return tmp_path


class _EmptyConfig:
    """A configparser stand-in that is always empty."""

    def get(self, section, key, fallback=None):
        return fallback

    def __contains__(self, item):
        return False


class _RecordingConfig(_EmptyConfig):
    def __init__(self):
        self.written = {}

    def get(self, section, key, fallback=None):
        return self.written.get(key, fallback)


class TestSeeding:
    """Writing into a file the user and a third-party plugin both own."""

    def test_first_run_seeds_both_spinners(self, grove_home, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        monkeypatch.setattr(gs, "spinners_file", lambda: grove_home / "spinners.json")
        assert gs.seed_spinner_art() is True
        data = json.loads((grove_home / "spinners.json").read_text())
        assert sorted(data) == ["grove", "groveGrowth"]

    def test_second_run_writes_nothing(self, grove_home, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        monkeypatch.setattr(gs, "spinners_file", lambda: grove_home / "spinners.json")
        gs.seed_spinner_art()
        assert gs.seed_spinner_art() is False

    def test_never_overwrites_an_existing_entry(self, grove_home, monkeypatch):
        """A user who tuned 'grove' keeps their tuning."""
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        path = grove_home / "spinners.json"
        path.write_text(json.dumps({"grove": {"frames": ["X"], "interval": 0.9}}))
        monkeypatch.setattr(gs, "spinners_file", lambda: path)

        gs.seed_spinner_art()
        data = json.loads(path.read_text())
        assert data["grove"] == {"frames": ["X"], "interval": 0.9}
        assert "groveGrowth" in data  # the missing one is still added

    def test_never_touches_foreign_entries(self, grove_home, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        path = grove_home / "spinners.json"
        path.write_text(json.dumps({"myOwn": {"frames": ["Z"], "interval": 0.2}}))
        monkeypatch.setattr(gs, "spinners_file", lambda: path)

        gs.seed_spinner_art()
        data = json.loads(path.read_text())
        assert data["myOwn"] == {"frames": ["Z"], "interval": 0.2}

    def test_corrupt_file_is_left_alone(self, grove_home, monkeypatch):
        """We must not clobber a file we cannot parse -- the user may be editing it."""
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        path = grove_home / "spinners.json"
        path.write_text("{not json")
        monkeypatch.setattr(gs, "spinners_file", lambda: path)

        assert gs.seed_spinner_art() is False
        assert path.read_text() == "{not json"

    def test_non_object_file_is_left_alone(self, grove_home, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        path = grove_home / "spinners.json"
        path.write_text("[1, 2, 3]")
        monkeypatch.setattr(gs, "spinners_file", lambda: path)

        assert gs.seed_spinner_art() is False
        assert path.read_text() == "[1, 2, 3]"


class TestSeating:
    """Choosing the default must not override a choice the user already made."""

    def test_seats_when_unset(self, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        written = {}
        monkeypatch.setattr("spruce_grove.config.get_value", lambda key: None)
        monkeypatch.setattr(
            "spruce_grove.config.set_value", lambda k, v: written.__setitem__(k, v)
        )
        assert gs.seat_grove_default() is True
        assert written == {"spinner_style": spinner_art.DEFAULT_GROVE_SPINNER}

    def test_does_not_override_an_explicit_choice(self, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        written = {}
        monkeypatch.setattr("spruce_grove.config.get_value", lambda key: "puppy")
        monkeypatch.setattr(
            "spruce_grove.config.set_value", lambda k, v: written.__setitem__(k, v)
        )
        assert gs.seat_grove_default() is False
        assert written == {}  # the user's pick stands

    def test_blank_value_counts_as_unset(self, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        written = {}
        monkeypatch.setattr("spruce_grove.config.get_value", lambda key: "   ")
        monkeypatch.setattr(
            "spruce_grove.config.set_value", lambda k, v: written.__setitem__(k, v)
        )
        assert gs.seat_grove_default() is True

    def test_config_failure_never_raises(self, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        def boom(key):
            raise RuntimeError("config exploded")

        monkeypatch.setattr("spruce_grove.config.get_value", boom)
        assert gs.seat_grove_default() is False


class TestInstall:
    def test_install_never_raises_when_seeding_fails(self, monkeypatch):
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        monkeypatch.setattr(
            gs, "seed_spinner_art", lambda: (_ for _ in ()).throw(OSError("nope"))
        )
        gs.install()  # must swallow

    def test_seeding_and_seating_are_independent(self, monkeypatch):
        """Seating is skipped when the user has a pick, but art still lands."""
        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        monkeypatch.setattr(gs, "seed_spinner_art", lambda: True)
        monkeypatch.setattr(gs, "seat_grove_default", lambda: False)
        gs.install()  # both paths reachable, neither raises


class TestSeamAgainstTheRealPlugin:
    """The install must land in the file the third-party plugin actually reads."""

    def _plugin_with_config(self, tmp_path, monkeypatch):
        """The plugin module, with its path constant derived from tmp_path.

        ``USER_SPINNERS_FILE`` is bound at import time, so in a full-suite run
        an earlier test may already have frozen it against the real home. A
        reload recomputes it from the config we just patched -- the faithful
        simulation of a fresh process, and the reason these tests must not
        compare against an already-imported constant.
        """
        import importlib

        monkeypatch.setattr("spruce_grove.config.CONFIG_DIR", str(tmp_path))

        import spruce_grove  # noqa: F401  (installs the code_puppy alias shim)
        from code_puppy_core_plugins.puppy_spinner import spinners as plugin

        return importlib.reload(plugin)

    def test_grove_seeds_the_file_the_plugin_loads(self, tmp_path, monkeypatch):
        plugin = self._plugin_with_config(tmp_path, monkeypatch)

        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        # Same file, discovered independently by each side.
        assert Path(plugin.USER_SPINNERS_FILE) == gs.spinners_file()

    def test_the_plugin_loads_the_seeded_art(self, tmp_path, monkeypatch):
        plugin = self._plugin_with_config(tmp_path, monkeypatch)

        from spruce_grove.plugins.grove_spinner import register_callbacks as gs

        monkeypatch.setattr(
            gs, "spinners_file", lambda: Path(plugin.USER_SPINNERS_FILE)
        )
        gs.seed_spinner_art()

        catalogue = plugin.get_catalogue()
        loaded = catalogue["groveGrowth"]
        assert loaded.source == "user"
        # The plugin normalises frames to a tuple; compare content, not type.
        assert list(loaded.frames) == spinner_art.GROVE_GROWTH
