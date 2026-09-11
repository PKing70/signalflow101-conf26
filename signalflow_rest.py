"""
signalflow_rest.py - Minimal SignalFlow REST/SSE helper

Splunk Observability Cloud can run SignalFlow programs through a REST
endpoint that streams Server-Sent Events (SSE). This helper keeps the
exercise scripts focused on the SignalFlow program and the values that
come back from it, while still using direct HTTP requests.
"""

import json

import requests


def _raise_for_status_with_hint(response, realm):
    if response.status_code in {401, 403}:
        message = (
            f"SignalFlow request failed with HTTP {response.status_code}.\n"
            "Check SPLUNK_API_TOKEN. It must be a token value/secret with the "
            f"API authorization scope for realm {realm}.\n"
            "If Exercise 1 or 2a can send metrics but Exercise 2b fails, your "
            "SPLUNK_INGEST_TOKEN is probably working but SPLUNK_API_TOKEN is "
            "missing, stale, or set to the ingest token by mistake."
        )
        raise requests.HTTPError(message, response=response)

    response.raise_for_status()


def stream_signalflow(
    program_text,
    token,
    realm,
    resolution=None,
    max_delay=None,
    read_timeout=None,
):
    """
    Execute a SignalFlow program and yield parsed SSE messages.

    Yields (event_name, payload, metadata_by_tsid). Metadata is updated as
    metadata events arrive, so data handlers can map tsId values back to
    dimensions such as participant_id.
    """
    url = f"https://stream.{realm}.observability.splunkcloud.com/v2/signalflow/execute"
    params = {}
    if resolution is not None:
        params["resolution"] = resolution
    if max_delay is not None:
        params["maxDelay"] = max_delay

    with requests.post(
        url,
        headers={
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "X-SF-Token": token,
        },
        json={"programText": program_text},
        params=params,
        stream=True,
        timeout=(10, read_timeout),
    ) as response:
        _raise_for_status_with_hint(response, realm)

        metadata_by_tsid = {}
        event_name = None
        data_lines = []

        for raw_line in response.iter_lines(decode_unicode=True):
            if raw_line is None:
                continue

            line = raw_line.strip("\r")
            if not line:
                if event_name and data_lines:
                    payload = _parse_payload(data_lines)
                    if event_name == "metadata":
                        tsid = payload.get("tsId")
                        if tsid:
                            metadata_by_tsid[tsid] = payload.get("properties", {})
                    yield event_name, payload, metadata_by_tsid

                event_name = None
                data_lines = []
                continue

            if line.startswith(":"):
                continue
            if line.startswith("event:"):
                event_name = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                data_lines.append(line.split(":", 1)[1].lstrip())


def _parse_payload(data_lines):
    text = "\n".join(data_lines)
    if not text:
        return {}
    return json.loads(text)
