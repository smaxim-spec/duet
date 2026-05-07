# DuetCoach — Technical Documentation
## Version 2.0.0 | Updated 2026-05-01 (Launch-Ready Release)

---

## Overview

DuetCoach is a daily sales roleplay practice app for insurance agents. It allows agents to practice sales conversations across 6 product categories using scripted, AI-powered, or script-adherence training modes. Includes a 7-day free trial of Pro features ($19/month subscription via Stripe). Built as a multi-file static site deployed on GitHub Pages.

- **Live URL**: https://duetbooksapp.github.io/duetcoach
- **App Direct URL**: https://duetbooksapp.github.io/duetcoach/app.html
- **GitHub Repo**: https://github.com/duetbooksapp/duetcoach
- **Firebase**: https://duet-crm-default-rtdb.firebaseio.com/duetcoach
- **Stripe Payment Link**: https://buy.stripe.com/8x2bJ17wu9gP9LW9iT5ZC00
- **Stripe Customer Portal**: https://billing.stripe.com/p/login/8x2bJ17wu9gP9LW9iT5ZC00
- **Local Dev File**: /Users/steve/Desktop/Duet/DuetCoach.html
- **Deploy Staging**: /tmp/duetcoach-deploy/

---

## Site Structure

| URL | File | Purpose |
|-----|------|---------|
| `/` | `index.html` | Marketing landing page |
| `/app.html` | `app.html` | The main app (mirror of DuetCoach.html) |
| `/DuetCoach.html` | `DuetCoach.html` | Legacy app URL (kept for backward compatibility) |
| `/terms.html` | `terms.html` | Terms of Service |
| `/privacy.html` | `privacy.html` | Privacy Policy |
| `/refund.html` | `refund.html` | Refund Policy |

---

## Architecture

- **Multi-file static site** with inline CSS and JavaScript (no external dependencies)
- **Firebase Realtime Database** (REST API) for cloud data storage and multi-device sync
- **Anthropic Claude API** (direct browser calls) for AI client mode and script scoring
- **ElevenLabs API** (direct browser calls) for voice synthesis
- **Stripe Payment Links + Customer Portal** for subscription billing
- **localStorage** for session data, API key storage, and onboarding state
- **GitHub Pages** for free static hosting

### Data Namespace
Each agent's data is stored at `/duetcoach/{agent_id}/` in Firebase with:
- `profile` — name, email, hashed PIN, paid status, trial start, terms acceptance timestamp
- `sessions` — array of all practice session records
- `settings` — preferences (mode, difficulty, daily goal)
- `streak` — current streak, longest streak, practice dates

Admin/system data:
- `/duetcoach/_pin_resets/{requestKey}` — PIN reset requests with status
- `/duetcoach/_feedback/{key}` — user feedback submissions
- `/duetcoach/_payments/{timestamp}` — Stripe success redirect logs (pending verification)

---

## Deployment Workflow

### Making Changes
1. Edit `/Users/steve/Desktop/Duet/DuetCoach.html` (working file)
2. Test locally: `file:///Users/steve/Desktop/Duet/DuetCoach.html`
3. Copy and push:
```bash
cp /Users/steve/Desktop/Duet/DuetCoach.html /tmp/duetcoach-deploy/index.html
cp /Users/steve/Desktop/Duet/DuetCoach.html /tmp/duetcoach-deploy/DuetCoach.html
cd /tmp/duetcoach-deploy
git add -A && git commit -m "description" && git push
```
4. Live at https://duetbooksapp.github.io/duetcoach within 30 seconds

### Git Remote
```
https://duetbooksapp:gho_TOKEN@github.com/duetbooksapp/duetcoach.git
```
(Uses same GitHub account as DuetBooks)

---

## Tab Structure

| Tab | Panel ID | Description |
|-----|----------|-------------|
| Practice | p0 | Mode selector, category/difficulty filters, persona cards, chat interface |
| History | p1 | Past sessions with scores, filters, expandable transcripts |
| Stats | p2 | Summary cards, bar chart, category breakdown, focus area, streak calendar |
| Team | p3 | Team leaderboard, weekly challenges, badges, invite link |
| Settings | p4 | API key, preferences, data management, account, about scoring |

---

## 3 Practice Modes

