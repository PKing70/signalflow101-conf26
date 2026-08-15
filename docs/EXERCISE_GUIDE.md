# SignalFlow 101: Build Your First App for Splunk Observability Cloud
### Workshop Exercise Guide — .conf26

---

## Welcome

This workshop assumes you're familiar with the core building blocks of Splunk Observability Cloud — dashboards, detectors, metrics, and dimensions. We're not going to cover those from scratch. Instead, we're going to focus on extending them.

Everything you interact with in Splunk Observability Cloud is powered by SignalFlow, Splunk's streaming analytics engine. When you build a chart or configure a detector in the UI, SignalFlow is running underneath it. Today you're going to write SignalFlow directly, in Python — which means you can go beyond what the UI exposes: define your own formulas, compute custom metrics, and build tooling that's repeatable, version-controlled, and deployable at scale.

---

## What You'll Need

- A browser
- The workshop credentials sheet handed out at the start of the session
- One supported Python environment:
  - Replit, the recommended in-room path
  - The Splunk Show Python environment, accessed over SSH, if Replit is blocked
  - Your own pre-existing Python environment

If you use Replit or the Splunk Show environment, you do not need to install Python on your laptop. If you use your own Python environment, it should already be working before the workshop starts.

---

## What You'll Build

By the end of this workshop you will have:

- A personal API endpoint running in the cloud, sending real metrics into our shared Splunk Observability Cloud organization
- SignalFlow programs that investigate a live fleet-wide latency anomaly and identify the culprit
- An Apdex score — a custom SLO metric computed in SignalFlow that Splunk Observability Cloud doesn't give you out of the box

The take-home exercises at the end of this document go further: real downstream latency measurement, programmatic detector creation, and a full SLO error budget burn rate — all in Python, all against your own Splunk Observability Cloud instance.

---

## How This Works

Each exercise follows the same broad pattern. Replit is the default attendee
path; Splunk Show SSH/CLI is the fallback if Replit is blocked; local Python is
only for attendees who already had it working before the workshop.

1. **Replit:** run the named workflow. The code blocks show what the workflow
   runs; you do not need to paste them during the timed workshop.
2. **Splunk Show SSH/CLI or local Python:** run the command for your
   environment, then review the Python listing if you have time.
3. **Observe** what happens in Splunk Observability Cloud
4. **Read** the explanation at your own pace

To stop any running script at any time, use the Replit Stop button or press
**Ctrl+C** in its terminal.

The checkpoints throughout the session are your signal to pause and look up — that's when we'll discuss what just happened and what it means before moving on.

The **Interesting parts** sections explain the Python you just ran. Read them
if you're curious or have time. Skip them if you need to keep pace — you won't
miss anything required.

---

## Getting Started: Complete One Setup Path

> 🔲 **Placeholder:** Workshop credential delivery instructions to be added once
> the workshop instance is provisioned. This section will include the QR code or
> URL for the credential page, login instructions, and where to find your token
> secret(s), the `us1` realm value, and participant ID.

For this workshop, your development environment/login is yours, but everyone sends data to the same Splunk Observability Cloud organization. Your `PARTICIPANT_ID` is a string assigned by workshop staff, not something copied from O11y or Splunk Show. It is what separates your metrics from everyone else's.

Before starting Exercise 1, complete exactly one setup guide and make sure its
setup check passes:

- **Replit, recommended:** follow [`REPLIT.md`](REPLIT.md).
- **Splunk Show SSH/CLI, if Replit is blocked:** follow [`SPLUNK_SHOW.md`](SPLUNK_SHOW.md).
- **Existing local Python, only if it already works:** follow [`LOCAL_PYTHON.md`](LOCAL_PYTHON.md).

The setup guides are the source of truth for importing or cloning the repo,
adding workshop values, and running the setup check. Come back here only after
your chosen setup path is ready.

You'll use these values during setup:

- The shared **realm** — `us1`
- The shared **ingest token secret** — used when Python sends metric datapoints
- Your **API token secret** — used when Python runs SignalFlow queries
- Your unique **participant ID** — assigned by workshop staff, such as `participant-042`

Your setup guide explains where to put these values for your environment.

---

## Exercise 1: Meet Your API

> ⏱ **Timing:** This exercise is timeboxed to 10 minutes. If you finish early, read the "Interesting parts" section while you wait for the checkpoint.

Your workshop environment can run a small API. Let's make sure everything is working — and prove that your Python environment can talk to Splunk Observability Cloud — before we go further.

### Step 1: Run your API

#### Replit

Run the workflow `1 - Start API`, then open the web preview.

#### Splunk Show SSH/CLI or local Python

If you are using Splunk Show SSH/CLI:

Open one terminal for the API, then run:

```bash
cd ~/signalflow101-conf26
python workshop.py serve
```

If you are using local Python on Mac/Linux:

Open one terminal for the API, then run:

```bash
cd ~/workshops/signalflow101-conf26
.venv/bin/python workshop.py serve
```

If you are using local Python on Windows PowerShell:

Open one terminal for the API, then run:

```powershell
Set-Location "$HOME\workshops\signalflow101-conf26"
.\.venv\Scripts\python workshop.py serve
```

Leave this API terminal running for the rest of the timed exercises.

If your instructor provides a URL or port-forwarding instructions, open that URL
in your browser.

Add `/hello` to the end of the URL. You should see your participant alias —
pulled from the `PARTICIPANT_ID` you configured earlier.

Expected browser result:

```json
{
  "participant_id": "participant-042",
  "message": "hello from participant-042",
  "simulated_processing_ms": 105.5
}
```

The relevant part of `workshop_api.py` is shown below.

```python
@app.get("/hello")
def hello():
    participant_id = current_participant_id()
    delay_ms = simulated_processing_delay_ms(participant_id)
    time.sleep(delay_ms / 1000)
    return {
        "participant_id": participant_id,
        "message": f"hello from {participant_id}",
        "simulated_processing_ms": round(delay_ms, 1),
    }
```

#### Interesting parts

The `/hello` endpoint is the API being measured. It returns your participant ID
and waits for a small simulated delay. The observability pattern is deliberately
simple: call an endpoint, measure the time, send that measurement as a metric.

If you see your participant alias, your API is running. Move on to Step 2.

### Step 2: Send your first metric to Splunk Observability Cloud

Now let's send a metric.

#### Replit

Run the workflow `1a - Send first metric`.

#### Splunk Show SSH/CLI or local Python

If you are using Splunk Show SSH/CLI:

Leave the API command from Step 1 running. Open another terminal, then run:

```bash
cd ~/signalflow101-conf26
python exercises/exercise1.py
```

If you are using local Python on Mac/Linux:

Leave the API command from Step 1 running. Open another terminal, then run:

```bash
cd ~/workshops/signalflow101-conf26
.venv/bin/python exercises/exercise1.py
```

If you are using local Python on Windows PowerShell:

Leave the API command from Step 1 running. Open another terminal, then run:

```powershell
Set-Location "$HOME\workshops\signalflow101-conf26"
.\.venv\Scripts\python exercises\exercise1.py
```

Expected terminal result:

```
Metric sent successfully.
participant_id: participant-042
latency:        287.3ms
```

The contents of `exercises/exercise1.py` are shown below for reference.

