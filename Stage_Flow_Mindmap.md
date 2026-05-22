# DuetCRM — Stage Flow Mind Map

> Visual reference for how leads move through CRM stages and into the DuetBooks policy lifecycle.
> Render the Mermaid diagram in any markdown viewer (GitHub, Notion, VS Code preview, etc.) or copy to https://mermaid.live for an interactive view.

---

## Full flowchart

```mermaid
flowchart TD
    NEW[🆕 NEW<br/>Lead just added, never called]

    NEW -->|3 calls<br/>No Answer/Left VM<br/>auto| ATT[📞 ATTEMPTING<br/>Tried but not reached]
    NEW -->|Connected| CONN[🤝 CONNECTED<br/>Picked up, brief chat]
    NEW -->|Discovery| DISC[🔍 DISCOVERY<br/>Real conversation, qualifying]
    NEW -->|Appt Set| MTG[📅 MEETING SET<br/>Appointment booked]

    ATT -->|Connected| CONN
    ATT -->|Discovery| DISC
    ATT -->|Appt Set| MTG
    ATT -->|10 attempts,<br/>no contact<br/>auto| LOSTAUTO[❌ LOST<br/>'No Contact After Max Attempts']

    CONN -->|Discovery| DISC
    CONN -->|Appt Set| MTG

    DISC -->|Appt Set| MTG
    DISC -->|Quoted| QUO[💰 QUOTED<br/>Numbers given to client]

    MTG -->|Confirmed| MTG
    MTG -->|Rescheduled| MTG
    MTG -->|Quoted| QUO

    QUO -->|App Submitted| APP[📄 APP SUBMITTED<br/>Hedge stage — 50/50<br/>DOES NOT push to DuetBooks]
    QUO -->|Won| WON[🏆 WON<br/>Real deal — pushes to DuetBooks]

    APP -->|Won| WON

    NEW -.->|Nurturing<br/>any stage| NUR[🌱 INCUBATOR<br/>Not now, follow up later<br/>hot/warm/cool]
    ATT -.->|Nurturing| NUR
    CONN -.->|Nurturing| NUR
    DISC -.->|Nurturing| NUR
    MTG -.->|Nurturing| NUR
    QUO -.->|Nurturing| NUR

    NEW -.->|Lost / Bad #| LOST[💀 LOST<br/>User picks reason via modal]
    ATT -.->|Lost| LOST
    CONN -.->|Lost| LOST
    DISC -.->|Lost| LOST
    MTG -.->|Lost| LOST
    QUO -.->|Lost| LOST
    APP -.->|Lost| LOST

    WON ==>|auto-push<br/>convertToPipeline| DBSUB[(📋 DuetBooks: SUBMITTED<br/>policyStatus=submitted)]
    DBSUB ==>|Next button| DBAPP[(📋 APPROVED)]
    DBAPP ==>|Next button| DBISS[(📋 ISSUED)]
    DBISS ==>|Mark Paid /<br/>Varicent match| DBPAID[(💰 PAID)]
    DBAPP -.->|Declined| DBDEC[(❌ DECLINED<br/>CRM banner asks for reason)]
    DBISS -.->|Declined| DBDEC
    DBSUB -.->|Paid less| DBPARTIAL[(💵 PAID PARTIAL)]

    classDef terminal fill:#c0392b,color:#fff
    classDef won fill:#1D9E75,color:#fff
    classDef nurture fill:#9b59b6,color:#fff
    classDef duetbooks fill:#534AB7,color:#fff
    classDef declined fill:#777,color:#fff

    class LOST,LOSTAUTO terminal
    class WON won
    class NUR nurture
    class DBSUB,DBAPP,DBISS,DBPAID,DBPARTIAL duetbooks
    class DBDEC declined
```

---

## The 5 Phases

| # | Phase | Stages | What's happening |
|---|---|---|---|
| 1 | **Hunting** | `new` → `attempting` | Calling, leaving voicemails, building call count |
| 2 | **Engaging** | `connected` → `discovery` | Got them on the phone, learning needs |
| 3 | **Committing** | `meeting_set` → `quoted` | Scheduled, numbers presented |
| 4 | **Closing** | `app_submitted` → `won` | Paperwork in flight → deal closed |
| 5 | **Policy** | DuetBooks: `submitted` → `approved` → `issued` → `paid` | Underwriting + payment lifecycle (DuetBooks owns) |