### 1. Scripted Mode (Free)
- Pre-built branching conversation trees per persona
- Client responses selected by keyword matching against agent's text
- No API key required
- Good for learning the conversation flow
- Scoring based on keyword accumulation

### 2. Claude API Mode (~$0.02/session)
- Claude plays the client in real-time using Anthropic API
- System prompt defines persona character, personality, objections, and behavior rules
- Fully dynamic — responds to exactly what the agent says
- Separate API call after session for scoring and coaching feedback
- Model: claude-sonnet-4-20250514

### 3. Script Training Mode (~$0.02/session)
- Agent practices their exact sales script against AI clients
- 27-29 checkpoints per category tracked in real-time
- Curveballs thrown ~30% of turns (tangents, emotional reactions, off-topic objections)
- Scored on: checkpoint adherence, script sequence, key phrases, curveball recovery, tone
- Progressive unlock: Easy (default) → Medium (score 75+) → Hard (score 80+)
- Per-category unlocking — each product tracks independently

---

## 6 Product Categories

### CD-to-Annuity
- **Script**: 5-stage (Connection → Engagement → Transition → Presentation → Commitment)
- **Checkpoints**: 27
- **Curveballs**: 15
- **Personas**: Margaret Chen (Easy), Robert & Linda Torres (Medium), Frank Kowalski (Hard)
- **Script File**: /Users/steve/Desktop/Duet/CD_Annuity_Call_Script.md

### Life Insurance (Final Expense)
- **Script**: 5-stage in-branch final expense conversation
- **Checkpoints**: 24
- **Curveballs**: 12
- **Personas**: Sarah Mitchell (Easy), James & Diane Hoffman (Medium), Carlos Rivera (Hard)
- **Script File**: /Users/steve/Desktop/Duet/Life_Insurance_Call_Script.md

### Life Conversion (Renewable Term → Fixed/UL)
- **Script**: 5-stage phone/outbound conversation from direct mail response
- **Checkpoints**: 27
- **Curveballs**: 12
- **Personas**: Tony Martinez (Easy), Rebecca Chen (Medium), Marcus Davis (Hard)
- **Script File**: /Users/steve/Desktop/Duet/Life_Conversion_Call_Script.md

### Long-Term Care (Eclipse Protector)
- **Script**: 5-stage in-office LTC/Eclipse Protector IUL conversation
- **Checkpoints**: 29
- **Curveballs**: 12
- **Personas**: Dorothy Williams (Easy), Gene & Patricia Anderson (Medium), Howard Price (Hard)
- **Product**: Securian Eclipse Protector II — $200K death benefit, $4,167/month LTC benefit, $629/month premium
- **Script File**: /Users/steve/Desktop/Duet/LTC_Call_Script.md

### Kids IUL (Wealth Building)
- **Script**: 5-stage conversation for parents wanting to build wealth for children
- **Checkpoints**: 28
- **Curveballs**: 12
- **Personas**: Jessica & Ryan Moore (Easy), Andre Washington (Medium), Kim & David Park (Hard)
- **Script File**: /Users/steve/Desktop/Duet/Kids_IUL_Call_Script.md

### IUL (Adult — Retirement/Banking/Income)
- **Script**: 5-stage with 3 presentation paths based on client goal
- **Paths**: Tax-Free Retirement, Infinite Banking, Lifetime Income Rider
- **Checkpoints**: 28
- **Curveballs**: 12
- **Personas**: Dr. Priya Patel (Easy/Retirement), Kevin & Maria Nguyen (Medium/Banking), Thomas Wright (Hard/Income Rider)
- **Script File**: /Users/steve/Desktop/Duet/Adult_IUL_Call_Script.md

---

## Scoring System

### Standard Modes (Scripted / Claude API)
5 categories, 20 points each, 100 total:
1. **Framework Completion** — Hit all 5 phases in order?
2. **Question Quality** — Open-ended, client-focused?
3. **Objection Handling** — Acknowledged and reframed?
4. **Empathy & Rapport** — Active listening, reflective statements?
5. **Close Technique** — Assumptive close tied to timeline?

### Script Training Mode
5 categories, 100 total:
1. **Checkpoints Hit** (30 pts) — How many of the script's checkpoints were covered
2. **Script Sequence** (20 pts) — Were checkpoints hit in the correct order?
3. **Key Phrases Used** (20 pts) — Framework language from the script
4. **Curveball Recovery** (20 pts) — Speed of getting back on script after distractions
5. **Tone & Language** (10 pts) — Permission-based vs. pushy phrasing

