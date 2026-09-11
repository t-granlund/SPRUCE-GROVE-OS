# Domain launch — sprucegrove.io (owner errand, ~15 min)

Status 2026-09-10: **sprucegrove.io is AVAILABLE** (RDAP 404, re-verified
evening of the 1.0.0 release). `sprucegrove.ai` could not be conclusively
probed (the .ai registry's RDAP redirects; DNS shows no NS records, which
suggests unregistered but is not authoritative). Recommendation: **buy
`sprucegrove.io`** — cheaper per year, reads cleanly, and the .io TLD is
native to developer tools. Add `sprucegrove.ai` later only if the product
gains traction worth defending (defensive registration is optional, not
launch-blocking).

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