```python
import random
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import INGEST_TOKEN, REALM, PARTICIPANT_ID

# Generate a fake latency value between 100ms and 500ms
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
        "X-SF-TOKEN": INGEST_TOKEN
    },
    json=payload
)

if response.status_code == 200:
    print(f"Metric sent successfully.")
    print(f"participant_id: {PARTICIPANT_ID}")
    print(f"latency:        {latency:.1f}ms")
else:
    print(f"Something went wrong: {response.status_code}")
    print(response.text)
```

#### Interesting parts

`from config import` pulls `INGEST_TOKEN`, `REALM`, and `PARTICIPANT_ID` from
the `.env` file or Replit Secrets you configured earlier.

The `payload` is the metric datapoint. It has a metric name
(`workshop.api.latency`), a value (`latency`), and a dimension
(`participant_id`) that tags the datapoint as yours.

`requests.post()` sends the datapoint to Splunk Observability Cloud's ingest
endpoint. The `X-SF-TOKEN` header is how Splunk Observability Cloud authorizes
the request. The fake latency value is enough for Exercise 1 because this step
is only proving that credentials, connection, ingest, and participant tagging
work.

### Step 3: Verify in Splunk Observability Cloud

> 🔲 **Placeholder:** Step-by-step instructions for finding a metric in the O11y Metric Finder or Data Explorer — to be added once the workshop instance is provisioned. Attendees will look for `workshop.api.latency` filtered by their `participant_id`.

When you find your metric, you're looking for `workshop.api.latency` filtered by your `participant_id`. If it's there, you're fully connected and ready to move on.

---

**What just happened?**

You sent a data point to Splunk Observability Cloud using the ingest API — the same API that monitoring agents, integrations, and instrumentation libraries use. The metric has a name, a value, and a dimension that identifies it as yours. That's the complete picture of a metric in Splunk Observability Cloud.

In Exercise 2, we'll replace the random value with something real — and that's when the investigation begins.

> 🔵 **Checkpoint 1** — Look up when you reach this point. We'll confirm everyone's metric is visible in Splunk Observability Cloud before moving on.

---

## Exercise 2: Real Metrics and a Mystery

> ⏱ **Timing:** This exercise is timeboxed to 15 minutes across two steps. Step 1 should take about 5 minutes. Step 2 runs until Checkpoint 2 at the 35-minute mark.

In Exercise 1 you proved the pipeline works. Now let's make the data meaningful — and introduce something unexpected in our fleet.

### Step 1: Start sending real latency

Your API responds to requests and measures how long each one takes.

#### Replit

Run the workflow `2 - Send latency metrics`.

#### Splunk Show SSH/CLI or local Python

If you are using Splunk Show SSH/CLI:

Use the same terminal where you ran `exercises/exercise1.py`, then run:

```bash
cd ~/signalflow101-conf26
python exercises/exercise2a.py
```

If you are using local Python on Mac/Linux:

Use the same terminal where you ran `exercises/exercise1.py`, then run:

```bash
cd ~/workshops/signalflow101-conf26
.venv/bin/python exercises/exercise2a.py
```

If you are using local Python on Windows PowerShell:

Use the same terminal where you ran `exercises\exercise1.py`, then run:

```powershell
Set-Location "$HOME\workshops\signalflow101-conf26"
.\.venv\Scripts\python exercises\exercise2a.py
```

Expected terminal result:

```
Sending real latency metrics for participant-042...
Press Ctrl+C to stop.

Sent: 142.3ms
Sent: 138.7ms
Sent: 145.1ms
```

Leave this running. In Replit, leave `2 - Send latency metrics` running. In
Splunk Show SSH/CLI or local Python, leave this terminal running.

The contents of `exercises/exercise2a.py` are shown below for reference.

```python
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import INGEST_TOKEN, REALM, PARTICIPANT_ID

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
            "X-SF-TOKEN": INGEST_TOKEN
        },
        json=payload
    )
    if response.status_code != 200:
        print(f"Warning: metric send failed ({response.status_code}) - check your workshop credentials")

print(f"Sending real latency metrics for {PARTICIPANT_ID}...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        start = time.time()
        response = requests.get("http://localhost:8000/hello", timeout=5)
        response.raise_for_status()
        latency_ms = (time.time() - start) * 1000

        send_latency(latency_ms)
        print(f"Sent: {latency_ms:.1f}ms")
        time.sleep(10)
except requests.RequestException as error:
    print("\nCould not reach your API at http://localhost:8000/hello.")
    print("Start the API workflow, or run the API serve command from the guide.")
    print(f"Details: {error}")
except KeyboardInterrupt:
    print("\nStopped. Head to the next terminal for Exercise 2b.")
```

#### Interesting parts

`send_latency()` wraps the Splunk Observability Cloud ingest call in a function
so the main loop stays readable: measure latency, send latency, wait 10 seconds.

`time.time()` captures the moment before and after the API call. The difference,
converted to milliseconds, is the real round-trip latency for
`http://localhost:8000/hello`.

`while True` keeps the script running until you stop it with **Ctrl+C**. This is
why the next step needs another terminal: this script is your live metric sender.


### Step 2: Investigate the fleet

With everyone's metrics flowing, let's look at the whole picture.

#### Replit

Leave `2 - Send latency metrics` running, then run the workflow
`3 - View fleet latency`.

#### Splunk Show SSH/CLI or local Python

If you are using Splunk Show SSH/CLI:

Leave `exercises/exercise2a.py` running in the previous terminal. Open another
terminal for the fleet query, then run:

```bash
cd ~/signalflow101-conf26
python exercises/exercise2b.py
```

If you are using local Python on Mac/Linux:

Leave `exercises/exercise2a.py` running in the previous terminal. Open another
terminal for the fleet query, then run:

```bash
cd ~/workshops/signalflow101-conf26
.venv/bin/python exercises/exercise2b.py
```

If you are using local Python on Windows PowerShell:

Leave `exercises\exercise2a.py` running in the previous terminal. Open another
terminal for the fleet query, then run:

```powershell
Set-Location "$HOME\workshops\signalflow101-conf26"
.\.venv\Scripts\python exercises\exercise2b.py
```

Expected terminal result:

```
--- Fleet Latency (top 15 of 128) ---
participant-000                          847.3ms  ████████████████████████████████████████████████████████████
participant-117                          224.8ms  ██████████████████████
participant-042                          143.2ms  ██████████████
...
```

One participant stands out. That's not a coincidence.

Now open the workshop dashboard in Splunk Observability Cloud to see the same
data visualized live:

https://app.us1.signalfx.com/#/dashboard/HPtrGG-A4AE?groupId=HPtqyd5A0AA

In the dashboard group **SignalFlow 101 - .conf26**, open **SignalFlow 101 -
Workshop Fleet** and look at **Fleet latency by participant**. The same outlier
should stand out there.

The contents of `exercises/exercise2b.py` are shown below for reference.

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM, PARTICIPANT_ID
from signalflow_rest import stream_signalflow

DISPLAY_LIMIT = 15

program = """
latency = data('workshop.api.latency').mean(over='1m').mean(by=['participant_id'])
latency.publish('avg_latency_by_participant')
"""

results = {}