---

## Voice Mode (ElevenLabs)

### Setup
- Requires ElevenLabs API key (Starter plan: $5/month, 30,000 credits)
- Key stored in Settings tab → Voice Mode section → localStorage only (never synced)
- Model: `eleven_flash_v2_5` (75ms latency — near real-time)

### Voice-to-Persona Mapping
| Persona | ElevenLabs Voice | Voice ID |
|---------|-----------------|----------|
| Margaret Chen | Lily (warm, mature female) | pFZP5JQG7iQjIQuC4Bku |
| Robert & Linda Torres | Eric (smooth, professional male) | cjVigY5qzO86Huf0OWal |
| Frank Kowalski | Brian (resonant male) | nPczCjzI2devNBz1zQrb |
| Sarah Mitchell | Sarah (young, warm female) | EXAVITQu4vr4xnSDxMaL |
| James & Diane Hoffman | Bill (older, friendly male) | pqHfZKP75CvOlQylNhV4 |
| Carlos Rivera | Chris (natural, down-to-earth) | iP95p4xoKVk53GoZ742B |
| Tony Martinez | Liam (young, energetic male) | TX3LPaxmHKxFdv7VOQHJ |
| Rebecca Chen | Matilda (professional female) | XrExE9yKIg1WjnnlVkGX |
| Marcus Davis | Callum (gravelly, edgy male) | N2lVS1w4EtoT3dr4eOWO |
| Dorothy Williams | Bella (warm, bright female) | hpp4J3VqNfWAUOO0d1Us |
| Gene & Patricia Anderson | Roger (easy-going male) | CwhRBWXzGAHq8TQ4Fs17 |
| Howard Price | Daniel (strong, professional) | onwK4e9ZLuTAKqWW03F9 |
| Jessica & Ryan Moore | Laura (sunny, enthusiastic) | FGY2WhTYpPnrIDTdsKH5 |
| Andre Washington | Will (conversational, laid back) | bIHbv24MWmeRgasZH58o |
| Kim & David Park | Jessica (playful American) | cgSgspJ2msm6clMCkdW9 |
| Dr. Priya Patel | Alice (clear, engaging educator) | Xb7hH8MSUJpSbSDYk0k2 |
| Kevin & Maria Nguyen | Charlie (confident, energetic) | IKne3meq5aSn9XLyUdCD |
| Thomas Wright | George (warm, captivating) | JBFqnCBsd6RMkjVDRZzb |

### Push-to-Talk Mic
- **Hold the 🎤 button** to speak, **release** to send (walkie-talkie style)
- Uses Web Speech API (`SpeechRecognition`) — free, browser-native
- `continuous: true` — stays listening while held, auto-restarts if browser pauses
- Words appear in text box in real-time as you speak
- On release: text auto-sends as your message
- Falls back to click-to-toggle on desktop (15-second auto-stop safety)

### Voice Toggle
- Checkbox in session bar: "🔊 Voice" — toggle on/off mid-session
- Only appears when ElevenLabs key is configured
- When on: mic button appears, client responses spoken aloud
- When off: text-only mode, no audio

---

## Session Audio Recording

### How It Works
- **Auto-starts** when a voice mode session begins
- Uses Web Audio API `MediaRecorder` + `createMediaStreamDestination()`
- Mixes two audio sources into one track:
  1. Your mic input (MediaStream from `getUserMedia`)
  2. ElevenLabs client voice (routed through `createMediaElementSource`)
- Records as WebM/Opus (or MP4 fallback)
- **🔴 REC** indicator pulses in the session bar during recording

### After Session
- Recording saved as base64 data URL attached to the session record
- Appears in History tab with built-in audio player and download button
- File size shown below player

### Storage Management
- Last 10 recordings kept in localStorage
- Older recordings auto-stripped to prevent storage overflow (sessions kept, audio removed)
- Recordings do NOT sync to Firebase (too large) — local device only
- Download any recording you want to keep permanently

---

## Session Notes

### Capture
- Text area appears in the score modal after every session
- Placeholder: "How did that feel? Where did you struggle? What will you do differently next time?"
- Saved when tapping any "Save &" button (Practice Again, New Scenario, View History)

