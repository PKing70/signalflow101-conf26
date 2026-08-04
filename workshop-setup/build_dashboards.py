"""
build_dashboards.py - Pre-workshop dashboard setup

Instructor use only. Run this after .env is configured with SPLUNK_REALM and
an API-capable token. The script is idempotent: if the workshop dashboard
already exists, it updates the expected chart definitions and prints the URL
instead of creating duplicates.
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

GROUP_NAME = "SignalFlow 101 - .conf26"
DASHBOARD_NAME = "SignalFlow 101 - Workshop Fleet"
DASHBOARD_TAGS = ["signalflow101", "conf26", "workshop"]
API_TIMEOUT = 30

REALM = (os.getenv("SPLUNK_REALM") or "").strip()
API_TOKEN = (
    os.getenv("SPLUNK_API_TOKEN")
    or os.getenv("SPLUNK_ACCESS_TOKEN")
    or ""
).strip()

PLACEHOLDERS = {
    "your-realm-here",
    "your-api-token-secret-here",
    "your-access-token-here",
}

if not REALM or REALM in PLACEHOLDERS:
    raise EnvironmentError("SPLUNK_REALM must be set in .env")
if not API_TOKEN or API_TOKEN in PLACEHOLDERS:
    raise EnvironmentError("SPLUNK_API_TOKEN or SPLUNK_ACCESS_TOKEN must be set in .env")

API_URL = f"https://api.{REALM}.observability.splunkcloud.com/v2"
HEADERS = {
    "Content-Type": "application/json",
    "X-SF-TOKEN": API_TOKEN,
}


def dashboard_url(dashboard_id, group_id=None):
    url = f"https://app.{REALM}.observability.splunkcloud.com/#/dashboard/{dashboard_id}"
    if group_id:
        return f"{url}?groupId={group_id}"
    return url


def request(method, path, **kwargs):
    response = requests.request(
        method,
        f"{API_URL}{path}",
        headers=HEADERS,
        timeout=API_TIMEOUT,
        **kwargs,
    )
    if response.status_code >= 400:
        print(f"Splunk O11y API returned HTTP {response.status_code}", file=sys.stderr)
        print(response.text[:2000], file=sys.stderr)
        response.raise_for_status()
    return response


def find_dashboard(name):
    response = request("GET", "/dashboard", params={"name": name, "limit": 100})
    for dashboard in response.json().get("results", []):
        if dashboard.get("name") == name:
            return dashboard
    return None


def find_dashboard_group(name):
    response = request("GET", "/dashboardgroup", params={"name": name, "limit": 100})
    for group in response.json().get("results", []):
        if group.get("name") == name:
            return group
    return None


def get_chart(chart_id):
    response = request("GET", f"/chart/{chart_id}")
    return response.json()


def create_dashboard_group():
    response = request(
        "POST",
        "/dashboardgroup",
        json={
            "name": GROUP_NAME,
            "description": "Dashboards for the SignalFlow 101 .conf26 workshop.",
        },
    )
    return response.json()


def get_or_create_dashboard_group():
    existing = find_dashboard_group(GROUP_NAME)
    if existing:
        return existing
    return create_dashboard_group()


def chart(name, description, program_text):
    return {
        "name": name,
        "description": description,
        "programText": program_text.strip(),
        "tags": DASHBOARD_TAGS,
    }


def workshop_charts():
    fleet_latency = """
latency = data('workshop.api.latency').mean(over='1m').mean(by=['participant_id'])
latency.publish('avg_latency_ms')
"""

    apdex = """
latency = data('workshop.api.latency', rollup='latest')
satisfied = latency.map(lambda x: 1 if x is not None and x < 300 else 0).sum(by=['participant_id']).sum(over='5m')
tolerating = latency.map(lambda x: 1 if x is not None and x >= 300 and x < 1200 else 0).sum(by=['participant_id']).sum(over='5m')
total = latency.map(lambda x: 1 if x is not None else 0).sum(by=['participant_id']).sum(over='5m')
apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""

    request_volume = """
requests = data('workshop.api.latency', rollup='count').sum(by=['participant_id']).sum(over='1m')
requests.publish('requests_per_minute')
"""

    chaos_bot_latency = """
chaos = data('workshop.api.latency',
    filter=filter('participant_id', 'participant-000')).mean(over='1m')
chaos.publish('participant_000_latency_ms')
"""

    return [
        chart(
            "Fleet latency by participant",
            "One-minute average workshop API latency, grouped by participant_id.",
            fleet_latency,
        ),
        chart(
            "Apdex by participant",
            "Live Apdex score using T=300ms and frustrated threshold 1200ms.",
            apdex,
        ),
        chart(
            "Request volume by participant",
            "One-minute datapoint count grouped by participant_id.",
            request_volume,
        ),
        chart(
            "Chaos bot latency",
            "Focused view of participant-000, the hidden anomalous API.",
            chaos_bot_latency,
        ),
    ]


def create_dashboard(group_id):
    response = request(
        "POST",
        "/dashboard/simple",
        params={"name": DASHBOARD_NAME, "groupId": group_id},
        json=workshop_charts(),
    )
    return response.json()


def update_chart(chart_id, desired):
    current = get_chart(chart_id)
    changed = False
    for field in ("name", "description", "programText", "tags"):
        if field == "tags" and sorted(current.get(field) or []) == sorted(desired.get(field) or []):
            continue
        if current.get(field) != desired.get(field):
            current[field] = desired.get(field)
            changed = True

    if not changed:
        return False

    request("PUT", f"/chart/{chart_id}", json=current)
    return True


def update_existing_dashboard_charts(dashboard):
    expected = {chart_definition["name"]: chart_definition for chart_definition in workshop_charts()}
    current_charts = []
    for chart_ref in dashboard.get("charts", []):
        chart_id = chart_ref.get("chartId") or chart_ref.get("id")
        if chart_id:
            current_charts.append(get_chart(chart_id))

    updated = 0
    current_by_name = {chart.get("name"): chart for chart in current_charts}
    for name, desired in expected.items():
        current = current_by_name.get(name)
        if not current:
            print(f"Expected chart is missing and was not recreated: {name}")
            continue
        if update_chart(current["id"], desired):
            updated += 1
    return updated


def main():
    existing = find_dashboard(DASHBOARD_NAME)
    if existing:
        updated = update_existing_dashboard_charts(existing)
        dashboard_id = existing["id"]
        group_id = existing.get("groupId")
        print("Workshop dashboard already exists.")
        print(f"Updated charts: {updated}")
        print(f"Name: {existing.get('name')}")
        print(f"ID:   {dashboard_id}")
        print(f"URL:  {dashboard_url(dashboard_id, group_id)}")
        return 0

    group = get_or_create_dashboard_group()
    group_id = group["id"]
    dashboard = create_dashboard(group_id)
    dashboard_id = dashboard["id"]
    group_id = dashboard.get("groupId") or group_id
    print("Workshop dashboard created.")
    print(f"Name: {dashboard.get('name')}")
    print(f"ID:   {dashboard_id}")
    print(f"URL:  {dashboard_url(dashboard_id, group_id)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
