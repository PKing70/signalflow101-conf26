"""
build_dashboards.py — Pre-workshop Dashboard Setup
----------------------------------------------------
INSTRUCTOR USE ONLY. Run once before the workshop to create
the pre-built dashboards that attendees will navigate to
during Exercise 2b and Exercise 3.

Creates:
  1. Fleet Dashboard  — workshop.api.latency by participant_id,
                        sorted descending (chaos-bot at the top)
  2. Apdex Dashboard  — Apdex scores by participant_id,
                        chaos-bot visibly low

Usage:
    python workshop-setup/build_dashboards.py

Run from the repo root with your instructor .env credentials loaded.
The script prints the dashboard URLs on completion — add these to
the exercise doc placeholders before the workshop.

TODO: implement once Splunk Show instance is provisioned and
      Charts/Dashboards API behavior is verified.
      Reference: https://dev.splunk.com/observability/docs/dashboards
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SPLUNK_ACCESS_TOKEN")
REALM = os.getenv("SPLUNK_REALM")

API_URL = f"https://api.{REALM}.observability.splunkcloud.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-SF-TOKEN": TOKEN
}


def create_fleet_dashboard():
    """
    TODO: Create a dashboard with:
    - Time series chart: workshop.api.latency grouped by participant_id
    - Table chart: 1-minute average latency per participant, sorted desc
    - Filter: last 15 minutes
    """
    raise NotImplementedError("Implement after O11y instance is provisioned")


def create_apdex_dashboard():
    """
    TODO: Create a dashboard with:
    - Single-value charts per participant showing Apdex score
    - Color thresholds: green >= 0.94, yellow >= 0.85, red < 0.85
    - Heatmap view if supported
    """
    raise NotImplementedError("Implement after O11y instance is provisioned")


if __name__ == "__main__":
    print("Building workshop dashboards...")
    print("NOTE: This script is not yet implemented.")
    print("See TODO comments above for what each dashboard should contain.")
    print("Implement after the Splunk Show instance is provisioned and tested.")