### History Tab
- Notes displayed in yellow "Your Notes" section per session
- Sessions without notes show a text area to add one later
- Existing notes have an "Edit note" link to modify

### Purpose
- Track personal reflections over time
- Identify recurring patterns ("rushed," "forgot the identity frame," "got thrown by the spouse objection")
- Future: Agent Performance Report will analyze notes for coaching insights

---

## Progressive Unlock System

Only applies to Script Training mode. Each category tracks independently.

| Level | Requirement |
|-------|------------|
| Easy | Always unlocked |
| Medium | Score 75+ on any Easy persona in that category |
| Hard | Score 80+ on any Medium persona in that category |

- Locked personas show lock icon, progress bar, and threshold text
- Celebration toast when a threshold is crossed
- Calculated from session history — no extra data stored

---

## Gamification Features

### 14 Badges
| Badge | Name | How to Earn |
|-------|------|-------------|
| ⭐ | First Steps | Complete 1 session |
| 🔥 | On Fire | 3-day streak |
| 💪 | Iron Will | 7-day streak |
| 🏆 | Unstoppable | 14-day streak |
| 👑 | Legend | 30-day streak |
| ⭐ | Sharp | Score 80+ |
| 💎 | Elite | Score 90+ |
| 🌍 | Well Rounded | Try all 12+ personas |
| 🥊 | Heavyweight | Score 75+ on Hard |
| 🎯 | Dedicated | 10 sessions |
| 🚀 | Committed | 25 sessions |
| 🥇 | Master | 50 sessions |
| 📚 | Full Range | All categories practiced |
| 🤖 | AI Sparring | Use Claude API mode |

### Weekly Challenges
Rotate automatically by week number:
1. Hard Mode Week — 3 Hard sessions
2. Consistency Challenge — Practice 5 of 7 days
3. Category Explorer — Practice all 4 categories
4. Score Crusher — 3 sessions scoring 75+
5. Marathon Week — 7 sessions
6. New Faces — 3 new personas
7. Objection Master — 3 CD-to-Annuity sessions

### Team Leaderboard
- Shows all registered agents ranked by streak
- Green dot = practiced today, gray = not yet
- Sessions this week, total sessions, best streak
- Current user highlighted with purple border
- Scores are private — only streaks and session counts visible

---

## Authentication

- PIN-based login (4-6 digits, SHA-256 hashed)
- Stored in Firebase at `/duetcoach/{agent_id}/profile`
- Session persists via `sessionStorage`
- Remembered agent names in `localStorage`
- API key stored in `localStorage` only (never sent to Firebase)

---

## Onboarding Flow (6 Steps)

Shown once per new account:
1. **Welcome** — Why practice daily (confidence, consistency, objection handling, accountability)
2. **How It Works** — 12+ personas, 6 categories, 5 sales framework phases
3. **Choose Your Mode** — Scripted vs Claude AI vs Script Training with API key input
4. **Scoring & Badges** — 5 scoring dimensions, badge preview
5. **Team & Accountability** — Green dots, streaks, weekly challenges, share link
6. **Ready to Practice** — Tips: start easy, move to hard, build the streak

Re-run available from Settings tab.

---

## Related Files

| File | Purpose |
|------|---------|
| `DuetCoach.html` | THE app (single file) |
| `CD_Annuity_Call_Script.md` | CD-to-Annuity sales script with checkpoints |
| `Life_Insurance_Call_Script.md` | Final expense sales script with checkpoints |
| `Life_Conversion_Call_Script.md` | Term conversion sales script with checkpoints |
| `LTC_Call_Script.md` | Long-term care / Eclipse Protector script |
| `Kids_IUL_Call_Script.md` | Kids IUL wealth-building script |
| `Adult_IUL_Call_Script.md` | Adult IUL (retirement/banking/income) script |
| `CD_Maturity_Email_Sequence.md` | 3-email cold outreach sequence for CD holders |
| `Duet_Project_Map.md` | Parent Duet CRM documentation |

---

## CSS Design System

Matches DuetBooks and DuetWithClaude:
```
--pri:#534AB7  (primary purple)
--grn:#1D9E75  (green - success)
--amb:#EF9F27  (amber - warning)
--red:#D94545  (red - error)
--bg:#f5f5f3   (page background)
--card:#fff    (card background)
--radius:8px   (border radius)
```

