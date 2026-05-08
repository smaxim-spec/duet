# DuetCRM — Changelog

> Complete version history for DuetCRM. Mirrors the in-app changelog (visible in Settings or by tapping the version footer).
>
> **Current version:** `v1.16.4` · Updated 2026-05-07
> **Source file:** `~/.duet-server/DuetCRM.html`
> **Deployed to:** `https://smaxim-spec.github.io/duet/`

---

## v1.16.4 — 2026-05-07 — Weekly Report "All Open Cases" reads from DuetBooks

Diane Lawson was showing as Issued in the report's "All Open Cases" section even though DuetBooks had her as Paid (2026-04-30). Root cause: that section reads from the CRM's local `pl` mirror, which only ever gets data pushed *into* it (from `convertToPipeline`) — DuetBooks status updates never flowed back, so `pl` stayed frozen.

- Report now fetches `/duetbooks/steve_maxim/cases.json` on every `genReport` call and uses it as the source of truth for "All Open Cases"
- Falls back to `pl` if the fetch hasn't completed yet (prevents flicker)
- Auto re-renders the report once if DuetBooks status snapshot differs from the previous render (only re-renders on actual change — no loops)
- Open filter also excludes `paid-partial` and `declined` (was only excluding `paid`)

---

## v1.16.3 — 2026-05-07 — Weekly Manager Report rebuild (Phase 3 of 3)

Closes the two-status refactor. The Weekly Manager Report gets a new top-section "🆕 Won Activity This Week" — flat table with both Opportunity and Policy explicit per row. Activity-based: rows naturally drop off the report once they're settled, so the manager sees only what changed (not a stale snapshot of every Won lead ever).

**Filter rule** — row appears when, in the report week (Fri-Thu):

- `stage` went to Won (`stageEnteredDate` in window)
- `stage` went to Lost (`stageEnteredDate` in window)
- `policyStatus` changed (`policyStatusChangedDate` in window)
- A `DECLINE: ...` historyNote was added

**Columns:** `Client | Premium | Product | Agent | Opportunity | Policy | Change | Notes`

The `Notes` column auto-populates with the most recent decline reason from `historyNotes` when `policyStatus = declined` — so manager sees "Carrier — health rating" alongside the 📋 Declined badge in one row.

**Sort order:** 🆕 New Win → 🔄 Policy advance → 💰 Settled → ❌ Declined → 📉 Lost

**Footer counter:**

- `🕒 In-flight: N (oldest X days)` — Won leads with policy not yet settled
- `⚠️ Stale (>30d no movement): N` — first 3 names listed for action

Same flat table is rendered into the Gmail HTML body, so "Open in Gmail" / "Copy HTML for Gmail" both deliver the new report to the manager.

The existing "Cases Submitted This Week" + "All Open Cases" + "CRM Activity stats" sections remain in the report (for commission detail). The new section sits at the top.

---

## v1.16.2 — 2026-05-07 — DuetBooks-presence detection fix

After v1.16.1 + DuetBooks v1.3.0 shipped, Vivian Cabaniss (and other manually-created DuetBooks cases) still showed "⚠ No Pipeline Case Found" with a "+ Create Case" button on the lead detail. Root cause: the CRM was checking the local `pl` array (which only gets cases from `convertToPipeline`), not DuetBooks itself. Manual DuetBooks cases never landed in `pl`.

- Presence-of-case detection now checks **both** local `pl` AND `lead.policyStatus` (which DuetBooks stamps via push-back). Either signal = case exists.
- Won-section header reads `✓ Case in DuetBooks — Issued` (or current status) instead of generic "Case in Pipeline"
- "+ Create Case" button hidden when `policyStatus` is set
- One-shot manual sync ran server-side: pushed current `policyStatus` from 7 DuetBooks cases (with `crmLeadId`) into their matching CRM leads — Vivian, Donna, Lidio, Deborah, Dorota, Kenneth, Jennifer

The 60+ legacy DuetBooks cases (`notes: "Imported from Duet Maxim account"`) have no `crmLeadId` to backfill from notes, so they remain unlinked. They'd need name+phone matching to push back. Deferring that until needed.

---

## v1.16.1 — 2026-05-07 — Two-status model (Phase 1 of 3)

