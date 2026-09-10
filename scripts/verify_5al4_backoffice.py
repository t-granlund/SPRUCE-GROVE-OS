"""Fresh headless verification for bead SPRUCE-GROVE-OS-5al.4 (backoffice checklist)."""

import os
import re
import runpy
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PLUGIN = Path.home() / ".spruce_grove/plugins/backoffice/register_callbacks.py"
OFFICIAL = re.compile(
    r"^https://(www\.)?(irs\.gov|dfa\.arkansas\.gov|atap\.arkansas\.gov|"
    r"sos\.arkansas\.gov|bentonvillear\.com)(/|$)"
)
CHECKS = []


def check(label, ok):
    CHECKS.append((label, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")


def main():
    print(f"timestamp: {datetime.now(timezone.utc).isoformat()}")
    tmp = Path(tempfile.mkdtemp(prefix="sg5al4_"))
    os.chdir(tmp)
    runpy.run_path(str(PLUGIN), run_name="verify_backoffice_plugin")

    from spruce_grove.callbacks import on_custom_command

    # pass-through: other commands untouched
    res = on_custom_command("something-else", "something-else")
    check("non-backoffice commands pass through (all None)", not any(res))

    res = on_custom_command("backoffice", "backoffice")
    check("/backoffice dispatched", any(res))

    md_path = tmp / "BACK-OFFICE-CHECKLIST.md"
    check("BACK-OFFICE-CHECKLIST.md written", md_path.is_file())
    md = md_path.read_text(encoding="utf-8")

    check("NOT LEGAL ADVICE banner", "NOT LEGAL ADVICE" in md)
    check("NOT TAX ADVICE banner", "NOT TAX ADVICE" in md)

    rows = [ln for ln in md.splitlines() if re.match(r"^\| \d+ \|", ln)]
    check(f">=10 gated rows (got {len(rows)})", len(rows) >= 10)

    urls = re.findall(r"<(https?://[^>]+)>", md)
    check(f">=10 source URLs (got {len(urls)})", len(urls) >= 10)
    check("one URL per gate", len(urls) == len(rows))
    bad = [u for u in urls if not OFFICIAL.match(u)]
    check(
        f"every URL on an official IRS/AR/city domain ({len(urls) - len(bad)}/{len(urls)})",
        not bad,
    )

    # live URL sweep
    print("\nLive URL sweep (fresh, today):")
    ok_codes = 0
    for u in urls:
        # GET (not HEAD): the ATAP portal 404s HEAD but 302s GET into its app.
        r = subprocess.run(
            [
                "curl",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                "--max-time",
                "20",
                "-A",
                "Mozilla/5.0 (sg-5al.4 verification sweep)",
                u,
            ],
            capture_output=True,
            text=True,
        )
        code = r.stdout.strip()
        live = code.startswith(("2", "3"))
        ok_codes += live
        print(f"  HTTP {code}  {u}  {'OK' if live else 'DEAD?'}")
    check(
        f"all URLs live or redirecting ({ok_codes}/{len(urls)})", ok_codes == len(urls)
    )

    print(f"\n{sum(1 for _, okk in CHECKS if okk)}/{len(CHECKS)} checks PASS")
    return 0 if all(okk for _, okk in CHECKS) else 1


sys.exit(main())
