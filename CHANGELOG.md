# DuetCRM — Changelog

> Complete version history for DuetCRM. Mirrors the in-app changelog (visible in Settings or by tapping the version footer).
>
> **Current version:** `v1.12.3` · Updated 2026-04-30
> **Source file:** `~/.duet-server/DuetCRM.html`
> **Deployed to:** `https://smaxim-spec.github.io/duet/`

---

## v1.12.3 — 2026-04-30 — Pre-push verification for Won leads

- Pre-push verification when marking a lead Won: if **Agent / Premium / Product** is blank, prompts you to fill in before pushing to DuetBooks
- No prompt at all when all 3 fields are filled — zero friction in the common case
- Product dropdown auto-filtered by lead's interest category (life, annuity, IUL, banking)
- Agent dropdown includes "Solo (no split — 100% to me)" as the default option
- "Push anyway with blanks" escape hatch preserves old behavior if needed
- Email, phone, notes, age remain unverified (per spec)

## v1.12.2 — 2026-04-30 — Timestamp action IDs + deletion-aware merge

- Action item IDs now timestamp-based (`Date.now()`) — eliminates cross-device collisions when phone & laptop add items while offline
- **Deletion-aware merge:** action items removed/moved on one device now propagate to the other instead of being silently re-added
- Sticky-done preserved on conflicts: if either device marked an item complete, it stays complete on merge
- One-time data fix: re-IDed all 29 action items globally + cleaned John Raifstanger / Daisy Delgado mismatch

## v1.12.1 — 2026-04-30 — Action items sync between phone and laptop

- **Fix:** Action items now sync between phone and laptop (merge logic was silently ignoring `actionItems` on pull)
- Union by id with sticky-done: items added on either device propagate; if same item is marked done on one device, the done state wins on merge
- Also detects when an item is marked done on one device and syncs the change

## v1.12.0 — 2026-04-16 — Gmail → Action Item import (laptop only)