try:
    for event_name, payload, metadata in stream_signalflow(program, API_TOKEN, REALM):
        if event_name != "data":
            continue

        for point in payload.get("data", []):
            tsid = point.get("tsId")
            value = point.get("value")
            if not tsid or value is None:
                continue
            participant = metadata.get(tsid, {}).get("participant_id", "unknown")
            results[participant] = value

        if results:
            sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
            display_results = sorted_results[:DISPLAY_LIMIT]
            own_result = next(
                (item for item in sorted_results if item[0] == PARTICIPANT_ID),
                None,
            )

            if own_result and own_result not in display_results:
                display_results.append(("...", None))
                display_results.append(own_result)

            print(f"\n--- Fleet Latency (top {min(DISPLAY_LIMIT, len(sorted_results))} of {len(sorted_results)}) ---")
            for participant, latency in display_results:
                if latency is None:
                    print(f"... {len(sorted_results)} participants reporting ...")
                    continue
                bar = "█" * int(latency / 10)
                print(f"{participant:<40} {latency:>8.1f}ms  {bar}")
except KeyboardInterrupt:
    print("\nStopped.")
```

#### Interesting parts

The string assigned to `program` is a SignalFlow program. `data()` selects your
metric stream, `.mean(over='1m')` computes a 1-minute average, and
`.mean(by=['participant_id'])` keeps each participant separate.

`stream_signalflow()` starts that SignalFlow computation through Splunk
Observability Cloud's REST API and keeps the response open as Server-Sent
Events. The script reads `data` events, uses metadata to map each internal
`tsid` back to a `participant_id`, then prints a small console bar chart so the
outlier is obvious even before you look at the dashboard.


---

**What just happened?**

You wrote and executed a SignalFlow program directly — the same computation engine that powers every chart in Splunk Observability Cloud. But instead of clicking through the UI to build a chart, you expressed the computation in code, ran it from your workshop environment, and streamed the results in real time.

One participant, `participant-000`, is running significantly slower than everyone else. That participant is a pre-seeded bot introduced before the workshop to create a controlled latency anomaly. Congratulations: you used Splunk Observability Cloud to spot an anomaly in a fleet of services, using a light form of [chaos engineering](https://en.wikipedia.org/wiki/Chaos_engineering).

In Exercise 3 we're going to quantify exactly how much slower `participant-000`
is, using a metric that Splunk Observability Cloud doesn't give you out of the
box.

> 🔵 **Checkpoint 2** — Look up when you reach this point. We'll discuss what you found, why one participant stands out, and what it means before moving on to Exercise 3.

---

## Exercise 3: Computing Apdex — Beyond What O11y Gives You

> ⏱ **Timing:** This exercise is timeboxed to 15 minutes. Start the workflow or script early — the 5-minute rolling window means it needs a few minutes of data before scores appear. Use that time to read the intro and the Interesting parts section.

You've found the chaos-bot. Now let's quantify the problem with a metric that Splunk Observability Cloud doesn't provide out of the box.

Apdex — Application Performance Index — is an industry-standard formula that converts raw latency measurements into a single satisfaction score between 0 and 1. It accounts for the fact that a request taking 400ms isn't a disaster, but one taking 2000ms is — and weights them accordingly.

The formula uses a threshold T. Requests under T are **satisfied**. Requests between T and 4T are **tolerating**. Requests over 4T are **frustrated**. For this workshop, T = 300ms, making the thresholds:

- **Satisfied:** under 300ms
- **Tolerating:** 300ms–1200ms
- **Frustrated:** over 1200ms

```
Apdex = (Satisfied + Tolerating/2) / Total
```

Scores are interpreted as follows:

| Score | Rating |
|---|---|
| 0.94–1.00 | Excellent |
| 0.85–0.93 | Good |
| 0.70–0.84 | Fair |
| 0.50–0.69 | Poor |
| Below 0.50 | Unacceptable |

Splunk Observability Cloud can show you latency. It can't compute Apdex — at least not without SignalFlow.

### Step 1: Compute Apdex

#### Replit

Leave `2 - Send latency metrics` running. Stop `3 - View fleet latency`, or
leave it alone and use another workflow slot, then run `4 - Compute Apdex`.

#### Splunk Show SSH/CLI or local Python

If you are using Splunk Show SSH/CLI:

Leave the real latency sender from Exercise 2a running. Stop the fleet latency
script from Exercise 2b with **Ctrl+C**, or open another terminal for Apdex,
then run:

```bash
cd ~/signalflow101-conf26
python exercises/exercise3.py
```

If you are using local Python on Mac/Linux:

Leave the real latency sender from Exercise 2a running. Stop the fleet latency
script from Exercise 2b with **Ctrl+C**, or open another terminal for Apdex,
then run:

```bash
cd ~/workshops/signalflow101-conf26
.venv/bin/python exercises/exercise3.py
```

If you are using local Python on Windows PowerShell:

Leave the real latency sender from Exercise 2a running. Stop the fleet latency
script from Exercise 2b with **Ctrl+C**, or open another terminal for Apdex,
then run:

```powershell
Set-Location "$HOME\workshops\signalflow101-conf26"
.\.venv\Scripts\python exercises\exercise3.py
```

Expected terminal result:

```
--- Apdex Scores (lowest 15 of 128, T=300ms) ---
participant-000                          0.52  Poor          ██████████
participant-042                          0.96  Excellent     ███████████████████
participant-117                          0.95  Excellent     ███████████████████
...
```

It may take 2–3 minutes before scores appear. The computation needs enough data
to fill the 5-minute rolling window. If you see no output yet, the script is
working — just wait.

The chaos-bot's Apdex score tells a clearer story than its raw latency alone.
It's not just slow — by an industry-standard measure, it's delivering a poor
experience.

Return to the same workshop dashboard and look at **Apdex by participant**. The
chaos-bot should now show a Poor or Unacceptable score while normal participants
remain Excellent.

The contents of `exercises/exercise3.py` are shown below for reference.

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM, PARTICIPANT_ID
from signalflow_rest import stream_signalflow

DISPLAY_LIMIT = 15

T = 300           # Satisfied threshold in ms
T_tolerating = T * 4  # 1200ms — frustrated threshold

program = f"""
latency = data('workshop.api.latency', rollup='latest')

satisfied = latency.map(lambda x: 1 if x is not None and x < {T} else 0).sum(by=['participant_id']).sum(over='5m')
tolerating = latency.map(lambda x: 1 if x is not None and x >= {T} and x < {T_tolerating} else 0).sum(by=['participant_id']).sum(over='5m')
total = latency.map(lambda x: 1 if x is not None else 0).sum(by=['participant_id']).sum(over='5m')

apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""

results = {}

try:
    for event_name, payload, metadata in stream_signalflow(program, API_TOKEN, REALM):
        if event_name != "data":
            continue

        for point in payload.get("data", []):
            tsid = point.get("tsId")
            value = point.get("value")
            if not tsid or value is None:
                continue
            participant = metadata.get(tsid, {}).get("participant_id", "unknown")
            results[participant] = value

        if results:
            sorted_results = sorted(results.items(), key=lambda x: x[1])
            display_results = sorted_results[:DISPLAY_LIMIT]
            own_result = next(
                (item for item in sorted_results if item[0] == PARTICIPANT_ID),
                None,
            )

            if own_result and own_result not in display_results:
                display_results.append(("...", None))
                display_results.append(own_result)

            print(f"\n--- Apdex Scores (lowest {min(DISPLAY_LIMIT, len(sorted_results))} of {len(sorted_results)}, T=300ms) ---")
            for participant, score in display_results:
                if score is None:
                    print(f"... {len(sorted_results)} participants reporting ...")
                    continue
                if score >= 0.94:
                    rating = "Excellent"
                elif score >= 0.85:
                    rating = "Good"
                elif score >= 0.70:
                    rating = "Fair"
                elif score >= 0.50:
                    rating = "Poor"
                else:
                    rating = "Unacceptable"
                bar = "█" * int(score * 20)
                print(f"{participant:<40} {score:.2f}  {rating:<12}  {bar}")
except KeyboardInterrupt:
    print("\nStopped.")
```