Responsive breakpoints: 768px (tablet), 480px (phone)
Mobile bottom nav with 5 tabs. Chat input fixed to bottom during sessions.

---

## localStorage Keys

| Key | Purpose |
|-----|---------|
| `db_coach_sessions` | Array of all practice session records |
| `db_coach_settings` | Preferences (mode, difficulty, daily goal) |
| `db_coach_streak` | Streak data (current, longest, practice dates) |
| `db_coach_apikey` | Anthropic API key (local only, never synced) |
| `dc_agent` | Current agent session (sessionStorage) |
| `dc_remembered_agents` | Remembered agent names for login |
| `dc_onboarding_done_{id}` | Onboarding completion flag per agent |

---

## Build History

| Date | Changes |
|------|---------|
| 2026-04-04 | Initial build — HTML shell, CSS, tab system, localStorage, 12 personas, 5 NEPQ phases |
| 2026-04-04 | Added scripted conversation trees for all personas |
| 2026-04-04 | Added Claude API mode (dynamic client + AI scoring) |
| 2026-04-04 | Added Practice, History, Stats, Settings tabs |
| 2026-04-04 | Deployed to GitHub Pages (duetbooksapp.github.io/duetcoach) |
| 2026-04-04 | Removed branded framework references (liability) |
| 2026-04-04 | Fixed mobile: pinned chat input bar, hidden nav during sessions |
| 2026-04-04 | Added PIN login/registration with Firebase cloud sync |
| 2026-04-04 | Added Team tab: leaderboard, 14 badges, weekly challenges, invite link |
| 2026-04-04 | Added 6-step onboarding wizard for new users |
| 2026-04-04 | Fixed Settings tab rendering to panel p4 |
| 2026-04-04 | Added Script Training mode: CD-to-Annuity (27 checkpoints, 15 curveballs) |
| 2026-04-04 | Added Life Insurance script training (24 checkpoints, 12 curveballs) |
| 2026-04-04 | Added Life Conversion category (27 checkpoints, 12 curveballs, 3 personas) |
| 2026-04-04 | Added Long-Term Care category (29 checkpoints, 12 curveballs, Eclipse Protector script) |
| 2026-04-04 | Added Kids IUL category (28 checkpoints, 12 curveballs, wealth-building script) |
| 2026-04-04 | Added Adult IUL category (28 checkpoints, 12 curveballs, 3 presentation paths) |
| 2026-04-04 | Added progressive unlock system (Easy→Medium 75+→Hard 80+, per category) |
| 2026-04-04 | Redesigned mode selector: 3 cards across with icons, descriptions, cost badges |
| 2026-04-04 | Shrunk practice calendar to compact 280px grid |
| 2026-04-04 | Added ElevenLabs voice mode: 18 unique persona voices, Flash v2.5 model |
| 2026-04-04 | Added push-to-talk mic: hold to record, release to send, auto-restart |
| 2026-04-04 | Added session audio recording: mic+TTS mixed, playback, download, REC indicator |
| 2026-04-04 | Added personal session notes: capture in score modal, view/edit in History |
| 2026-04-04 | Added searchable Help system with 14 topics (? button in top bar) |
| 2026-05-01 | **v2.0 Launch Release** — see new features below |
| 2026-05-01 | Created marketing landing page (index.html) with hero, pricing, features, FAQ |
| 2026-05-01 | Added Terms of Service, Privacy Policy, Refund Policy pages (Stripe verification) |
| 2026-05-01 | Moved app to /app.html with landing at root; DuetCoach.html kept for legacy |
| 2026-05-01 | Added email field + Terms acceptance checkbox on registration |
| 2026-05-01 | Added Forgot PIN flow with Firebase request logging |
| 2026-05-01 | Built admin dashboard (Steve Maxim only): user list, stats, PIN reset queue, grant/revoke Pro, delete users, CSV export, feedback inbox |
| 2026-05-01 | Built in-app feedback modal (saves to Firebase /_feedback/, shows in admin) |
| 2026-05-01 | Added Stripe paywall: 7-day trial, $19/mo subscription via Stripe Payment Link, customer portal for self-cancel |
| 2026-05-01 | Added Subscription section in Settings with plan badge + Upgrade/Manage buttons |
| 2026-05-01 | Replaced mailto links with in-app modals + Gmail compose URLs (mailto failed when no default email client) |
| 2026-05-01 | Scoring overhaul: strict Claude API rubrics, honest scripted scoring, fixed curveball/key phrase/tone in Script Training |
| 2026-05-01 | Category-specific key phrase scoring (was using only CD-to-Annuity phrases for all modes) |

