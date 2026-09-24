"""Fresh headless verification for bead SPRUCE-GROVE-OS-5al.3 (barber scaffold)."""

import os
import runpy
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PLUGIN = (
    Path.home()
    / "dev/Bentonville-Barbershop-website-mock-up/.spruce_grove/plugins/barber_scaffold/register_callbacks.py"
)
CHECKS = []


def check(label, ok):
    CHECKS.append((label, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")


def main():
    print(f"timestamp: {datetime.now(timezone.utc).isoformat()}")
    tmp = Path(tempfile.mkdtemp(prefix="sg5al3_"))
    os.chdir(tmp)
    runpy.run_path(str(PLUGIN), run_name="verify_barber_plugin")

    from spruce_grove.callbacks import on_custom_command

    # 1. unknown profile writes nothing
    res = on_custom_command("barber-scaffold bogus", "barber-scaffold")
    check("unknown profile handled (truthy result)", any(res))
    check("unknown profile wrote no site-out", not (tmp / "site-out").exists())

    # 2. main command builds site-out
    res = on_custom_command("barber-scaffold", "barber-scaffold")
    check("/barber-scaffold dispatched", any(res))
    out = tmp / "site-out"
    check("site-out/index.html exists", (out / "index.html").is_file())
    check("site-out/checklist.html exists", (out / "checklist.html").is_file())

    html = (out / "index.html").read_text(encoding="utf-8")
    check("grove token present (#0E130F)", "#0E130F" in html)
    check("brand name rendered", "Bentonville Barber" in html)

    # 3. idempotent rebuild: page count stable at 2
    pages1 = sorted(p.name for p in out.glob("*.html"))
    on_custom_command("barber-scaffold", "barber-scaffold")
    pages2 = sorted(p.name for p in out.glob("*.html"))
    check(
        f"idempotent rebuild ({pages1} == {pages2})",
        pages1 == pages2 and len(pages1) == 2,
    )

    # 4. alias dispatch
    tmp2 = Path(tempfile.mkdtemp(prefix="sg5al3_alias_"))
    os.chdir(tmp2)
    # reload plugin for fresh cwd-bound outroot
    for mod in [m for m in sys.modules if m.startswith("grove_site_core")]:
        del sys.modules[mod]
    runpy.run_path(str(PLUGIN), run_name="verify_barber_plugin2")
    res = on_custom_command("bbc-scaffold", "bbc-scaffold")
    check("alias /bbc-scaffold dispatched", any(res))
    check("alias built site-out/index.html", (tmp2 / "site-out/index.html").is_file())

    print(f"\n{sum(1 for _, ok in CHECKS if ok)}/{len(CHECKS)} checks PASS")
    return 0 if all(ok for _, ok in CHECKS) else 1


sys.exit(main())