#### Interesting parts

`T = 300` and `T_tolerating = T * 4` define the Apdex boundaries in
milliseconds. Changing `T` changes the whole computation.

The SignalFlow program turns each latency datapoint into counts: satisfied
requests, tolerating requests, and total requests. It groups those counts by
`participant_id`, sums them over a 5-minute window, then applies the Apdex
formula: `(satisfied + (tolerating / 2)) / total`.

SignalFlow is doing stream arithmetic live. This could be spreadsheet math
after the fact, but here it updates continuously as metrics arrive. The Python
rating labels (`Excellent`, `Good`, `Poor`, and so on) are just display logic
applied after SignalFlow returns each score.


---

**What just happened?**

You computed a metric that Splunk Observability Cloud doesn't ship — using the industry-standard formula, live, on streaming data, in a script you can run against any metric in any Splunk Observability Cloud instance.

That's what SignalFlow as an API unlocks. The UI gives you a powerful set of built-in analytics. The API gives you the engine underneath — and the engine can compute anything you can express mathematically. Apdex today. Error budget burn rate in the take-home exercises. A custom composite health score for your own business logic whenever you need one.

> 🔵 **Checkpoint 3** — Look up when you reach this point. We'll discuss the Apdex scores, confirm the chaos-bot is the culprit, and look at the workshop dashboard together before closing out the in-room exercises.

---

## Beyond the Workshop

The following exercises are designed to be completed at your own pace — during the workshop if you finish early, or on your own afterward. They build directly on everything you've done in the main exercises. There's no instructor pacing and no checkpoint pressure.

Each take-home exercise includes a timing estimate — not because you're racing, but so you know roughly what you're getting into before you start.

The take-home exercises do not include prebuilt Replit workflows. If you use
Replit for the take-home path, use the Shell or Console to run the commands
shown. Splunk Show SSH/CLI and local Python users use the same terminal
commands from the repo root.

In the take-home command blocks, `python ...` means the Python command for your
environment. In Splunk Show SSH/CLI and Replit Shell, use `python ...` as shown.
For local Python on Mac/Linux, use `.venv/bin/python ...`. For local Python on
Windows PowerShell, use `.\.venv\Scripts\python ...`.

---

## Take-home Exercise 1: Make Your API Interesting

> ⏱ **Estimated time:** 20–30 minutes. The three-terminal setup and the 5-minute Apdex window are the main time variables.

So far your API returns your participant alias from local configuration. Real APIs call other services — and those downstream calls are often where latency problems hide. In this exercise you'll add a real downstream dependency to your API: GitHub's public user API. Then you'll measure how long GitHub takes to respond, send that as a metric, and watch how real-world network variability affects your Apdex score.

Along the way we'll introduce a small but important idea: pulling repeated logic into a reusable function. By the end of this exercise, computing Apdex for any metric is a single line of code.

If you have a GitHub account, use your own username. If not, use a public GitHub username suggested by your instructor. The point is to measure a real downstream service with real network behavior.

### Python scripts at a glance

#### `apdex.py` — Reuse The Apdex Formula

This support file turns the Apdex SignalFlow program from Exercise 3 into a
function that can build the same computation for any metric name.

```python
program = build_apdex_program('workshop.github.latency')
```

What to notice: the math is no longer copied into every script. You give the
function a metric name, and it returns the SignalFlow program.

#### `takehome/takehome1_api.py` — Add A Downstream API Call

This file adds a `/github` endpoint that calls GitHub's public API and measures
how long GitHub takes to respond.

```python
start = time.time()
response = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}")
latency_ms = (time.time() - start) * 1000
```

What to notice: this is the same timing pattern from Exercise 2, but now the
latency comes from a real external dependency instead of your local API.

#### `takehome/takehome1_sender.py` — Send GitHub Latency

This file calls your `/github` endpoint repeatedly and sends the measured
downstream latency as `workshop.github.latency`.

```python
"metric": "workshop.github.latency",
"value": latency_ms,
```

What to notice: changing the metric name lets Splunk Observability Cloud track
GitHub dependency latency separately from your workshop API latency.

#### `takehome/takehome1_apdex.py` — Score The GitHub Metric

This file imports the reusable Apdex function and applies it to the GitHub
latency metric.

```python
from apdex import build_apdex_program
program = build_apdex_program('workshop.github.latency')
```

What to notice: once the Apdex logic is reusable, analyzing a new metric becomes
mostly a configuration choice.

### Step 1: Add your GitHub username to your config

Add your GitHub username to your workshop values:

- In Replit, add a new Secret named `GITHUB_USERNAME`.
- In Splunk Show SSH/CLI or your own Python environment, open your `.env` file
  and add one line:

```
GITHUB_USERNAME=your-github-username-here
```

### Step 2: Create a reusable Apdex function

In Exercise 3 you wrote the Apdex formula directly into your script. That works fine for one metric. Now that we're computing Apdex for a second metric, it makes sense to write the formula once and reuse it.

Open the root-level file `apdex.py`, or create it if needed, and paste the
following code into it:

```python
def build_apdex_program(metric_name, t=300, window='5m'):
    """
    Builds a SignalFlow program that computes Apdex for any metric.

    metric_name: the Splunk O11y metric to analyze
    t:           the satisfied threshold in milliseconds (default 300ms)
    window:      the rolling time window for the computation (default 5 minutes)
    """
    t_tolerating = t * 4
    return f"""
latency = data('{metric_name}', rollup='latest')
satisfied = latency.map(lambda x: 1 if x is not None and x < {t} else 0).sum(by=['participant_id']).sum(over='{window}')
tolerating = latency.map(lambda x: 1 if x is not None and x >= {t} and x < {t_tolerating} else 0).sum(by=['participant_id']).sum(over='{window}')
total = latency.map(lambda x: 1 if x is not None else 0).sum(by=['participant_id']).sum(over='{window}')
apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""
```

This file doesn't do anything on its own — it defines the function so other scripts can import and use it.

#### Interesting parts: Functions

**What a function is**
A function is a named, reusable block of code. Instead of writing the same logic repeatedly, you write it once, give it a name, and call it by that name whenever you need it. `build_apdex_program()` is a function — you give it a metric name and it gives you back a complete SignalFlow program string.

**The `def` keyword**
`def` tells Python you're defining a function. Everything indented beneath it is the function's body — the code that runs when you call it.

