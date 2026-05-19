"""
chaos_bot.py — Workshop Fleet Mystery Bot
------------------------------------------
INSTRUCTOR USE ONLY. Run this before and during the workshop.

Sends metrics as chaos-bot@conf26.splunk.com with elevated and
variable latency, creating the fleet anomaly that attendees
investigate in Exercise 2.

Behavior:
  - Baseline latency: ~600–900ms (P50 — clearly elevated vs attendees)
  - Occasional spikes: ~1400–2000ms (frustrated requests for P95 drama)
  - Spike frequency: ~1 in 5 requests, to create a meaningful P95/P50 gap
  - Send interval: every 5 seconds (faster than attendees to ensure
    the bot dominates the top of the sorted fleet view)

This produces an Apdex score of ~0.50–0.55 (Poor) while attendees
score ~0.95+ (Excellent), creating a clear and dramatic contrast.

Usage:
    python chaos-bot/chaos_bot.py

Stop with Ctrl+C. Run from the repo root so config.py is on the path,
but note that PARTICIPANT_ID from .env is NOT used — the bot always
identifies itself as chaos-bot@conf26.splunk.com.
"""

import os
import random
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SPLUNK_ACCESS_TOKEN")
REALM = os.getenv("SPLUNK_REALM")

if not TOKEN or not REALM:
    raise EnvironmentError(
        "SPLUNK_ACCESS_TOKEN and SPLUNK_REALM must be set in .env"
    )

# The chaos bot always uses this participant_id — never an attendee's
BOT_ID = "chaos-bot@conf26.splunk.com"

INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"

# Latency profiles
BASELINE_MIN = 600    # ms — elevated but not always frustrated
BASELINE_MAX = 900    # ms — P50 clearly above attendees (~140ms)
SPIKE_MIN    = 1400   # ms — above 1200ms frustrated threshold
SPIKE_MAX    = 2000   # ms — well into frustrated territory
SPIKE_CHANCE = 0.20   # 20% of requests are spikes

SEND_INTERVAL = 5     # seconds between sends


def generate_latency():
    """Generate a latency value with occasional spikes."""
    if random.random() < SPIKE_CHANCE:
        return random.uniform(SPIKE_MIN, SPIKE_MAX)
    return random.uniform(BASELINE_MIN, BASELINE_MAX)


def send_metric(latency_ms):
    payload = {
        "gauge": [
            {
                "metric": "workshop.api.latency",
                "value": latency_ms,
                "dimensions": {
                    "participant_id": BOT_ID
                }
            }
        ]
    }
    response = requests.post(
        INGEST_URL,
        headers={
            "Content-Type": "application/json",
            "X-SF-TOKEN": TOKEN
        },
        json=payload
    )
    return response.status_code


print(f"Chaos bot starting — sending as {BOT_ID}")
print(f"Baseline: {BASELINE_MIN}–{BASELINE_MAX}ms | "
      f"Spikes: {SPIKE_MIN}–{SPIKE_MAX}ms ({int(SPIKE_CHANCE * 100)}% frequency)")
print("Press Ctrl+C to stop.\n")

spike_count = 0
total_count = 0

while True:
    latency_ms = generate_latency()
    is_spike = latency_ms >= SPIKE_MIN
    status = send_metric(latency_ms)

    total_count += 1
    if is_spike:
        spike_count += 1

    spike_rate = (spike_count / total_count) * 100
    label = "SPIKE  " if is_spike else "normal "

    if status == 200:
        print(f"[{label}] {latency_ms:>7.1f}ms  "
              f"(spike rate: {spike_rate:.0f}% over {total_count} sends)")
    else:
        print(f"[ERROR] HTTP {status} — check credentials")

    time.sleep(SEND_INTERVAL)
