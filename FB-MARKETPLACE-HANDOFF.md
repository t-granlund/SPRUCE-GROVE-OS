# FB Marketplace Handoff — from Code-Puppy session 2026-09-10 (~11:50 PM)

> **UPDATE 2026-09-11 ~12:40 PM:** Peloton is LIVE (item 28856332870641241, in review).
> Weber/Colamy/Mower/Alienware are BLOCKED by FB's posting rate limit — resume steps,
> proven mechanics, and cleanup checklist live in `FB-RESUME-2026-09-11.md` (this folder).

## Mission
Post 5 items to Facebook Marketplace (account: Tyler Granlund, fresh burner-adjacent
profile per `facebook-setup-runbook.md`). Photos from iPhone dumps, listing copy from
voice memos, prices researched. Peloton FIRST (the others follow the same pattern).

## Asset map (everything lives in /Users/tygranlund/dev/RESALE-STUFF)
- Transcripts: `product-details-1-transcript.txt`, `product-details-2-transcript.txt`
  (source: `Product-Details-1.m4a`, `Product-Details-2.m4a`, transcribed with mockingbird)
- Listing copy (FB + Craigslist variants, one file per item): `listings-fb/*.txt`
- Photos (originals, HEIC+jpg): `resale/photos/<Item>/`
- FB upload staging: `resale/photos/__fb-staging/<item>/` (jpg-only)
- **PELOTON ORDERED SET (use this):** `resale/photos/__fb-staging/peloton-ordered/01.jpg`–`10.jpg`
  Order per listing doc: 01=IMG_0152 hero, 02=IMG_0150 "Activate your Bike+" trust shot,
  03=IMG_0140 shoes+box, 04=IMG_0144 w36 shoes, 05–10 = 0145–0151.
- Desktop symlink for drag & drop: `/Users/tygranlund/Desktop/peloton-listing-photos`
  (DELETE after done — cleanup)
- Clipboard convenience texts: `/tmp/listing-title.txt`, `/tmp/listing-description.txt`
- Product pages (linked in listing descriptions): `resale/site/*.html` → tylergranlund.com/resale/site/*

## Peloton listing (fill exactly)
- Photos: all 10 from peloton-ordered (in numeric order = intended display order)
- Title: `Peloton Bike+ — Factory Reset — Full Bundle: 2x Shoes, HR Band, Dumbbells, Mat`
- Price: 549
- Category: Sporting Goods  (copy says Exercise & fitness — FB UI shows "Sporting Goods")
- Condition: **Used - Like New**  (FB has no "Used - Excellent" for items)
- Description: body from `listings-fb/peloton-fb-marketplace.txt` (also `/tmp/listing-description.txt`)
- STOP after filling / before Publish unless user says otherwise.

## Current browser state (messy, clean up first)
- Chrome has TWO windows on `facebook.com/marketplace/create/item` + a Mazda tab +
  Spruce Grove tab. Keep ONE create window, close extras (there's also a stray
  460x279 popup window and possibly a leftover NSOpenPanel).
- One phantom Mail compose window may exist titled "(8) Create new listing | Facebook"
  — close it, DELETE draft (do not send!). Notion AI popup may be open; Escape it.
- FB form is EMPTY: Photos 0/10, no title/price. Fresh canvas. 
- Two earlier junk photos (YO BOI meme + Illuminating Concepts doc) were removed —
  do NOT re-add anything from photos/ root.

## Automation mechanics that WORK (and what broke)
Working dir tools already built (durable copies in
`/Users/tygranlund/dev/RESALE-STUFF/fb-automation/` — use those, /tmp copies may vanish):
- `/tmp/focus-fb.applescript` — activates the Chrome tab whose URL contains marketplace/create
- `/tmp/drive_fb_full.py`, `/tmp/drive_fb_photos.py` — Quartz CGEvent drivers
  (click/key/paste helpers; process IS Accessibility-trusted)
- Window capture for verification: `screencapture -l<CGWindowID> -x out.png`
  (get IDs via Quartz.CGWindowListCopyWindowInfo; captures window even when occluded!)
- AppleScript tab/URL control works great:
  `tell application "Google Chrome" to get/set URL of active tab of front window`, `loading of active tab`

What BROKE and why:
1. **Synthetic MOUSE CLICKS do not register inside the NSOpenPanel** (Chrome's file picker)
   or its "Go to Folder" sheet. Clicks on normal web pages work fine.
2. **Synthetic Return does not work in the Go-To sheet** either (clicks there just
   re-fill the path field; recents rows behave same).
3. KEYBOARD with modifiers WORKS in the panel: Cmd+V paste, Cmd+A select-all,
   Cmd+Shift+G, Cmd+Shift+D (Desktop shortcut), type-ahead file selection, Cmd+Down,
   Cmd+O confirm. → **Use a keyboard-only panel flow** (recommended):
   Add photos (mouse click on page = fine) → Cmd+Shift+G → paste path → then:
   ESC first if stale sheet, Cmd+Shift+D Desktop, type-ahead `peloton-listing-photos`,
   Cmd+Down, Cmd+A, Cmd+O.
4. **FOCUS WARS ARE THE REAL BOSS FIGHT.** Cedar/Spruce Grove desktop builds +
   Tauri app launches steal keyboard focus mid-sequence (a Mail share draft and
   Notion AI popup were spawned by stray keys). BEFORE driving UI:
   pause/quiet the other agent (Cedar) or wait for its build loop to settle, and
   ask user for 5 hands-off minutes. Verify frontmost app = Google Chrome before
   EVERY key batch (System Events: `name of first process whose frontmost is true`).
5. User/Chrome instability: Chrome got quit/closed 3× mid-flow. Session restore
   brought the create tab back, but check before clicking.

## Remaining work (priority order)
1. Cleanup stray windows/popups; verify Chrome frontmost + create tab active.
2. Peloton: upload 10 photos, fill all fields, verify, STOP at Next (no Publish
   without explicit user approval).
3. Then same loop for: Weber grill $275 (7 photos) → Colamy chair $75 (9) →
   Craftsman mower $99 (2) → Alienware AW3423DWF $325 (3, incl Specs.png).
   Copy in listings-fb/*.txt; photos in __fb-staging/<item>/.
   Consider numbering staging files 01..NN like peloton-ordered for correct order.
4. NOT YET: MacBook (see macbook-fb-marketplace.txt + MacBook-Air-Specs.md) —
   no photos yet; needs its own shoot.
5. Cleanup: remove Desktop symlink, kill /tmp scripts when done.

## Suggested first prompt for Spruce Grove CLI
(includes self-sufficiency: rebuild /tmp scripts if missing)

"Read /Users/tygranlund/SPRUCE-GROVE-OS/FB-MARKETPLACE-HANDOFF.md fully and execute
the 'Remaining work' section, starting with the Peloton listing. All context, copy,
photos, and known-good automation mechanics are in that file. Key rules: verify
Chrome is frontmost and the marketplace/create tab is active before EVERY input
batch; use keyboard-only flow inside the file picker (mouse clicks don't land on
NSOpenPanel here); never click Publish without asking me; stop if the user starts
typing in Chrome. Ask for a hands-off window before you start driving the UI."
