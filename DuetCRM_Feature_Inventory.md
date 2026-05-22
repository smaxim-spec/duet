# DuetCRM — Feature Inventory (for comparison)

> Comprehensive structured inventory of every feature in DuetCRM + DuetBooks as of v1.19.0 (2026-05-22).
> Built for side-by-side comparison against another CRM. Each line is a checkbox the comparator can mark.

---

## Quick stats

| Metric | DuetCRM |
|---|---|
| **Version** | v1.19.0 (CRM) + v1.3.0 (DuetBooks) |
| **Lines of code** | ~12,800 (single HTML file, CRM) + ~4,800 (DuetBooks) |
| **Build steps** | 0 — pure HTML/CSS/JS, no transpilation, no bundler |
| **External dependencies** | 0 — fully self-contained |
| **Total version history** | 19 minor releases + 19 patch releases ≈ 60+ documented changes |
| **Lead records under management** | 510 |
| **Documented architecture decisions** | 4 docs: Project Map, Changelog, Stage Flow Mindmap, Session Handoff |
| **Persistence layers** | localStorage + Firebase Realtime DB + Cloudflare Worker |
| **Companion apps integrated** | 2 (DuetBooks for cases, DuetIncome for income tracking) |
| **External service integrations** | 5 (Firebase, Calley API + webhook, Cloudflare Worker, Gmail, Google Calendar) |
| **Devices supported** | Laptop (desktop), Phone (mobile-first read-mostly architecture) |

---

## 1. Lead Management

- [ ] Add lead manually (Quick Add form)
- [ ] Add lead in bulk (paste rows from Excel/Salesforce)
- [ ] Add lead from phone (writes to `/phone_inbox_leads` queue)
- [ ] Auto-ingest phone-added leads every 60 seconds
- [ ] Deduplication by phone number (last 10 digits, case-insensitive)
- [ ] Import from Calley webhook (real-time)
- [ ] Import from Calley REST API (legacy fallback)
- [ ] Live search with autocomplete dropdown (name + phone, debounced)
- [ ] Smart search: phone-format detection (digits → phone, text → name)
- [ ] Bulk delete with snapshot backup before destruction
- [ ] All Leads table view with sorting + filtering
- [ ] Per-lead delete with confirmation
- [ ] Lead detail view (full editable record)
- [ ] Lead re-opening for new opportunity (preserves history, archives old)
- [ ] Repeat-business detection (existing client → new product)

## 2. Stage Pipeline (10 stages)

- [ ] **new** → fresh leads only, top-priority bucket
- [ ] **attempting** → tried but not reached
- [ ] **connected** → picked up, brief chat
- [ ] **discovery** → real conversation, qualifying
- [ ] **meeting_set** → appointment booked
- [ ] **quoted** → numbers given to client
- [ ] **app_submitted** → hedge stage, 50/50, intentionally NOT pushed to DuetBooks
- [ ] **won** → real deal, auto-pushes to DuetBooks
- [ ] **lost** → terminal, captures reason
- [ ] **incubator** (Nurturing) → parked with hot/warm/cool temperature
- [ ] Auto-promote `new` → `attempting` on first dial (v1.19.0)
- [ ] Auto-lost at 5 attempts with no contact (v1.19.0)
- [ ] Stage transitions logged with `stageEnteredDate`
- [ ] Stage move breadcrumb notices in UI
- [ ] Stage-aware action buttons (different buttons per stage)

## 3. Call Workflow

