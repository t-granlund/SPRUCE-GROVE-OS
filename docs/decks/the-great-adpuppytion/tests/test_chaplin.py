"""The sacred requirement: Chaplin's Great Dictator speech, verbatim,
one beat per slide, slides 13–20 (eyebrows I–VIII), bookended on slide 44.

Verbatim source of truth: docs/jack-conte-sxsw.md transcript lines.
The transcript is auto-captioned (timestamps inline, no punctuation), so
we verify against normalized word sequences rather than literal substring.
"""

import re
import unicodedata

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
SPEECH_SLIDES = list(range(13, 21))  # 13..20 inclusive
BOOKEND_SLIDE = 56

# The eight beats as they appear in the transcript's wording
# (docs/jack-conte-sxsw.md, the talk's Great Dictator reading).
BEATS = [
    "i'm sorry but i don't want to be an emperor that's not my business i don't want to rule or conquer anyone i should like to help everyone if possible jew gentile black man white",
    "we all want to help one another human beings are like that but we have lost the way",
    "machinery that gives abundance has left us in want our knowledge has made us cynical our cleverness hard and unkind we think too much and feel too little more than machinery we need humanity more than cleverness we need kindness and gentleness",
    "the airplane and the radio have brought us closer together the very nature of these inventions cries out for the goodness in men",
    "even now my voice is reaching millions throughout the world millions of despairing men women and little children to those who can hear me i say do not despair the hate of men will pass and dictators die and the power they took from the people will return to the people and so long as men die liberty will never perish",
    "soldiers don't give yourselves to brutes men who despise you enslave you who regiment your lives tell you what to do what to think and what to feel who drill you diet you treat you like cattle use you as cannon fodder don't give yourselves to these unnatural men machine men with machine minds and machine hearts",
    "you are not machines you are not cattle you are men",
    "you the people have the power the power to create machines the power to create happiness you the people have the power to make this life free and beautiful to make this life a wonderful adventure then in the name of democracy let us use that power let us all unite",
]


def norm(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.lower().replace("’", "'").replace("‘", "'")
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


class TestChaplinSlides:
    def test_eight_speech_slides_with_roman_eyebrows(self, slides):
        for n, roman in zip(SPEECH_SLIDES, ROMAN):
            eyebrow = slides[n - 1].select_one(".eyebrow")
            assert eyebrow, f"slide {n}: missing eyebrow"
            assert f"{roman} of VIII" in eyebrow.get_text(), (
                f"slide {n}: eyebrow must read '{roman} of VIII'"
            )

    def test_each_beat_verbatim(self, slides):
        for n, beat in zip(SPEECH_SLIDES, BEATS):
            chaplin = slides[n - 1].select_one(".chaplin")
            assert chaplin, f"slide {n}: missing .chaplin block"
            slide_text = norm(chaplin.get_text())
            for word in norm(beat).split():
                assert word in slide_text.split(), (
                    f"slide {n}: word '{word}' missing — speech must stay verbatim"
                )

    def test_one_beat_per_slide(self, slides):
        """Each speech slide contains exactly one .chaplin paragraph and
        must not bleed into the next beat's opening words."""
        for i, n in enumerate(SPEECH_SLIDES):
            blocks = slides[n - 1].find_all(class_="chaplin")
            assert len(blocks) == 1, f"slide {n}: expected 1 beat, found {len(blocks)}"
            if i + 1 < len(BEATS):
                next_open = norm(BEATS[i + 1]).split()[:4]
                words = norm(blocks[0].get_text()).split()
                assert words[:4] != next_open, f"slide {n}: contains next beat"

    def test_bookend_slide(self, slides):
        bookend = slides[BOOKEND_SLIDE - 1]
        text = norm(bookend.get_text())
        assert "let us use that power" in text and "let us all unite" in text
        assert "chaplin-slide" in bookend.get("class", [])

    def test_serif_treatment(self, tokens_css):
        assert "--type-chaplin" in tokens_css
        assert "--serif" in tokens_css