**Parameters and defaults**
`metric_name`, `t`, and `window` are parameters — inputs the function accepts. `t=300` and `window='5m'` are default values, meaning if you don't specify them the function uses those values automatically. You can override them when you need different thresholds for a different service.

**Why this matters**
The Apdex formula is now in exactly one place. If you want to change it — adjust the tolerating weight, add a fourth bucket, modify the grouping — you change it once in `apdex.py` and every script that uses it gets the update automatically. This is the principle behind maintainable code, and it's how production monitoring tooling is structured.

**A note on Exercise 3**
Now that `apdex.py` exists, you could rewrite the SignalFlow program section of `exercise3.py` like this:

```python
from apdex import build_apdex_program
program = build_apdex_program('workshop.api.latency')
```

Those two lines replace the entire program string from Exercise 3 and produce identical results. You don't need to go back and change `exercise3.py` — it still works exactly as written. But this is what abstraction looks like in practice: the same computation, expressed more cleanly, reusable across any metric you choose.


### Step 3: Add a new endpoint to your FastAPI

Paste the following into `takehome/takehome1_api.py`, save it, then run it from
the repo root:

```bash
python takehome/takehome1_api.py
```

The contents of `takehome/takehome1_api.py` are shown below for reference.

```python
import os
import time
import requests
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

app = FastAPI()

@app.get("/hello")
def hello():
    return {"participant": os.getenv("PARTICIPANT_ID")}

@app.get("/github")
def github_profile():
    start = time.time()
    response = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}",
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    latency_ms = (time.time() - start) * 1000
    data = response.json()
    return {
        "username": GITHUB_USERNAME,
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "downstream_latency_ms": round(latency_ms, 1)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

Open the URL your environment provides for port `8001` and add `/github` to the URL. You should see something like:

```json
{
  "username": "sarahj",
  "name": "Sarah Jones",
  "public_repos": 23,
  "followers": 41,
  "downstream_latency_ms": 187.4
}
```

#### Interesting parts

**The `/github` endpoint**
`@app.get("/github")` adds a new route to the FastAPI application alongside the existing `/hello` route. When a browser or script calls this URL, the function beneath it runs. It calls the GitHub API, measures how long that takes, and returns the result along with the measured latency.

**Why port 8001**
The original FastAPI runs on port 8000. Running this one on port 8001 means both can run simultaneously without conflicting. In browser environments, you may see both ports listed in the environment's preview or port-forwarding UI.

**`time.time()` before and after**
The latency measurement is identical to what `exercise2a.py` does — capture the time before the call, capture it again after, subtract to get the duration. The difference is that here we're measuring a real external HTTP call to GitHub rather than a local call to our own API. That's what makes the latency real and variable.

**`data.get("name")`**
`.get()` is a safe way to read a value from a dictionary in Python. If the key doesn't exist — for example if a GitHub user hasn't set a display name — it returns `None` rather than crashing. This matters when calling external APIs you don't control.


### Step 4: Send GitHub latency as a metric

Open a second terminal, paste the following into `takehome/takehome1_sender.py`,
save it, then run it from the repo root:

```bash
python takehome/takehome1_sender.py
```

The contents of `takehome/takehome1_sender.py` are shown below for reference.

```python
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import INGEST_TOKEN, REALM, PARTICIPANT_ID

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"

print(f"Sending GitHub latency metrics for {PARTICIPANT_ID}...")
print("Press Ctrl+C to stop.\n")

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
            "X-SF-TOKEN": INGEST_TOKEN
        },
        json=payload
    )

    if response.status_code != 200:
        print(f"Warning: metric send failed ({response.status_code}) - check your workshop credentials")
    else:
        print(f"Sent: {latency_ms:.1f}ms  (github_username: {GITHUB_USERNAME})")

    time.sleep(10)
```

You should see output like:

```
Sending GitHub latency metrics for participant-042...
Press Ctrl+C to stop.

Sent: 187.4ms  (github_username: sarahj)
Sent: 203.1ms  (github_username: sarahj)
Sent: 191.8ms  (github_username: sarahj)
```

#### Interesting parts

**The same ingest pattern**
This is the same `requests.post()` call from Exercise 1 and Exercise 2a — just pointed at `workshop.github.latency` instead of `workshop.api.latency`. From Splunk Observability Cloud's perspective, this is a completely separate metric that can be charted, aggregated, and alerted on independently.

**The second dimension**
The metric now carries two dimensions: `participant_id` as before, and `github_username`. In Splunk Observability Cloud, dimensions let you slice and filter metrics in multiple ways. In production you'd use multiple dimensions to answer questions like "is this slow for all users, or just users on this service in this region?" Here both dimensions identify you, but the pattern is exactly the same.

**Why a separate metric name**
`workshop.github.latency` is distinct from `workshop.api.latency`. Keeping them separate means you can compare local API latency against downstream dependency latency side by side — a useful production pattern for understanding where latency is actually coming from.

**Error handling**
Like `exercise2a.py`, this script checks the response status code and prints a warning if the metric send fails. Silent failures are the enemy of debugging — you always want to know immediately if something isn't working.

**`time.sleep(10)`**
Ten seconds between sends matches the interval in `exercise2a.py`. This gives Splunk Observability Cloud enough data points for meaningful aggregations while being respectful of GitHub's API rate limits for unauthenticated requests.


### Step 5: Compute Apdex for your GitHub metric

Open a third terminal, paste the following into `takehome/takehome1_apdex.py`,
save it, then run it from the repo root:

```bash
python takehome/takehome1_apdex.py
```

The contents of `takehome/takehome1_apdex.py` are shown below for reference.

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM
from apdex import build_apdex_program
from signalflow_rest import stream_signalflow

program = build_apdex_program('workshop.github.latency')

results = {}

try:
    for event_name, payload, metadata in stream_signalflow(program, API_TOKEN, REALM):
        if event_name != "data":
            continue

        for point in payload.get("data", []):
            tsid = point.get("tsId")
            value = point.get("value")
            if not tsid or value is None:
                continue
            participant = metadata.get(tsid, {}).get("participant_id", "unknown")
            results[participant] = value

        if results:
            print("\n--- GitHub Apdex Scores (T=300ms) ---")
            sorted_results = sorted(results.items(), key=lambda x: x[1])
            for participant, score in sorted_results:
                if score >= 0.94:
                    rating = "Excellent"
                elif score >= 0.85:
                    rating = "Good"
                elif score >= 0.70:
                    rating = "Fair"
                elif score >= 0.50:
                    rating = "Poor"
                else:
                    rating = "Unacceptable"
                bar = "█" * int(score * 20)
                print(f"{participant:<40} {score:.2f}  {rating:<12}  {bar}")
except KeyboardInterrupt:
    print("\nStopped.")
```

> ⏳ **Note:** As with Exercise 3, it may take 2–3 minutes before scores appear while the 5-minute window fills with data.

You should see Apdex scores for `workshop.github.latency` — and unlike the synthetic API, these will vary based on real network conditions between your Python environment and GitHub's servers.

#### Interesting parts

**`from apdex import build_apdex_program`**
This line imports the function you created in Step 2. The short `ROOT` setup at
the top of the script lets Python find the repo-level `apdex.py` file even
though this script lives in the `takehome/` folder.

