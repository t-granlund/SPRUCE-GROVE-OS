"""Regression tests for the Mockingbird transcriber's non-speech guards.

Context (2026-09-23): the desktop dictation loop — click record, talk, stop —
produced "thank you, thank you, thank you" on every take. Root cause: Whisper
was trained on YouTube captions and *hallucinates* stock phrases on
non-speech. The desktop carried a silent-but-happy result straight into the
prompt box, so the user saw "Thank you." as if they had said it.

Two independent guards now stand between the rig and the caller:

* a **peak-level gate** — a take that captured no audible signal never reaches
  Whisper at all; and
* a **hallucination check** on what came back — density (real speech here runs
  17-19 chars/sec; artifacts land under 2) plus a whole-line match against
  known stock tokens, gated so honest short utterances ("Thanks.") survive.

These tests pin both directions: non-speech is refused, real speech (including
speech that *contains* "thank you") still flows through.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# The plugin lives under user-plugins/; import it the way the loader does.
_PLUGIN_PARENT = Path(__file__).resolve().parents[2] / "user-plugins"
if str(_PLUGIN_PARENT) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_PARENT))

from mockingbird import transcriber  # noqa: E402


# ------------------------------- pure logic --------------------------------


class TestHallucinationHeuristic:
    """The density + artifact rule, exercised without any audio I/O."""

    @pytest.mark.parametrize(
        "text,duration",
        [
            ("Thank you.", 30.0),  # the reported bug, verbatim
            ("Thank you.", 5.0),
            ("Thanks for watching!", 12.0),
            ("you", 8.0),
            (".", 4.0),
            ("Please subscribe", 20.0),
        ],
    )
    def test_long_audio_with_stock_text_is_flagged(self, text, duration):
        assert transcriber._looks_like_hallucination(text, duration) is True

    def test_long_audio_with_a_single_short_token_is_flagged_by_density(self):
        # 5 s take yielding "Hi" = 0.4 chars/sec: not speech.
        assert transcriber._looks_like_hallucination("Hi", 5.0) is True

    @pytest.mark.parametrize(
        "text,duration",
        [
            ("This is the first recording in the Grove.", 2.17),  # measured real
            ("Thank you for reviewing this pull request.", 3.91),
            ("This is", 0.40),
        ],
    )
    def test_real_speech_is_never_flagged(self, text, duration):
        assert transcriber._looks_like_hallucination(text, duration) is False

    def test_speech_containing_thank_you_is_not_flagged(self):
        # The artifact rule is anchored to the WHOLE line: a sentence that
        # merely starts with "Thank you" is honest speech.
        text = "Thank you for reviewing this pull request.\nThe changes look correct."
        assert transcriber._looks_like_hallucination(text, 3.91) is False

    def test_short_honest_utterance_survives(self):
        # A real 0.8 s "Thanks." must not be thrown away as a hallucination.
        assert transcriber._looks_like_hallucination("Thanks.", 0.78) is False

    def test_short_take_with_stock_text_is_not_judged(self):
        # Too brief for the artifact rule to be trustworthy.
        assert transcriber._looks_like_hallucination("you", 0.5) is False


# ------------------------------ level gate ---------------------------------


class TestPeakGate:
    def test_silence_is_refused(self):
        assert (
            transcriber._peak_dbfs(_tone_or_silence("silence"))
            < transcriber._SILENCE_PEAK_DBFS
        )

    def test_speech_level_passes(self):
        assert (
            transcriber._peak_dbfs(_tone_or_silence("tone"))
            > transcriber._SILENCE_PEAK_DBFS
        )


def _tone_or_silence(kind: str) -> Path:
    """Synthesize a tiny fixture with ffmpeg (skips if ffmpeg is missing)."""
    import shutil
    import subprocess
    import tempfile

    ffmpeg = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    if not Path(ffmpeg).exists():
        pytest.skip("ffmpeg not available")
    out = Path(tempfile.mkdtemp(prefix="mb-test-")) / f"{kind}.wav"
    if kind == "silence":
        src = ["-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono", "-t", "1"]
    else:  # a loud tone at speech-like level
        src = [
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=1",
            "-af",
            "volume=0.3",
        ]
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", *src, str(out)],
        check=True,
        capture_output=True,
    )
    return out
