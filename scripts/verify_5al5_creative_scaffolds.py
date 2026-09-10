"""Fresh headless verification for bead SPRUCE-GROVE-OS-5al.5 (creative scaffolds)."""

import os
import runpy
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CREATIVE = Path.home() / ".spruce_grove/plugins/creative_scaffold/register_callbacks.py"
BARBER = (
    Path.home()
    / "dev/Bentonville-Barbershop-website-mock-up/.spruce_grove/plugins/barber_scaffold/register_callbacks.py"
)
LIB = Path.home() / ".spruce_grove/lib/grove_site_core"
CHECKS = []


def check(label, ok):
    CHECKS.append((label, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")


def main():
    print(f"timestamp: {datetime.now(timezone.utc).isoformat()}")
    tmp = Path(tempfile.mkdtemp(prefix="sg5al5_"))
    os.chdir(tmp)
    runpy.run_path(str(CREATIVE), run_name="verify_creative_plugin")

    from spruce_grove.callbacks import on_custom_command

    res = on_custom_command("creative-scaffold all", "creative-scaffold")
    check("/creative-scaffold all dispatched", any(res))

    fpv = tmp / "site-out" / "fpv"
    art = tmp / "site-out" / "artisans"
    check("site-out/fpv/index.html exists", (fpv / "index.html").is_file())
    check("site-out/artisans/index.html exists", (art / "index.html").is_file())
    check(
        "both profiles have checklists",
        (fpv / "checklist.html").is_file() and (art / "checklist.html").is_file(),
    )

    html = (fpv / "index.html").read_text(encoding="utf-8")
    check(
        "youtube-nocookie https iframe embed",
        "youtube-nocookie.com/embed" in html
        and "<iframe" in html
        and 'loading="lazy"' in html,
    )
    check(
        "click-to-zoom lightbox markers (img[data-lb] + data-full)",
        "data-lb" in html and "data-full" in html,
    )
    check("grove tokens present (#0E130F)", "#0E130F" in html)

    art_html = (art / "index.html").read_text(encoding="utf-8")
    check(
        "artisans FPO inline SVG tiles (offline)",
        "data:image/svg+xml;base64," in art_html,
    )
    check(
        "further profiles follow same structure",
        "data-lb" in art_html and "#0E130F" in art_html,
    )

    # reuse audit, AST-statement basis (documented): count ast.stmt nodes in the
    # shared grove_site_core path vs each plugin; reuse = shared / (shared + plugin).
    import ast

    def stmt_count(path):
        tree = ast.parse(Path(path).read_text())
        return len([n for n in ast.walk(tree) if isinstance(n, ast.stmt)])

    shared = sum(stmt_count(LIB / f) for f in ("builder.py", "cli.py", "tokens.py"))
    barber_stmts = stmt_count(BARBER)
    creative_stmts = stmt_count(CREATIVE)
    reuse_barber = shared / (shared + barber_stmts)
    reuse_creative = shared / (shared + creative_stmts)
    print(
        f"\nreuse audit (AST-statement basis): shared grove_site_core={shared} stmts; "
        f"barber plugin={barber_stmts} stmts -> shared-path reuse {100 * reuse_barber:.1f}%; "
        f"creative plugin={creative_stmts} stmts -> shared-path reuse {100 * reuse_creative:.1f}%"
    )
    check("barber rides >=80% shared code path", reuse_barber >= 0.8)
    check(
        "creative rides >=80% shared code path (no fork of .3)", reuse_creative >= 0.8
    )

    print(f"\n{sum(1 for _, ok in CHECKS if ok)}/{len(CHECKS)} checks PASS")
    return 0 if all(ok for _, ok in CHECKS) else 1


sys.exit(main())
