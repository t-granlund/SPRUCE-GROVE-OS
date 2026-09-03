"""Registry integrity: components.json is the contract for natural-language
edits — it must be valid, complete, and consistent with the actual deck."""

ACCENT_VARIANTS = {"gold", "sky", "violet", "mint", "coral"}


class TestRegistrySchema:
    def test_required_top_level_keys(self, registry):
        for key in ("archetypes", "components", "acts", "locks", "prompt_guide"):
            assert key in registry, f"components.json missing '{key}'"

    def test_four_archetypes(self, registry):
        assert set(registry["archetypes"]) == {"statement", "split", "stage", "ledger"}
        for name, spec in registry["archetypes"].items():
            assert spec.get("purpose"), f"archetype {name} needs a purpose line"
            assert spec.get("rules"), f"archetype {name} needs rules"

    def test_component_categories(self, registry):
        cats = set(registry["components"])
        assert {"typography", "data-viz", "interactive", "structure", "labels", "media"} <= cats
        for cat, comps in registry["components"].items():
            for name, spec in comps.items():
                assert spec.get("class"), f"{cat}.{name} missing class"

    def test_prompt_guide_nonempty(self, registry):
        assert len(registry["prompt_guide"]) >= 5, "prompt guide must cover common edits"


class TestRegistryMatchesDeck:
    def test_registered_slides_have_their_component(self, slides, registry):
        for cat, comps in registry["components"].items():
            for name, spec in comps.items():
                if spec.get("implemented_as"):
                    continue  # documented alternate implementation
                for n in spec.get("slides", []):
                    found = slides[n - 1].select(f".{spec['class']}")
                    assert found, f"slide {n}: registry says .{spec['class']} lives here"

    def test_act_classes_match_registry(self, slides, registry):
        for act_id, act in registry["acts"].items():
            # per-slide classes win (acts with mid-act hue transitions);
            # otherwise the act-level class applies to every slide
            per_slide = act.get("slide_classes", {})
            cls = act.get("class", "").split(" / ")[0].strip()
            for n in act["slides"]:
                expected = per_slide.get(str(n), cls)
                if not expected.startswith("act-"):
                    continue
                section_classes = set(slides[n - 1].get("class", []))
                assert expected in section_classes, (
                    f"slide {n}: act {act_id} expects .{expected}"
                )

    def test_locks_documented(self, registry):
        for lock in ("chaplin_verbatim", "brand_tokens", "type_floor", "motion_budget", "factcheck"):
            assert lock in registry["locks"]

    def test_motion_slots_agree_with_deck(self, slides, registry):
        slots = [
            (name, spec.get("slides", []))
            for comps in registry["components"].values()
            for name, spec in comps.items()
            if spec.get("animated")
        ]
        assert len(slots) == 2, "motion budget: exactly 2 animated components"
        for name, sl in slots:
            assert sl, f"animated component {name} must name its slide"
