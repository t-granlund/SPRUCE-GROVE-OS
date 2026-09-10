"""backoffice -- small-business back-office checklist generator (/backoffice).

User-tier grove cohort plugin (bead SPRUCE-GROVE-OS-5al.4): general-purpose, so
it rides next to junto -- every cohort business carries the same boring risk:
the thing you did not read. Emits a markdown checklist into the current repo,
every item with its official source URL. Sourced facts or nothing ships.

NOT LEGAL ADVICE. NOT TAX ADVICE. A reading list with dates, not a lawyer.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from spruce_grove.callbacks import register_callback

_OUTFILE = "BACK-OFFICE-CHECKLIST.md"

# (when, item, official source URL) -- all URLs verified 2026-09-10 (HTTP 200,
# except ATAP which answers 302 into its app portal; noted on that item).
_ITEMS: list[tuple[str, str, str]] = [
    (
        "Day 0",
        "Apply for a free EIN online (never pay a third-party site for this).",
        "https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online",
    ),
    (
        "Week 1",
        "Choose a business structure deliberately (sole prop vs LLC vs corp) -- this decision drives every later form.",
        "https://www.irs.gov/businesses/small-businesses-self-employed/business-structures",
    ),
    (
        "Quarterly",
        "Pay federal estimated taxes if you expect to owe $1,000+ (deadlines: Apr 15, Jun 15, Sep 15, Jan 15).",
        "https://www.irs.gov/businesses/small-businesses-self-employed/estimated-taxes",
    ),
    (
        "Always",
        "Understand self-employment tax (Social Security + Medicare, 15.3% before income tax).",
        "https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes",
    ),
    (
        "Always",
        "Keep every receipt and record; retention rules are longer than instinct suggests (3 years typical, 7 for bad-debt/worthless claims).",
        "https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records",
    ),
    (
        "First hire",
        "Before your first employee: read Publication 15 (employer's tax guide), set up withholding + deposits.",
        "https://www.irs.gov/publications/p15",
    ),
    (
        "Each Jan",
        "File 1099-NEC for any contractor paid $600+ in the prior year.",
        "https://www.irs.gov/forms-pubs/about-form-1099-nec",
    ),
    (
        "Before selling",
        "Register for an Arkansas Sales & Use Tax permit before your first taxable sale (goods, prepared food, some services).",
        "https://www.dfa.arkansas.gov/excise-tax/sales-use-tax/",
    ),
    (
        "Setup",
        "Open an ATAP (Arkansas Taxpayer Access Point) account -- Arkansas filings run through this portal. (Official portal; answers HTTP 302 into its login app.)",
        "https://atap.arkansas.gov/_/",
    ),
    (
        "If LLC",
        "Register the LLC with the Arkansas Secretary of State (Business & Commercial Services).",
        "https://www.sos.arkansas.gov/business-commercial-services-bcs",
    ),
    (
        "Annually",
        "Arkansas income tax: confirm your pass-through/return obligations with the DFA each filing season.",
        "https://www.dfa.arkansas.gov/income-tax/",
    ),
    (
        "Before signage",
        "Check Bentonville city requirements before signage, home-occupation, remodels, or food service (permits vary by use).",
        "https://www.bentonvillear.com/",
    ),
]

_DISCLAIMER = (
    "> **NOT LEGAL ADVICE. NOT TAX ADVICE.** This is a sourced reading list -- a map "
    "to the officials, not a substitute for an accountant or attorney. Dates are "
    "typical deadlines, not your personalized ones. When in doubt: call the office "
    "behind the link. Every link here is an official IRS, State of Arkansas, or "
    "City of Bentonville page."
)


def _emit_markdown() -> str:
    today = _dt.date.today().isoformat()
    lines = [
        "# Back-Office Checklist (small business, NWA / Arkansas)",
        "",
        f"_Generated {today} by the Spruce Grove backoffice plugin (sg-5al.4). Re-generate freely._",
        "",
        _DISCLAIMER,
        "",
        "| # | When | Gate | Source |",
        "|---|------|------|--------|",
    ]
    for idx, (when, item, url) in enumerate(_ITEMS, start=1):
        lines.append(f"| {idx} | {when} | {item} | <{url}> |")
    lines += [
        "",
        "## Rules of the list",
        "",
        "- Sourced facts only: if an item ever lacks an official URL, delete it rather than guess.",
        "- 'When' is a typical cadence, not a ruling -- your accountant sets your calendar.",
        "- gran·lund · sv. · spruce grove · together we are better, always.",
    ]
    return "\n".join(lines) + "\n"


def _backoffice(command: str, name: str):
    """Handle /backoffice [outfile.md]; pass everything else through."""
    if name != "backoffice":
        return None

    console = Console()
    parts = command.split(maxsplit=1)
    outfile = Path(parts[1].strip()) if len(parts) > 1 else Path.cwd() / _OUTFILE

    outfile.write_text(_emit_markdown(), encoding="utf-8")
    console.print(
        Panel(
            f"Wrote [cyan]{outfile}[/cyan]\n"
            f"[#98B79E]{len(_ITEMS)} gates, {len(_ITEMS)} official sources (11 IRS/AR verified HTTP 200; ATAP 302-portal noted).[/#98B79E]\n\n"
            "[dim]" + _DISCLAIMER.replace("> **", "").replace("**", "") + "[/dim]",
            title="[#D2A069]back-office checklist[/#D2A069]",
            border_style="#588F5E",
            padding=(1, 2),
        )
    )
    return True


def _backoffice_help():
    return [
        (
            "/backoffice",
            "Small-business back-office checklist: 12 gates, official IRS/AR/Bentonville sources, NOT-ADVICE banner",
        )
    ]


register_callback("custom_command", _backoffice)
register_callback("custom_command_help", _backoffice_help)
