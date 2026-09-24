# The anonymity exit — separating project identity from personal identity

Companion to bead `SPRUCE-GROVE-OS-r8c`. Written 2026-09-23 after an
independent audit of every tracked file (see the method at the end).

The pivot decision already exists — commit `bcc846c` (2026-09-18):
**"public surfaces show seats, not names — persons generalized, stories
kept."** Business names and details stay, per the stated policy. This document
covers what the pivot did *not* reach.

## The scope is 74 files, not 3

The bead lists three residues. A full scan of tracked files finds **320 lines
across 74 files**, and the bead's three items are not the most serious ones.
Ranked by real exposure:

| Rank | Surface | Why it outranks the bead |
|---|---|---|
| 1 | **git commit authorship** | Every commit is public, and `publish.yml` calls `gh release create --generate-notes`, which renders commit authors onto the public Releases page. No file edit fixes this; it is a git-identity setting. |
| 2 | **`.github/CODEOWNERS`** (10 lines) | This is an *active GitHub mechanism*, not text. `@t-granlund` (a personal account) is the sole required reviewer on every path, including the security-critical list. |
| 3 | **Model-facing system prompt** (`spruce_grove/agents/agent_spruce_grove.py:139`) | Ships in the wheel: *"…a custom grove planted by Tyler Granlund"*. Every user who asks the bot about its origins receives the name. |
| 4 | **`NOTICE:2`** | `Copyright 2026 Tyler Granlund` — the legally operative line for an Apache-2.0 distribution. |
| 5 | `TRADEMARKS.md:39` | Names the personal email as the takedown contact. |
| 6 | `SESSION-HANDOFF.md` | Tracked, public, 20 hits, plus infra/account detail. |
| 7 | **Generated artifacts** | `docs/field-guide/data.js` bakes in the absolute home path; `_site/**` is copied by CI from `pages-hub/**`, so editing `_site` directly is futile — fix the source. |
| 8 | `pyproject.toml` | What the bead leads with. Real, but cosmetic: a PyPI sidebar field. |
| 9 | Long tail | `BUILD-LOG.md` (16), `mission-control.html` (13), `docs/SOVEREIGNTY-EXECUTION.md` (10), `SOURCITY.md` (8), and ~60 more. |

## Two framing corrections

**`authors` is not the crux.** Setting it to an organisation name changes a
sidebar label. It leaves the copyright line, the shipped prompt, and the
release notes naming a person. Fixing it alone would look like progress while
changing nothing of substance.

**`authors` is not "the maintainer alone" either.** It already carries two
entries, and `Michael Pfaffenberger` **must stay** — that is upstream
Code Puppy attribution, not exposure. Any guardrail that flags his name is
wrong.

## Verified externally

- **PyPI bakes metadata into artifacts permanently.** Author/email live in
  each wheel's and sdist's `.dist-info/METADATA`. There is no edit-in-place;
  a yanked release keeps its original metadata in files already downloaded.
  PEP 440 gives *yank*, never delete. **Remedy is forward-only**: correct
  metadata takes effect from the next release.
- **`git filter-repo` is the current tool** (`filter-branch` is deprecated).
  But the guidance is to treat committed personal information as *permanently*
  in the object store: clones, forks and cached views may retain it after a
  force-push.
- **For non-credential personal data, forward-fix is defensible.** A name, an
  email and a domain are not secrets. `docs/SOVEREIGNTY-INFRASTRUCTURE.md`
  already states the honest limit: pseudonymity forward does not equal
  anonymity of the past.
- **Precedent exists** for an org identity in packaging metadata, e.g.
  `maintainers = [{name = "argparse-dataformat", email = "dev@argparse-dataformat.com"}]`.

## Recommendations

**A. `authors` → steward identity, upstream credited.** PEP 621 `authors` is
free text; `name` and `email` are each optional.

**B. Email: omit rather than invent.**  **Verified 2026-09-23:
`sprucegrove.io` has no MX records** — it serves the site via GitHub Pages but
cannot receive mail. Publishing a `stewards@sprucegrove.io` address would put a
bouncing contact in permanent package metadata, which is worse than none. The
options are (1) stand up a real mailbox first, then publish it, or (2) omit
the email — valid per PEP 621, harmless to tooling, losing only a contact
channel. **This is a decision for the steward, not for an agent to guess.**

**C. URLs → the project site.** `Homepage` should be `https://sprucegrove.io`,
not a personal domain. Add `Repository`, `Issues`, `Changelog`, `Documentation`.

**D. `SESSION-HANDOFF.md` → forward fix, not history rewrite.** Delete from
HEAD, gitignore it, and move durable content to its proper homes: a name-free
`docs/SESSION-START.md` pointing at the board, with operational detail going to
beads (already gitignored). **Reject the history rewrite**: the history is
public, mirrored and forked; rewriting would invalidate every `v1.0.x` tag,
break `publish.yml`'s version derivation, desync forks, and buy zero
recoverable anonymity. The sdist ships only `spruce_grove/` plus two
`models.json` files, so this file never reached PyPI — the exposure is
GitHub-only, which forward-fix fully covers.

**E. Order of operations.** `publish.yml` triggers on push to `main`;
`ci.yml` triggers on `pull_request`. **PRs do not publish.** So the whole
identity change must land as *one* PR, merged once, producing one consistent
release. Prerequisites that are not file edits: configure the repository's git
identity to a steward name (otherwise every future commit re-leaks and
`--generate-notes` republishes it), and decide the `NOTICE` copyright-holder
label. **Irreversible**: every published PyPI version is permanent, and the
git history is already effectively public.

## The guardrail

`tests/test_anonymity_audit.py` encodes the pivot policy as a test. It sits in
`tests/`, which `publish.yml` already runs in full before the version bump, so
a regression **blocks the release**.

It is a **denylist** — deliberately. A 74-file, 320-line cleanup cannot be
completed in one pass without inventing policy about the long tail, so the
audit starts where it can be honest: hard-failing on the surfaces that matter
today (packaging metadata, tracked private files, the shipped prompt, the
copyright line, `CODEOWNERS`) while recording the rest as a shrinking backlog.
`docs/field_guide_changelog.py` and its test are allowlisted, because that
module must *contain* the name in order to redact it.

Self-ratcheting: as surfaces are cleaned, add their globs to the strict set.
The backlog count is the progress meter.

## Method

Reproduce the audit: scan every `git ls-files` entry (skipping binaries) for
`(?i)\b(tyler|granlund)\b|tylergranlund\.com|hello@tylergranlund\.com`. The
scan counts what is *tracked*, which is what is *public*.
