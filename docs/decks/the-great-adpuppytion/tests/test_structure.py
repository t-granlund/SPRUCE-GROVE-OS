"""Structural invariants: slide count, archetype legality, single-hue rule,
motion budget, and component placement per components.json registry."""

import re

ACCENT_CLASSES = {"gold", "sky", "mint", "violet", "coral"}
ARCHETYPE_CLASSES = {"statement", "split", "stage"}

# Sanctioned multi-hue slides: panic rail (8), charter (55), personas (37),
# stat walls (28, 33, 43, 47, 52 — each stat carries its own accent by design),
# the stacks (38 three-pill, 46 pack ladder), MVV closer (53 — four-hue sequence)
MULTI_HUE_ALLOWED = {8, 28, 33, 37, 38, 43, 46, 47, 52, 53, 55}
# Sanctioned animated moments (motion budget = 2)
ANIMATED_ALLOWED = {23, 40}


def slide_num(idx):
    return idx + 1


def classes_of(section):
    return set(section.get("class", []))


def accent_hues(section):
    """Distinct accent-hue utility classes used anywhere in the slide."""
    hues = set()
    for el in section.find_all(True):
        hues |= classes_of(el) & ACCENT_CLASSES
    # act scoping on the section counts as the slide's hue
    act = classes_of(section) & {"act-sky", "act-coral", "act-mint", "act-violet"}
    if act:
        hues.add(act.pop().replace("act-", ""))
    elif not act:
        hues.add("gold")  # default act hue
    return hues


class TestDeckShape:
    def test_slide_count(self, slides, registry):
        assert len(slides) == 57
        reg_max = max(s for act in registry["acts"].values() for s in act["slides"])
        assert reg_max == 57, "registry acts must cover all 57 slides"

    def test_registry_covers_every_slide(self, slides, registry):
        covered = {s for act in registry["acts"].values() for s in act["slides"]}
        assert covered == set(range(1, 58))

    def test_reveal_config_unchanged(self, soup):
        script = soup.find_all("script")[-1].string
        for key in ("hash: true", "autoAnimate: true", "width: 1440", "height: 810"):
            assert key in script


class TestArchetypes:
    def test_every_statement_is_minimal(self, slides):
        """STATEMENT slides: no tables, no persona/stackrow components."""
        for i, s in enumerate(slides, 1):
            if "statement" not in classes_of(s):
                continue
            assert not s.find("table"), f"slide {i}: statement contains a table"
            assert not s.select(".persona, .stackrow, .rail, .termmock"), (
                f"slide {i}: statement contains stage/ledger components"
            )

    def test_images_only_in_split_or_stage(self, slides):
        # slide 50 exception: the brand logo on a STATEMENT is the Code-Puppy
        # era reveal — a typographic object, not an image (no .duo by design)
        LOGO_EXCEPTION = {50}
        for i, s in enumerate(slides, 1):
            imgs = s.find_all("img")
            if not imgs:
                continue
            if i in LOGO_EXCEPTION:
                assert all("code-puppy-" in (im.get("src") or "") for im in imgs)
                continue
            assert classes_of(s) & {"split", "stage"} or s.select(".split"), (
                f"slide {i}: image outside SPLIT/STAGE archetype"
            )
            for img in imgs:
                assert img.find_parent(class_="duo"), (
                    f"slide {i}: image missing .duo duotone treatment"
                )

    def test_tables_only_in_ledger_slides(self, slides, registry):
        ledger_slides = {39, 55}  # the two sanctioned LEDGER uses
        for i, s in enumerate(slides, 1):
            if s.find("table"):
                assert i in ledger_slides, f"slide {i}: table outside LEDGER"

    def test_motion_budget(self, slides):
        """Exactly two animated moments: sine draw + terminal type-in."""
        animated = set()
        for i, s in enumerate(slides, 1):
            if s.select(".sinewrap .draw") or s.select(".termmock .line"):
                animated.add(i)
        assert animated == ANIMATED_ALLOWED


class TestSingleHue:
    def test_one_accent_hue_per_slide(self, slides):
        """Slides use at most 2 accent hues (act color + one deliberate
        cross-accent), unless sanctioned multi-hue (rail/charter/personas)."""
        for i, s in enumerate(slides, 1):
            if i in MULTI_HUE_ALLOWED:
                continue
            hues = accent_hues(s)
            assert len(hues) <= 2, f"slide {i}: {sorted(hues)} hues — check DESIGN.md single-hue rule"


class TestEyebrows:
    def test_eyebrows_use_micro_only(self, slides):
        """Eyebrows and attributions are the only --type-micro consumers."""
        for i, s in enumerate(slides, 1):
            for el in s.select(".eyebrow, .attr, .lbl"):
                style = el.get("style", "")
                m = re.search(r"font-size:\s*([\d.]+)em", style)
                if m:
                    assert float(m.group(1)) >= 0.52, f"slide {i}: eyebrow below micro floor"
