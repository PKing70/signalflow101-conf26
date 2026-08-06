"""
Exercise 2a: Start Sending Real Latency
---------------------------------------
Measures real round-trip latency to your workshop API and sends it
as a metric every 10 seconds.

Leave this running and open a second terminal for Exercise 2b.
Press Ctrl+C to stop.
"""

import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import INGEST_TOKEN, REALM, PARTICIPANT_ID

INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"


def send_latency(latency_ms):
    payload = {
        "gauge": [
            {
                "metric": "workshop.api.latency",
                "value": latency_ms,
                "dimensions": {
                    "participant_id": PARTICIPANT_ID
                }
            }
        ]
    }
    response = requests.post(
        INGEST_URL,
        headers={
            "Content-Type": "application/json",
            "X-SF-TOKEN": INGEST_TOKEN
        },
        json=payload
    )
    if response.status_code != 200:
        print(f"Warning: metric send failed ({response.status_code}) - check your workshop credentials")


print(f"Sending real latency metrics for {PARTICIPANT_ID}...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        start = time.time()
        response = requests.get("http://localhost:8000/hello", timeout=5)
        response.raise_for_status()
        latency_ms = (time.time() - start) * 1000
        send_latency(latency_ms)
        print(f"Sent: {latency_ms:.1f}ms")
        time.sleep(10)
except requests.RequestException as error:
    print("\nCould not reach your API at http://localhost:8000/hello.")
    print("Start the API workflow, or run the API serve command from the guide.")
    print(f"Details: {error}")
except KeyboardInterrupt:
    print("\nStopped. Head to the next terminal for Exercise 2b.")
