"""grove_site_core.tokens -- granlund-grove design tokens as code.

Single source for the scaffolder's palette and base CSS. Ported from the
Spruce Grove pages-hub tokens.css (BB_ forest theme, WCAG 2.2 AAA on #0E130F).
Keep this identical to the hub so every cohort scaffold is visibly "the grove".
"""

TOKENS = {
    # surfaces
    "bg": "#0E130F",
    "bg_elev": "#121813",
    "bg_card": "#161D18",
    "panel": "#1B211C",
    # borders
    "line": "rgba(238,235,229,.10)",
    "line_2": "rgba(238,235,229,.18)",
    # text (AAA on bg)
    "t1": "#EEEBE2",
    "t2": "#D1CEC5",
    "t3": "#A5A699",
    # accents
    "cedar": "#E4AA71",
    "cedar_bright": "#F2A26A",
    "sage": "#98B79E",
    "mist": "#ECEBE5",
    "amber_soft": "#CAAB88",
    # forest decorative
    "spruce": "#1D3A2A",
    "spruce_deep": "#0E1F15",
    "moss": "#395F47",
    "bark": "#3D3026",
    # structure
    "radius": "14px",
    "radius_sm": "8px",
    "sans": '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    "mono": '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace',
    "display": '"Fraunces", Georgia, "Times New Roman", serif',
}

_WORDMARK = "gran\u00b7lund \u00b7 sv. \u00b7 spruce grove"

BASE_CSS = """/* grove_site_core.BASE_CSS -- generated from grove_site_core.tokens.TOKENS */
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: %(bg)s;
  background-image:
    radial-gradient(ellipse 80%% 60%% at 50%% -10%%, rgba(57,95,71,.35), transparent 60%%),
    radial-gradient(ellipse 60%% 40%% at 100%% 100%%, rgba(228,170,113,.08), transparent 70%%);
  color: %(t2)s;
  font-family: %(sans)s;
  font-size: 15px;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
a { color: %(cedar_bright)s; text-decoration: none; }
a:hover { text-decoration: underline; }
:focus-visible { outline: 2px solid %(cedar)s; outline-offset: 2px; border-radius: 4px; }
h1, h2, h3 { color: %(t1)s; font-family: %(display)s; letter-spacing: -0.02em; line-height: 1.2; }
code { font-family: %(mono)s; background: rgba(242,162,106,.10); color: %(cedar_bright)s; padding: 2px 6px; border-radius: 5px; font-size: .92em; }
::selection { background: %(cedar)s; color: %(bg)s; }
.wrap { max-width: 980px; margin: 0 auto; padding: 0 24px; }
.hero { padding: 72px 0 44px; }
.kicker {
  font-family: %(mono)s; font-size: 12px; letter-spacing: .16em; text-transform: uppercase;
  color: %(cedar)s; display: inline-block; border: 1px solid %(line_2)s;
  padding: 6px 14px; border-radius: 999px; margin-bottom: 20px;
}
.hero h1 { font-size: clamp(36px, 6vw, 58px); font-weight: 700; letter-spacing: -0.03em; }
.hero h1 em {
  font-style: normal;
  background: linear-gradient(92deg, %(cedar)s, %(cedar_bright)s, %(sage)s);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero p.lede { max-width: 640px; font-size: 18px; margin-top: 18px; }
section { padding: 40px 0; border-top: 1px solid %(line)s; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; }
.card {
  border: 1px solid %(line)s; border-radius: %(radius)s; background: %(bg_card)s; padding: 20px 22px;
}
.card .t { color: %(t1)s; font-weight: 600; margin-bottom: 6px; }
.card p { color: %(t3)s; font-size: 13.5px; margin: 0; }
.cta {
  display: inline-block; margin-top: 22px; padding: 12px 26px; border-radius: %(radius)s;
  background: %(spruce)s; border: 1px solid %(line_2)s; color: %(mist)s;
  font-weight: 600; font-size: 15px;
}
.cta:hover { background: %(moss)s; text-decoration: none; }
.check-list { list-style: none; margin: 0; padding: 0; }
.check-list li {
  border: 1px solid %(line)s; border-radius: %(radius)s; background: %(bg_card)s;
  padding: 14px 18px; margin-bottom: 10px; color: %(t2)s; font-size: 14px;
}
.check-list li .src { display: block; margin-top: 4px; font-family: %(mono)s; font-size: 11.5px; color: %(t3)s; }
footer { border-top: 1px solid %(line)s; padding: 32px 0 56px; color: %(t3)s; font-size: 13px; }
footer .wordmark { font-family: %(mono)s; font-size: 12px; letter-spacing: .12em; margin-top: 8px; display: block; }
""" % {
    "bg": TOKENS["bg"],
    "bg_card": TOKENS["bg_card"],
    "t1": TOKENS["t1"],
    "t2": TOKENS["t2"],
    "t3": TOKENS["t3"],
    "cedar": TOKENS["cedar"],
    "cedar_bright": TOKENS["cedar_bright"],
    "sage": TOKENS["sage"],
    "mist": TOKENS["mist"],
    "spruce": TOKENS["spruce"],
    "moss": TOKENS["moss"],
    "line": TOKENS["line"],
    "line_2": TOKENS["line_2"],
    "radius": TOKENS["radius"],
    "sans": TOKENS["sans"],
    "mono": TOKENS["mono"],
    "display": TOKENS["display"],
}


def base_css() -> str:
    """Return the shared scaffolder stylesheet (single string, no build step)."""
    return BASE_CSS


def wordmark() -> str:
    """Brand attribution footer: 'gran·lund · sv. · spruce grove'."""
    return _WORDMARK
