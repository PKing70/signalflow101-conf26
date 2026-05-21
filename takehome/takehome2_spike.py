"""
Take-home Exercise 2: Build a Detector That Pages You — Step 2
--------------------------------------------------------------
Sends artificially high latency values to trigger your Apdex detector.

Every data point is 1800ms — well above the 1200ms frustrated threshold —
so Apdex drops to zero immediately. The detector fires after the condition
persists for 5 minutes (lasting='5m').

Leave this running and watch for the alert in Splunk Observability Cloud.
Press Ctrl+C to stop, then restart exercise2a.py to resolve the alert.
"""

import time
import requests
from config import TOKEN, REALM, PARTICIPANT_ID

INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"

print(f"Sending high-latency metrics for {PARTICIPANT_ID}...")
print("This will trigger your Apdex detector. Press Ctrl+C to stop.\n")

try:
    while True:
        # Simulate frustrated requests — well above the 1200ms threshold.
        # Every data point lands in the frustrated bucket, dropping Apdex to zero.
        latency_ms = 1800

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
        else:
            print(f"Sent: {latency_ms}ms (frustrated request)")

        # Sending every 5 seconds — faster than normal — to fill the detection
        # window with frustrated requests as quickly as possible.
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopped. Restart exercise2a.py to resolve the alert.")
