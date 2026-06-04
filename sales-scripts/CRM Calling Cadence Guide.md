# CRM Calling Cadence System — Reference Guide
**Duet with Claude | Steve Maxim | AAA Life Specialist**
**Last Updated: March 28, 2026**

---

## Overview

Every lead in the CRM follows a structured calling cadence based on their stage. The system automatically:
- Surfaces leads in the **Call Today** queue when they're due for a call
- Tracks progress (e.g., "Attempt 7/15" or "Follow-up 2/5")
- Auto-advances leads when call limits are reached
- Prioritizes leads closest to closing money first

**Daily Call Goal: 40 dials**

---

## Stage-by-Stage Cadence

### NEW (Fresh Leads)
- **Calls:** 3 per day (Morning, Afternoon, Evening blocks)
- **Schedule:** Day 1 only
- **Auto-advance:** After 3 calls with no contact → moves to **Attempting**

### ATTEMPTING (No Contact Yet)
- **Calls:** 3 per day (Morning, Afternoon, Evening blocks)
- **Schedule:**
  - Day 1: 3 calls (done in New stage)
  - Day 2: 3 calls → **wait 2 days**
  - Day 4-5: 3 calls → **wait 2 days**
  - Day 7: 3 calls → next day
  - Day 8-9: 3 calls (final round)
- **Total:** 15 attempts maximum
- **Auto-advance:** After 15 calls with no contact → **Lost** (reason: "No Contact After Max Attempts")

### CONNECTED (Spoke But No Meeting Yet)
- **Calls:** 1 per follow-up day
- **Frequency:** Every 2 days
- **Max follow-ups:** 5
- **Auto-advance:** After 5 follow-ups → **Nurturing** (warm)

### DISCOVERY (Learning Their Needs)
- **Calls:** 1 per follow-up day
- **Frequency:** Every 3 days
- **Max follow-ups:** 4
- **Auto-advance:** After 4 follow-ups → **Nurturing** (warm)

### MEETING SET (Appointment Booked)
- **Calls:** 1 per follow-up day
- **Special:** Confirmation call shows day before meeting
- **Frequency:** Every 3 days after meeting
- **Max follow-ups:** 3 (post-meeting)
- **Auto-advance:** After 3 follow-ups → **Nurturing** (warm)

### QUOTED (Solution Presented, Waiting on Decision)
- **Calls:** 1 per follow-up day
- **Frequency:** Every 2 days (these are hot — money on the table)
- **Max follow-ups:** 5
- **Auto-advance:** After 5 follow-ups → **Nurturing** (warm)

### NURTURING (Not Ready Yet)
- **Hot:** Call every 3 days
- **Warm:** Call every 7 days
- **Cool:** Call every 14 days
- **No maximum** — ongoing until they're ready or you change status

---

## Call Blocks (Time-of-Day)

Used for **New** and **Attempting** stages (3 calls per day):

| Block | Time Window |
|-------|------------|
| Morning | 9:00 - 10:00 AM |
| Afternoon | 1:00 - 2:00 PM |
| Evening | 5:30 - 6:30 PM |

The system enforces sequential order: Morning first, then Afternoon, then Evening.

---

## Call Outcomes & Auto-Actions

| Outcome | What Happens |
|---------|-------------|
| **No Answer** | Stays in current stage, counts toward attempt limit |
| **Left VM** | Stays in current stage, counts toward attempt limit |
| **Spoke - Interested** | Moves to **Discovery** |
| **Spoke - Wants Info** | Moves to **Meeting Set** |
| **Spoke - Not Ready** | Moves to **Nurturing** (warm) |
| **Spoke - Not Interested** | Moves to **Lost** |
| **Incorrect Number** | Moves to **Lost** (reason: Incorrect Number) |

---

## Call Today Queue Priority

Leads are sorted by proximity to money:

| Priority | Stage | Why |
|----------|-------|-----|
| 1 | Quoted (due today) | Closest to closing |
| 2 | Meeting Set (due today) | Appointment follow-up |
| 3 | New | Fresh leads, strike while hot |
| 4 | Attempting (active block) | Volume dial cadence |
| 5 | Connected (due today) | Already spoke, follow up |
| 6 | Discovery (due today) | Building relationship |
| 7-8 | Nurturing (hot) | Re-engagement |
| 15 | Nurturing (warm) | Longer-term follow-up |
| 25 | Nurturing (cool) | Low-priority check-in |

---

## Queue Visibility Rules

A lead only appears in the Call Today queue when action is needed:

- **New:** Always visible
- **Attempting:** Only during active call blocks (hidden during wait days)
- **Connected:** Visible when 2+ days since last call
- **Discovery:** Visible when 3+ days since last call
- **Meeting Set:** Visible day before meeting, day after, then every 3 days
- **Quoted:** Visible when 2+ days since last call
- **Nurturing:** Visible based on temperature (hot: 3d, warm: 7d, cool: 14d)
- **Won/Lost:** Never visible in queue

---

## History Panel

Each lead's detail page has a unified **History** panel that shows:
- **Call entries** — with block badge (morning/afternoon/evening), outcome, and notes
- **Note entries** — added via the "+ Add Note" button, shown with purple NOTE badge
- All entries sorted newest first

---

## Split Agent Email Notification

When a lead moves to **App Submitted**, the system:
1. Auto-creates a pipeline case in Book of Business
2. Moves the lead to **Won**
3. If the lead has an assigned split agent with an email, shows a toast to email them with:
   - Case details (client, product, premium, their commission)
   - Their stats (leads referred, cases won, conversion rate)
   - Goal tracker progress bar

---

## Settings

Adjustable in the Settings tab:
- **Daily Call Goal** — default 40
- **Weekly Appointment Goal** — default 15

---

*Generated by Duet with Claude*
