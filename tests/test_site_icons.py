"""Every published page must declare its icons, and every icon must resolve.

The failure this guards is quiet: a page can reference an icon with the wrong
relative prefix (nested pages need ``../assets/``, root pages ``./assets/``),
which renders fine locally and 404s on the real site. Checking presence alone
would have missed exactly that -- the first pass at this fix hardcoded
``./assets/`` and broke six nested pages -- so the resolution check is the
important half.
"""

import re
from pathlib import Path


SITE = Path(__file__).resolve().parent.parent / "_site"

FAVICON_RE = re.compile(r'<link\s+rel=["\']icon["\'][^>]*>', re.IGNORECASE)
APPLE_RE = re.compile(r'<link\s+rel=["\']apple-touch-icon["\'][^>]*>', re.IGNORECASE)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)


def _pages():
    return sorted(SITE.rglob("*.html"))


class TestIconsDeclared:
    def test_the_site_exists(self):
        assert _pages(), "no pages found under _site -- wrong path?"

    def test_every_favicon_page_declares_apple_touch(self):
        missing = [
            str(p.relative_to(SITE))
            for p in _pages()
            if FAVICON_RE.search(p.read_text(encoding="utf-8"))
            and not APPLE_RE.search(p.read_text(encoding="utf-8"))
        ]
        assert not missing, f"pages missing apple-touch-icon: {missing}"


class TestIconsResolve:
    def test_every_relative_icon_href_points_at_a_real_file(self):
        """The bug that a presence-only check would have passed."""
        broken = []
        for page in _pages():
            text = page.read_text(encoding="utf-8")
            for tag_re in (FAVICON_RE, APPLE_RE):
                for tag in tag_re.findall(text):
                    match = HREF_RE.search(tag)
                    if not match:
                        continue
                    href = match.group(1)
                    if href.startswith(("http://", "https://", "data:")):
                        continue  # a self-contained page may inline its icon
                    if not (page.parent / href).resolve().exists():
                        broken.append(f"{page.relative_to(SITE)} -> {href}")
        assert not broken, f"icon links that do not resolve: {broken}"

    def test_declared_icons_all_use_one_consistent_prefix(self):
        """A page that references its two icons inconsistently is the bug.

        The depth mistake shows up as the favicon and apple-touch icons on one
        page disagreeing about where ``assets`` lives -- which is exactly what
        a hardcoded prefix produced. Asserting a literal ``../`` would be
        wrong: ``_site/field-guide/`` is a self-contained sub-site with its own
        ``assets/`` directory, so a bare ``assets/`` is correct there. What
        must never happen is two icons on the same page disagreeing.
        """
        offenders = []
        for page in _pages():
            text = page.read_text(encoding="utf-8")
            prefixes = []
            for tag_re in (FAVICON_RE, APPLE_RE):
                for tag in tag_re.findall(text):
                    match = HREF_RE.search(tag)
                    if not match or match.group(1).startswith(("http", "data:")):
                        continue
                    prefixes.append(match.group(1).rsplit("/", 1)[0])
            if len(set(prefixes)) > 1:
                offenders.append(f"{page.relative_to(SITE)}: {sorted(set(prefixes))}")
        assert not offenders, f"pages with inconsistent icon prefixes: {offenders}"
