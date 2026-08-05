# CONTEXT.md — SignalFlow 101 Workshop · Working State Handoff

This file is for continuing work in a new Claude conversation.
Paste it at the start of a new chat to restore full context.

---

## Who I Am

I am a Senior Staff Technical Writer at Splunk on the developer advocacy team.
I build documentation, code examples, and workshops for Splunk Enterprise apps.
I am NOT a Splunk Observability Cloud expert — I know Python and workshop design
well, but needed to learn O11y concepts as we built this. I am presenting solo
(co-presenter was laid off). A new co-presenter will join eventually.

My GitHub: https://github.com/PKing70
Workshop repo: https://github.com/PKing70/signalflow101-conf26

---

## The Workshop

**Title:** SignalFlow 101: Build Your First App for Splunk Observability Cloud
**Conference:** .conf26
**Format:** 60-minute hands-on workshop
**Session ID:** DEV1942

**Audience:** Splunk Observability Cloud users and power users. Familiar with
dashboards, detectors, metrics, dimensions. NOT expected to be developers or
coders. May be analysts or admins. Should not be talked down to — they are
technically sophisticated, just not in Python specifically.

**Core premise:** Everything in Splunk O11y is powered by SignalFlow. The UI
is one way in. The API — callable from Python, curl, Terraform, anything — is
another. This workshop shows attendees what SignalFlow unlocks beyond the UI.

---

## Workshop Arc (60 minutes)

| Time  | Activity |
|-------|----------|
| 0:00  | Intro, SignalFlow framing |
| 0:10  | Setup — workshop environment, credentials |
| 0:20  | Checkpoint 1 — metric visible in O11y |
| 0:22  | Exercise 2 begins |
| 0:35  | Checkpoint 2 — chaos-bot found |
| 0:37  | Exercise 3 begins |
| 0:50  | Checkpoint 3 — Apdex scores visible |
| 0:52  | Demo: programmatic dashboard (instructor runs) |
| 0:55  | Take-home overview, resources |
| 0:58  | Q&A |

---

## Key Design Decisions (and why — important for new co-presenter too)

**Shared O11y organization, not per-attendee O11y**
Each attendee has their own development environment/login, but the workshop
uses one shared Splunk Observability Cloud organization for up to 200
attendees. This gives us the social "whole class" dashboard moment and one
cleanup job.

**participant_id dimension = participant alias**
Use aliases like `participant-001` through `participant-200`, not attendee
email addresses. Easier privacy story on shared dashboards and still unique.

**Python environment options**
Zero install friction is the priority. Supported attendee paths are Replit,
the shared Splunk Show Python environment over SSH/CLI, and a participant's
own pre-existing Python environment. Local Python is not a support target
during the 60-minute session.

**Paste-and-run instructional approach**
Code blocks just work when pasted. Optional collapsed `<details>` explainers
for attendees who want to understand the code. No one is required to read them.
Voice/tone: treat audience as intelligent professionals, not CS students.
Never explain what Apdex is. Do explain what `import` means.

**chaos-bot as the fleet mystery, not a real attendee**
`participant-000` sends elevated latency metrics before and during the
workshop. Attendees investigate and find it. Never target a real attendee
as the "slow one" — they're already under enough pressure.

**Apdex as the "beyond the UI" payoff**
Apdex (T=300ms) is the metric O11y can't compute natively. SignalFlow can.
This is the moment that justifies the whole workshop. Don't rush it.

**The "API platform" insight**
Splunk O11y isn't a web app with an API bolted on — it's an API platform with
a web app built on top. Python, curl, Terraform, CI/CD all have equal access.
This is stated explicitly in Exercise 2's talking points and the slide deck.

---

## Repository Structure

