# Self-Update — the grove tends itself

How Spruce Grove OS stays current on its own, what it operates with to
exist, and the contracts that keep a self-updating tool from ever breaking
a running session.

---

## The loop

Every startup runs this sequence without blocking the user:

```
launch ─▶ daemon thread ─▶ GET pypi.org/pypi/spruce-grove/json
                        ─▶ compare (installed vs latest)
                        ├─ equal ──────▶ idle (one "current version" line)
                        └─ newer ──────▶ report status (message bus)
                                        ├─ owns console? ─▶ schedule for exit
                                        │                   (env stash)
                                        └─ is a child? ───▶ report only;
                                                            parent upgrades
   ...
run ─▶ exit path (atexit) ─▶ pending? ─▶ uv tool upgrade spruce-grove
                                        ├─ exit 0 ─▶ next launch is current
                                        └─ failure ▶ log + manual command
```

Pieces it operates with:

| Piece | Role |
|---|---|
| `spruce_grove/version_checker.py` | PyPI fetch + comparison + status messages; decides *whether* to actuate |
| `spruce_grove/self_update.py` | Actuation only: `uv tool upgrade`, guards, reporting; never decides |
| `uv tool` env on disk | The thing being replaced — installed via `uv tool install spruce-grove` |
| PyPI JSON API | Source of truth for "latest" (5s timeout; fetch failure = observe-only) |
| Startup daemon thread | Non-blocking, never joined at exit — a hung network cannot hang a session |
| Message bus + i18n | All reporting goes through `t("version.self_update_*")` — 3 locales |

## Session-safety model

The design question: how do you swap the code of a running program without
breaking it? Answer: **you don't touch the disk while the process is
importing from it.** Actuation is deferred to process exit, and process
boundaries do the rest.

- A running session keeps executing the version it started with — its
  modules stay warm, and **nothing on disk changes underneath it**.
- `uv tool upgrade` runs on the exit path (`atexit`), once the interpreter
  has finished importing grove code. The disk is replaced only when nothing
  can import from it any more.
- The **next** process launched resolves imports from the new code.

### The premise this used to get wrong

Earlier revisions of this document claimed the risk was negligible, because
"the running session's imports are already resolved" and the only exposure
was "a daemon-threaded long-runner importing a brand-new submodule
mid-session." **That premise was false, and the architecture is what made it
false.** The grove imports tool modules *lazily*, at the moment an agent
first needs them:

```python
# spruce_grove/tools/_lazy.py
def lazy_registration(module: str, name: str):
    def register(*args, **kwargs):
        return getattr(import_module(module), name)(*args, **kwargs)  # imports at first use
```

So mid-session imports are the **normal path for every tool**, not an edge
case — and the first `invoke_agent` is exactly when they happen. Upgrading
the disk during a session therefore half-mixed two versions: the process held
the old module table while the files on disk were new.

Observed live (2026-09-22/23): a session started 18:04 cached
`spruce_grove.harness` before the ToolContext vocabulary landed; the install
was upgraded at 09:29; the next lazy import of a browser tool raised
`ImportError`, and because tool registration had no per-tool guard, **every**
agent whose toolset included it died — delegation included.

Three fixes, in layers:

1. **Deferral** (this document's contract): actuation waits for exit, so the
   hazard class is gone rather than merely survivable.
2. **Per-tool isolation** (`8d74d2d`): a tool that fails to register is
   skipped and named, never fatal to the agent run.
3. **A diagnosable binding**: the lazy `ToolContext` resolution raises an
   ImportError that names the stale-process cause and the restart fix,
   instead of a bare `ImportError`.

The honest label for (2) and (3): they are **graceful degradation**, not
full function. A stale session survives, minus the tools that could not
import. Only a restart restores everything. (1) is what stops it happening
at all.

### When the grove is a child process

The desktop shell (and any other parent driving the CLI as a child) is a
special case: the child's `stdin` is a pipe, not a console. A child must not
upgrade its own live installation — the parent is mid-flight, and the parent
owns the console. So in that case actuation is **reported, not performed**:
the child says a newer release exists and leaves the upgrade to the process
that owns it. A bare interactive session owns its console and defers to its
own exit.

## Contracts (the part that must never rot)

1. **`perform_self_update` never raises.** Every path returns `True`/`False`
   and reports. `_maybe_self_update` in `version_checker.py` wraps it in a
   last-resort try/except anyway — defense in depth.
2. **Never actuate in tests.** `tests/conftest.py` sets `NO_AUTO_UPDATE=1`
   for the entire suite. No test can ever mutate a real installation.
3. **Never actuate on source checkouts.** `self_update_supported()`
   requires the `uv` binary *and* the package to live under
   `.../uv/tools/...`. Editable installs are sacred.
4. **Actuation is a subprocess with a bounded timeout.** 180s inline; 60s on
   the exit path (`EXIT_UPGRADE_TIMEOUT_SECONDS`), where the wait is
   user-visible and a miss simply defers to the next launch.
5. **Actuation never runs while the process can still import.** Deferred to
   the exit path; a child process never actuates at all (it reports and lets
   its parent act).

## Escape hatches & rollback

| Intent | Action |
|---|---|
| Keep checking, never auto-upgrade | `NO_AUTO_UPDATE=1` |
| Silence the entire check | `NO_VERSION_UPDATE=1` (pre-existing gate in `cli_runner.py`) |
| Check normally, skip the exit-time install | `SPRUCE_GROVE_UPDATE_AT_EXIT=0` |
| Pin a known-good version | `uv tool install spruce-grove==X.Y.Z` |
| Force re-resolve after a just-published release | `uv cache clean spruce-grove && uv tool upgrade spruce-grove` |

Note the last one: uv's registry cache can lag PyPI by a few minutes after
a fresh publish. The JSON API and uv's index are different caches.

## Release-pipeline caveats (learned the hard way, 2026-09-15)

`.github/workflows/publish.yml` builds and publishes **on every push to
main**, then pushes a `[ci skip]` version-bump commit + tag back. Two races
this design allows — both observed live the day self-update shipped:

1. **Hollow releases.** The bump+tag lands *after* the build, so a push
   that arrives between "bump committed" and "feature commit pushed" gets
   versioned by the *next* run. 1.0.37 shipped with a feature's version
   number but without the feature. If a release seems to lack a change,
   check `git rev-list -n1 vX.Y.Z` against the change's commit *before*
   trusting the version number.
2. **CI as the guardrail.** A commit that pairs a new test with an
   unfixed implementation fails its run, and `needs: test` blocks the
   publish. The next commit (fix + tests) is the one that ships. Broken
   code cannot ride the conveyor; it just costs a queued run.

The publish workflow serializes runs (`concurrency: pypi-publish`,
cancel-in-progress: false) precisely so back-to-back pushes cannot race
versions — every push still gets released, one at a time.
