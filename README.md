# SignalFlow 101: Build Your First App for Splunk Observability Cloud

**Workshop · 60 minutes · .conf26 · DEV1942**

Short link: [https://tinyurl.com/DEV1942](https://tinyurl.com/DEV1942)

This repository contains everything you need for the SignalFlow 101 workshop. You'll write Python that talks directly to the Splunk Observability Cloud SignalFlow API — sending metrics, investigating a fleet-wide latency anomaly, and computing an Apdex score that the O11y UI can't give you out of the box.

---

## Get Started (Attendees)

Choose one path and stay in that guide for the whole workshop. Each guide
includes setup, Splunk Observability Cloud token lookup, Exercise 1, Exercise 2,
Exercise 3, and the take-home exercises for that environment.

The supported workshop paths are:

1. **[Replit](docs/EXERCISES_REPLIT.md)** — recommended in-room path; browser-based Python with repo-defined workflows. Visual, easy, and fun! Not every IT department allows Replit, so we have fallback paths below.
2. **[Splunk Show SSH](docs/EXERCISES_SPLUNK_SHOW.md)** — the exact same code as Replit, but running from a hosted Linux instance command line. Choose this if you like old-school, command-line experiences, or if Replit is blocked by your laptop, browser, or policy.
3. **[Local Python](docs/EXERCISES_LOCAL.md)** — use this if you already code in Python on your laptop. It runs the exact same code as the other paths. We won't have time to set up your Python installation or IDE during the workshop, and we might not be familiar with your environment if you have questions.

Do not try to merge instructions across files. Pick the one environment you are
using and keep reading that guide.

For the workshop, each participant has their own development environment/login,
but everyone sends data to the same Splunk Observability Cloud organization in
realm `us1`. `PARTICIPANT_ID` is assigned by workshop staff and separates your
metrics from everyone else's.

The workshop handout provides links to the repo, Splunk Show, and the workshop
O11y organization. It does not print token values; after signing in to O11y,
copy the current ingest and API token values from **Settings > Access Tokens**.

---

## Repository Structure

```
signalflow101-conf26/
│
├── README.md                        ← you are here
├── requirements.txt                 ← Python dependencies
├── .replit                          ← Replit run button and workflow configuration
├── config.py                        ← loads credentials from environment or .env
├── workshop.py                      ← helper commands used by workflows and CLI paths
├── workshop_api.py                  ← personal API measured by the exercises
├── apdex.py                         ← reusable Apdex SignalFlow program builder
├── .env.example                     ← credential template — copy to .env
│
├── exercises-python/                ← in-workshop Python scripts, not attendee docs
│   ├── exercise1.py                 ← send your first metric
│   ├── exercise2a.py                ← send real measured latency
│   ├── exercise2b.py                ← investigate the fleet with SignalFlow
│   ├── exercise3.py                 ← compute Apdex
│   └── apdex.py                     ← compatibility import for the reusable Apdex function
│
├── takehome/                        ← self-paced exercises for after the workshop
│   ├── takehome1_api.py             ← FastAPI with GitHub downstream dependency
│   ├── takehome1_sender.py          ← send GitHub latency metrics
│   ├── takehome1_apdex.py           ← Apdex on the GitHub metric
│   ├── takehome2_detector.py        ← create a detector via REST API
│   ├── takehome2_spike.py           ← trigger the detector intentionally
│   ├── takehome3_slo.py             ← compute SLO burn rate
│   └── takehome3_detector.py        ← create a burn rate detector
│
├── chaos-bot/
│   └── chaos_bot.py                 ← instructor-run bot that seeds the fleet mystery
│
├── workshop-setup/                  ← instructor use only
│   ├── build_dashboards.py          ← programmatically creates/updates the workshop dashboard
│   ├── generate_participant_aliases.py ← creates participant-001 style aliases
│   └── INSTRUCTOR_NOTES.md         ← day-of setup checklist
│
└── docs/
    ├── EXERCISE_GUIDE.md            ← path picker for old links
    ├── EXERCISES_REPLIT.md          ← complete Replit attendee guide
    ├── EXERCISES_SPLUNK_SHOW.md     ← complete Splunk Show SSH attendee guide
    ├── EXERCISES_LOCAL.md           ← complete local Python attendee guide
    ├── signalflow101_conf26.pptx    ← slide deck (working draft)
    └── signalflow101_conf26.pdf     ← PDF export for easy viewing
```

---

*© 2026 · DEV1942 SignalFlow 101 · .conf26*
