# DuetCRM — Project Map & Section Guide

> Use this to orient any new conversation. Ask to work on a specific section by name.
>
> **Current version:** `v1.18.0` (2026-05-17) — see [CHANGELOG.md](./CHANGELOG.md) for full version history.
> **Companion:** DuetBooks `v1.3.0` (2026-05-07) — at `~/Desktop/DuetBooks/DuetBooks.html`.

## Recent Architectural Additions (since v1.12.3)

These are the major changes someone picking up a new session needs to know about:

### Two-Status Model (v1.16.1 + v1.16.2 + v1.16.3 + DuetBooks v1.3.0)
- Every lead now carries **two** statuses:
  - **Opportunity status** = CRM `lead.stage` (terminal at Won/Lost — never auto-revert)
  - **Policy status** = `lead.policyStatus` (mirrors DuetBooks case lifecycle: pending/submitted/approved/issued/paid/paid-partial/declined)
- Linked via `case.crmLeadId` written by `convertToPipeline` / `showCreateCaseModal` / `importCRMLead`
- DuetBooks pushes status changes back via PATCH `/leads/data/<idx>/policyStatus` (single-field patch, no race with concurrent CRM saves)
- Lead detail displays both badges side-by-side
- New `lead.declineReason` flow: when `policyStatus='declined'`, banner prompts for reason → prepends `DECLINE:` historyNote
- Weekly Report has new flat-table "Activity for This Week" section above "Cases Submitted This Week" — activity-based filter (new Wins / policy advances / settled / declined / lost this week)
- App Submitted stage **never** auto-pushes to DuetBooks (intentionally — used for 50/50 hedging)

### CRM Cleanup Tool (v1.16.0)
- New `🧹 Cleanup` tab in CRM nav. Reconciles CRM Won leads against DuetBooks cases.
- Three buckets: ✅ Safe to remove / ⚠️ Review (mismatches or CRM-only data) / ❌ No match
- Bulk-delete with optional historyNotes/wonReason copy to DuetBooks notes
- Pre-delete snapshot always written to `/backups/cleanup_TIMESTAMP`
- Won-only scope (App Submitted excluded per architecture)

### DuetBooks → CRM Pending Banner (DuetBooks v1.2.0 / v1.3.0)
- DuetBooks Dashboard banner: "N Won leads in DuetCRM not yet in DuetBooks"
- Modal lists each with prefilled data; per-row Import creates the DuetBooks case + initial `status='submitted'` + writes `crmLeadId`
- Match rule: fuzzy client name (lowercase + strip non-alphanumeric) AND phone (last 10 digits) when both sides have phone
- One-shot `backfillCrmLeadIds()` parses `"From CRM lead #N"` out of legacy case notes

### Calley Webhook Sync (v1.17.0)
- Replaces the broken `calleySyncResults` API path (used `localhost:8787/calley-proxy` + valid Calley token)
- New `syncCalleyFromWebhook()` reads `/calley_webhook_logs` directly (no proxy, no token, works on phone)
- Webhook Firebase auto-key used as `calleyId` for dedup
- Auto-runs silently 4s after CRM load + manual `🔄 Sync Calley` button
- Source of webhook: Cloudflare Worker at `calley-webhook.smaxim.workers.dev`

### Phone Inbox Auto-Poll (v1.17.1)
- Laptop polls `/phone_inbox_leads` every 60s in the background (in addition to load-time + manual Sync)
- Phone-added leads appear on laptop within a minute without reload
- No-op on phone (only laptop ingests)

### Loss-Reason Modal (v1.18.0)
- Marking a lead Lost now opens a modal: required reason dropdown (5 options) + optional 150-char notes
- New `LOST_REASONS`: Not interested / Already insured / Underwriting / health issue / Objection not resolved / Timing / not ready
- Old records preserve legacy labels (no migration)
- Cancel = no writes (true no-op); auto-loss paths unchanged
- Activity report appends loss reason: `📉 Lost (Timing / not ready)`

