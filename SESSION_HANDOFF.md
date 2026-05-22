# DuetCRM — Session Handoff (2026-05-20)

> Read this first when starting a new conversation about DuetCRM / DuetBooks. It captures the current state, recent decisions, and where to pick up.

---

## State as of session end (2026-05-20)

| App | Version | Source | Deployed |
|---|---|---|---|
| **DuetCRM** | `v1.18.0` | `~/.duet-server/DuetCRM.html` | https://smaxim-spec.github.io/duet/ |
| **DuetBooks** | `v1.3.0` | `~/Desktop/DuetBooks/DuetBooks.html` | https://duetbooksapp.github.io/duetbooks/ |
| Firebase | open rules | `https://duet-crm-default-rtdb.firebaseio.com/` | — |
| Calley webhook | Cloudflare Worker | `~/.duet-server/calley-webhook-worker.js` | `calley-webhook.smaxim.workers.dev` |

**Lead count:** ~510 (was 502 at start of session)
**DuetBooks cases:** ~69
**New leads not reached:** 201 (snapshot in `~/Desktop/Duet_New_Leads_Not_Reached_2026-05-19.xlsx`)

---

## Major architectural shifts during this session

### 1. Two-status model (CRM v1.16.1 → v1.16.4 + DuetBooks v1.3.0)
Every lead carries **both** an `opportunity` (CRM `stage`, terminal at Won/Lost) and a `policy` status (`policyStatus`, mirrors DuetBooks lifecycle). DuetBooks pushes status changes back to CRM via `PATCH /leads/data/<idx>/policyStatus`. Lead detail displays both badges side-by-side. App Submitted intentionally **never** auto-pushes to DuetBooks (50/50 hedge stage).