**`program = build_apdex_program('workshop.github.latency')`**
This single line replaces the entire SignalFlow program string from Exercise 3. The function takes the metric name, fills in the formula, and returns the complete program. Notice how much shorter and more readable this script is compared to `exercise3.py` — the Apdex computation is identical, just expressed more cleanly.

**Everything else is identical to Exercise 3**
The SignalFlow REST call, the message loop, and the result printing are unchanged. Only the metric name changed. That's the practical value of the abstraction: write the computation once, apply it to anything.


---

**What just happened?**

You instrumented a real downstream dependency and applied Apdex to it with a single function call. The formula didn't change — only the metric name did. In production this pattern scales directly: one `build_apdex_program()` function, applied across as many services as you need, each producing a consistent and comparable Apdex score.

---

## Take-home Exercise 2: Build a Detector That Pages You

> ⏱ **Estimated time:** 20–30 minutes. The `lasting='5m'` condition on the detector means you'll need to leave the spike script running for several minutes before the alert fires.

Every detector you've ever created in Splunk Observability Cloud — every threshold, every alert condition, every notification rule — was created by making REST API calls. The UI you normally use is a convenient front end for those same calls.

That means anything that can make an HTTP request can do what the UI does. Python can. curl can. Terraform can. A CI/CD pipeline can. A bash script running on a cron job can. Splunk Observability Cloud isn't a web application with an API bolted on — it's an API platform with a web application built on top of it. The UI and your Python scripts have exactly equal access to everything the platform can do.

In this exercise you'll create a detector programmatically using the REST API directly — no UI, no clicks. Then you'll trigger it intentionally and watch the alert fire in Splunk Observability Cloud.

### Python scripts at a glance

#### `takehome/takehome2_detector.py` — Create A Detector By API

This file sends a detector definition to Splunk Observability Cloud's REST API.
The detector uses SignalFlow to compute Apdex and then watches for a bad score.

```python
detect(when(apdex < 0.85, lasting='5m')).publish('Apdex below Good threshold')
```

What to notice: `detect()` turns a SignalFlow computation into an alerting
condition. The rest of the file packages that condition as a detector object.

#### `takehome/takehome2_spike.py` — Trigger The Detector

This file sends intentionally bad latency values for your participant ID so the
detector has something to alert on.

```python
latency = random.uniform(1500, 2500)
```

What to notice: the detector is watching real metric data. To test it, you do
not call the detector directly; you send data that violates its condition.

### Step 1: Create the detector

Paste the following into `takehome/takehome2_detector.py`, save it, then run it
from the repo root:

```bash
python takehome/takehome2_detector.py
```

The contents of `takehome/takehome2_detector.py` are shown below for reference.

```python
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM, PARTICIPANT_ID

API_URL = f"https://api.{REALM}.observability.splunkcloud.com"

# The SignalFlow program that powers this detector.
# This is identical to what the UI generates when you build a detector manually.
signalflow_program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='latest')
satisfied = latency.map(lambda x: 1 if x is not None and x < 300 else 0).sum(over='5m')
tolerating = latency.map(lambda x: 1 if x is not None and x >= 300 and x < 1200 else 0).sum(over='5m')
total = latency.map(lambda x: 1 if x is not None else 0).sum(over='5m')
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
        "X-SF-TOKEN": API_TOKEN
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
```

You should see output like:

```
Detector created successfully.
Name:        Apdex Monitor — participant-042
ID:          Ab1Cd2EfGhI
View it at:  https://app.us1.observability.splunkcloud.com/#/detector/v2/Ab1Cd2EfGhI
```

Click that URL. Your detector is live in Splunk Observability Cloud — created entirely in code, visible in the UI, watching your metrics right now.

#### Interesting parts

**The SignalFlow program**
This is the same Apdex computation from Exercise 3, with two additions. `filter('participant_id', '{PARTICIPANT_ID}')` narrows the computation to just your metrics — unlike Exercise 3 which watched the whole fleet, this detector only watches you. The `detect(when(...))` call at the end is what makes this a detector rather than a computation — it defines the condition that triggers an alert.

**The detector object**
This JSON structure is exactly what the O11y UI constructs when you click through the detector builder. Every field maps to something you've seen in the UI:
- `name` and `description` — what you type in the first screen
- `rules` — the alert conditions tab, including severity and notification targets
- `signalFlowText` — the SignalFlow tab that most users never open
- `notifications` — empty here, but this is where you'd add email, PagerDuty, Slack, and so on

**The detector ID**
Every object in Splunk Observability Cloud — detectors, dashboards, charts — has a unique ID assigned by the API when it's created. That ID is what the URL is built from. You can use it later to update or delete the detector programmatically, using the same REST pattern.

**`requests.post()` to the detector endpoint**
This is the same HTTP call pattern from Exercise 1 — just pointed at `/v2/detector` instead of the ingest endpoint. The API is consistent across everything in Splunk Observability Cloud: authenticate with `X-SF-TOKEN`, send JSON, get JSON back. That pattern works for dashboards, charts, tokens, teams — everything the UI can do.

**Why not the SignalFlow client?**
The SignalFlow Python client is optimized for running computations and streaming results. Creating and managing detectors, dashboards, and other O11y objects is done through the REST API directly. Both are valid Python. Both talk to Splunk Observability Cloud. They're different tools for different jobs, and both are just HTTP under the hood.


### Step 2: Trigger the detector intentionally

Now let's make the alert fire. Open a second terminal, paste the following into
`takehome/takehome2_spike.py`, save it, then run it from the repo root:

```bash
python takehome/takehome2_spike.py
```

The contents of `takehome/takehome2_spike.py` are shown below for reference.

```python
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import INGEST_TOKEN, REALM, PARTICIPANT_ID

INGEST_URL = f"https://ingest.{REALM}.observability.splunkcloud.com/v2/datapoint"

print(f"Sending high-latency metrics for {PARTICIPANT_ID}...")
print("This will trigger your Apdex detector. Press Ctrl+C to stop.\n")

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
            "X-SF-TOKEN": INGEST_TOKEN
        },
        json=payload
    )

    if response.status_code != 200:
        print(f"Warning: metric send failed ({response.status_code}) - check your workshop credentials")
    else:
        print(f"Sent: {latency_ms}ms (frustrated request)")

    # Sending every 5 seconds — faster than normal — to fill the detection
    # window with frustrated requests as quickly as possible.
    time.sleep(5)
```

Leave this running. Within a few minutes your Apdex score will drop below 0.85 and your detector will fire.

> 🔲 **Placeholder:** O11y Alerts navigation steps — to be added once the workshop instance is provisioned.

> ⏳ **Note:** The detector uses `lasting='5m'` — it won't fire until the condition has been true for 5 continuous minutes. Leave `takehome2_spike.py` running and check back after a few minutes.

#### Interesting parts

**The hardcoded latency value**
Unlike `exercise2a.py` which measured real latency, this script sends a fixed value of 1800ms — well above the 1200ms frustrated threshold. This is intentional. We're not measuring anything real here; we're injecting bad data to prove the detector works. In production this technique is called fault injection, and it's a standard way to validate that alerting is correctly configured before you need it in a real incident.