### Dark Mode Polish (v1.16.9)
- Coach Notes (Critical/Warning/Insight) had hard-coded light backgrounds — fixed with rgba tints + explicit `color:var(--txt)`
- Other dark-mode contrast fixes throughout

### Tap-to-Call Disposition (v1.15.6 → v1.15.8)
- Tapping a phone-queue Call button now opens dialer + disposition prompt (Left VM / No Answer / Bad # / Connected / Discovery / Appt Set / Nurturing / Lost)
- Disposition prompt uses `setTimeout(showCallOutcomePrompt, 0, leadId)` so the dialer opens instantly, toast appears on return

## Architecture Overview
- **Single HTML file** (current name: `DuetCRM.html`, ~12,800 lines as of v1.18.0)
  - Source of truth: `~/.duet-server/DuetCRM.html`
  - Synced to: `~/.duet-server/index.html`, `~/Desktop/Duet/DuetCRM.html`, `~/Desktop/Duet/index.html`
- **No external dependencies** — inline CSS + JS, self-contained
- **Persistence**: localStorage + Firebase Realtime Database
- **Desktop**: Python HTTP server on port 8787 (`duet_server.py`) — runs as background process; restart with `pkill -f duet_server.py; nohup python3 ~/.duet-server/duet_server.py > /tmp/duet.log 2>&1 &`
- **Mobile**: GitHub Pages at `smaxim-spec.github.io/duet/` (no PIN gate currently)
- **Firebase URL**: `https://duet-crm-default-rtdb.firebaseio.com/`
- **Firebase rules**: open public read/write (`{".read":true,".write":true}`)

## Companion Apps
- **DuetBooks** — `~/Desktop/DuetBooks/DuetBooks.html`, deployed to `duetbooksapp/duetbooks` repo. Source of truth for case/commission data. Reads/writes Firebase path `duetbooks/steve_maxim/cases.json`.
- **DuetIncome** — `~/.duet-server/DuetIncome.html`, deployed to `duetbooksapp/duetincome`.

## Supporting Files (in `~/Desktop/Duet/`)
| File | Purpose |
|------|---------|
| `DuetCRM.html` (also `index.html`) | **THE app** — single-file CRM |
| `CHANGELOG.md` | Full version history (mirrors in-app changelog) |
| `Duet_Project_Map.md` | This file |
| `CRM Calling Cadence Guide.md` | Call cadence reference doc |
| `Adult_IUL_Call_Script.md` | Sales script |
| `CD_Annuity_Call_Script.md` | Sales script |
| Various `.md` scripts | Sales playbooks |

## Supporting Files (in `~/.duet-server/`)
| File | Purpose |
|------|---------|
| `duet_server.py` | Python HTTP server: serves files + proxies Calley API + Google Calendar/Gmail endpoints |
| `calendar_api.py` | Google Calendar integration helpers |
| `gmail_api.py` | Gmail read-only integration (action item import) — added v1.12.0 |
| `calley-webhook-worker.js` | Cloudflare Worker source code (deployed separately to `calley-webhook.smaxim.workers.dev`) |
| `google_credentials.json` | OAuth client secret |
| `google_token.json` | Saved OAuth token with scopes: contacts + calendar + gmail.readonly |

## Cloudflare Worker (Calley webhooks)
- Deployed at `https://calley-webhook.smaxim.workers.dev/`
- Receives Calley call dispositions via webhook
- Matches contacts to CRM leads by phone, appends to lead's callLog in Firebase
- Auto-promotes stages (new→attempting@3calls, attempting→incubator@10calls, etc.)
- Source: `~/.duet-server/calley-webhook-worker.js`

## Scheduled Tasks
| Task ID | Schedule | What it does |
|---------|----------|-------------|
| `sync-google-contacts` | 8 AM & 5 PM daily | Push new CRM leads to Google Contacts |
| `update-evolution-report` | 9 PM daily | Regenerate evolution doc with day's changes |
| `payroll-update` | 9 AM on 1st & 16th | Process Varicent/Workday PDFs from Gmail |

## Deployment Workflow
```bash
# 1. Edit the source
vim ~/.duet-server/DuetCRM.html

# 2. Bump version + add changelog entry (lines ~316-410)

# 3. Sync to all four deploy targets
cp ~/.duet-server/DuetCRM.html ~/.duet-server/index.html
cp ~/.duet-server/DuetCRM.html ~/Desktop/Duet/DuetCRM.html
cp ~/.duet-server/DuetCRM.html ~/Desktop/Duet/index.html

# 4. Mirror changelog entry into ~/Desktop/Duet/CHANGELOG.md (insert at top)

# 5. Commit + push
cd ~/Desktop/Duet
git add DuetCRM.html index.html CHANGELOG.md
git commit -m "vX.Y.Z: <one-line summary>"
git push origin main

# 6. Wait ~30-60s for GitHub Pages to deploy, then verify:
curl -s https://smaxim-spec.github.io/duet/ | grep "APP_VERSION"
```

## To pick up new version on devices
- **Laptop**: Cmd+Shift+R the CRM tab
- **Phone**: Force-close PWA + reopen (or Settings → Safari → Clear History & Website Data if cache is stuck)

---

## SECTION 1: Core Infrastructure (lines 1-900)

### What's here
- HTML structure, CSS variables, navbar, tab panels, modals
- Firebase sync engine (fbSave, fbLoad, fbLoadAll, firebaseLoadAll, firebasePushAll)
- Auto-backup system (createFirebaseBackup, restoreFirebaseBackup)
- Settings management (defaultSettings, agent name, branch, share %, goals)
- Products catalog (26 products with rates, categories, basis types)
- 2025 demo data (60 pipeline cases, 12 pay periods)
- 2026 projection data (10 cases, 8 periods)
- Data persistence (saveData, saveLeads, saveAgents, saveAppts, switchYear)

### Key constants
- `FIREBASE_URL`, `APP_VERSION`, `DEVICE_NAME`
- `products[]` — 26 insurance/annuity/banking products
- `defaultSettings{}` — agent config defaults
- `CALL_OUTCOMES[]` — 14 call result options
- `CALLEY_STAGE_LISTS{}` — 7 stage-to-list mappings
- `CARRIER_PHONES{}` — 11 products mapped to carrier phone numbers

### To work on this section, say:
"I want to work on **Core Infrastructure** — Firebase sync, settings, products, or data persistence"

---

## SECTION 2: Utilities & Formatters (lines 900-1265)

### What's here
- Date formatting (toYMD)
- Click-to-call links (carrierPhoneLink, clientPhoneLink)
- Commission calculation (calcCase)
- Tier badges (tierLabel, tierText)
- Status badges and progress bars (statusBadge, statusBar)
- Toast notifications (showToast)
- DOM shortcuts ($, $1)
- Currency formatting (fmt)
- Product option builder (prodOptions)
- Needs Analysis question frameworks (NA_QUESTIONS)

### To work on this section, say:
"I want to work on **Utilities** — formatting, calculation helpers, or needs analysis questions"

---

## SECTION 3: Calley Auto-Dialer Integration (lines 905-1194)

### What's here
- Calley API proxy config and auth token management
- Stage-to-list mapping (7 Calley lists)
- Push leads to Calley (single + batch)
- Export leads as XLS for manual Calley import
- Sync call results back from Calley with auto-stage transitions
- Disposition mapping (Calley outcomes → CRM outcomes)

### Status: POST /NewContact endpoint deprecated. Waiting on Calley for new endpoint.

### To work on this section, say:
"I want to work on **Calley Integration** — auto-dialer push, sync, or export"

---

## SECTION 4: Tab 0 — Walkthrough / Summary Dashboard (lines 1376-1512)

### What's here
- YTD statistics (cases, paid, varicent, MMA tier)
- Key months table with Varicent bonuses
- Split Agent Performance Report
- Product breakdown by category
- Reset demo data function

### To work on this section, say:
"I want to work on **Walkthrough Dashboard** — the summary/overview tab"

---

## SECTION 5: Tab 1 — $100K Goal Tracker (lines 1514-1753)

### What's here
- Monthly Varicent heat map
- Year-over-year comparison (2025 vs 2026)
- "What you need to sell" calculator
- Lead funnel visualization
- Bottleneck analysis with coaching advice
- Pay period detail table (gross/net/taxes/deductions)

### To work on this section, say:
"I want to work on **Goal Tracker** — the $100K dashboard, monthly heat map, or funnel analysis"

---

## SECTION 6: Tab 2 — Pipeline / Book of Business (lines 1755-2073)

### What's here
- Pipeline table with sort/filter (status, product category)
- Inline case editing
- Add new case form (with phone field)
- Advance case status (pending → submitted → approved → issued → paid)
- Split agent assignment and commission recalculation
- Carrier click-to-call on product names
- Client click-to-call on client names

### To work on this section, say:
"I want to work on **Pipeline / Book of Business** — cases, statuses, or commission tracking"

---

## SECTION 7: Tab 3 — Pay Period Entry (lines 2075-2210)

### What's here
- Two-panel form: Varicent statement + Workday payslip
- Live calculation preview
- Case match suggestions (within 5% variance)
- Confirm match (mark case as paid)
- Save new pay period record

### To work on this section, say:
"I want to work on **Pay Period Entry** — Varicent/Workday data entry or matching"

---

## SECTION 8: Tab 4 — Rate Table (lines 2211-2232)

### What's here
- Reference table of all products by category
- Product name, T4 rate, basis, special flags

### To work on this section, say:
"I want to work on **Rate Table** — product rates reference"

---

## SECTION 9: Tab 5 — Settings & Reports (lines 2233-2950)

### What's here
- Settings modal (agent name, branch, share %, goals, manager emails)
- Backup/Restore (JSON download + Firebase cloud backups)
- Manager Weekly Report generator (genReport)
  - Friday-Thursday week, goal progress, pipeline, CRM activity
  - HTML email body + Gmail compose link
- Agent Notification emails (commission update per agent)
- Changelog display

### To work on this section, say:
"I want to work on **Settings & Reports** — settings, backups, weekly reports, or agent emails"

---

## SECTION 10: Tab 6 — CRM / My Leads (lines 2951-5826) ⭐ LARGEST SECTION

### What's here
This is the biggest section (~2,875 lines). Sub-sections:

#### 10A: CRM State & Constants (lines 2951-3100)
- View state (queue/all/lead/bulk/agents/schedule)
- Stage definitions, colors, labels
- Meeting types, locations, calendar config
- Win/loss reasons, interest categories

#### 10B: Call Queue (lines 3100-3400)
- Smart Search bar (searches ALL leads including won/lost)
- Call cadence engine (10-attempt schedule across time blocks)
- Follow-up cadence by stage
- Queue filters (today/morning/afternoon/evening/new)
- Priority sorting (money-closest-to-close first)
- Callback date system (surfaces won/lost leads on due date)

#### 10C: Lead Detail View (lines 3400-3700)
- Full lead profile with edit capability
- Call log with outcome tracking
- Stage transition with auto-conversions
- Needs Analysis questionnaire
- Create pipeline case from lead
- Meeting scheduling with Google Calendar
- Callback scheduling (quick picks + custom)
- New Opportunity / Reopen for repeat business
- Past Deals history display

#### 10D: All Leads Table (lines 3700-3900)
- Filterable by stage, agent, search query
- Tel: links on phone numbers
- Bulk operations
- "Showing X of Y" count

#### 10E: Bulk Import (lines 3900-4100)
- 10-row grid for rapid lead entry
- Salesforce campaign bulk import

#### 10F: Split Agent Directory (lines 4100-4300)
- Agent CRUD (add/edit/remove)
- Alias mapping for name normalization
- Agent lead count and commission totals
- "Show leads" modal per agent

#### 10G: Schedule View (lines 4300-4500)
- Appointment slots by business day
- Meeting confirmations and reminders

### To work on this section, say:
"I want to work on **CRM** — then specify: Call Queue, Lead Detail, All Leads, Bulk Import, Agents, or Schedule"

---

## SECTION 11: Tab 7 — Funnel Health (lines 5527-5826)

### What's here
- $100K goal tracker (mirrored from dashboard)
- Weekly pipeline pace
- CRM activity vs last week
- Stage breakdown visualization
- Deal mix advisor (commission by product category)
- Split agent referral flow with timeframe toggle

### To work on this section, say:
"I want to work on **Funnel Health** — pipeline analysis, deal mix, or agent referral flow"

---

## SECTION 12: Tab 8 — CD to Annuity Conversion (lines 5827-6356)

### What's here
- CD vs Fixed Annuity comparison calculator
- Year-by-year growth illustration
- Tax impact (CD annual tax vs annuity tax-deferred)
- FDIC/guarantee, liquidity comparison
- Client email generation
- NEPQ Guided Conversation (5-phase questioning)
- Objection Handling scripts (5 scenarios)
- Florida Medicaid Asset Protection rules

### To work on this section, say:
"I want to work on **CD to Annuity** — comparison tool, NEPQ scripts, or Medicaid rules"

---

## SECTION 13: Tab 9 — Annuity vs Annuity Comparison (lines 6358-6781)

### What's here
- Compare two fixed annuity products side-by-side
- Feature table (issuer, term, bonus, guarantees, strategies)
- Year-by-year growth comparison
- Recommendation engine (age/term/rate analysis)
- Client email generation
- Product feature database (annuityFeatures)
- Illustration rate tables (avaIllustrationRates)

### To work on this section, say:
"I want to work on **Annuity Comparison** — product features, illustration rates, or recommendation engine"

---

## SECTION 14: Quick Book System (lines 6782-6982)

### What's here
- Floating action button (FAB) for quick booking
- Side-by-side form + Google Calendar iframe
- Client name search with CRM lead matching
- Next 5 business days with time slots
- Auto-update lead stage to meeting_set
- Google Calendar event creation

### To work on this section, say:
"I want to work on **Quick Book** — appointment booking or calendar integration"

---

## SECTION 15: Initialization & Auto-Sync (lines 6984-7041)

### What's here
- App startup sequence
- Firebase initial load with callback
- Auto-backup check (7-day threshold)
- 60-second polling interval for multi-device sync
- Top bar update

### To work on this section, say:
"I want to work on **Startup / Sync** — initialization, polling, or auto-backup"

---

## Pending / Future Work
- **Calley API new endpoint** — waiting on Calley support response
- **Call Scripts by stage** — deferred, user wants to add later
- **Multi-Agent Dashboards** — if partners join, agent-level views + leaderboard
- **Product Recommendation Engine** — auto-suggest based on needs analysis
- **Automated Email Sequences** — nurture emails by stage/time. First implementation: CD Maturity cold sequence (3-touch: auto-renewal trigger → tax angle → breakup). Select a lead → "Start CD Conversion Sequence" → auto-personalize from lead data (name, CD amount, maturity date, community) → timeline view (Day 0/5/13) → one-click Gmail compose pre-filled → track which email each lead is on. Template at `Desktop/Duet/CD_Maturity_Email_Sequence.md`
- **Performance Analytics** — call-to-close ratios, cycle time
- **Offline-First (Service Worker)** — full offline + background sync
- **Sell the CRM proposal** — Steve wants to create a sales pitch document
- **Install Superpowers plugin** — Evaluate obra/superpowers agentic skills framework for structured dev workflow (planning, TDD, systematic debugging, verification). Already cloned to `~/.claude/plugins/superpowers/` — needs SessionStart hook activation via `/clear` or new session. See: github.com/obra/superpowers
