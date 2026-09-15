# LICENSE ANALYSIS — Apache-2.0 vs MIT for the Grove

> Working research document for pre-prod launch. The question: does the Grove's
> license actually stand its ground when a bad actor takes the work, strips the
> story, and sells it as their own? What can each license do, what can't it,
> and what does the law actually give us.
>
> **This is research, not legal advice.** Before final rollout with real stakes,
> one session with an IP attorney. Everything below is verifiable law and
> license text; the judgment calls are flagged as judgment calls.

---

## 0. Ground truth (verified 2026-09-15)

| Repo | License | Copyright line | NOTICE file |
|---|---|---|---|
| `code_puppy` (upstream) | MIT | (c) 2025 Mike Pfaffenberger | none |
| `SPRUCE-GROVE-OS` | MIT | (c) 2025 Mike Pfaffenberger **only** | none |
| `spruce-grove-desktop` | MIT | (c) 2026 Tyler Granlund | none |
| `leather-apron-club` | **none** | — | — |

Three findings that matter before any rollout:

1. **The OS LICENSE carries only Pfaffenberger's line.** Tyler Granlund's
   2026 authorship is not on it. The lineage is honest in git history but
   invisible in the legal artifact.
2. **No NOTICE files anywhere.** Under Apache-2.0 that file is the
   traceability backbone. Under MIT it is simply absent — nothing forces a
   story to travel with the code.
3. **The club site is unlicensed** → default all-rights-reserved. Nobody may
   legally reuse the creed, the standing questions, or the method. For a
   movement that wants its words to spread, that is backwards.

---

## 1. The two licenses, in plain words

### MIT — one sentence of duty

> Keep the copyright notice and permission notice "in all copies or
> substantial portions of the Software."

That is the *entire* obligation. No requirement to mark what you changed. No
NOTICE file. No patent grant. You may rebrand, sell, close, and ship — as long
as a copy of the notice rides along *somewhere* in the copies or substantial
portions.

**Where it leaks:**
- "**Substantial portions**" is undefined. Take a small-but-decisive slice,
  and a bad actor argues in good faith that no notice was owed at all.
