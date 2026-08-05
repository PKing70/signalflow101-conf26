# Instructor Rehearsal Guide

This document is for instructors and reviewers only. Do not send it to
attendees during the workshop. It includes the chaos-bot reveal.

Use this guide when you need to simulate the workshop end-to-end, including
the instructor-run chaos-bot and a normal participant view. It is intended for
dry runs, video capture, and co-presenter review.

## Video Capture Quick Start

Send this section to a reviewer who needs to set up before recording.
No Codex setup is required.

Before starting, the reviewer needs:

- The repo URL: `https://github.com/PKing70/signalflow101-conf26`.
- Access to the shared Splunk O11y organization.
- The workshop dashboard URL.
- Token secrets for `SPLUNK_INGEST_TOKEN` and `SPLUNK_API_TOKEN`.
- The realm, currently `us1`.
- A rehearsal participant ID outside the real attendee range, such as
  `participant-777`.
- A Replit account, unless using the CLI fallback path.

Then:

1. Clone or update the repo.
2. Create a local `.env` file for the chaos-bot with `SPLUNK_REALM=us1` and
   `SPLUNK_INGEST_TOKEN=<token secret>`.
3. Create the repo-local Python environment and install dependencies.
4. Start the chaos-bot locally.
5. In Replit, import the same repo or pull the latest `main`, add the four
   workshop values in Secrets, and run the attendee workflows in order:
   `0 - Check setup`, `1 - Start API`, `2 - Send latency metrics`,
   `3 - View fleet latency`, and `4 - Compute Apdex`.
6. Capture output only after secrets are hidden. The key visuals are `/hello`,
   sender output, fleet latency with `participant-000` as the outlier, Apdex
   with `participant-000` as Poor, and the Splunk O11y dashboard.

The detailed version of each step follows.

## Start From A Local Checkout

If this is a new local checkout:

```bash
git clone https://github.com/PKing70/signalflow101-conf26.git
cd signalflow101-conf26
```

If the repo already exists locally:

```bash
cd /path/to/signalflow101-conf26
git switch main
git pull
```

If `git pull` reports local changes, stop and use a fresh clone in another
folder for the rehearsal. Do not overwrite local work just to record the demo.

Use Python 3.10 or newer. On Mac/Linux, `python3` is usually the safest command.
On Windows PowerShell, use `py -3`.

Confirm Python before continuing:

Mac/Linux:

```bash
python3 --version
```

Windows PowerShell:

```powershell
py -3 --version
```

## Goal

By the end of this rehearsal, you should have:

- One terminal or environment running the chaos-bot as `participant-000`.
- One participant environment running as a test participant, such as
  `participant-777` or `participant-345`.
- Live latency metrics visible in Splunk Observability Cloud for both IDs.
- Fleet latency output that shows `participant-000` as the outlier.
- Apdex output that shows `participant-000` as Poor and the normal participant
  as Excellent.
- Clean screenshots or video clips that do not expose tokens or secrets.

## What To Prepare

You need access to the shared workshop Splunk Observability Cloud organization.

For the instructor chaos-bot:

- `SPLUNK_REALM`
- `SPLUNK_INGEST_TOKEN`

For the participant simulation:

- `SPLUNK_REALM`
- `SPLUNK_INGEST_TOKEN`
- `SPLUNK_API_TOKEN`
- `PARTICIPANT_ID`

Use token secrets, not token IDs.

For rehearsal and screenshots, use a participant ID outside the real attendee
assignment range, such as `participant-777` or `participant-345`. Do not use a
real attendee's assigned ID.

## Recommended Screen Layout

Use two separate environments:

- Instructor terminal: runs the chaos-bot.
- Participant environment: runs the same steps an attendee will run.

For participant simulation, Replit is the preferred path because it matches the
likely attendee experience. If Replit is unavailable, use the Splunk Show
SSH/CLI path or your own local Python environment.

Do not add a visible Replit workflow for the chaos-bot. Attendees import this
repo too, and a visible chaos-bot workflow would spoil the reveal.

## Step 1: Start The Chaos-Bot

From a terminal in the repo root, configure instructor values. You can copy the
example file and edit it, or create `.env` manually:

Mac/Linux:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

For the chaos-bot, `.env` only needs the ingest values:

```text
SPLUNK_REALM=us1
SPLUNK_INGEST_TOKEN=<token secret>
```

The chaos-bot ignores `PARTICIPANT_ID` and always sends as `participant-000`.

If the local Python environment does not have the workshop packages installed,
create a repo-local virtual environment and install dependencies:

Mac/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

If package install fails because a private package index returns an auth error,
rerun it against public PyPI:

Mac/Linux:

```bash
.venv/bin/python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

Then run:

Mac/Linux:

```bash
.venv/bin/python chaos-bot/chaos_bot.py
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python chaos-bot/chaos_bot.py
```

Expected output:

```text
Chaos bot starting - sending as participant-000
Satisfied: 180-280ms (25%) | Tolerating: 650-900ms (55%) | Frustrated: 1400-2000ms (20%)
Press Ctrl+C to stop.

