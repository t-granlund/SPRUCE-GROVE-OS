"""grove_site_core.cli -- shared /command plumbing for cohort scaffold plugins.

DRY contract (sg-5al.5 followthrough): barber + creative scaffolds repeat the
same dispatch, target-resolution, panel, and help bones. Those bones live here
once. Cohort plugins ship only: sys.path insert, PROFILE data, one call.

Usage from a plugin's register_callbacks.py:

    from grove_site_core.cli import register_scaffold_command
    register_scaffold_command(
        name="creative-scaffold",
        profiles=PROFILES,               # dict[key, profile-dict]
        outroot=Path.cwd() / "site-out",
        help_line="Creative cohort site starters ...",
        panel_title="creative cohort scaffolds",
    )
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from spruce_grove.callbacks import register_callback


def register_scaffold_command(
    *,
    name: str,
    profiles: dict,
    outroot: Path,
    help_line: str,
    panel_title: str,
    panel_subtitle: str = "site-out/ only \N{DOT OPERATOR} no network \N{DOT OPERATOR} data-driven profiles",
    aliases: tuple[str, ...] = (),
) -> None:
    """Register a ``/<name> [profile|all]`` scaffold command + help entry.

    Multi-profile plugins get ``outroot/<key>/``; single-profile plugins build
    straight into ``outroot``. Bad arguments print usage, never a traceback.
    """
    command_names = {name, *aliases}
    per_profile_dir = len(profiles) > 1

    def _targets(arg: str) -> list[str]:
        key = arg.strip().lower()
        if key in profiles:
            return [key]
        if key in ("", "all"):
            return sorted(profiles)
        return []

    def _handler(command: str, cmd_name: str):
        if cmd_name not in command_names:
            return None
        console = Console()
        arg = command.split(maxsplit=1)[1] if " " in command else ""
        targets = _targets(arg)
        if not targets:
            choices = ", ".join(sorted(profiles)) + (
                ", or all" if len(profiles) > 1 else ""
            )
            console.print(
                f"[yellow]Unknown profile '{arg}'. Usage: /{name} (choices: {choices})[/yellow]"
            )
            return True

        from grove_site_core.builder import build_site

        built = []
        for key in targets:
            outdir = outroot / key if per_profile_dir else outroot
            report = build_site(profiles[key], outdir)
            built.append(
                f"[#98B79E]{key}[/#98B79E] -> {report['outdir']} ({len(report['written'])} pages)"
            )
        console.print(
            Panel(
                "\n".join(built)
                + "\n\n[dim]Shared grove_site_core path. Preview: open index.html in a browser.[/dim]",
                title=f"[#D2A069]{panel_title}[/#D2A069]",
                subtitle=panel_subtitle,
                border_style="#588F5E",
                padding=(1, 2),
            )
        )
        return True

    def _help():
        return [(f"/{name}", help_line)]

    register_callback("custom_command", _handler)
    register_callback("custom_command_help", _help)