```
signalflow101-conf26/
├── README.md
├── .replit                      ← Replit run button and workflow config
├── config.py                    ← loads env/.env, exports INGEST_TOKEN/API_TOKEN/REALM/PARTICIPANT_ID
├── workshop.py                  ← helper commands used by workflows and CLI paths
├── workshop_api.py              ← personal API measured by exercises
├── signalflow_rest.py           ← direct SignalFlow REST/SSE helper
├── apdex.py                     ← reusable build_apdex_program() function
├── requirements.txt
├── .env.example                 ← copy to .env, never commit .env
├── .gitignore
├── exercises/
│   ├── exercise1.py             ← send fake latency, verify pipeline
│   ├── exercise2a.py            ← send real measured latency (continuous)
│   ├── exercise2b.py            ← SignalFlow fleet investigation
│   ├── exercise3.py             ← Apdex computation
│   └── apdex.py                 ← compatibility import for build_apdex_program()
├── takehome/
│   ├── takehome1_api.py         ← FastAPI with /github endpoint (port 8001)
│   ├── takehome1_sender.py      ← sends workshop.github.latency
│   ├── takehome1_apdex.py       ← Apdex on GitHub metric via apdex.py
│   ├── takehome2_detector.py    ← creates Apdex detector via REST API
│   ├── takehome2_spike.py       ← injects 1800ms latency to trigger detector
│   ├── takehome3_slo.py         ← computes SLO burn rate in SignalFlow
│   └── takehome3_detector.py    ← creates burn rate detector via REST API
├── chaos-bot/
│   └── chaos_bot.py             ← instructor runs this before/during workshop
├── workshop-setup/
│   ├── build_dashboards.py      ← creates/updates the workshop dashboard
│   ├── generate_participant_aliases.py ← prints participant alias CSV
│   ├── REHEARSAL_GUIDE.md       ← instructor-only chaos-bot + participant simulation guide
│   └── INSTRUCTOR_NOTES.md      ← day-of checklist, timing, contingencies
└── docs/
    ├── EXERCISE_GUIDE.md        ← complete exercise document
    ├── REPLIT.md                ← Replit setup and workflow guide
    ├── SPLUNK_SHOW.md           ← Splunk Show SSH/CLI setup guide
    ├── signalflow101_conf26.pptx ← slide deck draft
    └── signalflow101_conf26.pdf  ← PDF export
```

---

## Python / API Approach

**Credential loading:** All scripts import from `config.py` at repo root.
`config.py` uses `python-dotenv` to load `.env` when present, also works with
Replit Secrets/environment variables, and validates the required values
(INGEST_TOKEN, API_TOKEN, REALM, PARTICIPANT_ID) on import, failing fast with a
clear message if any are missing.

**Metric ingest (Exercises 1, 2a, chaos-bot, take-home senders):**
Direct REST API via `requests.post()` to:
`https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint`
Header: `X-SF-TOKEN: {INGEST_TOKEN}`

**SignalFlow computations (Exercises 2b, 3, take-home Apdex/SLO):**
Uses direct REST via `requests.post()` to:
`https://stream.{REALM}.observability.splunkcloud.com/v2/signalflow/execute`
The response is a Server-Sent Events stream parsed by `signalflow_rest.py`.

Pattern used throughout:
```python
from signalflow_rest import stream_signalflow

for event_name, payload, metadata in stream_signalflow(program, API_TOKEN, REALM):
    if event_name == "data":
        for point in payload.get("data", []):
            tsid = point.get("tsId")
            value = point.get("value")
            meta = metadata.get(tsid, {})
```

**Detector creation (take-home 2 and 3):**
Direct REST API via `requests.post()` to:
`https://api.{REALM}.observability.splunkcloud.com/v2/detector`
⚠️ VERIFY: detector URL format for UI navigation after creation.

---

## Chaos Bot

`chaos-bot/chaos_bot.py` — fully implemented.
Sends as `participant-000` (never an attendee alias).

Parameters (tunable at top of file):
- Satisfied: 180-280ms, 25% frequency
- Tolerating: 650-900ms, 55% frequency
- Frustrated: 1400-2000ms, 20% frequency
- Send interval: 5 seconds
- Expected Apdex: ~0.50–0.55 (Poor) vs attendees at ~0.95+ (Excellent)

Run from repo root: `python chaos-bot/chaos_bot.py`
Requires only SPLUNK_INGEST_TOKEN (or SPLUNK_ACCESS_TOKEN fallback) and
SPLUNK_REALM in .env (not PARTICIPANT_ID).

For dry runs and reviewer/video-capture simulation, use
`workshop-setup/REHEARSAL_GUIDE.md`. It walks through running the instructor
chaos-bot alongside a normal participant environment without exposing this
attendee-spoiling flow in Replit workflows.

---

## Apdex Formula

T = 300ms for this workshop (safer than 200ms given browser and shared-environment network latency).

```
Apdex = (Satisfied + Tolerating/2) / Total

Satisfied:   latency < 300ms
Tolerating:  300ms <= latency < 1200ms  (T to 4T)
Frustrated:  latency >= 1200ms
```

Ratings: 0.94+ Excellent | 0.85+ Good | 0.70+ Fair | 0.50+ Poor | <0.50 Unacceptable