**Why 1800ms specifically**
At 1800ms every single data point lands in the frustrated bucket — scoring zero in the Apdex formula. This guarantees the Apdex score drops to zero quickly and the detector fires within the 5-minute `lasting` window. A more subtle spike might take longer to trigger, making the exercise frustrating rather than instructive.

**Why 5 seconds instead of 10**
Normal senders use `time.sleep(10)`. This script uses 5 seconds — faster — because we want to fill the 5-minute detection window with frustrated requests as quickly as possible. The comment in the code makes that reasoning explicit, which is good practice: future-you (or a colleague) should understand why a number was chosen.

**The same ingest pattern, again**
This is the third script in this workshop that sends metrics via `requests.post()` to the ingest endpoint. The pattern is identical every time — because it is identical. Once you know it, it works everywhere in Splunk Observability Cloud.


### Step 3: Resolve the alert

Stop `takehome2_spike.py` with Ctrl+C, then restart `exercise2a.py` to resume sending normal latency metrics. Within a few minutes your Apdex score will recover above 0.85 and the alert will clear automatically.

Watch the detector transition from alerting to resolved in the O11y UI. This is the full alert lifecycle — trigger, notify, resolve — created and managed entirely through the API.

---

**What just happened?**

You created a production-grade detector without touching the Splunk Observability Cloud UI. The detector is powered by the same SignalFlow computation from Exercise 3, extended with a `detect()` condition. It will keep watching your metrics and firing alerts for as long as it exists in your O11y instance.

The code that created it is a template. Change the metric name, adjust the threshold, add a notification target — and you have a detector for any service in your infrastructure. A team managing many microservices could run a script like this once per service, creating consistent, version-controlled detectors across their fleet in seconds.

That's what it means for Splunk Observability Cloud to be an API platform. The UI is one way in. Python is another. curl is another. Terraform is another. They all speak the same language — HTTP and JSON — and they all have equal access to everything the platform can do.

---

## Take-home Exercise 3: The SLO Error Budget

> ⏱ **Estimated time:** 25–35 minutes. This is the most conceptually rich exercise — budget extra time to read the intro carefully before running the scripts.

You've measured latency. You've computed Apdex. You've built a detector that fires when quality drops. Now let's put all of that into a framework that ties it to a business commitment.

### What is an SLO?

A Service Level Objective is a target for how reliable your service needs to be. Not "as reliable as possible" — that's not a target, it's a wish. An SLO is specific and measurable: "99.5% of requests will complete in under 300ms, measured over a rolling 30-day window."

SLOs matter because they make reliability a conversation rather than a feeling. When an engineer wants to deploy a risky change, the question isn't "do you think this is safe?" — it's "do we have enough error budget to absorb this if it goes wrong?"

### What is an error budget?

If your SLO says 99.5% of requests must be satisfied, then 0.5% can be unsatisfied — that 0.5% is your error budget. It's the amount of degraded experience your service is allowed to deliver while still meeting its commitment.

Error budgets reframe how teams think about reliability. Instead of treating every incident as a failure, you ask: "how much of our budget did this consume?" A brief spike that consumed 2% of the monthly budget is a different conversation than one that consumed 80%.

### What is burn rate?

Burn rate measures how fast you're consuming your error budget. A burn rate of 1.0 means you're consuming it at exactly the sustainable pace — by the end of your SLO window you'll have used exactly 100% of your budget. A burn rate of 2.0 means you're consuming it twice as fast — you'll exhaust your budget halfway through the window. A burn rate of 0.5 means you're well within your target.

The value of burn rate alerting is early warning. If your budget is 0.5% per month and you're burning at 10x, you don't need to wait until the budget is exhausted to know something is wrong. Alert at 2x burn rate — while you still have time to respond.

This is the alerting strategy recommended by the Google SRE workbook, and it's what SRE teams at scale actually use. Splunk Observability Cloud doesn't compute burn rate natively. SignalFlow does.

### What we're building

For this exercise we'll define an SLO for your workshop API:

- **Target:** 99.5% of requests must be satisfied (under 300ms) in a rolling 1-hour window
- **Allowed error rate:** 0.5% (1 - 0.995)
- **Alert threshold:** 2x burn rate

We're using a 1-hour window rather than the production-standard 30 days because in a workshop environment you don't have 30 days of data. The math is identical — only the window changes.

### Python scripts at a glance

#### `takehome/takehome3_slo.py` — Compute Burn Rate

This file turns latency into an error budget burn rate. It counts frustrated
requests, compares that error rate to the SLO target, and publishes the result.

```python
current_error_rate = frustrated / total
burn_rate = current_error_rate / ALLOWED_ERROR_RATE
```

What to notice: burn rate is not another raw measurement. It is a derived signal
that tells you how quickly user-impacting failures are consuming the budget you
said the service could spend.

#### `takehome/takehome3_detector.py` — Alert On Budget Burn

This file creates a detector that alerts when the burn rate is too high for too
long.

```python
detect(when(burn_rate > 2.0, lasting='10m')).publish('Burn rate above 2x')
```

What to notice: this is the same detector pattern from Take-home Exercise 2,
but the condition is now tied to an SLO commitment instead of a simple Apdex
threshold.

### Step 1: Compute your burn rate

Paste the following into `takehome/takehome3_slo.py`, save it, then run it from
the repo root:

```bash
python takehome/takehome3_slo.py
```

The contents of `takehome/takehome3_slo.py` are shown below for reference.

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM, PARTICIPANT_ID
from signalflow_rest import stream_signalflow

SLO_TARGET = 0.995              # 99.5% of requests must be satisfied
ALLOWED_ERROR_RATE = 1 - SLO_TARGET  # 0.005
WINDOW = '1h'                   # Rolling window for the computation
BURN_RATE_THRESHOLD = 2.0       # Alert when burning budget twice as fast as sustainable

program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='latest')

total = latency.map(lambda x: 1 if x is not None else 0).sum(over='{WINDOW}')
frustrated = latency.map(lambda x: 1 if x is not None and x >= 1200 else 0).sum(over='{WINDOW}')
current_error_rate = frustrated / total
burn_rate = current_error_rate / {ALLOWED_ERROR_RATE}

