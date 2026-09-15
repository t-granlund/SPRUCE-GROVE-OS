# PyPI name claim — the 10-minute owner errand

> **STATUS (2026-09-15): DONE.** `spruce-grove` is claimed and live on PyPI,
> publishing on every push to main via **OIDC trusted publishing** (no
> `PYPI_API_TOKEN` secret — the token steps below are historical). The
> release pipeline now also serializes runs and self-heals its own push
> races; see `docs/SELF-UPDATE.md` for how releases reach users without
> anyone pressing an update button.

Status as of 2026-09-10: `spruce-grove` / `sprucegrove` / `spruce_grove` all
return HTTP 404 on pypi.org (re-verified Sept 10 evening). The wheel builds
clean (`uv build` -> `dist/spruce_grove-0.1.0*`, `twine check` PASSED) and
`.github/workflows/publish.yml` is fully wired — it publishes **on every push
to main** using a `PYPI_API_TOKEN` repo secret (auto patch-bump, twine upload,
tag). The only missing ingredient is the secret, and the secret needs an
account only Tyler can create.

## The errand (one sitting, ~10 min)

1. **Create the PyPI account** — https://pypi.org/account/register/
   (use a real email; enable 2FA when prompted).
2. **Create an API token** — https://pypi.org/manage/account/token/
   - First token: scope "Entire account (all projects)" — a project-scoped
     token cannot exist before the project does.
   - Copy it (starts `pypi-`).
3. **Add the GitHub secret**:
   ```sh
   gh secret set PYPI_API_TOKEN --repo t-granlund/SPRUCE-GROVE-OS
   # paste when prompted — or Settings -> Secrets and variables -> Actions
   ```
4. **Trigger the publish** — the next push to main does it, or re-run the
   last "Build and Publish to PyPI" run:
   ```sh
   gh run list --repo t-granlund/SPRUCE-GROVE-OS --workflow publish.yml
   gh run rerun <id> --repo t-granlund/SPRUCE-GROVE-OS
   ```
5. **Verify the claim**:
   ```sh
   curl -s -o /dev/null -w "%{http_code}\n" https://pypi.org/pypi/spruce-grove/json
   # expect 200; the CLI's version checker goes green the next time it runs
   ```
6. **Rotate the token** — once the project exists, create a project-scoped
   token (scope: `spruce-grove`) and replace the secret with it. Least power
   on the wire.

## Good news about the "three spellings"

PyPI normalizes names per PEP 503: `-`, `_`, and `.` are equivalent.
Claiming `spruce-grove` automatically covers `spruce_grove` — one claim,
two spellings down. Only the no-separator `sprucegrove` is a genuinely
different project name; if that squat matters, it needs a tiny placeholder
upload under that name (separate errand, low priority — `uv build` a stub
with `name = "sprucegrove"` and `twine upload` it once with the same token).

## Heads-up

- The workflow publishes **every push to main** (test job -> patch bump ->
  upload -> tag). That is the release train by design; from the moment the
  secret exists, pushes ship. Use `[ci skip]` in a commit message to land
  work without releasing.
- The test job provisions a fake `LILAC_API_KEY` etc. so the suite runs
  without real provider keys; if the first publish run goes red in tests,
  read the log before assuming the claim failed — the upload only happens
  after tests pass.
- `dist/` is gitignored; the artifacts built locally on Sept 10 were
  verified with `uvx twine check` (PASSED) but PyPI will get freshly built
  ones from CI.