Leads now carry **both** an Opportunity status (CRM-side, terminal at Won/Lost) and a **Policy status** (DuetBooks-side, lifecycle: Pending/Submitted/Approved/Issued/Paid/Paid-Partial/Declined). This is Phase 1 of the two-status refactor — Phase 2 is the DuetBooks push-back side, Phase 3 is the rebuilt weekly report.

**What changed in CRM:**

- `lead.policyStatus` and `lead.policyStatusChangedDate` are new fields on the lead schema
- Lead detail header shows two badges side-by-side: Opportunity (existing stage badge) + 📋 Policy (new)
- `convertToPipeline` + `showCreateCaseModal` write `crmLeadId: lead.id` onto every new DuetBooks case so DuetBooks can push policy-status changes back to the matching CRM lead
- Both push paths initialize `lead.policyStatus = "submitted"` at the moment of conversion, so the Policy badge appears immediately on a new Won lead
- New decline-reason flow: when `policyStatus === "declined"`, a red banner appears on lead detail with a single input. Saving prepends a `"DECLINE: ..."` entry to `historyNotes` — surfaces on the rebuilt weekly report (Phase 3)
- Cleanup tool scope correction: only targets `stage === "won"` leads (was Won + App Submitted). App Submitted is intentionally a CRM-only "in-flight 50/50" stage and is **never** pushed to DuetBooks

**Backups before this build:**

- `/backups/pre_two_status_20260507T185547` (combined: 502 leads + 69 DuetBooks cases, 548KB)
- Local source backups: `~/Desktop/Duet/.backups_pre_two_status_20260507T185547/{DuetCRM,DuetBooks}.html.bak`

**No data migration ran.** Existing Won leads will get `policyStatus` only when (a) their DuetBooks case status next changes after Phase 2 ships, or (b) they re-flow through Won.

---

## v1.16.0 — 2026-05-07 — 🧹 CRM Cleanup tool (DuetBooks reconciliation)

DuetBooks is the source of truth for closed deals. This new tool walks every CRM Won/App Submitted lead, fuzzy-matches it against DuetBooks cases by client name, and gives you a one-click bulk-delete for the duplicates.

**Three buckets:**

- ✅ **Safe to remove** — Matched in DuetBooks, no field mismatches, no CRM-only data. Auto-checked.
- ⚠️ **Review needed** — Matched, but has field mismatches (amount/product/agent differ between CRM and DuetBooks) or CRM-only data (historyNotes / wonReason / callLog). Not auto-checked — you decide per row.
- ❌ **No match in DuetBooks** — Kept in CRM. Create the DuetBooks case manually before they can be cleaned up. (Vivian Cabaniss-style cases land here.)

**Lost leads are never touched.**

**What happens on delete:**

1. Backup snapshot of full `/leads` written to `/backups/cleanup_TIMESTAMP` (reversible)
2. CRM `historyNotes` + `wonReason` appended to the matching DuetBooks case's `notes` field (skippable per row via "Skip note copy" checkbox)
3. `callLog` discarded — recoverable from the backup if ever needed
4. Selected leads filtered out of the local `leads` array and pushed to Firebase
5. DuetBooks cases themselves are never deleted, only optionally annotated

**Pre-tool baseline backup:** `/backups/cleanup_20260507T174719` (502 leads, 486KB)

**Fuzzy match rule:** lowercase + strip non-alphanumeric, so "Daisy Delgado live" === "Daisy Delgado-live".

**Mismatch detection:**

- Amount: flagged if CRM > $0 and either DuetBooks shows different value (>$1 diff) or shows $0
- Product: flagged if both sides have a product and they don't match
- Agent: flagged unless one side's first word is a substring of the other (so "Mary P" vs "Mary Petty" doesn't flag — first word matches)

**Access:** CRM tab → 🧹 Cleanup button in the nav row.

---

## v1.15.8 — 2026-05-07 — Restore instant native dialer open

The synchronous toast render in v1.15.7 fixed the disposition-prompt lag, but it blocked iOS from showing the native "Call <number>?" confirmation dialog until our toast finished building — now the dialer felt slow.

- Defer the toast to the next event-loop tick (`setTimeout(showCallOutcomePrompt, 0, leadId)`) so iOS handles `tel:` navigation immediately
- Dialer opens instantly; the toast appears right after (briefly hidden behind the native dialog on iOS, visible when you dismiss it)
- Best of both worlds: dialer is snappy, toast is queued and ready when you return

---

## v1.15.7 — 2026-05-07 — Speed up disposition prompt on iOS

