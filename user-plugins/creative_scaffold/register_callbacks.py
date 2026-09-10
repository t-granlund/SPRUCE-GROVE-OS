"""creative_scaffold -- grove cohort scaffolds for the creative tier (sg-5al.5).

/creative-scaffold [fpv|artisans|all] builds grove-styled site starters into
./site-out/<profile>/ using the SHARED grove_site_core (builder + cli) -- the
same rendering path the barber scaffold (sg-5al.3) rides. Data differs; code
doesn't. No network, writes only in ./site-out/.

Profiles:
- fpv:      FPV drone cinematography portfolio (showreel embed + lightbox gallery)
- artisans: handmade-goods storefront starter (the squiggle-cutters pattern)
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

_LIB = Path.home() / ".spruce_grove" / "lib"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

from grove_site_core.cli import register_scaffold_command  # noqa: E402 -- sys.path bootstrap above is the plugin-lib contract

_SVG_COLORS = ["#1D3A2A", "#395F47", "#E4AA71", "#98B79E"]


def _fpo_tile(label: str, color: str) -> str:
    """Inline SVG data URI placeholder tile (no network fetch, clearly fake)."""
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='480' height='270'>"
        f"<rect width='100%' height='100%' fill='{color}'/>"
        f"<text x='50%' y='52%' font-family='monospace' font-size='28' fill='#0E130F' "
        f"text-anchor='middle'>FPO {label}</text></svg>"
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


PROFILES: dict[str, dict] = {
    "fpv": {
        "brand_name": "Full Send Aerial",
        "tagline": "fpv cinematography \N{DOT OPERATOR} through the trees",
        "hero_copy": (
            "First-person drone work for people who do things at speed. Athlete chases, "
            "property flythroughs, one-take storytelling most rigs physically cannot do. "
            "If it moves fast, we can follow it faster."
        ),
        "services": [
            {
                "title": "Athlete Chase",
                "desc": "Follow-cam through terrain at sprint speed. Bikes, boards, runners, anything brave.",
            },
            {
                "title": "Property Flythrough",
                "desc": "One-take interior/exterior transitions. Real estate and venues that sell themselves.",
            },
            {
                "title": "Event Coverage",
                "desc": "Cinematic sweeps and crowd energy -- the aftermovie your event deserves.",
            },
            {
                "title": "Brand One-Takes",
                "desc": "The continuous-shot flex: product reveals, shop walkthroughs, launch clips.",
            },
        ],
        "media": {
            "video_url": "https://www.youtube-nocookie.com/embed/REPLACE-WITH-SHOWREEL",
            "video_label": "Showreel (placeholder -- replace ID before launch)",
            "gallery": [
                {
                    "src": _fpo_tile("TREE LINE", _SVG_COLORS[1]),
                    "alt": "FPO: threading a tree line at speed",
                },
                {
                    "src": _fpo_tile("RIDGE", _SVG_COLORS[0]),
                    "alt": "FPO: ridge dive at golden hour",
                },
                {
                    "src": _fpo_tile("SPRINT", _SVG_COLORS[2]),
                    "alt": "FPO: sprint follow on singletrack",
                },
            ],
        },
        "checklist": [
            {
                "item": "Replace the showreel embed placeholder with the real video ID.",
                "source": "owner showreel; youtube-nocookie embed",
            },
            {
                "item": "Confirm commercial drone ops compliance: FAA Part 107 certificate current, operations documented under its rules.",
                "source": "https://www.faa.gov/uas/commercial_operators",
            },
            {
                "item": "Swap all FPO tiles for graded 4K stills from real shoots.",
                "source": "Anderson's flight log exports",
            },
            {
                "item": "Add insurance certificate reference before any paid booking page goes live.",
                "source": "liability policy broker of record",
            },
            {
                "item": "Permission/location policy page: private property consent + no-fly-zone discipline.",
                "source": "https://www.faa.gov/uas",
            },
        ],
        "footer_note": "Adrenaline responsibly sourced. Film permit-friendly, Part 107-aware.",
    },
    "artisans": {
        "brand_name": "The Squiggle Shop",
        "tagline": "handmade, honest, and slightly crooked on purpose",
        "hero_copy": (
            "Wood, vinyl, and whatever the scroll saw dreams about tonight. Handmade "
            "goods from the grove -- every piece a little different, because machines "
            "are the ones that repeat themselves."
        ),
        "services": [
            {
                "title": "Squiggle Cuts",
                "desc": "Flowing organic cuts in plywood and acrylic -- wall pieces, plant stakes, shelf critters.",
            },
            {
                "title": "Custom Commissions",
                "desc": "Your idea, my scroll saw. Names, logos, wedding gifts, shop signs.",
            },
            {
                "title": "Market Drops",
                "desc": "Limited runs for local markets and the occasional pop-up. First come, first loved.",
            },
        ],
        "media": {
            "gallery": [
                {
                    "src": _fpo_tile("SQUIGGLE", _SVG_COLORS[3]),
                    "alt": "FPO: squiggle wall piece in maple",
                },
                {
                    "src": _fpo_tile("COMMISSION", _SVG_COLORS[2]),
                    "alt": "FPO: custom name sign, cursive Baltic birch",
                },
                {
                    "src": _fpo_tile("MARKET", _SVG_COLORS[0]),
                    "alt": "FPO: market table with fresh cuts",
                },
            ],
        },
        "checklist": [
            {
                "item": "Swap FPO tiles for real product photography (natural light, same angle set).",
                "source": "maker bench + daylight window",
            },
            {
                "item": "Decide the commission intake channel (form service or mailto) and publish the policy.",
                "source": "no backend per design",
            },
            {
                "item": "Set sales-tax nexus facts straight: craft-market and online sales may each trigger AR rules.",
                "source": "https://www.dfa.arkansas.gov/excise-tax/sales-use-tax/",
            },
            {
                "item": "Photograph 3 before/after commission stories for the grid (trust beats polish).",
                "source": "customer permission required",
            },
        ],
        "footer_note": "Made by hand in NWA. Slightly crooked, wholly honest.",
    },
}

register_scaffold_command(
    name="creative-scaffold",
    profiles=PROFILES,
    outroot=Path.cwd() / "site-out",
    help_line="Creative cohort site starters (FPV drone portfolio, artisan shop) into ./site-out/ -- profile data over shared grove core",
    panel_title="creative cohort scaffolds",
)
