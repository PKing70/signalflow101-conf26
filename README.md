# SignalFlow 101: Build Your First App for Splunk Observability Cloud

**Workshop · 60 minutes · .conf26 · DEV1942**

Short link: [https://tinyurl.com/DEV1942](https://tinyurl.com/DEV1942)

This repository contains everything you need for the SignalFlow 101 workshop. You'll write Python that talks directly to the Splunk Observability Cloud SignalFlow API — sending metrics, investigating a fleet-wide latency anomaly, and computing an Apdex score that the O11y UI can't give you out of the box.

---

## Get Started (Attendees)

Use the environment named by your instructor. The supported workshop paths are:

1. **Replit** — browser-based Python with repo-defined workflows.
2. **Splunk Show Python environment** — SSH into the shared workshop host and run the CLI commands from a terminal.
3. **Your own Python environment** — only if you already had Python working before the workshop.

### Replit

Use [docs/REPLIT.md](docs/REPLIT.md) if the workshop is running in Replit. Replit uses **Secrets** for `SPLUNK_REALM`, token secrets, and `PARTICIPANT_ID`, then provides named workflows for the timed in-room exercise steps.

### Splunk Show SSH/CLI

Use [docs/SPLUNK_SHOW.md](docs/SPLUNK_SHOW.md) if the workshop is running in the shared Splunk Show Python environment. Your instructor will provide SSH/login details. This path uses `.env` for workshop values and terminal commands such as `python workshop.py check`.

### Existing Local Python

Use your own Python environment only if it was already working before the workshop. We will not troubleshoot laptop-specific Python, firewall, package manager, or IDE issues during the 60-minute session. Copy `.env.example` to `.env`, fill in the workshop values, install `requirements.txt`, then follow `docs/EXERCISE_GUIDE.md`.

For the workshop, each participant has their own development environment/login, but everyone sends data to the same Splunk Observability Cloud organization. The realm is shared, and `PARTICIPANT_ID` is what separates your metrics from everyone else's. Your instructor will tell you whether `SPLUNK_API_TOKEN` is a personal token from your Splunk O11y login or a shared workshop API token.

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
├── exercises/                       ← in-workshop exercise scripts
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
    ├── EXERCISE_GUIDE.md            ← full exercise document
    ├── REPLIT.md                    ← Replit setup and workflow guide
    ├── SPLUNK_SHOW.md               ← Splunk Show SSH/CLI setup guide
    ├── signalflow101_conf26.pptx    ← slide deck (working draft)
    └── signalflow101_conf26.pdf     ← PDF export for easy viewing
```

---

## Running on Your Own Splunk Observability Cloud Instance

The workshop uses a shared instance provisioned via Splunk Show. To run these exercises against your own instance after the workshop:

1. Open `.env` and replace the workshop values with your own token secrets and realm
2. Your ingest token: **Settings → Access Tokens** in the O11y UI, with ingest authorization scope
3. Your API token: your user API access token, or an access token with API authorization scope
4. Your realm: **Settings → My Profile** in the O11y UI
5. Use any unique `PARTICIPANT_ID` value, such as `participant-042`

Don't have an instance yet? [Start a free trial](https://www.splunk.com/en_us/download/splunk-observability-cloud-free-trial.html).

---

## Fallback Environments

If the recommended environment is unavailable, see the **Appendix** in `docs/EXERCISE_GUIDE.md` for the supported workshop alternatives.

---

*© 2025 Splunk Inc. · SignalFlow 101 · .conf26*
