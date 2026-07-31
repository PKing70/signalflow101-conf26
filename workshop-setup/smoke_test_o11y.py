"""
Instructor smoke test for the Splunk Observability Cloud workshop.

Run this before working on dashboards or the lab guide UI steps. It sends one
metric datapoint, then executes a bounded SignalFlow query to prove the same
metric can be read back through the REST/SSE API.
"""

import argparse
import sys
import threading
import time
import uuid
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from config import API_TOKEN, INGEST_TOKEN, PARTICIPANT_ID, REALM  # noqa: E402
except OSError as error:
    print(error)
    raise SystemExit(1) from None

from signalflow_rest import stream_signalflow  # noqa: E402

METRIC_NAME = "workshop.api.latency"


def splunk_string(value):
    """Escape a value for a single-quoted SignalFlow string."""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def send_datapoint(latency_ms, run_id):
    payload = {
        "gauge": [
            {
                "metric": METRIC_NAME,
                "value": latency_ms,
                "dimensions": {
                    "participant_id": PARTICIPANT_ID,
                    "source": "smoke-test",
                    "test_run_id": run_id,
                },
            }
        ]
    }
    response = requests.post(
        f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint",
        headers={
            "Content-Type": "application/json",
            "X-SF-Token": INGEST_TOKEN,
        },
        json=payload,
        timeout=10,
    )
    return response


def signalflow_program(run_id):
    participant = splunk_string(PARTICIPANT_ID)
    run = splunk_string(run_id)
    return f"""
latency = data('{METRIC_NAME}',
    filter={{
        'participant_id': '{participant}',
        'source': 'smoke-test',
        'test_run_id': '{run}',
    }},
    rollup='latest')
latency.publish('smoke_latency')
"""


def send_readback_sample(latency_ms, run_id):
    time.sleep(2)
    send_datapoint(latency_ms, run_id)


def read_back(timeout_seconds, latency_ms, run_id):
    deadline = time.monotonic() + timeout_seconds
    program = signalflow_program(run_id)
    sender = threading.Thread(
        target=send_readback_sample,
        args=(latency_ms, run_id),
        daemon=True,
    )
    sender.start()

    while time.monotonic() < deadline:
        remaining = max(1, deadline - time.monotonic())
        try:
            events = stream_signalflow(
                program,
                API_TOKEN,
                REALM,
                resolution=10000,
                max_delay=1000,
                read_timeout=remaining,
            )
            for event_name, payload, metadata in events:
                if time.monotonic() >= deadline:
                    return None, None
                if event_name != "data":
                    continue

                for point in payload.get("data", []):
                    value = point.get("value")
                    if value is None:
                        continue

                    tsid = point.get("tsId")
                    dimensions = metadata.get(tsid, {}) if tsid else {}
                    participant = dimensions.get("participant_id", PARTICIPANT_ID)
                    return value, participant
        except requests.exceptions.ReadTimeout:
            break

    sender.join(timeout=0)
    return None, None


def print_token_hint(stage, response):
    print(f"{stage} failed with HTTP {response.status_code}.")
    if response.text:
        print(response.text[:1000])
    if response.status_code in {401, 403}:
        if stage == "Ingest":
            print("Check that the token has the INGEST authorization scope.")
        else:
            print("Check that the token has the API authorization scope and a Power or Admin role.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--latency-ms", type=float, default=123.4)
    args = parser.parse_args()

    run_id = f"smoke-{uuid.uuid4().hex[:8]}"

    print("Splunk O11y workshop smoke test")
    print(f"Realm:          {REALM}")
    print(f"Participant ID: {PARTICIPANT_ID}")
    print(f"Metric:         {METRIC_NAME}")
    print(f"Run ID:         {run_id}")
    print()

    try:
        response = send_datapoint(args.latency_ms, run_id)
    except requests.RequestException as error:
        print(f"Ingest request failed before Splunk returned a response: {error}")
        return 1

    if response.status_code != 200:
        print_token_hint("Ingest", response)
        return 1

    print(f"Ingest OK: sent {args.latency_ms:.1f}ms")
    print("SignalFlow: waiting for readback...")

    try:
        value, participant = read_back(args.timeout, args.latency_ms, run_id)
    except requests.exceptions.HTTPError as error:
        response = error.response
        if response is not None:
            print_token_hint("SignalFlow", response)
        else:
            print(f"SignalFlow failed: {error}")
        return 1
    except requests.RequestException as error:
        print(f"SignalFlow request failed before Splunk returned data: {error}")
        return 1

    if value is None:
        print(f"No SignalFlow data returned within {args.timeout} seconds.")
        print("Ingest worked, so check the metric in Data Explorer and verify the API token scope.")
        return 2

    print(f"SignalFlow OK: {participant} is reporting {value:.1f}ms")
    print("End-to-end O11y smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
