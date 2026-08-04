# SignalFlow 101: Build Your First App for Splunk Observability Cloud

**Workshop · 60 minutes · .conf26**

This repository contains everything you need for the SignalFlow 101 workshop. You'll write Python that talks directly to the Splunk Observability Cloud SignalFlow API — sending metrics, investigating a fleet-wide latency anomaly, and computing an Apdex score that the O11y UI can't give you out of the box.

---

## Get Started (Attendees)

Click the button below to launch a pre-configured Python environment in your browser. No installation required.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/PKing70/signalflow101-conf26)

Once your Codespace is open:

1. Open the `.env` file and fill in the workshop realm, token secret(s), and your unique participant alias
2. Open `docs/EXERCISE_GUIDE.md` and follow along

For the workshop, each participant has their own development environment/login, but everyone sends data to the same Splunk Observability Cloud organization. The realm is shared, and `PARTICIPANT_ID` is what separates your metrics from everyone else's. Your instructor will tell you whether `SPLUNK_API_TOKEN` is a personal token from your Splunk O11y login or a shared workshop API token.

---

## Repository Structure

```
signalflow101-conf26/
│
├── README.md                        ← you are here
├── .devcontainer/
│   └── devcontainer.json            ← Codespace configuration
├── requirements.txt                 ← Python dependencies (auto-installed)
├── config.py                        ← loads credentials from .env
├── workshop_api.py                  ← personal API auto-started in Codespaces
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

If GitHub Codespaces is unavailable, see the **Appendix** in `docs/EXERCISE_GUIDE.md` for Google Colab, Replit, and local Python alternatives.

---

*© 2025 Splunk Inc. · SignalFlow 101 · .conf26*
