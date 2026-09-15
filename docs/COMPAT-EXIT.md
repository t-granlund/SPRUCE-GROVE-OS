# COMPAT-EXIT — Recreating the compatibility contracts, properly

> **STATUS: DRAFT — awaiting council approval.** Nothing here executes
> until a steward signs off. Per `GOVERNANCE.md`, removing or recreating a
> compatibility contract requires a unanimous, written exit plan — this is
> that plan.

The contracts below were inherited as load-bearing compatibility shims
during the import (see `PROVENANCE.md`). They were the right call then:
they kept the fork running and the upstream line compatible. But a shim
with no exit date is drift wearing a tie. This ledger gives each one a
**proper recreation**: what it does, why it exists, the grove-owned
replacement, and the exit criteria that must be true before it is
removed.

Every replacement follows the same shape:

1. **Build the grove-native thing first** (same behavior, grove naming,
   grove tests).
2. **Dual-load during transition** (old contract keeps working, new one
   is preferred, deprecation notices are loud but not fatal).
3. **Exit when the evidence says zero** (no internal uses, no user
   configs on the old key, upstream connector no longer requires
   drop-in parity).
4. **Publish the exit** (the observatory records the removal like any
   other release).

---

## 1. `code-puppy-core-plugins` dependency

- **Does:** provides the official plugin bundle as an external package,
  pinned in pyproject.
- **Why it exists:** free leverage — upstream's plugin suite without
  vendoring.
- **Proper recreation:** grove-owned plugin package
  (`spruce-grove-plugins`) carrying the plugins the grove actually uses,
  under the `spruce_grove.plugins` entry-point group, hash-pinned and
  audited like everything else.
- **Exit criteria:** feature parity for every plugin the grove keeps;
  zero features lost; upstream bundle can still be installed *as a
  third-party plugin* by anyone who wants it (user-tier, not bundled).
- **Risk if rushed:** losing hardened behaviors (tool hooks, credential
  handling) that users depend on daily.

## 2. Entry-point group `code_puppy.plugins`

- **Does:** the discovery group external plugin packages register under.
- **Proper recreation:** register the same plugin objects under
  `spruce_grove.plugins` too; the loader reads both groups during
  transition (new group preferred).
- **Exit criteria:** all known external plugins dual-registered or
  migrated; docs updated; one full release cycle with zero old-group
  registrations observed in the wild.
- **Note:** keeping the old group loading is what makes upstream plugin
  bundles drop-in compatible — the connector's free leverage. The exit
  date is a council decision, not a cleanup reflex.

## 3. `code_puppy.*` import shim (`_code_puppy_compat.py`)

- **Does:** resolves legacy `code_puppy.*` imports to `spruce_grove.*` —
  meta-path shim, appended so a real install wins.
- **Why it exists:** upstream-authored code and community plugins keep
  working unrenamed; the connector's porting path stays open.
- **Proper recreation:** this one *is* the bridge — the proper form is
  not replacement but **tightening**: module-level `DeprecationWarning`
  when shim-resolved imports come from outside our own tree, plus a
  coverage test asserting exactly which legacy names exist.
- **Exit criteria:** the upstream connector is retired or reworked so
  drop-in parity is no longer required (a council-unanimous call — see
  `SOVEREIGNTY.md` acceleration path, move 1).

## 4. `agent_code_puppy` module + `CodePuppyAgent` class

- **Does:** re-exports the grove agent under legacy names.
- **Proper recreation:** keep the re-export; add deprecation warnings;
  publish the grove-native names (`agent_spruce_grove`,
  `SpruceGroveAgent`) everywhere docs and examples live.
- **Exit criteria:** two release cycles after deprecation warnings ship,
  with no known consumer in the connector's reviewed set.

## 5. `get_puppy_name()` alias

- **Does:** legacy alias for `get_grove_name()`.
- **Proper recreation:** alias already delegates; add the deprecation
  warning; docs/examples migrated.
- **Exit criteria:** same as (4).

## 6. Persisted `puppy_name` config key

- **Does:** lets upgraded configs keep their pet name via fallback.
- **Proper recreation:** a **one-time migration writer**: on first run
  after upgrade, copy `puppy_name` → `grove_name` and mark the old key
  migrated (keep reading it as a fallback for downgrades).
- **Exit criteria:** migration writer shipped for a full cycle;
  telemetry-free check (config file scan is local-only) shows fallback
  reads trending to zero over a release or two.

## 7. `PUPPY_KENNEL_ROOT` env var

- **Does:** consumed by the external kennel plugin.
- **Proper recreation:** `SPRUCE_GROVE_KENNEL_ROOT` takes precedence;
  old var stays read-only during transition; docs updated.
- **Exit criteria:** kennel plugin reads the new var; old var documented
  as deprecated for two cycles.

## 8. `PURPLE_PUPPY` / `_PUPPY` in theme/spinner tests

- **Does:** names defined inside the external plugin bundle, referenced
  by our tests.
- **Proper recreation:** grove-owned theme constants; tests reference
  the new names with a compat assertion that the external names still
  resolve (so bundle drift is visible).
- **Exit criteria:** rides with contract (1).

---

## The rule that governs all eight

A compatibility contract is a promise to users, not to our nostalgia.
Recreate it properly, run both doors honestly, and close it only when the
evidence — not the calendar — says the promise has been kept a better way.
