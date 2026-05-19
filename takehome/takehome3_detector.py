"""
Take-home Exercise 3: The SLO Error Budget — Step 2
----------------------------------------------------
Creates a burn rate detector via the Splunk O11y REST API.
Fires when error budget burn rate exceeds 2x for 10 minutes.

Uses Critical severity — a sustained 2x burn rate is more serious
than Apdex dropping below Good threshold (which used Warning).
"""

import requests
from config import TOKEN, REALM, PARTICIPANT_ID

API_URL = f"https://api.{REALM}.observability.splunkcloud.com"

SLO_TARGET = 0.995
ALLOWED_ERROR_RATE = 1 - SLO_TARGET
WINDOW = '1h'
BURN_RATE_THRESHOLD = 2.0

signalflow_program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='count')

total = latency.sum(over='{WINDOW}')
frustrated = latency.map(lambda x: 1 if x >= 1200 else 0).sum(over='{WINDOW}')
current_error_rate = frustrated / total
burn_rate = current_error_rate / {ALLOWED_ERROR_RATE}

detect(when(burn_rate > {BURN_RATE_THRESHOLD}, lasting='10m')).publish('SLO burn rate exceeded')
"""

detector = {
    "name": f"SLO Burn Rate — {PARTICIPANT_ID}",
    "description": f"Fires when error budget burn rate exceeds {BURN_RATE_THRESHOLD}x for 10 minutes",
    "signalFlowText": signalflow_program,
    "rules": [
        {
            "name": "Burn rate exceeded",
            "description": f"Error budget burning at more than {BURN_RATE_THRESHOLD}x sustainable rate",
            "severity": "Critical",
            "detectLabel": "SLO burn rate exceeded",
            "notifications": [],
            "parameterizedSubject": "SLO Alert — Burn rate exceeded for {{detector.name}}",
            "parameterizedBody": f"Current burn rate has exceeded {BURN_RATE_THRESHOLD}x. Your error budget is being consumed faster than sustainable. Investigate immediately."
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
    print(f"Burn rate detector created successfully.")
    print(f"Name:        {result.get('name')}")
    print(f"ID:          {detector_id}")
    print(f"View it at:  https://app.{REALM}.observability.splunkcloud.com/#/detector/v2/{detector_id}")
else:
    print(f"Something went wrong: {response.status_code}")
    print(response.text)
