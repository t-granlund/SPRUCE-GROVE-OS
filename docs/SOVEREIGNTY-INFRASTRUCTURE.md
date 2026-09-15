# SOVEREIGNTY INFRASTRUCTURE — the migration runbook

> **STATUS: DRAFT — awaiting council approval.** This runbook moves
> Spruce Grove OS to fully grove-owned infrastructure: a pseudonymous
> steward identity, domain control, source control outside corporate
> platforms, and dependency ownership. Every step is reversible until the
> final cutover is approved. Per `GOVERNANCE.md`, infrastructure decisions
> require unanimous council sign-off plus a rollback plan.

---

## 0. The honesty preamble — read before anything else

Two truths the Gate requires on the record:

1. **Pseudonymity forward ≠ anonymity of the past.** The current repo
   history carries author identities and corporate emails; the public
   manifesto carries a name; domain registration history is archived by
   third parties; public snapshots exist. A new steward identity makes
   the *future* clean; it cannot unwrite the past. Anyone claiming
   otherwise is selling something. What it DOES achieve: going forward,
   the infrastructure, the domains, and the releases belong to an
   identity with no personal trace — no corporate email, no employer
   tie, no single-person dependency.
2. **Owning it all means patching it all.** Self-hosting moves the
   supply-chain risk from "big vendor's pipeline" to "our pipeline."
   The great registry incidents of recent years (dependency worms,
   hijacked packages, social-engineered releases) hit *open, unreviewed
   supply* — the defense is not ownership alone but ownership **plus the
   Gate**: hash-pinned locks, allowlisted dependencies, counsel review,
   and more than one person holding keys. A bus-of-one with root on a
   box is less secure than what we have today. The council model is what
   makes this work.

---

## 1. The steward identity (Phase A — TYLER executes)

- [ ] **Dedicated steward email** on a privacy-respecting provider or on
  the grove's own domain mailbox (Phase B). Never reused anywhere else.
- [ ] **Password manager** with a shared steward vault. Two-person access
  from day one.
- [ ] **Hardware security keys ×2 per steward** (FIDO2). Registrar,
  email, repo host, and CI all bind to these. No SMS anywhere — SIM
  swaps are the oldest attack there is.
- [ ] **Recovery kit**: sealed offline document (vault master password,
  recovery codes, account inventory) held by both stewards in separate
  physical locations.
- [ ] Choose the identity name: unrelated to any person, place, or
  employer; short; available as a handle everywhere. It will appear in
  git history, registry metadata, and certificates forever.

## 2. Domains (Phase B — TYLER executes, COUNCIL approves)

- [ ] **Inventory every domain** and its current registrar/account.
- [ ] **`sprucegrove.io`** → transfer into the steward registrar
  account. Prefer a registrar built for privacy (the kind that registers
  domains in its own name on your behalf) or an established registrar
  with full WHOIS privacy enabled. Pay from the steward payment rail.
- [ ] **`tylergranlund.com`**: a domain with a personal name in it cannot
  be made anonymous — the name is the asset. Council decision: keep it
  personal (fine — it just never touches the project), or drop it at
  renewal. It must not become project infrastructure either way.
- [ ] **DNS hosting** on the steward account; enable DNSSEC; document
  every record in the vault.
- [ ] Honest limits: certificate transparency logs will show
  `sprucegrove.io` (that's the domain, not the person — fine); historical
  WHOIS/DNS records pre-dating the transfer may persist in third-party
  archives.

## 3. Source control off the corporate platform (Phase C — COUNCIL approves)

Dual-home first; never a cliff:

- [ ] **Stand up Forgejo** (self-hosted, own VPS or own hardware) on the
  steward identity. Migrate repos, issues, releases, and labels with the
  migration tooling; verify.
- [ ] **CI: Woodpecker** (self-hosted) wired to Forgejo. Port both
  workflows (publish + pages) and prove a full release + site deploy
  runs green on the new rails before anything changes hands.
- [ ] **GitHub becomes a frozen read-only mirror** — announced as such,
  synced one-way for a transition window. The public URL everyone
  bookmarks keeps working.
- [ ] **Pages → Caddy** on the steward VPS serving the same `_site`
  artifact the workflow already builds; certificates via Let's Encrypt.
  Same bytes, new rails.
- [ ] **PyPI strategy** (council decision, both options are legitimate):
  (a) keep publishing to the public index from grove-owned CI — reach
  and `uv tool install` for everyone; (b) additionally host a grove
  wheel index on the steward infra and document the flag. The lockfile
  (`uv.lock`) already hash-pins every artifact either way — that is the
  supply-chain defense that works *today*.
- [ ] **Handover**: repo ownership transfers to the steward account/org
  on each platform; the historical account steps back to a mirror role,
  then retires from project duties entirely.

## 4. Build & runtime tooling (Phase D — COUNCIL approves)

- [ ] **Node removal from CI** — the one npm-adjacent tie (a stats
  injection step in the pages build) is replaced with stdlib Python in
  this same change set. After that: zero `node`, zero `npm` anywhere in
  build, test, or release.
- [ ] **Docker audit**: the CLI runtime has zero container dependencies;
  colima/docker on dev machines is personal tooling, not a project tie.
  Documented so nobody re-adds one.
- [ ] **Dependency ownership policy**: allowlist + hash-pinned lockfile
  (in force), quarterly `pip-audit` pass in council, and the vendor-
  don't-sync rule from `LIVING-UPDATES.md` (debt with a name and a date).
- [ ] **Reproducible releases**: same commit → same wheel hash, proven
  in CI, published beside every release.

## 5. What stays true no matter where this runs

- The five Gate criteria, the wall, and the council (see
  `GOVERNANCE.md`).
- The connector stays read-only, gated, and company-free on public
  surfaces.
- The observatory keeps publishing receipts — from grove rails.
- Backups: 3-2-1 (repos, domain config, vault) — the insurance mirror
  tradition continues under the steward identity.

## 6. Execution order & the wall

```
Week 1   steward identity + vault + keys (Tyler)  → council verifies
Week 1-2 sprucegrove.io transfer + DNS (Tyler)    → council verifies
Week 2   Forgejo + Woodpecker + Caddy up (pair)   → dual-home proof run
Week 3   full release + site deploy on new rails  → council sign-off
Week 4   GitHub → frozen mirror; ownership handover → council sign-off
         CODEOWNERS steward handles live; wall fully armed
```

Nothing in this runbook executes without its council checkmark. The
infrastructure IS a release: it passes the Gate like everything else.
