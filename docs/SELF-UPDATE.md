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
                                        └▶ uv tool upgrade spruce-grove
                                           ├─ exit 0 ─▶ "self-update complete;
                                           │             next launch starts on
                                           │             the new version"
                                           └─ failure ▶ warn + manual command
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
breaking it? Answer: **you don't.** You swap the *disk*, and let process
boundaries do the rest.

- A running session has all its modules warm and internally consistent —
  it keeps executing the version it started with, to the end of its life.
- The on-disk environment is replaced by `uv tool upgrade` (fresh venv,
  atomic enough at the uv layer).
- The **next** process launched resolves imports from the new code.

No lazy-import mixing matters in practice because the running session's
imports are already resolved; the exposure window is a daemon-threaded
long-runner importing a brand-new submodule mid-session, which the
"restart to switch" message makes explicit rather than pretending away.

## Contracts (the part that must never rot)

1. **`perform_self_update` never raises.** Every path returns `True`/`False`
   and reports. `_maybe_self_update` in `version_checker.py` wraps it in a
   last-resort try/except anyway — defense in depth.
2. **Never actuate in tests.** `tests/conftest.py` sets `NO_AUTO_UPDATE=1`
   for the entire suite. No test can ever mutate a real installation.
3. **Never actuate on source checkouts.** `self_update_supported()`
   requires the `uv` binary *and* the package to live under
   `.../uv/tools/...`. Editable installs are sacred.
4. **Actuation is a subprocess with a 180s timeout.** The daemon thread is
   never joined; worst case is a warning line.

## Escape hatches & rollback

| Intent | Action |
|---|---|
| Keep checking, never auto-upgrade | `NO_AUTO_UPDATE=1` |
| Silence the entire check | `NO_VERSION_UPDATE=1` (pre-existing gate in `cli_runner.py`) |
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