The new tap-to-call disposition toast (v1.15.6) felt sluggish on iPhone — toast only appeared *after* dismissing the native phone-call confirmation dialog. Root cause: the `setTimeout(..., 50)` I wrapped the call in got paused by Safari during the `tel:` handoff to the dialer.

- Fix: render the toast synchronously in onclick (no setTimeout) so it appears the instant you tap, before iOS hands control to the dialer
- Tightened toast slide-in from 0.3s to 0.12s for extra snap

---

## v1.15.6 — 2026-05-07 — Tap-to-call opens disposition prompt

When you tap a lead's "📞 Call" button on phone or a name in Today's Priorities on desktop, the dialer opens **and** the disposition prompt appears so you can log the outcome (No Answer / Left VM / Bad # / Connected / Discovery / Appt Set / Nurturing / Lost) without hopping to lead detail.

- Phone Call Queue 📞 Call button now triggers the prompt
- Desktop Today's Priorities name tap-to-dial now triggers the prompt
- Picking a disposition logs the call and updates stage; "Appt Set" also opens Quick Book pre-linked to the lead
- Refactored: extracted shared `showCallOutcomePrompt()` so `dialLead()` (Calley speed-to-lead) and the new tap-to-call entrypoints use the same UI

---

## v1.15.2 — 2026-05-05 — Desktop auto-forceCloudSync on load

**Root-cause fix for the recurring "Don McCoy disappears" bug.** Every time we manually fixed the leads in Firebase, the laptop's stale localStorage would push back on the next save and clobber Firebase again — losing whatever lead I'd just added.

Phone has auto-forceCloudSync since v1.13.1; desktop did not. Desktop relied on the buggy `firebaseLoadAll` merge path. **Now desktop also runs forceCloudSync on every page load** (~2s after init). Cloud is treated as truth on every refresh — laptop pulls fresh state, then any subsequent saves push that fresh state back, no clobbering.

`forceCloudSync` already internally calls `ingestPhoneInbox` (added in v1.15.1), so phone-captured leads still get ingested.

## v1.15.1 — 2026-05-05 — Phone inbox ingest reliability fix

Hot fix: phone-captured leads (added via the phone's "+ Add Lead" button) weren't reliably being ingested into the main `/leads` array on the laptop. Don McCoy was added from the phone twice but never appeared on the laptop.

**Root cause:** `ingestPhoneInbox()` was only wired to `firebaseLoadAll`'s success callback. That function has the silent-fail merge bug we routed around in v1.13.1 — when it bails early, the ingest never runs.

**Fix:**
- `forceCloudSync()` (the 🔄 Sync button) now also triggers `ingestPhoneInbox()` after the pull
- Desktop now auto-runs `ingestPhoneInbox()` on every page load (~2s after init), independent of `firebaseLoadAll`
- Phone unchanged (it never ingests; it's the producer)

**One-time data fix:** Manually ingested Don McCoy (id=501) from the inbox + cleared the duplicate inbox entry that resulted from the user trying twice.

## v1.15.0 — 2026-05-03 — Phone mobile-first UI

The phone app was getting clunky — too many tabs, dashboards, and tools that don't matter when you're in the field. Stripped it down to what you actually use:

**Phone home screen now shows ONLY:**
- **+ Add Lead** button (prominent green)
- **📅 Schedule** button (prominent purple)
- **🔍 Search** bar with live autocomplete (tap result → lead detail)
- **Today's Appointments** (collapsible card, with type/location)
- **📞 Call Queue (top 10)** — prioritized, with **tap-to-call** buttons
- **📌 Action Items** — read-only display (no checkboxes / no delete)
- **📓 Coach Journal** entry button (red/green based on today's status)
- **🔄 Sync** button (escape hatch, kept from v1.13.1)

**Bottom nav simplified** to just **CRM** and **Book** — no Reports tab, no More menu.

**Lead detail on phone** — action item checkboxes/delete buttons hidden. Bullets shown instead. Tap-to-call (`tel:` links), email links, and Schedule Appt button all still work.

**Hidden from phone entirely:**
- Reports tab (and Manager Weekly Report)
- Funnel Health tab
- Year Summary tab
- CD → Annuity tool
- Annuity vs Annuity tool
- S&P vs Annuity tool
- Bulk Add
- Agents management
- Year toggle (2025/2026)

Everything still accessible on desktop unchanged.

## v1.14.0 — 2026-05-03 — Past Manager Weekly Reports + snapshot archive

You can now re-run Manager Weekly Reports for past weeks. Two-tier approach:

**Phase 1 — Live reconstruction (works for past weeks immediately):**
- Refactored `genReport(weekStartYMDArg)` to accept an optional Friday date
- Added "📅 Week:" dropdown above the report — last 12 weeks selectable
- Selecting a past week filters all metrics (cases, calls, action items, etc.) to that Friday–Thursday range
- Amber banner warns that values reflect current case statuses, not point-in-time

**Phase 2 — Snapshot archive (perfect fidelity going forward):**
- Every time you view the current week's report, an exact HTML snapshot auto-saves to Firebase under `weekly_report_snapshots/<friday-date>/<filter>_<prodfilter>.json`
- Throttled to 1 save per minute per filter combo to avoid hammering Firebase
- When you re-view a past week, the snapshot is fetched and replaces the reconstructed view automatically (purple banner confirms snapshot is showing)
- Falls back to reconstruction if no snapshot exists for that week (weeks before v1.14.0 deployed)

**UX details:**
- Default selection: current week (no behavior change for normal use)
- Past-week banner shows weeks-ago label ("last week", "3 weeks ago")
- "← Back to current week" button on banners for quick return

## v1.13.1 — 2026-05-03 — Phone auto-rescue + manual Sync button

Hot fix shipped same day as v1.13.0. After v1.13.0 deployed, phone was showing only 114 of 471 leads — the long-standing `firebaseLoadAll` merge bug combined with iOS Safari localStorage quota limits caused partial loads on phone.

- **Phone auto-rescue:** on every load, phone now silently force-pulls fresh data from each Firebase path (leads, appointments, agents, pipelines, periods, settings) and replaces in-memory + localStorage. Bypasses the buggy merge logic entirely.
- **NEW "🔄 Sync" button** in CRM header (both devices): one-tap manual escape hatch when anything looks out of sync. Shows "🔄 Synced from cloud · N leads, M appts" toast.
- **`forceCloudSync()`** function added — direct-fetches each Firebase path. Tolerates localStorage quota errors (continues with in-memory only).

## v1.13.0 — 2026-05-03 — Phone read-mostly architecture

Desktop is now the **source of truth**. Phone is read-mostly with a limited capture inbox. This eliminates the entire class of cross-device merge bugs that plagued v1.11.x and v1.12.x (action items appearing on wrong leads, deleted items coming back, lead names getting swapped, etc.).

**Phone behavior:**
- Phone never pushes the full `leads` or `appointments` arrays to Firebase — `saveLeads()` and `saveAppts()` early-return on phone
- **"Add Lead" on phone** → writes ONLY the new lead to `/phone_inbox_leads` (Firebase POST = append-only)
- **"Schedule Appointment" on phone** → writes ONLY the new appointment to `/phone_inbox_appts`
- Other phone edits (action items, stage changes, notes) update local view for the session but do NOT sync — replaced by cloud truth on next pull
- Phone shows "📱 Read-mostly" badge in version footer
- Phone's `firebasePushAll` button now disabled (was: clobbered cloud with phone's view)

**Desktop behavior:**
- Same as before, plus on each load: `ingestPhoneInbox()` runs after Firebase pull
- For each new lead/appointment in the phone inbox: dedup, append to main array, push merged result to cloud, clear inbox
- Toast appears: "📱 Ingested N leads/appointments from phone"

**What this kills (gone forever):**
- ❌ Phone overwriting desktop's edits
- ❌ ID collisions when devices are offline
- ❌ Action items appearing on wrong leads
- ❌ Lead names getting swapped on push (Peter Nelson → Jason Massey)
- ❌ Deleted items coming back via stale push
- ❌ Coach Journal "phantom days missed" on other device
- ❌ Most of the v1.12.x merge complexity (deletion-aware logic still in place but largely unnecessary now with single writer)

**What you give up on phone:**
- Marking action items done in the field (do on desktop)
- Editing notes / stage from phone (do on desktop)
- Calley pushes from phone (was already desktop-only)

**What you keep on phone:**
- Full read access to all leads, appointments, dashboard, action items, journal, reports
- Add new lead on the go ✅
- Schedule appointment on the go ✅
- Tap-to-call any lead ✅

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
