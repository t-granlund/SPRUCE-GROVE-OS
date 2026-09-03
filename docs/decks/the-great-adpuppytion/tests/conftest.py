"""Shared fixtures: parsed deck HTML, CSS sources, registry, slide model."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

DECK = Path(__file__).resolve().parent.parent
REPO_DOCS = DECK.parent.parent  # code_puppy/docs


@pytest.fixture(scope="session")
def deck_dir():
    return DECK


@pytest.fixture(scope="session")
def soup():
    return BeautifulSoup((DECK / "index.html").read_text(), "html.parser")


@pytest.fixture(scope="session")
def slides(soup):
    """Top-level <section> elements inside .slides, in order (1-indexed)."""
    return soup.select(".slides > section")


@pytest.fixture(scope="session")
def theme_css():
    return (DECK / "theme.css").read_text()


@pytest.fixture(scope="session")
def tokens_css():
    return (DECK / "tokens.css").read_text()


@pytest.fixture(scope="session")
def registry():
    import json

    return json.loads((DECK / "components.json").read_text())


@pytest.fixture(scope="session")
def transcript():
    return (REPO_DOCS / "jack-conte-sxsw.md").read_text()
