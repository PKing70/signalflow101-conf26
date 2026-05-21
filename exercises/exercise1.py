"""
Exercise 1: Meet Your API
-------------------------
Sends a single metric to Splunk Observability Cloud to verify
your credentials and connection are working.

Run this script, then look for workshop.api.latency in the
O11y Data Explorer filtered by your participant_id.
"""

import random
import requests
from config import TOKEN, REALM, PARTICIPANT_ID

# Generate a fake latency value between 100ms and 500ms.
# We'll replace this with a real measured value in Exercise 2.
latency = random.uniform(100, 500)

payload = {
    "gauge": [
        {
            "metric": "workshop.api.latency",
            "value": latency,
            "dimensions": {
                "participant_id": PARTICIPANT_ID
            }
        }
    ]
}

response = requests.post(
    f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint",
    headers={
        "Content-Type": "application/json",
        "X-SF-TOKEN": TOKEN
    },
    json=payload
)

if response.status_code == 200:
    print(f"Metric sent successfully.")
    print(response.status_code)
    print(f"participant_id: {PARTICIPANT_ID}")
    print(f"latency:        {latency:.1f}ms")
else:
    print(f"Something went wrong: {response.status_code}")
    print(response.text)
