"""
Take-home Exercise 1: Make Your API Interesting — Step 4
---------------------------------------------------------
Measures real latency to the GitHub API and sends it as
workshop.github.latency to Splunk Observability Cloud.

Run in a second terminal while takehome1_api.py is running.
Press Ctrl+C to stop.
"""

import os
import time
import requests
from dotenv import load_dotenv
from config import TOKEN, REALM, PARTICIPANT_ID

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"

if not GITHUB_USERNAME:
    raise EnvironmentError(
        "GITHUB_USERNAME not set in .env — add it before running this script."
    )

print(f"Sending GitHub latency metrics for {PARTICIPANT_ID}...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        start = time.time()
        requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        latency_ms = (time.time() - start) * 1000

        payload = {
            "gauge": [
                {
                    "metric": "workshop.github.latency",
                    "value": latency_ms,
                    "dimensions": {
                        "participant_id": PARTICIPANT_ID,
                        "github_username": GITHUB_USERNAME
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
            print(f"Sent: {latency_ms:.1f}ms  (github_username: {GITHUB_USERNAME})")

        time.sleep(10)
except KeyboardInterrupt:
    print("\nStopped.")