---

## v2.0 Launch Release Notes

### Marketing & Legal Pages

- **Landing page** at root URL — hero, social proof, how-it-works, features grid, 6-category showcase, pricing comparison, FAQ, footer with legal links
- **Terms of Service** — personal practice only, no AAA affiliation, no sales guarantees, Florida governing law, third-party API responsibility
- **Privacy Policy** — what's stored where, API keys local only, recordings local only, GDPR/CCPA compliance language
- **Refund Policy** — 7-day free trial, no refunds after charge except duplicates/service issues, exception process

### User Authentication 2.0

- **Email field required** at registration (used for Forgot PIN, Stripe receipts, communications)
- **Terms acceptance checkbox** required before account creation — must agree to all 3 legal pages
- **Forgot PIN flow** — name + email submitted to Firebase `/_pin_resets/`; admin sees in dashboard and resets to temporary PIN
- **Account profile** now stores: name, email, hashed PIN, paid status, trial start date, terms acceptance timestamp

### Admin Dashboard (Hidden, Steve Maxim Only)

The admin tab appears only when logged in as exactly "Steve Maxim". Provides:

- **Stat cards**: Total Users, Paid Subscribers, Active This Week, Pending PIN Resets
- **Pending PIN Reset Requests** — approve to set a 4-digit temp PIN, opens Gmail compose with PIN pre-filled
- **Feedback Inbox** — all feedback submissions sorted by recency, unread badge, mark-read, delete, "Reply via Gmail" link
- **All Users table** — name, email, plan badge (Pro/Free), session count, streak, last active, action buttons
- **User actions**: Grant Pro / Revoke Pro / Delete account
- **Search filter** by name or email
- **CSV export** of all users for external analysis

### Stripe Subscription System

#### Pricing
- **Free tier**: Scripted mode in all 6 categories, no credit card required
- **Pro tier**: $19/month, includes Claude AI mode, Script Training, Voice mode, Session recording, Progressive unlock, Team features
- **7-day free trial** automatically granted on registration via Stripe Payment Link

#### Stripe Configuration
- **Product**: "DuetCoach Pro" at $19.00 USD/month recurring
- **Payment Link**: https://buy.stripe.com/8x2bJ17wu9gP9LW9iT5ZC00
- **Trial**: 7 days, $0 due today, $19 charged on day 8 unless canceled
- **Customer info collected**: Email + Full Name (no business name, no phone, no address)
- **Tax**: Collected automatically (Stripe Tax)
- **Post-payment redirect**: `https://duetbooksapp.github.io/duetcoach/app.html?paid=success`
- **Customer Portal**: https://billing.stripe.com/p/login/8x2bJ17wu9gP9LW9iT5ZC00 (users sign in with email to cancel/update)

#### Paywall Logic
- `isUserPaid()` returns true if: admin, profile.paid===true, or within 7-day trial window
- Free users see Claude AI and Script Training mode cards locked with "🔒 PRO" badge
- Clicking locked modes opens Upgrade modal with Stripe Payment Link
- Upgrade modal shows 7-day trial CTA, $19/mo pricing, feature list, current trial day count
- After payment, Stripe redirects to `?paid=success` → toast notification + Firebase log to `/_payments/` for admin verification
- **Admin must manually flag user as paid** in admin dashboard after verifying in Stripe (MVP — webhook automation in future)

#### Settings Subscription Section
- Shows current plan: Admin / Pro / Free Trial / Free
- "Upgrade to Pro" button (free/trial users) → Stripe Payment Link
- "Manage Subscription" button (paid users) → Stripe Customer Portal

### In-App Feedback System

- **Feedback button (💬)** in top bar next to Help button
- Opens modal in-app (no mailto, no email client dependency)
- User picks type: Bug Report / Feature Request / Question / Compliment
- Free-text message field
- Submits to Firebase `/_feedback/{key}` with: type, message, agent ID, name, email, paid status, timestamp, app version, user agent
- Admin sees all feedback in Admin Dashboard inbox
- Fallback link: "email steve.maxim@gmail.com directly" uses Gmail compose URL

