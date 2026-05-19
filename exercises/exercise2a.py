"""
Exercise 2a: Start Sending Real Latency
----------------------------------------
Measures real round-trip latency to your FastAPI endpoint
and sends it to Splunk Observability Cloud every 10 seconds.

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

while True:
    start = time.time()
    requests.get("http://localhost:8000/hello")
    latency_ms = (time.time() - start) * 1000

    send_latency(latency_ms)
    print(f"Sent: {latency_ms:.1f}ms")
    time.sleep(10)
