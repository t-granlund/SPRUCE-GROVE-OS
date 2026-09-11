# Domain launch — sprucegrove.io (owner errand, ~15 min)

Status 2026-09-11: **sprucegrove.io is AVAILABLE** (RDAP 404, re-verified
post-1.0.0) and **priced, live from Porkbun's public API**:
`$28.12` first year / `$51.80` renewal (`.io` registry wholesale rose
industry-wide; ~$50/yr is the honest ongoing cost everywhere — Cloudflare
Registrar at-cost lands in the same renewal band). `sprucegrove.ai`: `$82.70`
flat — skip unless defending the brand later becomes worth it.

Recommendation: **buy `sprucegrove.io` at Porkbun ($28.12 today)**, enable
auto-renew + registrar lock. Cloudflare Registrar is the equally fine
alternative if you prefer your DNS and registration in one at-cost place.

## The errand

1. **Buy the domain** at any registrar (Cloudflare Registrar is at-cost and
   pairs well with Pages): search `sprucegrove.io`, checkout, enable
   auto-renew + registrar lock.
2. **Point DNS at GitHub Pages** (the announcement page already deploys to
   Pages as `announce.html` on every push to `main`):
   - `A` records for the apex (`sprucegrove.io`):
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `t-granlund.github.io`
3. **Tell Pages about the domain**: repo Settings → Pages → Custom domain →
   `sprucegrove.io` (leave "Enforce HTTPS" until the certificate provisions,
   then enable).
4. **Make the announcement page the site root** (one-line follow-up, do this
   when the domain is live):
   - In `.github/workflows/pages.yml`, copy
     `cp pages-hub/announce.html _site/index.html` — or better, decide
     whether the hub or the announcement is the public front door. Both stay
     reachable (`/announce.html` links everything).
   - Commit a `CNAME` file containing `sprucegrove.io` at the Pages root.
5. **Verify**: `curl -sI https://sprucegrove.io | head -3` → 200 from Pages,
   certificate issued (can take a few minutes to an hour after DNS).

## What the public sees, by URL (today)

| URL | Page |
|-----|------|
| `https://t-granlund.github.io/SPRUCE-GROVE-OS/` | hub landing |
| `.../announce.html` | **product announcement (1.0.0)** |
| `.../field-guide/`, `.../releases/`, `.../architecture/`, `.../design/`, `.../flat/` | docs |

After step 4, `https://sprucegrove.io` serves the announcement page and the
old URLs keep working under the domain.

## Not included in this errand

- Email on the domain (set up later; zero need at launch).
- `sprucegrove.ai` defensive buy (optional, decide post-launch).
