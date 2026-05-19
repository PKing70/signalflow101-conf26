# SignalFlow 101: Build Your First App for Splunk Observability Cloud

**Workshop · 60 minutes · .conf26**

This repository contains everything you need for the SignalFlow 101 workshop. You'll write Python that talks directly to the Splunk Observability Cloud SignalFlow API — sending metrics, investigating a fleet-wide latency anomaly, and computing an Apdex score that the O11y UI can't give you out of the box.

---

## Get Started (Attendees)

Click the button below to launch a pre-configured Python environment in your browser. No installation required.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/splunk/signalflow101-conf26)

Once your Codespace is open:

1. Open the `.env` file and fill in your workshop credentials (handed out at the start of the session)
2. Open `docs/EXERCISE_GUIDE.md` and follow along

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
├── .env.example                     ← credential template — copy to .env
│
├── exercises/                       ← in-workshop exercise scripts
│   ├── exercise1.py                 ← send your first metric
│   ├── exercise2a.py                ← send real measured latency
│   ├── exercise2b.py                ← investigate the fleet with SignalFlow
│   ├── exercise3.py                 ← compute Apdex
│   └── apdex.py                     ← reusable Apdex function (introduced in take-home 1)
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
│   ├── build_dashboards.py          ← programmatically creates Fleet + Apdex dashboards
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

1. Open `.env` and replace the workshop values with your own access token and realm
2. Your access token: **Settings → Access Tokens** in the O11y UI
3. Your realm: **Settings → My Profile** in the O11y UI

Don't have an instance yet? [Start a free trial](https://www.splunk.com/en_us/download/splunk-observability-cloud-free-trial.html).

---

## Fallback Environments

If GitHub Codespaces is unavailable, see the **Appendix** in `docs/EXERCISE_GUIDE.md` for Google Colab, Replit, and local Python alternatives.

---

*© 2025 Splunk Inc. · SignalFlow 101 · .conf26*