- [ ] Tap-to-call from phone queue (`tel:` link)
- [ ] Disposition prompt after call (Left VM / No Answer / Bad # / Connected / Discovery / Appt Set / Nurturing / Lost / Quoted / Won / Confirmed / Rescheduled / Callback)
- [ ] Synchronous render — disposition appears instantly on tap
- [ ] iOS-tuned: doesn't block native dialer modal
- [ ] Per-lead call log (full history, never overwritten)
- [ ] Call blocks: morning / afternoon / evening / calley
- [ ] Auto-stage progression based on disposition
- [ ] Calley speed dialer integration (push leads from CRM)
- [ ] Calley webhook ingestion (real-time, no API token required)
- [ ] Daily call goal (configurable, default 40)
- [ ] Call queue with smart prioritization (callbacks first, then new, then attempting)
- [ ] Today's Priorities widget (quoted follow-up, meeting follow-up, callback due)
- [ ] Tap-to-dial on priorities + right-click to open detail
- [ ] "Mark Lost" modal: required reason dropdown (5 options) + optional 150-char notes

## 4. Two-Status Model (architectural cornerstone — unlikely in any baseline CRM)

- [ ] **Opportunity status** (`stage`) — CRM-side, terminal at Won/Lost
- [ ] **Policy status** (`policyStatus`) — DuetBooks-side, lifecycle: pending → submitted → approved → issued → paid (+ paid-partial, declined)
- [ ] Both badges shown side-by-side on lead detail
- [ ] Linked via `case.crmLeadId` (back-pointer from DuetBooks case to CRM lead)
- [ ] One-shot backfill parses `crmLeadId` from legacy notes (`"From CRM lead #N"`)
- [ ] Name+phone fuzzy match for legacy cases without `crmLeadId`
- [ ] DuetBooks push-back on every status change via PATCH `/leads/data/<idx>/policyStatus`
- [ ] Single-field PATCH avoids race conditions with concurrent CRM saves
- [ ] Decline-reason banner appears on lead detail when policy declined
- [ ] Decline reason auto-prepended as `DECLINE: ...` historyNote
- [ ] Decline reason surfaces in weekly report's Notes column

## 5. DuetBooks Integration (companion app)

- [ ] CRM → DuetBooks auto-push on `stage='won'` (via `convertToPipeline`)
- [ ] Pre-push verification modal: requires agent, premium, product (or "Push anyway" override)
- [ ] DuetBooks initial status: `submitted` (not `pending`)
- [ ] App Submitted intentionally does NOT push (hedge stage)
- [ ] DuetBooks dashboard banner: "N Won leads in DuetCRM not yet in DuetBooks"
- [ ] Import modal in DuetBooks with prefilled data + per-row Import button
- [ ] Product name mapping (CRM names → DuetBooks names via `CRM_TO_BOOKS_PRODUCT`)
- [ ] CRM Cleanup tool: reconciles Won leads against DuetBooks
- [ ] Cleanup buckets: ✅ Safe to remove / ⚠️ Review (mismatches) / ❌ No match
- [ ] Bulk delete with optional historyNotes/wonReason copy to DuetBooks notes
- [ ] Pre-cleanup snapshot to `/backups/cleanup_TIMESTAMP`
- [ ] Mismatch detection: amount, product variant, agent name (with first-word fuzzy)
- [ ] Varicent payroll reconciliation in DuetBooks
- [ ] Auto-mark paid on Varicent match (pushes back to CRM)

## 6. Multi-Device Sync

- [ ] Real-time Firebase persistence
- [ ] Phone-inbox pattern: phone writes append-only, laptop ingests
- [ ] Read-mostly phone architecture (phone never pushes leads array directly)
- [ ] Auto-poll phone-inbox every 60s on laptop (v1.17.1)
- [ ] forceCloudSync escape hatch with 🔄 Sync button
- [ ] Per-device identifier (`DEVICE_NAME`) tracked on writes
- [ ] Dedup-by-phone on phone-inbox ingest
- [ ] Phone appointment inbox (separate path from leads)
- [ ] Conflict-free design: phone/laptop never race on same record

## 7. Reporting

- [ ] Weekly Manager Report (Friday-Thursday window)
- [ ] **Activity-based filter** (not snapshot) — rows appear only when something changed this week
- [ ] Activity types: New Win / Lost / Policy advance / Settled / Declined / Decline reason added
- [ ] Flat table format (email-friendly)
- [ ] Both Opportunity + Policy columns explicit per row
- [ ] Auto-populated Notes column with decline reasons
- [ ] Sort: 🆕 New Win → 🔄 Policy advance → 💰 Settled → ❌ Declined → 📉 Lost
- [ ] Footer counter: In-flight + oldest days + Stale (>30d) with first 3 names
- [ ] "Cases Submitted This Week" section (commission detail)
- [ ] "All Open Cases" section (pulls from DuetBooks live, not stale local mirror)
- [ ] "CRM Activity stats" (calls / new leads / appts, this week vs last week)
- [ ] $100K Goal Progress section with adjusted-total math
- [ ] Past-week snapshots stored in Firebase (replay historical reports)
- [ ] Gmail HTML body (Open in Gmail / Copy HTML buttons)
- [ ] Mailto fallback (truncates body if too long)
- [ ] Past-week filter dropdown with snapshot recovery

## 8. Lead Detail Features

- [ ] Two status badges side-by-side (Opportunity + Policy)
- [ ] Call log timeline (merged with history notes, chronological)
- [ ] History notes (free-form, timestamped)
- [ ] Decline reason banner with input → DECLINE: historyNote
- [ ] Win reason capture (7 options) via toast modal
- [ ] Client images / PDF documents (base64 stored in lead, Firebase-synced)
- [ ] Objections tracker (per-objection status + response)
- [ ] Needs Analysis (per-product questionnaires)
- [ ] Inline editable fields (name, phone, email, age, premium, notes)
- [ ] Stage move buttons (compact row, hides current stage)
- [ ] Mark Lost button → modal with reason + notes
- [ ] Schedule appointment with time-slot picker
- [ ] Quick Book for meeting set
- [ ] Calley push button
- [ ] Repeat business / New Opportunity flow
- [ ] Callback scheduling with date picker
- [ ] Lost-lead historical view (preserves all data after loss)

## 9. Mobile-First Phone UI (v1.15.0)

- [ ] Phone-specific render path (`renderPhoneApp()`)
- [ ] Tap-to-call with auto disposition prompt
- [ ] Bottom nav (Add Lead / Schedule / Search)
- [ ] Phone home: Top 10 prioritized call queue
- [ ] Live search with mobile keyboard
- [ ] Search results dropdown with tap-to-open
- [ ] Today's appointments view
- [ ] Action items (read-only on phone)
- [ ] Phone-specific schedule view
- [ ] Mobile-tuned button sizes (touch targets)
- [ ] Add lead from phone (writes to inbox, not direct push)
- [ ] Schedule appointment from phone (writes to inbox)
- [ ] Coach Journal accessible on phone

## 10. Smart / Coaching Features

- [ ] Coach Journal (two-way communication with sales coach)
- [ ] Sales Mastery / Lesson of the Week (rotating coaching content)
- [ ] Daily Call Goal tracking
- [ ] Coach Notes (Critical / Warning / Good / Insight) — auto-generated based on weekly stats
- [ ] Stale lead detection (in-flight >30 days)
- [ ] Auto-loss at 5 attempts (v1.19.0)
- [ ] Speed-to-lead workflow (new lead → dial prompt within 5s)
- [ ] Smart prioritization in call queue (callbacks first, then by stage)
- [ ] Action items (Gmail import + per-lead reminders)
- [ ] Frustrations / Wins tracking in journal

## 11. Data Integrity & Recovery

- [ ] Backup pattern: every destructive operation snapshots first
- [ ] Firebase `/backups/cleanup_TIMESTAMP` (before bulk deletes)
- [ ] Firebase `/backups/auto_TIMESTAMP` (after every code release)
- [ ] Firebase `/backups/pre_stage_rules_*`, `/backups/pre_loss_modal_*`, etc. (per build)
- [ ] Local source backups (`~/Desktop/Duet/.backup_*.html`)
- [ ] Audit log (DuetBooks tracks status changes affecting financial totals)
- [ ] Weekly report snapshots (past-week reproduction)
- [ ] Cleanup tool preview before destruction
- [ ] DuetBooks case merge with history preservation
- [ ] Idempotent ingest (dedup by Firebase key, by phone, by calleyId)

## 12. External Integrations

- [ ] **Firebase Realtime Database** — primary persistence
- [ ] **Cloudflare Worker** — Calley webhook receiver
- [ ] **Calley REST API** — bidirectional (push leads + pull results)
- [ ] **Gmail API** — read-only, action-item import
- [ ] **Google Calendar API** — appointment scheduling
- [ ] **Python proxy server** (`duet_server.py`) — local on port 8787, handles OAuth + Calley proxy
- [ ] **GitHub Pages** — mobile deploy target
- [ ] **localStorage** — offline cache

## 13. UI / UX Polish

- [ ] Dark mode (theme variables)
- [ ] Light mode with branded color palette (purple #534AB7 primary)
- [ ] Consistent badge color scheme aligned with DuetBooks (Issued/Approved = purple, Submitted = amber, Paid = green, Declined = gray)
- [ ] Toast notifications with auto-dismiss
- [ ] Persistent toasts for actions requiring response (disposition picker)
- [ ] Modal overlays with focus management
- [ ] Accessibility: keyboard shortcuts (Y/N for dial prompt)
- [ ] Loading states for async fetches
- [ ] Empty states with helpful prompts
- [ ] Color-coded stage badges (10 colors)
- [ ] Color-coded policy badges (7 colors)
- [ ] Animated transitions (slideIn, slideDown — 0.12s for snappiness)
- [ ] Stage move breadcrumb notices
- [ ] Sticky filter chips

## 14. Sales Productivity

- [ ] Sales scripts library (8 scripts: IUL, CD, Annuity, Term, etc.)
- [ ] Per-product needs analysis questionnaires
- [ ] Objection tracker per lead
- [ ] Top objections leaderboard
- [ ] Carrier rate table reference
- [ ] Win reason analytics (% breakdown by reason)
- [ ] Lost reason analytics (% breakdown by reason)
- [ ] Source-of-business analytics
- [ ] Agent referral performance (cases per agent, partner payout)
- [ ] Hit rate calculations (contact rate, appt rate, close rate)
- [ ] 3MMA (3-month moving average) tracking
- [ ] Tier progression (T1/T2/T3/T4 commission tiers)

## 15. Architecture / Engineering Quality

- [ ] Single-file deploy (no build, no bundling, no compile step)
- [ ] Zero external runtime dependencies
- [ ] 4-target sync deploy pattern (source + 3 mirrors)
- [ ] Git-tracked version control with semantic versioning
- [ ] In-app changelog (visible at version footer tap)
- [ ] Comprehensive external documentation:
  - [ ] `Duet_Project_Map.md` — section-by-section code guide
  - [ ] `CHANGELOG.md` — full version history
  - [ ] `Stage_Flow_Mindmap.md` — visual stage flow with Mermaid
  - [ ] `SESSION_HANDOFF.md` — fresh-session pickup doc
- [ ] Idempotent operations (re-runs are safe)
- [ ] Race-condition-free design (single-field PATCH, append-only queues)
- [ ] Pure functions where possible
- [ ] No nuclear deletes — soft archive + history preservation

---

## What makes DuetCRM hard to replicate

These are the items that took real iterative refinement and would be near-impossible for a one-shot AI generation:

1. **Two-status model with bidirectional sync** — separates opportunity from policy lifecycle. Required 4 versions (1.16.1, 1.16.2, 1.16.3, 1.16.4 + DuetBooks 1.3.0) to get right.

2. **Phone-inbox pattern** — read-mostly mobile architecture with append-only queues. Solved real race-condition bugs ("Don McCoy disappears") that surface only on multi-device usage.

3. **Calley webhook integration** — Cloudflare Worker receives Calley webhooks, writes to Firebase, CRM auto-ingests every 60s. Replaces a brittle REST API + local proxy approach.

4. **DuetBooks reconciliation** — both directions. CRM Cleanup pulls duplicates out; DuetBooks pending banner pulls missing ones in. Fuzzy name+phone matching with mismatch detection.

5. **Activity-based weekly report** — naturally bounded (doesn't grow unbounded). Manager sees what changed, not a snapshot.

6. **Pre-build + post-release backup discipline** — every destructive operation snapshots first to Firebase + local. Fully reversible.

7. **Iterative rule refinement** — stage transition rules evolved over 19 versions based on real usage feedback (e.g., v1.19.0 changed first-dial promotion threshold and auto-loss threshold based on the user's actual workflow needs).

8. **Documentation discipline** — 4 architecture docs kept in sync with code via every release.

---

## How to use this for the comparison

Open a new Claude session and paste:

```
I'm comparing two CRMs:

1. DuetCRM — full feature inventory in
   ~/Desktop/Duet/DuetCRM_Feature_Inventory.md
   (and current state in ~/Desktop/Duet/SESSION_HANDOFF.md)

2. [Other CRM] — built with Microsoft Copilot.
   File at: [path]

Run a side-by-side comparison. For each category in the inventory,
mark ✅ (both have), ❌ (Duet has, other doesn't),
or ➖ (other has, Duet doesn't). Total counts at the bottom.
Produce a markdown summary with the verdict.
```

Then drop the Copilot HTML file and let the new session do the work cold.

---

*Generated 2026-05-22 — pairs with [SESSION_HANDOFF.md](./SESSION_HANDOFF.md) and [Duet_Project_Map.md](./Duet_Project_Map.md).*