burn_rate.publish('burn_rate')
current_error_rate.publish('current_error_rate')
"""

latest = {}

try:
    for event_name, payload, metadata in stream_signalflow(program, API_TOKEN, REALM):
        if event_name != "data":
            continue

        for point in payload.get("data", []):
            tsid = point.get("tsId")
            value = point.get("value")
            if not tsid or value is None:
                continue
            label = metadata.get(tsid, {}).get("sf_metric", "unknown")
            latest[label] = value

        if len(latest) == 2:
            error_rate = latest.get("current_error_rate", 0)
            burn_rate = latest.get("burn_rate", 0)

            if burn_rate >= BURN_RATE_THRESHOLD:
                status = f"BURNING TOO FAST - {burn_rate:.2f}x"
            elif burn_rate >= 1.0:
                status = f"Elevated - {burn_rate:.2f}x"
            else:
                status = f"Healthy - {burn_rate:.2f}x"

            print(f"\n--- SLO Status for {PARTICIPANT_ID} ---")
            print(f"SLO target:         {SLO_TARGET * 100:.1f}%")
            print(f"Allowed error rate: {ALLOWED_ERROR_RATE * 100:.2f}%")
            print(f"Current error rate: {error_rate * 100:.3f}%")
            print(f"Burn rate:          {status}")
except KeyboardInterrupt:
    print("\nStopped.")
```

> ⏳ **Note:** This computation uses a 1-hour rolling window. If you haven't been sending metrics for close to an hour, the burn rate will be based on a partial window. It will still work — just keep that context in mind when reading the results.

You should see output like:

```
--- SLO Status for participant-042 ---
SLO target:         99.5%
Allowed error rate: 0.50%
Current error rate: 0.031%
Burn rate:          Healthy - 0.06x
```

If you still have `takehome2_spike.py` running from the previous exercise, your output will look quite different:

```
--- SLO Status for participant-042 ---
SLO target:         99.5%
Allowed error rate: 0.50%
Current error rate: 100.000%
Burn rate:          BURNING TOO FAST - 200.00x
```

A burn rate of 200x means you'd exhaust your entire hourly error budget in about 18 seconds.

#### Interesting parts

**The SLO constants**
`SLO_TARGET`, `ALLOWED_ERROR_RATE`, `WINDOW`, and `BURN_RATE_THRESHOLD` are defined at the top as Python variables — not inside the SignalFlow program. They're the parameters of your SLO commitment, the things you'd change when applying this to a different service or a stricter standard. Keeping them at the top makes them easy to find and adjust without reading through the rest of the code.

**The SignalFlow program**
The computation has four steps that map directly to the burn rate formula:

- `total` counts all requests in the rolling window
- `frustrated` counts only the requests that exceeded 1200ms — the ones that violated the SLO
- `current_error_rate` divides frustrated by total — the fraction of requests that were unsatisfactory
- `burn_rate` divides the current error rate by the allowed error rate. If those two numbers are equal, burn rate is exactly 1.0. If current error rate is double the allowed rate, burn rate is 2.0.

**Two `publish()` calls**
This program publishes two streams: `burn_rate` and `current_error_rate`. The result-reading loop waits until `len(latest) == 2` before printing — it collects both values before displaying them together. Each published stream arrives as a separate time series, and `meta.get('sf_metric')` tells us which label belongs to which value.

**The three status levels**
Healthy, elevated, and burning too fast map to real alerting tiers used in production SRE practice. The 2x threshold is a common starting point — your organization's risk tolerance may call for a different number.

**Why frustrated and not satisfied**
In the Apdex formula we counted satisfied and tolerating requests. Here we only count frustrated ones — requests over 1200ms — because the SLO is specifically about the worst-case experience. SignalFlow lets you express whatever definition fits your commitment.


### Step 2: Create a burn rate detector

Now let's make Splunk Observability Cloud watch this for you automatically.
Paste the following into `takehome/takehome3_detector.py`, save it, then run it
from the repo root:

```bash
python takehome/takehome3_detector.py
```

The contents of `takehome/takehome3_detector.py` are shown below for reference.

```python
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM, PARTICIPANT_ID

API_URL = f"https://api.{REALM}.observability.splunkcloud.com"

SLO_TARGET = 0.995
ALLOWED_ERROR_RATE = 1 - SLO_TARGET
WINDOW = '1h'
BURN_RATE_THRESHOLD = 2.0

signalflow_program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='latest')

total = latency.map(lambda x: 1 if x is not None else 0).sum(over='{WINDOW}')
frustrated = latency.map(lambda x: 1 if x is not None and x >= 1200 else 0).sum(over='{WINDOW}')
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
        "X-SF-TOKEN": API_TOKEN
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
```

You should see output like:

```
Burn rate detector created successfully.
Name:        SLO Burn Rate — participant-042
ID:          Xy9Gh3JkLmN
View it at:  https://app.us1.observability.splunkcloud.com/#/detector/v2/Xy9Gh3JkLmN
```

Click the URL. Your burn rate detector is live — watching your error budget in real time, ready to fire the moment your service starts consuming it too fast.

#### Interesting parts

**The `lasting='10m'` condition**
In Take-home Exercise 2 the detector used `lasting='5m'`. Here we use 10 minutes. Burn rate can spike briefly and recover without indicating a real problem. Requiring the condition to persist for 10 minutes filters out transient spikes and ensures the alert represents a sustained trend. In production you'd tune this duration based on how quickly your team can respond and how much budget a 10-minute spike actually consumes.

**Severity: Critical**
Take-home Exercise 2 used Warning severity. This detector uses Critical — a sustained 2x burn rate is a more serious condition than Apdex dropping below the Good threshold. Splunk Observability Cloud uses severity to prioritize alerts and route them to different notification channels. The `notifications` array is where you'd configure that routing.

**The same REST pattern, again**
This is the same `requests.post()` call to the detectors endpoint from Take-home Exercise 2. The payload structure is identical — different SignalFlow, different name, different severity. Once you know the pattern, every Splunk Observability Cloud detector follows it.

**What you'd add for production**
The `notifications` array is empty here for simplicity. In a real deployment you'd add your PagerDuty integration ID, your Slack webhook, or your email address. The detector you just created is one JSON field away from being fully production-ready.


---

**What just happened?**

You implemented a complete SLO monitoring stack in Python:

- A SignalFlow computation that measures error budget burn rate in real time
- A detector that fires when that burn rate exceeds a sustainable threshold
- Both tied to your own SLO commitment, expressed as constants at the top of each script

This is the full arc of what SignalFlow as an API makes possible. The chaos-bot that was causing problems at the start of this workshop? With a burn rate detector in place, you'd have known about it within minutes — not because someone noticed a chart, but because the system told you automatically, with enough context to act.

---

## Running These Exercises on Your Own Instance

The workshop used a shared Splunk Observability Cloud organization provisioned for the event. Once you're back at your desk, you can run these exercises — or build on them — against your own instance.

### If you already have a Splunk Observability Cloud org

Open your `.env` file and replace the workshop values with your own:

```
SPLUNK_ACCESS_TOKEN=your-own-access-token
SPLUNK_REALM=your-own-realm
PARTICIPANT_ID=participant-042
```

If you are using the split-token setup, use this format instead:

```
SPLUNK_REALM=your-own-realm
SPLUNK_INGEST_TOKEN=your-own-ingest-token-secret
SPLUNK_API_TOKEN=your-own-api-token-secret
PARTICIPANT_ID=participant-042
```

Your access tokens and realm are available in your Splunk Observability Cloud account under **Settings → Access Tokens** and **Settings → My Profile** respectively. Everything else stays the same — the scripts, the SignalFlow programs, and the detector definitions all work against any Splunk Observability Cloud org without modification.

### If you don't have a Splunk Observability Cloud org yet

Splunk Observability Cloud Free Edition gives you an org without a paid
subscription. You can sign up at:

**[https://www.splunk.com/en_us/download/infrastructure-monitoring.html](https://www.splunk.com/en_us/download/infrastructure-monitoring.html)**

Once your Free Edition org is provisioned, find your token secret(s) and realm
in the account settings and update your `.env` file as described above.

---

*SignalFlow 101: Build Your First App for Splunk Observability Cloud — .conf26*
*Exercise Guide v0.1 — Pre-production draft. Placeholders to be resolved against live Splunk Show instance.*
