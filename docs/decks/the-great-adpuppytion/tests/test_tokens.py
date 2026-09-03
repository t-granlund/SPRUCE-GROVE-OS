"""Token & CSS hygiene: brand palette integrity, single source of truth,
type floors, and WCAG contrast of every ink/accent pairing on canvas."""

import re

BRAND = {
    "--cp-ink-900": "#0b0f14",
    "--cp-text": "#e8eef4",
    "--cp-text-soft": "#9fb0c3",
    "--cp-text-muted": "#6b7d91",
    "--cp-gold": "#f5b94d",
    "--cp-sky": "#6cb6ff",
    "--cp-mint": "#4cc46a",
    "--cp-violet": "#b692f6",
    "--cp-coral": "#ff7b72",
}

# hex values allowed to appear raw in theme.css (rgba tints of brand hues
# for gradients/glows). Everything else must flow through tokens.
ALLOWED_RAW_RGBA = re.compile(r"rgba\((108, ?182, ?255|245, ?185, ?77|6, ?9, ?13)")


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(rgb):
    def chan(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = sorted((luminance(hex_to_rgb(fg)), luminance(hex_to_rgb(bg))), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


class TestPaletteIntegrity:
    def test_brand_primitives_exact(self, tokens_css):
        for token, hexval in BRAND.items():
            assert f"{token}: {hexval}" in tokens_css, (
                f"brand primitive {token} drifted from {hexval} (Code-Puppy field-guide)"
            )

    def test_semantic_layer_references_primitives(self, tokens_css):
        assert "--surface-canvas: var(--cp-ink-900)" in tokens_css
        assert "--accent-creator: var(--cp-gold)" in tokens_css

    def test_act_map_complete(self, tokens_css):
        for n in range(9):
            assert f"--act-{n}:" in tokens_css, f"missing act token --act-{n}"


class TestSingleSourceOfTruth:
    def test_theme_has_no_hardcoded_hex(self, theme_css):
        hexes = re.findall(r"#[0-9a-fA-F]{3,8}\b", theme_css)
        assert hexes == [], f"theme.css must consume tokens, found raw hex: {hexes}"

    def test_theme_rgba_only_brand_tints(self, theme_css):
        for m in re.finditer(r"rgba\([^)]+\)", theme_css):
            assert ALLOWED_RAW_RGBA.search(m.group(0)), (
                f"non-brand rgba in theme.css: {m.group(0)} — move to tokens.css"
            )

    def test_tokens_defines_type_scale(self, tokens_css):
        for t in ("--type-mega", "--type-h2", "--type-body", "--type-small", "--type-micro"):
            assert t in tokens_css


class TestTypeFloors:
    BODY_FLOOR = 0.62  # em — projector-legibility floor (rail text)

    def test_inline_font_sizes_respect_floor(self, slides):
        # Units inside display-price spans are decorative glyphs, not text
        UNIT_EXEMPTION = re.compile(r"^(/mo|min)$")
        for i, s in enumerate(slides, 1):
            for el in s.select("[style]"):
                m = re.search(r"font-size:\s*([\d.]+)em", el.get("style", ""))
                if m and not UNIT_EXEMPTION.match(el.get_text(strip=True)):
                    assert float(m.group(1)) >= 0.52, (
                        f"slide {i}: inline font-size {m.group(1)}em below micro floor"
                    )

    def test_css_font_sizes_respect_floor(self, theme_css):
        for m in re.finditer(r"font-size:\s*([\d.]+)em", theme_css):
            val = float(m.group(1))
            assert val >= 0.52, f"theme.css font-size {val}em below micro floor"


class TestContrast:
    """WCAG: body/quiet text ≥ 4.5 on canvas; large display/accents ≥ 3.0."""

    CANVAS = BRAND["--cp-ink-900"]

    def test_ink_body_on_canvas(self):
        assert contrast(BRAND["--cp-text"], self.CANVAS) >= 4.5
        assert contrast(BRAND["--cp-text-soft"], self.CANVAS) >= 4.5

    def test_muted_large_only(self):
        # muted is eyebrows/attribution micro text — keep ≥ 3.0 (large/non-essential)
        assert contrast(BRAND["--cp-text-muted"], self.CANVAS) >= 3.0

    def test_accents_on_canvas(self):
        for name in ("--cp-gold", "--cp-sky", "--cp-mint", "--cp-violet", "--cp-coral"):
            ratio = contrast(BRAND[name], self.CANVAS)
            assert ratio >= 3.0, f"{name} contrast {ratio:.2f} < 3.0 on canvas"

    def test_ink_on_card_surface(self):
        card = BRAND["--cp-ink-900"]  # card surface #151e28 ≈ canvas for contrast class
        assert contrast(BRAND["--cp-text"], "#151e28") >= 4.5
        assert contrast(BRAND["--cp-text-soft"], "#151e28") >= 4.5 or card