See [Duet_Project_Map.md § Two-Status Model](./Duet_Project_Map.md#two-status-model-v1161--v1162--v1163--duetbooks-v130) for the full mechanics.

### 2. CRM Cleanup tool (v1.16.0)
New nav tab. Reconciles Won CRM leads against DuetBooks, three buckets, bulk-delete with note preservation. **Always writes `/backups/cleanup_TIMESTAMP` first.**

### 3. DuetBooks → CRM pending banner (DuetBooks v1.2.0 → v1.3.0)
DuetBooks Dashboard shows orange banner for Won leads not yet in DuetBooks. Import modal creates the case + back-link via `crmLeadId`. Match rule: fuzzy name + phone (last 10 digits).

### 4. Calley webhook sync (v1.17.0)
Old `calleySyncResults` (used Calley REST API via `localhost:8787` proxy) is dead — replaced by `syncCalleyFromWebhook()` reading `/calley_webhook_logs` directly. Works on phone too. Auto-runs 4s after CRM load.

### 5. Phone-inbox auto-poll (v1.17.1)
Laptop polls `/phone_inbox_leads` every 60s — phone-added leads appear on laptop within a minute without manual reload.

### 6. Loss-reason modal (v1.18.0)
Marking Lost opens a modal: required dropdown (5 reasons) + optional 150-char notes. Cancel = no writes. Auto-loss paths (Calley, 10-attempt timeout, Bad #) bypass the modal.

### 7. Weekly Manager Report rebuild (v1.16.3 → v1.16.6)
New "Activity for This Week" flat-table section above "Cases Submitted This Week". Activity-based filter (Won this week / policy advance / settled / declined / lost this week). Both Opportunity and Policy columns explicit per row. Section order swapped per user pref (Cases Submitted on top). Policy badge colors aligned to DuetBooks scheme (Issued/Approved = purple).

### 8. Dark mode contrast fixes (v1.16.8 → v1.16.9)
Coach Notes (Critical/Warning/Insight callouts) and Sales Mastery cards had hard-coded light backgrounds without explicit text color — unreadable in dark mode. Fixed with rgba tints + `color:var(--txt)`.

---

## One-shot scripts run during this session (data state changes)

| Date | What | Why |
|---|---|---|
| 2026-05-07 | Linked 18 DuetBooks cases to CRM leads by name match + pushed `policyStatus` | Catch up the pre-two-status backlog (Cheryl, Adamastor, Courtney, John R., etc.) |
| 2026-05-07 | Pushed `policyStatus` from 7 cases with notes-parseable `crmLeadId` | Initial sync after DuetBooks v1.3.0 |
| 2026-05-15→19 | Ingested 50 Calley webhook calls + 31 stage transitions | Catch up pre-webhook-sync backlog |
| 2026-05-15 | Ingested Marilyn Pedroso from stuck `/phone_inbox_leads` | Phone-inbox sync gap |
| 2026-05-19 | Built `Duet_New_Leads_Not_Reached_2026-05-19.xlsx` (201 leads) | Caller assistance |

---

## Open items / known issues

| # | Item | Notes |
|---|---|---|
| 1 | **Firebase auth** still wide open (`{".read":true,".write":true}`) | Google sent warning email; plan was Anonymous Auth, ~1-2hrs work. Untouched. |
| 2 | **firebaseLoadAll merge bug** not root-fixed | Routed around via `forceCloudSync` (works fine, but underlying merge logic is still buggy). |
| 3 | **40 legacy DuetBooks cases** have no `crmLeadId` and no CRM match | Clients only in DuetBooks (Theresa Holloway, William B Steverson, etc.) — no action needed but they stay orphaned. |
| 4 | **4 ambiguous DuetBooks cases** skipped during auto-link | Daisy Delgado (3 cases, CRM stage='new' — reopened opportunity), Edward McKee (CRM stage='discovery' — reopened). Manual decision required. |
| 5 | **Adam Santos ↔ Adamastor Santos** name mismatch | Same person, different spellings. Was a discussion topic — fuzzy matcher can't catch nickname differences across phone-less DuetBooks records. Resolved by user manually (Adamastor stage moved on naturally). |
| 6 | **3 stale Issued cases** in DuetBooks (26-31 days) | John Mogavero $100k / Jennifer Jeffers $4k / Dupe Kuforiji $2.4k. User wanted to verify in carrier portal before marking paid. |
| 7 | **Caller-XLSX ingest script not yet built** | When the assistant returns the spreadsheet with Call Outcomes filled, will need a script to import those outcomes back into CRM. |

---

## Deploy routine (CRITICAL — don't skip steps)

Per [user's auto-memory `feedback_duetbooks_deploy.md`] and the CHANGELOG conventions:

### DuetCRM deploy
1. Edit `~/.duet-server/DuetCRM.html`
2. Bump `APP_VERSION` + `APP_BUILD_DATE` + add CHANGELOG entry in-app (lines ~316-410)
3. Mirror entry into `~/Desktop/Duet/CHANGELOG.md` (top)
4. **Sync all 4 deploy targets:**
   - `~/.duet-server/DuetCRM.html` (source)
   - `~/.duet-server/index.html`
   - `~/Desktop/Duet/DuetCRM.html`
   - `~/Desktop/Duet/index.html`
5. `cd ~/Desktop/Duet && git add . && git commit -m "vX.Y.Z: ..." && git push origin main`
6. Verify: `curl -s https://smaxim-spec.github.io/duet/ | grep APP_VERSION`
7. **Auto-backup**: `curl PUT https://duet-crm-default-rtdb.firebaseio.com/backups/auto_TIMESTAMP.json` with leads snapshot

### DuetBooks deploy (DIFFERENT REPO)
1. Edit `~/Desktop/DuetBooks/DuetBooks.html`
2. Bump version, add changelog entry in-app
3. Copy to `~/Desktop/DuetBooks/index.html`
4. `cd ~/Desktop/DuetBooks && git add . && git commit && git push origin main`
5. Pushes to `duetbooksapp/duetbooks` (NOT smaxim-spec) → serves at `duetbooksapp.github.io/duetbooks/`

---

## Key data paths

```
Firebase: https://duet-crm-default-rtdb.firebaseio.com/
├── leads/data[]              # CRM leads (array under .data key)
├── duetbooks/steve_maxim/
│   ├── cases[]                # DuetBooks cases (source of truth for closed deals)
│   ├── payperiods[]
│   ├── settings
│   └── auditLog
├── phone_inbox_leads          # Phone→Laptop append-only queue
├── phone_inbox_appts          # Phone→Laptop append-only queue
├── calley_webhook_logs        # Cloudflare Worker writes here on every Calley webhook
├── pipeline_2026              # Legacy CRM pipeline mirror (stale — don't trust)
├── backups/                   # All snapshots (pre-cleanup, pre-build, auto, etc.)
└── ... (other paths)
```

---

## Critical conventions

- **`crmEditId`** is the variable for which lead is open in detail view (NOT `selectedLeadId` — that was the bug we fixed in v1.15.4)
- **Phone is read-mostly.** Phone never pushes the leads/appointments array directly. Phone-only writes go to `/phone_inbox_*` (POST = append).
- **Desktop ingests phone inbox** on every load + every 60s (v1.17.1) via `ingestPhoneInbox()`
- **DuetBooks is truth for closed deals.** CRM's local `pl` mirror is legacy/stale — for "All Open Cases" the report fetches DuetBooks directly (v1.16.4).
- **Backup before destructive ops.** Cleanup tool, one-shot scripts, manual deletes — always snapshot to `/backups/*_TIMESTAMP.json` first.
- **camelCase field names** (`lostReason`, `lossNotes`, `policyStatus`, `policyStatusChangedDate`, `crmLeadId`, `wonReason`, `historyNotes`).

---

## Where things live

| Question | Answer |
|---|---|
| Where do I add code for CRM features? | `~/.duet-server/DuetCRM.html` (single file, ~12,800 lines) |
| Where do I add code for DuetBooks features? | `~/Desktop/DuetBooks/DuetBooks.html` (~4,800 lines) |
| Where's the Cloudflare Worker source? | `~/.duet-server/calley-webhook-worker.js` |
| Where do I find the section guide? | [`Duet_Project_Map.md`](./Duet_Project_Map.md) — has line-range table for each section |
| Where do I find recent version history? | [`CHANGELOG.md`](./CHANGELOG.md) |
| What if I break something? | Restore from `/backups/auto_TIMESTAMP` or `/backups/cleanup_TIMESTAMP` (most recent is `auto_2026...`) |

---

## Pick-up prompt for next session

To start a new session with full context, paste this:

> I'm continuing work on DuetCRM. Current version is **v1.18.0**, DuetBooks is **v1.3.0**. Read `~/Desktop/Duet/SESSION_HANDOFF.md` for the full state — that covers the two-status model, CRM Cleanup tool, DuetBooks→CRM pending banner, Calley webhook sync, phone-inbox auto-poll, and loss-reason modal we built in the previous session. Open items are listed in section "Open items / known issues." Today's task: [...].