[tolerating]   743.5ms  (spike rate: 0% over 1 sends)
[satisfied ]   214.7ms  (spike rate: 0% over 2 sends)
[frustrated]  1568.2ms  (spike rate: 33% over 3 sends)
```

Leave this running for the full rehearsal. Give it at least 2-3 minutes before
checking Apdex so the 5-minute SignalFlow window has enough samples.

## Step 2: Run The Participant Simulation In Replit

Follow the attendee path in `docs/REPLIT.md`.

Use these rehearsal values:

| Replit Secret | Rehearsal Value |
|---|---|
| `SPLUNK_REALM` | `us1` |
| `SPLUNK_INGEST_TOKEN` | workshop ingest token secret |
| `SPLUNK_API_TOKEN` | workshop API token secret |
| `PARTICIPANT_ID` | `participant-777` or another non-attendee test ID |

Then run these workflows:

1. `0 - Check setup`
2. `1 - Start API`
3. Open Preview and add `/hello` to the path.
4. `2 - Send latency metrics`
5. `3 - View fleet latency`
6. Stop the fleet query.
7. `4 - Compute Apdex`

Expected `/hello` output:

```json
{
  "participant_id": "participant-777",
  "message": "hello from participant-777",
  "simulated_processing_ms": 105.5
}
```

Expected sender output:

```text
API is reachable.
{
  "participant_id": "participant-777",
  "message": "hello from participant-777",
  "simulated_processing_ms": 92.3
}
Sending real latency metrics for participant-777...
Press Ctrl+C to stop.

Sent: 93.7ms
Sent: 112.0ms
```

Expected fleet output after the chaos-bot has run for a few minutes:

```text
--- Fleet Latency (top 2 of 2) ---
participant-000                              847.3ms  ████████████████████████████████████████████████████████████
participant-777                               96.1ms  █████████
```

Expected Apdex output after the chaos-bot has run for a few minutes:

```text
--- Apdex Scores (lowest 2 of 2, T=300ms) ---
participant-000                          0.52  Poor          ██████████
participant-777                          1.00  Excellent     ████████████████████
```

The exact numbers will vary. The important pattern is that `participant-000`
has much higher latency and a much lower Apdex score than the normal
participant.

## CLI Fallback For Participant Simulation

If you are rehearsing without Replit, use a second terminal or environment with
all four participant values configured:

```text
SPLUNK_REALM=us1
SPLUNK_INGEST_TOKEN=<token secret>
SPLUNK_API_TOKEN=<token secret>
PARTICIPANT_ID=participant-777
```

Run:

```bash
python workshop.py check
```

In terminal 1:

```bash
python workshop.py serve
```

In terminal 2:

```bash
python workshop.py send
```

In terminal 3:

```bash
python workshop.py fleet
```

Stop the fleet query, then run:

```bash
python workshop.py apdex
```

## Validate In Splunk Observability Cloud

Open the workshop dashboard:

```text
https://app.us1.observability.splunkcloud.com/#/dashboard/HOkNhxUAwAE?groupId=HOkNjAJA4AM
```

In dashboard group `SignalFlow 101 - .conf26`, open
`SignalFlow 101 - Workshop Fleet`.

Verify:

- `Fleet latency by participant` shows both the test participant and
  `participant-000`.
- `Chaos-bot latency` shows only `participant-000`.
- `Apdex by participant` shows `participant-000` as Poor or Unacceptable after
  enough data has accumulated.
- Normal participant IDs remain Excellent.

## Capture Checklist

For a clean reviewer or video-capture pass:

- Do not show `.env`, Replit Secrets, Splunk token pages, or copied token
  values.
- Capture Replit import/setup only after secrets are already entered, or blur
  the Secrets pane.
- Capture `0 - Check setup` succeeding.
- Capture Preview at `/hello`.
- Capture the sender printing `Sent: ...ms`.
- Capture the fleet query showing `participant-000` above the test participant.
- Capture Apdex showing `participant-000` as Poor and the test participant as
  Excellent.
- Capture the Splunk O11y dashboard after at least 2-3 minutes of bot traffic.

## Troubleshooting

**`participant-000` is missing:** Confirm the chaos-bot is still running, the
realm is `us1`, the ingest token is a token secret, and the bot has had at
least one minute to send data.

**The test participant is missing:** Confirm the participant sender is still
running, `PARTICIPANT_ID` is set to the test ID, and the Replit Secrets or
`.env` values are in the same Splunk realm as the chaos-bot.

**Fleet output works but Apdex is empty:** Wait another 2-3 minutes. Apdex uses
a longer SignalFlow window and needs enough samples to classify.

**`participant-000` Apdex is not Poor yet:** Let the bot continue to run. The
distribution converges over time. If it remains too healthy after a longer run,
tune the probabilities in `chaos-bot/chaos_bot.py`.

**More than one chaos series appears:** Stop any duplicate chaos-bot processes.
Only one bot should run as `participant-000`.

## Reset After Rehearsal

Stop the chaos-bot and participant sender with `Ctrl+C` or the Replit Stop
button. No Splunk data cleanup is normally required; the workshop charts use
recent time windows, so rehearsal datapoints age out.
