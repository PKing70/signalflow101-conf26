"""
Exercise 2a: Start Sending Real Latency
----------------------------------------
Measures real round-trip latency to the Splunk Observability Cloud
ingest endpoint and sends it as a metric every 10 seconds.

Leave this running and open a second terminal for Exercise 2b.
Press Ctrl+C to stop.
"""

import time
import requests
from config import TOKEN, REALM, PARTICIPANT_ID

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
            "X-SF-TOKEN": TOKEN
        },
        json=payload
    )
    if response.status_code != 200:
        print(f"Warning: metric send failed ({response.status_code}) — check your credentials in .env")


print(f"Sending real latency metrics for {PARTICIPANT_ID}...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        start = time.time()
        requests.get(f"https://ingest.{REALM}.observability.splunkcloud.com", timeout=5)
        latency_ms = (time.time() - start) * 1000
        send_latency(latency_ms)
        print(f"Sent: {latency_ms:.1f}ms")
        time.sleep(10)
except KeyboardInterrupt:
    print("\nStopped. Head to the next terminal for Exercise 2b.")