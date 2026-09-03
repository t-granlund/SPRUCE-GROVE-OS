"""Generate the Code Puppy Field Guide data file from the live repo.

Usage:
    cd /Users/tygranlund/code_puppy
    python docs/generate-field-guide.py

Outputs:
    docs/field-guide/data.js

The companion index.html + app.js render this data into a local,
launchable documentation site.
"""

from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import ast

from field_guide_changelog import _get_recent_commits

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_DIR = DOCS_DIR / "field-guide"
OUTPUT_FILE = OUTPUT_DIR / "data.js"
USER_PLUGINS_DIR = Path.home() / ".code_puppy" / "plugins"


def _find_installed_core_plugins_dir() -> Path | None:
    """Locate the installed code_puppy_core_plugins package.

    Upstream moved builtin plugins out of this repo into the
    ``code-puppy-core-plugins`` companion package (visible in site-packages
    of the uv tool install). Guide completeness depends on scanning it.
    """
    try:
        result = subprocess.run(
            [
                "/opt/homebrew/bin/uv",
                "tool",
                "run",
                "--from",
                "code-puppy",
                "python",
                "-c",
                "import code_puppy_core_plugins, pathlib; "
                "print(pathlib.Path(code_puppy_core_plugins.__file__).parent)",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        if result.returncode == 0:
            candidate = Path(result.stdout.strip().splitlines()[-1])
            if candidate.is_dir():
                return candidate
    except Exception:
        pass
    # Last-ditch: glob the known uv tools layout.
    uv_site = Path.home() / ".local" / "share" / "uv" / "tools"
    for candidate in sorted(uv_site.glob("code-puppy/lib/*/site-packages/code_puppy_core_plugins")):
        if candidate.is_dir():
            return candidate
    return None


def _run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout.strip()


def _strip_ansi_osc(text: str) -> str:
    """Remove ANSI escape sequences and OSC color codes from output."""
    # OSC sequences: ESC ] ... BEL or ESC \x9c
    text = re.sub(r"\x1b\].*?(?:\x07|\x9c)", "", text)
    # ANSI CSI sequences
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    # Other control sequences
    text = re.sub(r"\x1b[\(\)][AB012]", "", text)
    return text


def _get_git_info() -> dict:
    try:
        head = _run(["git", "rev-parse", "--short", "HEAD"])
        branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return {"head": head, "branch": branch}
    except Exception:
        return {"head": "unknown", "branch": "unknown"}


def _get_current_version() -> str:
    try:
        version = _run(
            ["/opt/homebrew/bin/uv", "tool", "list"], check=False
        )
        for line in version.splitlines():
            if line.startswith("code-puppy"):
                return line.strip()
    except Exception:
        pass
    try:
        import tomllib

        with open(REPO_ROOT / "pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("version", "unknown")
    except Exception:
        pass
    return "unknown"


# Hand-written, plain-language summaries for the well-known core tools.
# These are the durable TL;DRs shown on tool cards; anything not listed
# here falls back to the introspected docstring.
TOOL_DESCRIPTIONS: dict[str, str] = {
    "list_agents": "List every sub-agent available for delegation, with what each one is good at.",
    "invoke_agent": "Delegate a task to a named sub-agent. Use this to hand off research, QA, or specialist work instead of doing it yourself.",
    "invoke_agent_with_model": "Delegate to a sub-agent while pinning a specific model for that run.",
    "list_available_models": "Show the models configured in the model factory and which providers they route to.",
    "list_files": "List files and directories with smart filtering (skips build artifacts, caches, and noise). Read-only.",
    "read_file": "Read a file's contents, optionally a line range. Use before modifying anything.",
    "grep": "Recursively search file contents with ripgrep regex. Fast way to find usages, definitions, and config.",
    "create_file": "Create a new file or overwrite an existing one with full content.",
    "replace_in_file": "Apply targeted find-and-replace edits. Prefer this over full rewrites; keeps diffs small.",
    "delete_snippet": "Remove the first occurrence of an exact text snippet from a file.",
    "delete_file": "Delete a file with a logged diff of what was removed. Use sparingly.",
    "edit_file": "Deprecated compound tool; auto-expands to create/replace/delete. Prefer the specific tools.",
    "agent_run_shell_command": "Run a shell command with timeout, optional background execution, and output streaming. Your hands.",
    "agent_share_your_reasoning": "Record the agent's reasoning for observability in the TUI and logs.",
    "ask_user_question": "Ask the human multiple related questions in an interactive picker. Use when input is genuinely required.",
    "load_image_for_analysis": "Load an image from disk so the model can see and analyze it.",
    "activate_skill": "Load a SKILL.md's full instructions into context before doing work that needs it.",
    "list_or_search_skills": "Discover skills by keyword search across name, description, and tags.",
    "universal_constructor": "Helios' tool-forging tool: create, call, list, update, and inspect persistent custom Python tools.",
}


def _get_tools() -> list[dict]:
    """Discover tools from the live TOOL_REGISTRY, with summaries."""
    sys.path.insert(0, str(REPO_ROOT))
    try:
        from code_puppy.tools import get_available_tool_names

        names = sorted(get_available_tool_names())
    except Exception as exc:
        print(f"Warning: could not load tools: {exc}")
        return []

    categories = {
        "agent": ["list_agents", "invoke_agent", "invoke_agent_with_model", "list_available_models"],
        "file": ["list_files", "read_file", "grep", "create_file", "replace_in_file", "delete_snippet", "delete_file", "edit_file"],
        "shell": ["agent_run_shell_command", "agent_share_your_reasoning"],
        "browser": [n for n in names if n.startswith("browser_")],
        "skills": ["activate_skill", "list_or_search_skills"],
        "user": ["ask_user_question", "load_image_for_analysis"],
        "constructor": ["universal_constructor"],
    }

    tools: list[dict] = []
    for name in names:
        cat = "other"
        for c, members in categories.items():
            if name in members:
                cat = c
                break
            if name.startswith("browser_"):
                cat = "browser"
        tools.append(
            {
                "name": name,
                "category": cat,
                "description": TOOL_DESCRIPTIONS.get(name, ""),
            }
        )
    return tools


def _get_agents() -> list[dict]:
    """Discover built-in Python agents and JSON agents."""
    sys.path.insert(0, str(REPO_ROOT))
    os.environ["TERM"] = "dumb"

    agents: list[dict] = []
    seen_names: set[str] = set()

    # Built-in Python agents
    agents_dir = REPO_ROOT / "code_puppy" / "agents"
    for file in sorted(agents_dir.glob("agent_*.py")):
        modname = file.stem
        try:
            module = __import__(f"code_puppy.agents.{modname}", fromlist=["*"])
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and attr.__name__.endswith("Agent")
                    and attr.__name__ not in {"BaseAgent", "JSONAgent"}
                ):
                    inst = attr()
                    if inst.name in seen_names:
                        continue
                    seen_names.add(inst.name)
                    agents.append(
                        {
                            "name": inst.name,
                            "display_name": inst.display_name,
                            "description": inst.description,
                            "type": "python",
                            "tools": inst.get_available_tools(),
                        }
                    )
        except Exception as exc:
            print(f"Warning: could not load agent {modname}: {exc}")

    # JSON agents from user config
    user_agents_dir = Path.home() / ".code_puppy" / "agents"
    if user_agents_dir.exists():
        for json_file in sorted(user_agents_dir.glob("*.json")):
            try:
                data = json.loads(json_file.read_text())
                name = data.get("name", json_file.stem)
                if name in seen_names:
                    continue
                seen_names.add(name)
                agents.append(
                    {
                        "name": name,
                        "display_name": data.get("display_name", name),
                        "description": data.get("description", "Custom JSON agent"),
                        "type": "json",
                        "tools": data.get("tools", []),
                    }
                )
            except Exception as exc:
                print(f"Warning: could not read JSON agent {json_file}: {exc}")

    return sorted(agents, key=lambda a: a["name"])


def _first_sentence(text: str, limit: int = 160) -> str:
    """Extract the first sentence of a docstring/README, trimmed to limit."""
    text = text.strip()
    if not text:
        return ""
    # Cut at the first period followed by space/newline, else just truncate.
    m = re.search(r"\.(\s|$)", text)
    sentence = text[: m.end()].strip() if m else text
    sentence = sentence.replace("\n", " ").strip()
    if len(sentence) > limit:
        sentence = sentence[: limit - 1].rstrip() + "..."
    return sentence


def _scan_plugin_register_callbacks(register_file: Path) -> dict:
    """Statically extract which callbacks a plugin registers in register_callbacks.py."""
    hooks = set()
    try:
        tree = ast.parse(
            register_file.read_text(encoding="utf-8", errors="replace")
        )
    except Exception:
        return {"hooks": []}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        is_register = (
            isinstance(func, ast.Name)
            and func.id == "register_callback"
        ) or (
            isinstance(func, ast.Attribute)
            and func.attr == "register_callback"
        )
        if not is_register or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            hooks.add(first.value)

    return {
        "hooks": sorted(hooks),
        "hasCustomCommand": "custom_command_help" in hooks,
    }


def _scan_plugin_dir(item: Path, tier: str) -> dict | None:
    """Extract one plugin's metadata from a directory. Returns None if not a plugin."""
    if not item.is_dir() or item.name.startswith("_") or item.name == "__pycache__":
        return None

    # A plugin must have a register_callbacks.py somewhere to do anything.
    if not (item / "register_callbacks.py").exists():
        return None

    readme = item / "README.md"
    desc = ""
    if readme.exists():
        desc = _first_sentence(
            readme.read_text(encoding="utf-8", errors="replace").lstrip("# ")
        )
    if not desc:
        # Fall back to the register_callbacks module docstring.
        try:
            tree = ast.parse(
                (item / "register_callbacks.py").read_text(
                    encoding="utf-8", errors="replace"
                )
            )
            desc = _first_sentence(ast.get_docstring(tree) or "")
        except Exception:
            pass

    files = []
    for f in sorted(item.iterdir()):
        if f.is_file() and f.suffix == ".py":
            try:
                files.append({"name": f.name, "lines": sum(1 for _ in f.open(errors="replace"))})
            except Exception:
                files.append({"name": f.name, "lines": 0})

    meta = _scan_plugin_register_callbacks(item / "register_callbacks.py")

    return {
        "name": item.name,
        "tier": tier,
        "description": desc,
        "hooks": meta["hooks"],
        "hasCustomCommand": meta["hasCustomCommand"],
        "files": files,
        "hasReadme": readme.exists(),
        "hasSkill": (item / "SKILL.md").exists(),
    }


def _get_plugins() -> list[dict]:
    """Deep-extract plugins from all three tiers: builtin-shim, installed
    core-plugins package, and user plugins. Dedupes by name with the
    richest record winning."""
    by_name: dict[str, dict] = {}

    def absorb(item: Path, tier: str) -> None:
        record = _scan_plugin_dir(item, tier)
        if record is None:
            return
        existing = by_name.get(record["name"])
        if existing is None:
            by_name[record["name"]] = record
            return
        # Prefer the record with actual content (repo dirs are often stubs
        # since the core-plugins exodus, while the installed package has the
        # real code — and vice versa for files still living in the repo).
        existing_richness = len(existing["files"]) + len(existing["hooks"])
        new_richness = len(record["files"]) + len(record["hooks"])
        if new_richness > existing_richness:
            record["tier"] = f"{tier} (also in {existing['tier']})"
            by_name[record["name"]] = record
        else:
            existing["tier"] = f"{existing['tier']} (also in {tier})"

    repo_plugins = REPO_ROOT / "code_puppy" / "plugins"
    if repo_plugins.is_dir():
        for item in sorted(repo_plugins.iterdir()):
            absorb(item, "builtin")

    core_pkg = _find_installed_core_plugins_dir()
    if core_pkg is None:
        print("Warning: installed code_puppy_core_plugins package not found; "
              "plugin extraction may be incomplete")
    else:
        for item in sorted(core_pkg.iterdir()):
            absorb(item, "core-package")

    if USER_PLUGINS_DIR.is_dir():
        for item in sorted(USER_PLUGINS_DIR.iterdir()):
            absorb(item, "user")

    return sorted(by_name.values(), key=lambda p: p["name"])


def _extract_frontmatter(text: str) -> dict:
    """Parse simple YAML frontmatter (name/description/tags) from a SKILL.md."""
    meta: dict = {}
    if not text.startswith("---"):
        return meta
    end = text.find("\n---", 3)
    if end == -1:
        return meta
    for line in text[3:end].splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"\'')
    return meta


def _get_skills() -> list[dict]:
    """Discover skills from all SKILL.md sources: repo plugins, the
    installed core-plugins package, and the user skills/plugins dirs."""
    skills: list[dict] = []
    seen: set[str] = set()

    roots: list[Path] = [REPO_ROOT / "code_puppy" / "plugins"]
    core_pkg = _find_installed_core_plugins_dir()
    if core_pkg is not None:
        roots.append(core_pkg)
    roots.append(Path.home() / ".code_puppy" / "skills")
    roots.append(USER_PLUGINS_DIR)

    paths: list[Path] = []
    for root in roots:
        if root.is_dir():
            paths.extend(sorted(root.rglob("SKILL.md")))

    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        meta = _extract_frontmatter(text)
        name = meta.get("name") or path.parent.name
        if name in seen:
            continue
        seen.add(name)
        path_str = str(path)
        if "/code_puppy_core_plugins/" in path_str:
            source = "core-package"
        elif path_str.startswith(str(REPO_ROOT)):
            source = "builtin"
        else:
            source = "user"
        body_intro = ""
        # First non-frontmatter, non-heading line as a fallback description.
        body = re.sub(r"^---.*?---", "", text, flags=re.S).strip()
        for line in body.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                body_intro = line
                break
        if path_str.startswith(str(REPO_ROOT)):
            rel = str(path.relative_to(REPO_ROOT))
        elif source == "core-package":
            rel = "code_puppy_core_plugins/" + "/".join(
                path_str.split("/code_puppy_core_plugins/")[-1].split("/")
            )
        else:
            rel = str(path)
        skills.append(
            {
                "name": name,
                "source": source,
                "description": meta.get("description", body_intro),
                "path": rel,
            }
        )
    return sorted(skills, key=lambda s: s["name"])


# The agentic SDLC lifecycle: which puppy power to reach for at each stage,
# in plain language. Data-driven so the frontend just renders it.
SDLC_STAGES: list[dict] = [
    {
        "stage": "1. Ideate & Spec",
        "goal": "Turn a fuzzy idea into a crisp, testable plan.",
        "use": [
            "code-puppy to draft the design and spike options",
            "Agent Creator to spin up a domain-specialist sub-agent if the work repeats",
            "kennel memory to record decisions so the next session knows them",
        ],
        "output": "A written spec + acceptance criteria the agent can verify against.",
    },
    {
        "stage": "2. Explore & Research",
        "goal": "Verify facts before writing code.",
        "use": [
            "web-puppy for docs, version compatibility, and API research",
            "web-retriever (via invoke_agent) for scraping/automation flows",
            "grep/read_file to ground decisions in the existing codebase",
        ],
        "output": "A citation-backed summary of constraints and known-good approaches.",
    },
    {
        "stage": "3. Build",
        "goal": "Implement in small, reviewable diffs.",
        "use": [
            "replace_in_file over full rewrites (small diffs, easy review)",
            "Plugins over core edits (golden rule: new functionality = a plugin, not core)",
            "Helios / universal_constructor when you need a tool that doesn't exist",
        ],
        "output": "Working code that respects the repo's conventions (DRY, YAGNI, <600 lines/file).",
    },
    {
        "stage": "4. Test & QA",
        "goal": "Prove it works and looks right.",
        "use": [
            "agent_run_shell_command to run the test suite for real",
            "qa-kitten for visual/assertion QA on UIs",
            "Loop: run, read failures, fix, re-run. Don't stop at 'should work'.",
        ],
        "output": "A green test run, not a promise.",
    },
    {
        "stage": "5. Secure & Comply",
        "goal": "Ship something you won't regret.",
        "use": [
            "destructive_command_guard & force_push_guard plugins to block foot-guns",
            "Project plugin trust-gate so repo code can't silently self-approve",
            "Review diffs and secrets handling before commit",
        ],
        "output": "Code with guardrails active and no leaked secrets.",
    },
    {
        "stage": "6. Ship & Polish",
        "goal": "Make it badass and beautiful, then deliver.",
        "use": [
            "Design-system tokens (like the CPU deck's tokens.css) for prompt-addressable theming",
            "The field guide itself to onboard collaborators",
            "dbos_durable_exec for long jobs that must survive crashes",
        ],
        "output": "A stable, documented artifact you're proud to demo.",
    },
]


def _get_file_excerpt(rel_path: str, lines: int = 80) -> str:
    try:
        file_path = REPO_ROOT / rel_path
        text = file_path.read_text()
        return "\n".join(text.splitlines()[:lines])
    except Exception:
        return ""


def _inline_script_block(content: str) -> str:
    """Return content safe to embed inside an HTML <script> block."""
    # Escape the HTML-closing sequence so it does not terminate the script tag.
    return content.replace("</script>", "<\\/script>")


def _inline_image_assets(html: str, base_dir: Path) -> str:
    """Inline assets/*.png references as base64 data URIs.

    The flat HTML is meant to open standalone (file://) from docs/, where a
    relative ``assets/<name>.png`` path would NOT resolve. Inlining the logo
    and favicon as data URIs keeps the file truly self-contained, matching the
    same philosophy used for inlined JS/CSS/data above.
    """
    pattern = re.compile(r'(src|href)="assets/([A-Za-z0-9_.\-]+\.png)"')

    def _sub(m: re.Match) -> str:
        fname = m.group(2)
        fpath = base_dir / "assets" / fname
        if not fpath.exists():
            return m.group(0)
        b64 = base64.b64encode(fpath.read_bytes()).decode("ascii")
        return f'{m.group(1)}="data:image/png;base64,{b64}"'

    return pattern.sub(_sub, html)


def _write_flat_html(data: dict) -> Path:
    """Write a single self-contained HTML file with all CSS/JS/data inlined."""
    flat_path = DOCS_DIR / "field-guide-flat.html"

    html_template = (OUTPUT_DIR / "index.html").read_text()
    app_js = (OUTPUT_DIR / "app.js").read_text()
    data_js = "window.FIELD_GUIDE_DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"

    # Inline data.js
    # NOTE: use a replacement FUNCTION (not a string) for every re.sub below.
    # A string replacement makes re.sub interpret backslash sequences in the
    # JSON/JS payload (e.g. \n, \g) as escape/group references, silently
    # corrupting embedded script content. A lambda returns the text verbatim.
    html_template = re.sub(
        r'<script\s+src="data\.js"></script>',
        lambda m: f'<script>\n{_inline_script_block(data_js)}\n</script>',
        html_template,
    )

    # Inline app.js
    html_template = re.sub(
        r'<script\s+src="app\.js"></script>',
        lambda m: f'<script>\n{_inline_script_block(app_js)}\n</script>',
        html_template,
    )

    # Remove external Google Fonts links for a fully offline file
    html_template = re.sub(
        r'<link[^>]+fonts\.googleapis\.com[^>]*>\n?',
        "",
        html_template,
    )
    html_template = re.sub(
        r'<link[^>]+fonts\.gstatic\.com[^>]*>\n?',
        "",
        html_template,
    )

    # Adjust the launch banner text for direct-file usage
    html_template = html_template.replace(
        "Serve this folder and open in your browser:",
        "Open this file directly in your browser. No server required.",
    )
    html_template = html_template.replace(
        "cd docs/field-guide && python3 -m http.server 8080",
        "file:///path/to/field-guide-flat.html",
    )

    # Inline PNG assets (logo + favicon) as base64 data URIs so the flat
    # file is truly standalone — relative asset paths won't resolve from
    # docs/field-guide-flat.html.
    html_template = _inline_image_assets(html_template, OUTPUT_DIR)

    flat_path.write_text(html_template)
    return flat_path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    changelog_data = _get_recent_commits(_run, REPO_ROOT)

    data = {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "repoPath": str(REPO_ROOT),
            "repoHead": _get_git_info()["head"],
            "branch": _get_git_info()["branch"],
            "currentVersion": _get_current_version(),
            "sourceUrl": "https://github.com/mpfaffenberger/code_puppy",
        },
        "stats": {
            "tools": len(_get_tools()),
            "agents": len(_get_agents()),
            "plugins": len(_get_plugins()),
            "skills": len(_get_skills()),
            "commitsLast2Months": changelog_data["total_commits"],
            "releases": len(changelog_data["releases"]),
        },
        "tools": _get_tools(),
        "agents": _get_agents(),
        "plugins": _get_plugins(),
        "skills": _get_skills(),
        "sdlc": SDLC_STAGES,
        "changelog": changelog_data,
        "excerpts": {
            "agentCreatorPrompt": _get_file_excerpt(
                "code_puppy/agents/agent_creator_agent.py", 200
            ),
            "heliosPrompt": _get_file_excerpt(
                "code_puppy/agents/agent_helios.py", 180
            ),
            "baseAgent": _get_file_excerpt(
                "code_puppy/agents/base_agent.py", 120
            ),
        },
    }

    # Clean up ANSI/OSC noise that might leak in from imports
    data = json.loads(_strip_ansi_osc(json.dumps(data)))

    js = "window.FIELD_GUIDE_DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    OUTPUT_FILE.write_text(js)
    print(f"Generated {OUTPUT_FILE} ({len(js):,} chars)")

    # Also emit a single flat HTML file that opens without a server
    flat_path = _write_flat_html(data)
    flat_size = flat_path.stat().st_size
    print(f"Generated {flat_path} ({flat_size:,} bytes)")


if __name__ == "__main__":
    main()
