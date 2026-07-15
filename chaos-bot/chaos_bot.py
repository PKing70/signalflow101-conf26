"""
chaos_bot.py — Workshop Fleet Mystery Bot
------------------------------------------
INSTRUCTOR USE ONLY. Run this before and during the workshop.

Sends metrics as participant-000 with elevated and
variable latency, creating the fleet anomaly that attendees
investigate in Exercise 2.

Behavior:
  - Satisfied latency: ~180-280ms (25% of requests)
  - Tolerating latency: ~650-900ms (55% of requests)
  - Frustrated latency: ~1400-2000ms (20% of requests)
  - Send interval: every 5 seconds (faster than attendees to ensure
    the bot dominates the top of the sorted fleet view)

This produces an Apdex score of ~0.50-0.55 (Poor) while attendees
score ~0.95+ (Excellent), creating a clear and dramatic contrast.

Usage:
    python chaos-bot/chaos_bot.py

Stop with Ctrl+C. Run from the repo root so config.py is on the path,
but note that PARTICIPANT_ID from .env is NOT used. The bot always
identifies itself as participant-000.
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

# The chaos bot always uses this participant_id - never an attendee's.
BOT_ID = "participant-000"

INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"

# Latency profiles. This mix yields an expected Apdex around 0.52:
# 0.25 satisfied + (0.55 tolerating / 2) + 0 frustrated = 0.525.
SATISFIED_MIN = 180
SATISFIED_MAX = 280
SATISFIED_CHANCE = 0.25

TOLERATING_MIN = 650
TOLERATING_MAX = 900
TOLERATING_CHANCE = 0.55

SPIKE_MIN = 1400
SPIKE_MAX = 2000
SPIKE_CHANCE = 0.20

SEND_INTERVAL = 5     # seconds between sends


def generate_latency():
    """Generate a latency value across satisfied/tolerating/frustrated buckets."""
    roll = random.random()
    if roll < SPIKE_CHANCE:
        return random.uniform(SPIKE_MIN, SPIKE_MAX)
    if roll < SPIKE_CHANCE + SATISFIED_CHANCE:
        return random.uniform(SATISFIED_MIN, SATISFIED_MAX)
    return random.uniform(TOLERATING_MIN, TOLERATING_MAX)


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


print(f"Chaos bot starting - sending as {BOT_ID}")
print(
    f"Satisfied: {SATISFIED_MIN}-{SATISFIED_MAX}ms "
    f"({int(SATISFIED_CHANCE * 100)}%) | "
    f"Tolerating: {TOLERATING_MIN}-{TOLERATING_MAX}ms "
    f"({int(TOLERATING_CHANCE * 100)}%) | "
    f"Frustrated: {SPIKE_MIN}-{SPIKE_MAX}ms "
    f"({int(SPIKE_CHANCE * 100)}%)"
)
print("Press Ctrl+C to stop.\n")

spike_count = 0
total_count = 0

while True:
    latency_ms = generate_latency()
    is_spike = latency_ms >= SPIKE_MIN
    if latency_ms < 300:
        bucket = "satisfied "
    elif is_spike:
        bucket = "frustrated"
    else:
        bucket = "tolerating"
    status = send_metric(latency_ms)

    total_count += 1
    if is_spike:
        spike_count += 1

    spike_rate = (spike_count / total_count) * 100
    if status == 200:
        print(f"[{bucket}] {latency_ms:>7.1f}ms  "
              f"(spike rate: {spike_rate:.0f}% over {total_count} sends)")
    else:
        print(f"[ERROR] HTTP {status} - check credentials")

    time.sleep(SEND_INTERVAL)