The reusable function `build_apdex_program(metric_name, t=300, window='5m')`
in root-level `apdex.py` generates the full SignalFlow program string.
Verified against live O11y data: Apdex bucket counting must classify latency
values, so the program uses `rollup='latest'` and maps each present value to
bucket counters. `rollup='count'` counts datapoints in the rollup interval and
does not preserve the latency value for threshold comparisons.

---

## Take-home Exercises Summary

**TH1 — Make Your API Interesting**
Adds /github endpoint to FastAPI, measures real GitHub API latency, sends as
`workshop.github.latency` with both `participant_id` and `github_username`
dimensions. Introduces `build_apdex_program()` abstraction. ~20–30 min.

**TH2 — Build a Detector That Pages You**
Creates Apdex detector via REST API (Warning severity, lasting='5m').
Triggers it with `takehome2_spike.py` (sends 1800ms flat). ~20–30 min.

**TH3 — The SLO Error Budget**
SLO: 99.5% satisfied in 1h window. Computes burn rate = current_error_rate /
allowed_error_rate. Alert at 2x. Creates burn rate detector (Critical severity,
lasting='10m'). ~25–35 min.

---

## Outstanding Items / Placeholders

### Must resolve before conference (requires O11y instance):
- [ ] Verify SignalFlow REST/SSE parsing against the real O11y instance
- [x] Verify Apdex bucket counting semantics in SignalFlow
- [ ] Verify detector URL format in O11y UI
- [x] Implement `workshop-setup/build_dashboards.py`
- [ ] Fill in remaining O11y navigation steps:
      - Exercise 1 Step 3: finding metric in Data Explorer
- [ ] Fill in credential delivery section (Splunk Show flow TBD)
- [ ] Run `workshop-setup/REHEARSAL_GUIDE.md` against real data and tune chaos-bot parameters if needed
- [ ] Full dry run end-to-end, timed

### Pending external dependencies:
- [ ] Splunk Show instance provisioning details
- [ ] .conf26 official PowerPoint template → final slides
- [ ] New co-presenter identified → onboarding rationale summary

### Nice to have:
- [ ] Replit attendee workflow dry run
- [ ] Splunk Show SSH/CLI dry run
- [ ] Screenshots from real O11y instance for slide deck

---

## Slide Deck State

Draft PPTX at `docs/signalflow101_conf26.pptx` (29 slides).
Built from .conf24 DEV1588B as style reference. PowerPoint reports
a minor repair issue on open — acceptable for draft, will be rebuilt
from official .conf26 template when available.

Slide structure:
1. Forward-looking statements
2. Title slide
3. Presented by (photo placeholders)
4–8. Your Workshop agenda (builds up)
9. What is SignalFlow? (section divider)
10–11. SignalFlow concept + code
12. Workshop repo QR/link
13. Exercise 1 section divider
14. Exercise 1 content
15. Checkpoint 1
16. Exercise 2 section divider
17. Exercise 2a content
18. Exercise 2b content
19. Checkpoint 2
20. Exercise 3 section divider
21. Apdex explainer
22. Exercise 3 code
23. Checkpoint 3
24. "Splunk O11y is an API platform" quote slide
25. Beyond the Workshop section divider
26. Take-home overview
27. Key Takeaways
28. Workshop repo QR/link (closing)
29. Congrats / Thank you

---

## Immediate Next Steps (start here)

1. **Validate Exercise 1** against free trial O11y instance — proves ingest works
2. **Verify participant_id aliases** such as `participant-042` group correctly
3. **Verify SignalFlow REST/SSE helper** — run exercise2b.py
4. **Verify Apdex bucket counting** — run exercise3.py against live data
5. **Run chaos-bot rehearsal** using `workshop-setup/REHEARSAL_GUIDE.md` and observe in O11y
6. **Keep dashboard validation current** — Fleet latency, chaos-bot latency, and Apdex charts
7. **Fill in exercise doc placeholders** as each piece is verified

---

## Voice and Tone (important for all content)

- Audience knows what Apdex, P95, latency, detectors, and dimensions are. Never define these.
- Audience does NOT know what `import`, a function, or a lambda is. Explain briefly.
- Tone: senior SRE colleague who is a good explainer. Not a teacher talking down, not a developer assuming too much.
- Never say "straightforward", "honestly", or "genuinely."
- No bullet points in prose. No excessive bolding.
- Pitchman tone crept in occasionally in earlier drafts — watch for it and dial back.

---

*Last updated: May 2026 · Repo: github.com/PKing70/signalflow101-conf26*