- **Distribution-triggered only.** Run the code as a hosted service and never
  distribute a copy — no notice is ever owed to anyone. The most common
  modern rip (SaaS on someone else's work) never even triggers MIT's one term.
- **Rebranding is legal by design.** New name, new logo, notice buried in a
  tarball nobody opens. Fully compliant. Nothing about *accountability*.

### Apache-2.0 — four duties and a shield

Section 4 requires a recipient to:

- **(a)** pass along the license;
- **(b)** carry **prominent notices on modified files** stating that they
  changed them;
- **(c)** retain **all copyright, patent, trademark, and attribution notices**
  from the source;
- **(d)** if a **NOTICE file** exists, include a readable copy of it — in the
  distribution, source, docs, *or generated display*;
- **(e)** not use the licensor's **trademarks** (explicit).

Section 3 adds the differentiator: every contributor **grants users a patent
license** for their contributions — and that grant **terminates** if the user
sues over patents alleging the Work infringes. The defensive-termination
clause. MIT says nothing about patents at all; an implicit license exists in
some doctrines and is contested in others.

**The practical difference:** Apache builds a *paper trail through the rebrand*.
A bad actor must affirmatively delete the NOTICE text and the change-markers to
hide the lineage — and deliberate deletion of copyright/attribution information
is a separate legal claim (below). MIT's single buried notice gives no such
tripwire.

---

## 2. The bad-actor playbook — and what each license does about it

| The play | What he does | MIT response | Apache-2.0 response |
|---|---|---|---|
| **The Rebrander** | rip, rename, ship as his product | Compliant if the notice hides somewhere in the package. Accountability: none. | Must keep NOTICE readable and mark changed files. Removing them → license breach **and** a §1202 claim. |
| **The Stripper** | delete headers/credits, keep the code | Breach of the notice condition → copyright claim; header deletion can be CMI removal (§1202). Hard to prove *intent*. | §4(c) breach is cleaner to prove; NOTICE deletion is a bright-line §1202 fact pattern. |
| **The Cloud Host** | run it as SaaS, never distribute | **Nothing.** No distribution = no trigger. | **Same.** This is the gap in *both* — only AGPL-style terms reach it (at real adoption cost). Mitigate with trademarks, speed, and public works instead. |
| **The Patent Ambusher** | contribute nothing, sue the users | No grant. Users rely on contested implicit-license theories. | Explicit §3 grant shields users; suing the Work's users **terminates** the ambusher's own license. |
| **The Name Thief** | clone the name and the mark | License is silent; trademark law applies (don't count on license text). | §4(e) expressly withholds marks — plus trademark law. Still: **register the marks**, the license alone is not a shield. |
| **The Fork-and-Close** | take it proprietary | Allowed. Permissive licenses permit this by design. | Allowed too. The answer is speed, community, and the NOTICE trail — not the license. |
| **The Silent Servant** | uses it internally, never credits | Legal. And fine — the Grove wants use; credit obligations attach to *redistribution*, not to use. | Same. |

The honest read: **neither license stops a determined actor from taking the
code.** The difference is what evidence exists *after* he does — and which
extra legal hooks his cleanup creates.

---

## 3. The law behind standing your ground (US; the club is Bentonville)

- **Copyright infringement** — 17 U.S.C. § 501. Breach of an open-source
  license's *conditions* is infringement, not mere contract breach:
  *Jacobsen v. Katzer*, 535 F.3d 1373 (Fed. Cir. 2008) — attribution-style
  conditions are enforceable copyright conditions. Open-source licenses are
  also enforceable as contracts (*Artifex v. Hancom*, 9th Cir. 2020).
- **Registration is the force multiplier** — 17 U.S.C. § 412: register before
  the infringement (or within 3 months of publication) and statutory damages
  reach **up to $150,000 per work for willful infringement** (§ 504(c)) plus
  attorney's fees (§ 505). Unregistered: actual damages and profits only —
  usually less than the lawyer. **Practical: register the major releases.**
- **DMCA § 1202 — the attribution-stripping hook.** Copyright Management
  Information includes the identifying information and the terms that travel
  with a work in electronic form. Intentionally removing or altering CMI,
  knowing it will induce, enable, or conceal infringement: civil statutory
  damages of **$2,500–$25,000 per violation** (§ 1203), and criminal liability
  for willful commercial advantage (§ 1204 — up to $500,000 / 5 years, first
  offense). § 1202 is a separate cause of action; its damages do not hinge on
  copyright registration. This is the claim that fits "he ripped out our
  names" — and the NOTICE-based Apache structure makes the removal
  intentional-looking rather than accidental.
- **DMCA § 512 takedowns** — the cheap, fast lever against GitHub repos, app
  stores, and hosts. Use it for clear cases; counter-notice rules (§ 512(g))
  punish abusive filings.
- ***Dastar Corp. v. Twentieth Century Fox*, 539 U.S. 23 (2003)** — a warning
  shot: you generally **cannot** use the Lanham Act as a backdoor
  "attribution" claim for copying creative works; that ground belongs to
  copyright law. Trademark law still fully protects **names and marks**
  ("Spruce Grove," the TreeMark, "Code Puppy," "The Leather Apron Club") —
  but only if they are asserted and ideally **registered**. The license texts
  themselves grant no trademark rights.
- **SaaS reality** — no permissive license reaches internal/hosted use. If the
  fear is a hosted rip, the honest options are: AGPL-3.0 for the pieces that
  matter (with its adoption costs), trademark enforcement on service names,
  and out-shipping him in public.

---

## 4. Attribution, accountability, and not being a twat

A license governs copies. It cannot govern conscience. Accountability for the
Grove is a *stack*, and the license is one layer of it:

1. **The NOTICE file carries the lineage.** Whatever license is chosen, the
   Code Puppy ancestry is written into NOTICE verbatim: Pfaffenberger's MIT
   notice and copyright stay for the inherited code (legally required under
   MIT's own terms, and the Grove's ethos requires it regardless). "Inspired
   by and built from" becomes a legal artifact, not a README sentiment.
2. **PROVENANCE as a first-class file** — the Grove already practices this
   (FACTCHECK.md, recorded lineage, git history as receipts). Formalize it:
   who made what, from what, when. Git history is the deepest receipt there
   is; it survives rebrands unless someone rewrites it, and rewriting is
   itself evidence.
3. **A covenant, not just a license.** The club's creed — fair, honest, true;
   don't be a twat — belongs in a Code of Conduct (Contributor Covenant or
   the club's own words) referenced by CONTRIBUTING. Norms do the daily work
   law does only in the worst week.
4. **Register what matters.** Copyright registration for major releases
   (cheap, per-work, unlocks statutory damages), trademark applications for
   the names and marks (TEAS, few hundred dollars per class). Unregistered
   rights are real but weak.
5. **Release provenance hardening** — signed tags, and (worth evaluating)
   artifact attestations on PyPI/github releases so "is this build really
   theirs" has a cryptographic answer.
6. **Public works.** The club's receipts culture — visible builds for named
   neighbors — is the strongest anti-rip force there is: a thief can copy the
   artifact, never the standing relationship with the people who watched it
   get made.

---

## 5. Decision matrix

| Criterion | Keep MIT | Move code to Apache-2.0 |
|---|---|---|
| Attribution travels with rebrands | Weak (one buried notice) | **Strong** (NOTICE §4(d) + change-markers §4(b)) |
| Patent posture for the builder community | None explicit | **Explicit grant + defensive termination** |
| Strip-the-headers enforcement hook | Breach + contested §1202 | Breach + **bright-line §1202** |
| Trademark clarity | Silent | **Explicit §4(e) reservation** |
| Adoption friction | **Lowest** (corporate default comfort) | Modest (lawyers ask about NOTICE duties) |
| Copyleft compat (if ever needed) | MIT code can move anywhere | Apache code can move anywhere except GPLv2-only |
| Matches the mission's words | Partly | **Closer**: accountability is built into the artifact |
| SaaS rip protection | None | None (AGPL would be the separate lever) |

**Recommendation (judgment call, flagged as such):**

1. **Move the code repos (SPRUCE-GROVE-OS, spruce-grove-desktop) to
   Apache-2.0**, with a NOTICE file that (a) carries the Grove's own
   attribution and (b) preserves Pfaffenberger's MIT notice for the Code
   Puppy lineage, verbatim. Add Tyler's 2026 copyright line to the LICENSE —
   currently missing entirely. This is the configuration where ripping the
   work *creates evidence of the rip*.
2. **Keep `code_puppy` upstream exactly as it is** (MIT, Pfaffenberger).
   Upstream's license is upstream's to govern; the Grove honors it and says
   so in NOTICE.
3. **License the club's content under CC BY 4.0** — attribution built into
   the license itself for the creed, the standing questions, the method, the
   pages. Keep the names/marks as trademarks, not licensed content.
4. **Add a TRADEMARKS.md**: names and marks are not covered by the license;
   community use of the creed is welcome, branding is asked about first.
5. **Register**: copyright for major tagged releases; trademarks for the
   Grove names/marks when rollout is real.
6. **Attorney pass** before final rollout — one session to bless the
   relicense path and the NOTICE text. Flagged as a launch prerequisite.

### What the Apache move changes, concretely

- `LICENSE` → Apache-2.0 text (with Tyler Granlund 2026 + lineage note)
- `NOTICE` → Grove attribution + Code Puppy lineage (MIT notice preserved)
- `pyproject.toml` → `license = "Apache-2.0"`, classifier updated
- README badge + release notes relicense entry
- Desktop repo same treatment
- Club repo: CC BY 4.0 in a LICENSE file + TRADEMARKS.md

---

## 6. Standing-your-ground playbook (when it actually happens)

0. **Before anything**: the paper trail exists (git history, NOTICE,
   PROVENANCE, registered copyrights, marks). The fight is won in setup.
1. **Preserve evidence immediately** — archive the infringing pages, hash the
   repos, screenshot with timestamps.
2. **The polite letter first.** Most rips are carelessness, not malice. A
   short notice with the lineage and a 7-day cure window costs nothing and
   makes the later record look reasonable. *Be kinder than necessary — and
   put it in writing.*
3. **DMCA § 512 takedowns** to the host/repo/app-store. Fast, cheap,
   effective for clear cases.
4. **The § 1202 claim** rides along in any infringement complaint: he did not
   just copy — he *removed the names*, knowingly. That is the twat-tax, in
   statutory-damage form.
5. **If registered**: statutory damages up to $150k/work (willful) + fees.
6. **Community light**: state the facts, publicly, without slander. The club
   watches its own. Facts only — the receipts are strong enough.

---

## 7. Next-step checklist

- [ ] Decide: Apache-2.0 (recommended) vs stay MIT — Tyler's call
- [ ] Attorney session to bless relicense + NOTICE text (launch prerequisite)
- [ ] Draft NOTICE with full lineage (Pfaffenberger MIT notice verbatim)
- [ ] Add Tyler's 2026 copyright to every Grove artifact that lacks it
- [ ] TRADEMARKS.md + shortlist of marks to register (Spruce Grove, TreeMark,
      Leather Apron Club; Code Puppy belongs to upstream)
- [ ] CC BY 4.0 for club content; un-license the site's current limbo
- [ ] Copyright registration cadence for tagged releases
- [ ] Code of Conduct wired into CONTRIBUTING (the covenant layer)
- [ ] Revisit the SaaS question: AGPL for which pieces, if any — explicit
      decision, even if the decision is "not now"