---

## Transition triggers

| From | To | Trigger | Auto/Manual |
|---|---|---|---|
| `new` | `attempting` | 3+ calls logged with No Answer / Left VM | 🤖 **AUTO** (logCall + Calley sync) |
| `new`/`attempting` | `connected` | Disposition = "Connected" | 👆 Manual |
| `new`/`attempting`/`connected` | `discovery` | Disposition = "Discovery" | 👆 Manual |
| any active | `meeting_set` | Disposition = "Appt Set" | 👆 Manual |
| `discovery`/`meeting_set`/`quoted` | `quoted` | Disposition = "Quoted" / manual stage | 👆 Manual |
| `quoted`/`meeting_set` | `app_submitted` | Disposition = "App Submitted" | 👆 Manual — **NOT pushed to DuetBooks** |
| `quoted`/`app_submitted` | `won` | Disposition = "Won" / manual stage | 👆 Manual — **AUTO-pushes to DuetBooks at status=submitted** |
| `attempting` | `lost` (auto) | 10+ attempts, no contact ever | 🤖 **AUTO** — reason "No Contact After Max Attempts" |
| any | `lost` (user) | Click "📉 Mark Lost" button | 👆 Modal — required reason + optional 150-char notes |
| any | `lost` (Calley) | Calley feedback "Lost" or "Bad #" | 🤖 **AUTO** — defaults "Not Interested" / "Bad Number" |
| any | `incubator` | Disposition = "Nurturing" | 👆 Manual — temp=warm by default |

---

## Terminal states (lead is no longer "active")

- **`won`** — drives the DuetBooks policy lifecycle. Two-status model: opportunity stays Won forever, policy cycles through underwriting.
- **`lost`** — reason captured (from modal or auto-default).
- **`incubator`** — parked. Comes back when callback date hits.

---

## Critical architecture rule

> **Only `won` auto-pushes to DuetBooks.** `app_submitted` is deliberately CRM-only — used when you've sent the app but think it's 50/50. Don't clutter DuetBooks with speculative records.

This is why both the CRM Cleanup tool and the DuetBooks pending banner filter on `stage === 'won'` only.

---

## DuetBooks-side flow (after Won)

```mermaid
stateDiagram-v2
    [*] --> Submitted: CRM auto-push<br/>(convertToPipeline)
    Submitted --> Approved: Next button / dropdown
    Approved --> Issued: Next button / dropdown
    Issued --> Paid: Mark Paid /<br/>Varicent reconciliation
    Submitted --> Declined: Carrier rejected
    Approved --> Declined: Health rating, etc.
    Issued --> Declined: Final decline
    Submitted --> PaidPartial: Partial payment
    Approved --> PaidPartial: Partial payment
    Issued --> PaidPartial: Partial payment
    Paid --> [*]
    Declined --> [*]: CRM banner asks for reason<br/>(prepends DECLINE: historyNote)
    PaidPartial --> [*]

    classDef terminal fill:#777,color:#fff
    class Declined,Paid,PaidPartial terminal
```

Every status change in DuetBooks **pushes back to the matching CRM lead** via `PATCH /leads/data/<idx>/policyStatus` if the case has `crmLeadId`. This is what makes the Policy badge in the CRM lead detail stay in sync.

---

## Quick decision guide for the rep

```
Did they pick up?
├── No  → Pick: No Answer / Left VM / Bad #
│         └── 3rd call → AUTO-promotes to Attempting
│         └── 10th call with no contact → AUTO-marks Lost
├── Yes, briefly → "Connected" → stage moves to Connected
├── Yes, real talk → "Discovery" → stage moves to Discovery
├── Yes, booked → "Appt Set" → stage moves to Meeting Set + Quick Book opens
├── Yes, gave quote → "Quoted" → stage moves to Quoted
├── Yes, sent app (might fail) → "App Submitted" → stays in CRM, not DuetBooks
├── Yes, closed → "Won" → AUTO-pushes to DuetBooks at submitted
├── Yes, no thanks → "📉 Mark Lost" → modal asks reason + notes
└── Yes, not now → "Nurturing" → parks in Incubator (set callback date)
```

---

*Generated 2026-05-22 — pairs with [Duet_Project_Map.md](./Duet_Project_Map.md) and [SESSION_HANDOFF.md](./SESSION_HANDOFF.md).*
