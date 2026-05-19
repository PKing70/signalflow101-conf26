"""
Take-home Exercise 2: Build a Detector That Pages You — Step 1
--------------------------------------------------------------
Creates an Apdex detector via the Splunk O11y REST API.
The detector fires when your Apdex score drops below 0.85
(Good threshold) for 5 continuous minutes.

After running, click the URL in the output to see your detector
live in the Splunk Observability Cloud UI.
"""

import requests
from config import TOKEN, REALM, PARTICIPANT_ID

API_URL = f"https://api.{REALM}.observability.splunkcloud.com"

# The SignalFlow program that powers this detector.
# Identical to what the UI generates when you build a detector manually —
# this is just expressing it directly in code.
signalflow_program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='count')
satisfied = latency.map(lambda x: 1 if x < 300 else 0).sum(over='5m')
tolerating = latency.map(lambda x: 1 if 300 <= x < 1200 else 0).sum(over='5m')
total = latency.sum(over='5m')
apdex = (satisfied + (tolerating / 2)) / total
detect(when(apdex < 0.85, lasting='5m')).publish('Apdex below Good threshold')
"""

detector = {
    "name": f"Apdex Monitor — {PARTICIPANT_ID}",
    "description": "Fires when Apdex score drops below 0.85 (Good threshold) for 5 minutes",
    "signalFlowText": signalflow_program,
    "rules": [
        {
            "name": "Apdex degraded",
            "description": f"Apdex for {PARTICIPANT_ID} has dropped below Good threshold",
            "severity": "Warning",
            "detectLabel": "Apdex below Good threshold",
            "notifications": [],
            "parameterizedSubject": "Apdex Alert — {{detector.name}}",
            "parameterizedBody": "Apdex score has dropped below 0.85 for {{participant_id}}. Current score: {{value}}"
        }
    ],
    "programOptions": {
        "minimumResolution": 0,
        "maxDelay": 0
    }
}

response = requests.post(
    f"{API_URL}/v2/detector",
    headers={
        "Content-Type": "application/json",
        "X-SF-TOKEN": TOKEN
    },
    json=detector
)

if response.status_code == 200:
    result = response.json()
    detector_id = result.get("id")
    print(f"Detector created successfully.")
    print(f"Name:        {result.get('name')}")
    print(f"ID:          {detector_id}")
    print(f"View it at:  https://app.{REALM}.observability.splunkcloud.com/#/detector/v2/{detector_id}")
else:
    print(f"Something went wrong: {response.status_code}")
    print(response.text)
