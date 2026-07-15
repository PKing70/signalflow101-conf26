"""
workshop_api.py - Personal workshop API

This FastAPI app runs in each participant's Codespace. The workshop
scripts measure this endpoint and send the latency to Splunk
Observability Cloud.

The app intentionally reads .env on each request. That lets the server
start before an attendee has filled in their credentials, then pick up
PARTICIPANT_ID as soon as the file is saved.
"""

import hashlib
import os
import random
import time
from pathlib import Path

from dotenv import dotenv_values
from fastapi import FastAPI


ENV_PATH = Path(__file__).with_name(".env")
DEFAULT_PARTICIPANT_ID = "participant-unconfigured"
PLACEHOLDER_IDS = {"participant-your-number", "your.email@example.com", "your-email-here"}

app = FastAPI(title="SignalFlow 101 Workshop API")


def current_participant_id():
    """Read the participant alias from .env without requiring a restart."""
    values = dotenv_values(ENV_PATH) if ENV_PATH.exists() else {}
    participant_id = values.get("PARTICIPANT_ID") or os.getenv("PARTICIPANT_ID")
    if not participant_id:
        return DEFAULT_PARTICIPANT_ID
    participant_id = participant_id.strip()
    if not participant_id or participant_id in PLACEHOLDER_IDS:
        return DEFAULT_PARTICIPANT_ID
    return participant_id


def simulated_processing_delay_ms(participant_id):
    """
    Give each participant a stable, normal-looking latency band.

    This keeps the fleet chart visually interesting while ensuring normal
    participants remain comfortably below the 300ms Apdex threshold.
    """
    digest = hashlib.sha256(participant_id.encode("utf-8")).hexdigest()
    stable_offset = int(digest[:8], 16) % 120
    jitter = random.uniform(-15, 25)
    return max(25, 85 + stable_offset + jitter)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    participant_id = current_participant_id()
    delay_ms = simulated_processing_delay_ms(participant_id)
    time.sleep(delay_ms / 1000)
    return {
        "participant_id": participant_id,
        "message": f"hello from {participant_id}",
        "simulated_processing_ms": round(delay_ms, 1),
    }