### Bug Fixes in v2.0

- **Mailto failures** — replaced all `mailto:` links with either in-app modals or Gmail compose URLs (Chrome had no default email handler, opened blank pages)
- **Forgot PIN flow** no longer attempts to open user's email client
- **Admin Reset PIN** shows the temp PIN in a modal with "Open in Gmail" button + "Copy PIN" button
- **Feedback button** no longer uses mailto

---

## Help System

- **"?" button** in top bar opens a searchable help modal
- **14 topics** covering all features
- **Search bar** filters topics by keyword in real-time
- **Collapsible topics** — tap to expand/collapse
- Topics: Getting Started, Practice Modes, Personas, Script Training, Progressive Unlock, Voice Mode, Session Recording, Scoring, Session Notes, Team & Leaderboard, Badges, Weekly Challenges, Settings, Tips for Improvement

---

## Launch Materials

| File | Purpose |
|------|---------|
| `DuetCoach_Welcome_Email.md` | Email template for inviting first beta users |
| `DuetCoach_Video1_AnthropicKey.md` | Loom script for Anthropic API key setup video |
| `DuetCoach_Video2_ElevenLabsKey.md` | Loom script for ElevenLabs API key setup video |
| `DuetCoach_Video3_FirstSession.md` | Loom script for first practice session walkthrough |

### Pre-Launch Checklist (Soft Launch)
- [x] Marketing landing page with clear value prop
- [x] Terms / Privacy / Refund pages live
- [x] Stripe Payment Link verified and tested with real card
- [x] 7-day free trial configured
- [x] Stripe Customer Portal activated
- [x] Admin dashboard functional (user list, feedback, PIN resets)
- [x] In-app feedback button working (no mailto)
- [x] Forgot PIN flow tested
- [ ] Record 3 setup videos using saved Loom scripts
- [ ] Send welcome email to first beta user
- [ ] Monitor admin dashboard for first activity

---

## Pending / Future Work

### Near-Term (Post-Soft-Launch)
- **Stripe Webhook Automation** — Currently admin must manually flag users as paid after Stripe payment. A webhook endpoint (Firebase Cloud Function or Zapier/Make) could auto-update Firebase profile.paid when Stripe sends `customer.subscription.created` event. Eliminates manual admin step.
- **Email Sending Backend** — Currently PIN resets and feedback responses require Steve to manually compose emails via Gmail. A simple SendGrid or Mailgun integration would automate temp-PIN delivery and feedback acknowledgments.
- **Trial Expiration Email** — Send reminder on day 5 of trial: "Your trial ends in 2 days. Upgrade to keep Pro features."
- **Cancellation Win-Back** — When user cancels via Stripe portal, log it; send a follow-up "What can we improve?" email a week later.

### Mid-Term Features
- **NotebookLM Integration** — Pull real objection patterns from logged calls, personalize difficulty based on CRM win/loss data, adapt scenarios to each agent's weak spots
- **Call Recording Import** — Upload real call recordings, extract scripts from actual conversations, auto-generate personalized curveballs based on real client pushback
- **Agent-Specific Weak Spot Detection** — Analyze each agent's scoring history to auto-weight curveballs toward their weakest areas
- **Agent Performance Report** — After 10+ sessions per agent, generate AI-powered coaching report from scores + notes + transcripts. "Generate Report" button on Stats tab, costs ~$0.03-0.05 per report
- **Custom Script Upload** — Allow agents or managers to upload new scripts via the app (not just code changes)
- **Mobile-First Optimization** — Currently desktop-Chrome optimized. Mobile Safari has spotty Web Speech and recording support. Could build a simpler mobile UX that works around these limitations.

### Long-Term / Enterprise
- **Manager Dashboard** — Aggregate view of all agents' progress, identify who needs coaching on what (vs. current admin which is single-user only)
- **Multi-Office Leaderboard** — Compare teams across different AAA branches
- **Team Plans** — Group billing where one manager pays for X agents (vs. each agent paying $19/mo individually)
- **Session Replay** — Watch a past session play back in real-time with coaching annotations
- **White-Label Option** — Strip "DuetCoach" branding for other insurance organizations to license
