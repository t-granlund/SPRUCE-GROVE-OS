"""Regression tests for the public-site generators.

The observatory's provenance chips and the field guide's author rendering
must agree on who "the grove" is. These tests pin the canonical grove-author
classification and the anonymized display form, so an anonymity regression
(like a divergent classifier copy mislabeling the grove's own commits as
upstream-synced) fails loudly here instead of shipping quietly to the
public observatory.
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "docs" / "field_guide_changelog.py"
UPDATES = REPO_ROOT / "pages-hub" / "generate-updates.py"

# generate-field-guide.py does `from field_guide_changelog import ...` at module
# scope; running it as a script puts docs/ on the path, loading it from here
# does not. Add it so the import resolves.
_DOCS = str(REPO_ROOT / "docs")
if _DOCS not in sys.path:
    sys.path.insert(0, _DOCS)


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


def test_field_guide_never_publishes_a_home_absolute_path():
    """The published field guide must not name the maintainer's account.

    data.js ships to sprucegrove.io/field-guide/. An absolute checkout path
    (`/Users/<name>/...`) put a username on the public page. The generator now
    emits a home-relative `~/...` form — assert that, and that no home root
    leaks in any rendered artifact.
    """
    import json

    gen = _load(REPO_ROOT / "docs" / "generate-field-guide.py", "gen_field_guide")
    shown = gen._display_repo_path(REPO_ROOT)
    assert shown.startswith("~/"), shown
    assert str(Path.home()) not in shown

    # And the committed data.js the site builds from carries no home root.
    data_js = (REPO_ROOT / "docs" / "field-guide" / "data.js").read_text(encoding="utf-8")
    for prefix in ("window.FIELD_GUIDE_DATA = ", "const FIELD_GUIDE_DATA = "):
        if data_js.startswith(prefix):
            data_js = data_js[len(prefix):]
            break
    data = json.loads(data_js.strip().rstrip(";\n"))
    repo_path = data.get("meta", {}).get("repoPath", "")
    assert "/Users/" not in repo_path and "/home/" not in repo_path, repo_path
    assert str(Path.home()) not in data_js
