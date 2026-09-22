"""Regression tests for the public-site generators.

The observatory's provenance chips and the field guide's author rendering
must agree on who "the grove" is. These tests pin the canonical grove-author
classification and the anonymized display form, so an anonymity regression
(like a divergent classifier copy mislabeling the grove's own commits as
upstream-synced) fails loudly here instead of shipping quietly to the
public observatory.
"""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "docs" / "field_guide_changelog.py"
UPDATES = REPO_ROOT / "pages-hub" / "generate-updates.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_provenance_classifier_treats_the_grove_as_grove_grown():
    updates = _load(UPDATES, "generate_updates")
    # The anonymized display form AND the raw grove identities are grove.
    assert "prov gr" in updates._prov_chip("the grove")
    assert "prov gr" in updates._prov_chip("Tyler Granlund")
    assert "prov gr" in updates._prov_chip("tyler.granlund")
    # Everyone else — bots, upstream contributors, unknown — is upstream.
    assert "prov up" in updates._prov_chip("github-actions[bot]")
    assert "prov up" in updates._prov_chip("")
    assert "prov up" in updates._prov_chip(None)


def test_display_author_anonymizes_every_grove_identity():
    changelog = _load(CHANGELOG, "field_guide_changelog")
    for author in changelog.GROVE_AUTHORS:
        assert changelog._display_author(author) == changelog.GROVE_DISPLAY_NAME
    # Upstream contributors and bots keep their names: credit, not exposure.
    assert changelog._display_author("github-actions[bot]") == "github-actions[bot]"


def test_both_generators_classify_from_one_canonical_set():
    """Same members — the provenance chip imports, it does not copy."""
    changelog = _load(CHANGELOG, "field_guide_changelog_canonical")
    updates = _load(UPDATES, "generate_updates_canonical")
    assert updates.GROVE_AUTHORS == changelog.GROVE_AUTHORS
    # And the display form the changelog emits is recognized by the chips.
    assert updates._is_grove_author(changelog.GROVE_DISPLAY_NAME)
