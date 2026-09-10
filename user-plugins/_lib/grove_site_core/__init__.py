"""grove_site_core -- shared scaffolder library for grove cohort plugins.

Not itself a plugin: a plain importable package consumers reach by adding
``~/.spruce_grove/lib`` to sys.path. Kept user-tier because multiple cohort
projects (barbershop, creatives) reuse it (sg-5al.3/ sg-5al.5 reuse contract).
"""

from grove_site_core.builder import build_site, render_checklist, render_index
from grove_site_core.tokens import TOKENS, base_css, wordmark

__all__ = [
    "TOKENS",
    "base_css",
    "wordmark",
    "build_site",
    "render_index",
    "render_checklist",
]