- **NEW:** 📧 From Email button on each lead's Action Items — imports action items directly from Gmail
- Shows recent threads (auto-filtered by lead's email if available)
- Extracts action text + due date from email using smart heuristics (action verbs, date phrases like "by Friday")
- Editable preview before saving — tweak text or date as needed
- Requires `duet_server.py` running locally (laptop only); first use will trigger Gmail OAuth consent

## v1.11.2 — 2026-04-16 — Priority-sorted Calley push

- Calley push is now priority-sorted: fresh (0-call) leads go to the **top** of Calley, 3+ attempt leads to the **bottom**
- Tie-breaker: newer leads first within same call count — so hot Salesforce leads get priority
- Push toast now shows the breakdown (e.g. "45 fresh, 22 @1call, 18 @2calls, 12 @3+calls") so you can see sorting worked

## v1.11.1 — 2026-04-16 — Coach Journal Firebase sync

- Coach Journal now syncs across devices via Firebase (was localStorage-only, causing phantom "days missed" on other devices)
- Journal entries merge by date+text — no duplicates across laptop & phone
- One-time migration pushes existing laptop journal entries to Firebase

## v1.11.0 — 2026-04-16 — Won lead → DuetBooks dual-write + Calley webhook

- **Fix:** Won leads now sync to BOTH `pipeline_2026` AND `duetbooks/steve_maxim/cases` paths — previously cases were falling through the cracks (Robin Menzies, Dorota Kalinowski)
- Dedupe check prevents double-adding on repeat Won conversions
- Unwrapped Firebase cases path back to raw array format DuetBooks expects
- **Calley Webhook receiver deployed** (Cloudflare Worker at `calley-webhook.smaxim.workers.dev`) — bypasses broken CallDetail API
- Coach Journal red/green indicator on dashboard — stays red persistently until journal entry made
- Red pulsing Journal button added to nav bar next to Call Queue
- Calley Reset & Re-Push now filter-aware — only resets leads matching current CRM view/stage
- Single Calley list workflow — excludes Bad #, Wrong Number, and invalid phones on push

## v1.1.0 — 2026-03-29 — Objections log + Git deployment

- Objections & Concerns log — track client pushback with category, response, and status (Open/Addressed/Resolved)
- Open objection count badge on CRM lead cards for quick visibility
- Response field auto-marks objection as Addressed when filled in
- Git-based deployment to GitHub Pages for easy phone updates

## v1.0.0 — 2026-03-29 — Annuity tools + Manager Report + versioning

- Annuity vs Annuity comparison tool with feature highlighting and HTML email generation
- CD to Annuity conversion tool with NEPQ framework and FL Medicaid info
- Illustration rate input system with saveable custom rates
- Product name standardization (GA renamed to MM / MassMutual Ascend)
- Manager weekly report now includes CRM statistics
- Agent name alias mapping for legacy data compatibility
- **App versioning system with changelog** (this very list)

## v0.3.0 — 2026-03-28 — Firebase + GitHub Pages

- Firebase Realtime Database sync (replaced Google Sheets)
- GitHub Pages hosting with PIN-protected mobile access
- Cloud backup system with rotation (keeps last 5)
- Appointment scheduling with Google Calendar integration
- vCard (.vcf) export for Google Contacts
- Gmail compose integration
- macOS LaunchAgent for auto-start server
- Data loss prevention safety checks on sync

## v0.2.0 — 2026-03-27 — Full CRM module

- Full CRM module with lead management (10 stages)
- 15-call cadence system with morning/afternoon/evening blocks
- Speed dialer with disposition tracking
- Daily call queue with priority scoring and briefing
- Funnel Health dashboard with stage distribution
- NEPQ discovery questionnaire (Annuity, Life, IUL, Banking)
- Stage-specific follow-up cadences (Connected/Discovery/Meeting/Quoted)
- Daily call goal set to 40 dials

## v0.1.0 — 2026-03-26 — Initial launch

- Sales pipeline dashboard with 2025/2026 year toggle
- Commission calculator with split agent handling
- Pay period tracking with YTD summaries
- Split agent management (15 agents)
- Book of Business view
- $100K net income goal tracker
- Year Summary with year-over-year comparisons
- Reports module with exportable weekly summaries

---

## Major themes by quarter

| Period | Focus |
|---|---|
| **Late Mar 2026** | Foundation — pipeline, CRM module, cadence system, Firebase sync, GitHub Pages mobile |
| **Mid Apr 2026** | Calley webhook integration, Won → DuetBooks dual-write fix, Coach Journal sync, Gmail-to-Action-Item, priority-sorted Calley pushes |
| **End Apr 2026** | Cross-device action item sync (collision-free IDs, deletion-aware merge), pre-push verification for Won leads |

## How to add a new version entry

1. Edit `~/.duet-server/DuetCRM.html` lines ~316–410 (the in-app `CHANGELOG` array). Add new entry at top.
2. Bump `APP_VERSION` and `APP_BUILD_DATE` (lines 316–317).
3. Mirror the entry into this file (insert at top under the current version header).
4. Run the standard deploy:
   ```bash
   cp ~/.duet-server/DuetCRM.html ~/.duet-server/index.html
   cp ~/.duet-server/DuetCRM.html ~/Desktop/Duet/DuetCRM.html
   cp ~/.duet-server/DuetCRM.html ~/Desktop/Duet/index.html
   cd ~/Desktop/Duet && git add DuetCRM.html index.html CHANGELOG.md && git commit -m "vX.Y.Z: <one-line summary>" && git push
   ```
5. Verify it's live: `curl -s https://smaxim-spec.github.io/duet/ | grep "APP_VERSION"`

## Known issues / open items

- **`firebaseLoadAll` merge bug** — sometimes returns `pulled=false` even when cloud has newer data, leaving laptop's localStorage stale. Workaround: hard refresh (Cmd+Shift+R) or run a one-liner to manually pull pipeline data.
- **Past Manager Weekly Reports** — currently no way to re-run a report for a past week. Plan drafted for Phase 1 (week selector dropdown) + Phase 2 (snapshot archive).
- **DuetBooks sync direction** — DuetBooks is source of truth; CRM's pipeline_2026 view doesn't auto-pull DuetBooks edits made post-submission. Manual workaround works; auto-sync planned.
