Par# Video 2: Getting Your ElevenLabs API Key
## Target length: 3-4 minutes

---

## Loom Setup
- Record desktop, your face in corner
- Have two browser tabs ready: elevenlabs.io and DuetCoach Settings page
- Sign out of both before recording so you can show the full flow

---

## Script

### [0:00] Intro
"Hey, this is Steve again. In the last video we got the Anthropic key — that's what powers the AI conversation. This video covers ElevenLabs, which is what gives the AI clients realistic voices in DuetCoach.

ElevenLabs has a free tier that gives you about 5-8 practice sessions a month. If you want more, the Starter plan is $5 a month and covers daily practice. Your call — start free, upgrade if you want more usage."

### [0:25] Step 1 — Go to ElevenLabs
"Open a new tab and go to **elevenlabs.io**. That's e-l-e-v-e-n-l-a-b-s dot i-o.

Click 'Sign Up' in the top right. Use Google sign-in if you have an account — easiest path."

[Show: navigating, clicking Sign Up, signing in with Google]

### [0:55] Step 2 — Skip the Onboarding
"After signing up, ElevenLabs will ask you a couple of questions about what you want to do. Choose **'ElevenCreative'** when it asks you to pick a platform — that's the one we need.

Then on the 'What would you like to do?' screen, pick **'Text to Speech'** and **'Voice cloning.'** Click Continue.

You can skip any other onboarding screens — we don't need them for DuetCoach."

[Show: ElevenCreative selection, Text to speech selection, skipping]

### [1:30] Step 3 — Find the API Keys Page
"Once you're in, look at the bottom of the left sidebar. You'll see a section called **'Developers.'** Click on it.

In the Developers area, click **'API Keys'** at the top.

Click the **'Create Key'** button on the right side."

[Show: clicking Developers, clicking API Keys tab, clicking Create Key]

### [2:00] Step 4 — Configure the Key
"A panel slides out on the right. Here's what to set:

**Name:** Type 'DuetCoach' so you remember what it's for.

**Restrict Key:** Leave the toggle on — this is for security.

**Endpoints:** This is important. The only one we need is **'Text to Speech.'** Click 'Access' next to it. Leave all the others as 'No Access.'

Click **'Create Key'** at the bottom."

[Show: naming, selecting Text to Speech, clicking Create]

### [2:40] Step 5 — Copy and Paste
"Same as Anthropic — the key only shows once. Copy it now. It starts with **sk_** followed by a string of characters.

Hop over to DuetCoach. Click **Settings** tab.

Scroll to the **'Voice Mode (ElevenLabs)'** section.

Paste your key.

Click **Save**, then click **Test.** You should hear a quick voice sample — that confirms it's working.

Then check the box that says **'Enable Voice Mode.'**"

[Show: copying, pasting in DuetCoach, Save, Test (with sound), checking Enable]

### [3:20] Wrap Up
"You're set up. The next video I'll walk you through your first practice session and show you how to use voice mode. Stay tuned."

---

## Things to Remember to Show
- The exact path through ElevenCreative onboarding
- Only enabling 'Text to Speech' permission (not the others)
- The Test button playing a sample (mention to listeners they should hear something)
- The 'Enable Voice Mode' checkbox

## Things NOT to Show
- Your actual API key (blur or use a fake one in post)
- Your billing info if you upgrade

## Optional Mention
- "If you want unlimited practice, the $5/month Starter plan covers about 25 sessions a month — way more than the free tier."
