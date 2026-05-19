# SignalFlow 101: Build Your First App for Splunk Observability Cloud
### Workshop Exercise Guide — .conf26

---

## Welcome

This workshop assumes you're familiar with the core building blocks of Splunk Observability Cloud — dashboards, detectors, metrics, and dimensions. We're not going to cover those from scratch. Instead, we're going to focus on extending them.

Everything you interact with in Splunk Observability Cloud is powered by SignalFlow, Splunk's streaming analytics engine. When you build a chart or configure a detector in the UI, SignalFlow is running underneath it. Today you're going to write SignalFlow directly, in Python — which means you can go beyond what the UI exposes: define your own formulas, compute custom metrics, and build tooling that's repeatable, version-controlled, and deployable at scale.

---

## What You'll Need

- A browser
- Your conference registration email address
- The workshop credentials sheet handed out at the start of the session

That's it. No installation. No configuration. Just open your browser and follow along.

---

## What You'll Build

By the end of this workshop you will have:

- A personal API endpoint running in the cloud, sending real metrics into our shared Splunk Observability Cloud instance
- SignalFlow programs that investigate a live fleet-wide latency anomaly and identify the culprit
- An Apdex score — a custom SLO metric computed in SignalFlow that Splunk Observability Cloud doesn't give you out of the box

The take-home exercises at the end of this document go further: real downstream latency measurement, programmatic detector creation, and a full SLO error budget burn rate — all in Python, all against your own Splunk Observability Cloud instance.

---

## How This Works

Each exercise follows the same pattern:

1. **Paste** the code block into your environment
2. **Run** it
3. **Observe** what happens in Splunk Observability Cloud
4. **Read** the explanation at your own pace

To stop any running script at any time, press **Ctrl+C** in its terminal.

The checkpoints throughout the session are your signal to pause and look up — that's when we'll discuss what just happened and what it means before moving on.

The **"What does this code do?"** sections are optional and collapsed by default. Open them if you're curious or have time. Skip them if you need to keep pace — you won't miss anything required.

---

## Getting Started: Your Workshop Credentials

> 🔲 **Placeholder:** Splunk Show credential delivery instructions to be added once the workshop instance is provisioned. This section will include the QR code or URL for the credential page, login instructions using your conference registration email, and where to find your access token and realm once logged in.

Once you have your credentials, you'll need three pieces of information:

- Your **access token** — provided via the workshop credentials page
- Your **realm** — for example, `us1` or `us0`; also provided with your credentials
- Your **participant ID** — the email address you used to register for .conf26

Open the file called `.env` in your Codespace. It looks like this:

```
SPLUNK_ACCESS_TOKEN=your-token-here
SPLUNK_REALM=your-realm-here
PARTICIPANT_ID=your-email-here
```

Replace the placeholder values with your credentials and your email address, then save the file. Every script in this workshop reads from this file automatically — you won't need to enter your credentials again.

---

## Exercise 1: Meet Your API

> ⏱ **Timing:** This exercise takes approximately 8–12 minutes. If you finish early, read the "What does this code do?" section while you wait for the checkpoint.

Your Codespace is already running a small API. Let's make sure everything is working — and prove that your Python environment can talk to Splunk Observability Cloud — before we go further.

### Step 1: Visit your API

In your Codespace, look for the **Ports** tab at the bottom of the screen. You'll see port `8000` listed. Click the globe icon next to it to open your API in a browser tab.

Add `/hello` to the end of the URL. You should see your name — pulled from the `PARTICIPANT_ID` you set in your `.env` file.

If you see your name, your API is running. Move on to Step 2.

### Step 2: Send your first metric to Splunk Observability Cloud

Now let's send a metric. Paste the following into the file called `exercise1.py` in your Codespace and click **Run**:

```python
import requests
import random
from config import TOKEN, REALM, PARTICIPANT_ID

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
        "X-SF-TOKEN": TOKEN
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

You should see output like:

```
Metric sent successfully.
participant_id: sarah.jones@example.com
latency:        287.3ms
```

### Step 3: Verify in Splunk Observability Cloud

> 🔲 **Placeholder:** Step-by-step instructions for finding a metric in the O11y Metric Finder or Data Explorer — to be added once the workshop instance is provisioned. Attendees will look for `workshop.api.latency` filtered by their `participant_id`.

When you find your metric, you're looking for `workshop.api.latency` filtered by your `participant_id`. If it's there, you're fully connected and ready to move on.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The imports**
The first few lines load tools we need. Think of `import` like opening an app before you use it — `requests` is how Python sends data over the internet, and `random` generates the fake latency value. `from config import` pulls your credentials from the `.env` file you configured earlier — `TOKEN`, `REALM`, and `PARTICIPANT_ID` are available throughout the script without repeating the setup code.

**The payload**
This is the metric itself — structured the way Splunk Observability Cloud expects to receive it. It has three parts: a name (`workshop.api.latency`), a value (your random latency number), and a dimension (`participant_id`) that tags the metric as yours.

In Splunk Observability Cloud, dimensions are how you slice and filter metrics — by host, by service, by environment. In this workshop, `participant_id` is doing the same job. Every metric you send will carry it, which means your data stays identifiable even though we're all sharing the same Splunk Observability Cloud instance.

**Sending it**
`requests.post()` sends the payload to Splunk Observability Cloud's ingest endpoint — a URL built from your realm. The `X-SF-TOKEN` header is how Splunk Observability Cloud knows the request is authorized.

**The response check**
If Splunk Observability Cloud accepted the metric, it responds with status code `200` and the script prints your confirmation. Any other code means something went wrong — most likely a credential issue — and the script prints the error to help you diagnose it.

**Why a fake latency value?**
In Exercise 1 we just want to prove the pipeline works — credentials, connection, ingest. The value doesn't need to be meaningful yet. In Exercise 2 we'll replace this random number with a latency that's actually measured from your API.

</details>

---

**What just happened?**

You sent a data point to Splunk Observability Cloud using the ingest API — the same API that monitoring agents, integrations, and instrumentation libraries use. The metric has a name, a value, and a dimension that identifies it as yours. That's the complete picture of a metric in Splunk Observability Cloud.

In Exercise 2, we'll replace the random value with something real — and that's when the investigation begins.

> 🔵 **Checkpoint 1** — Look up when you reach this point. We'll confirm everyone's metric is visible in Splunk Observability Cloud before moving on.

---

## Exercise 2: Real Metrics and a Mystery

> ⏱ **Timing:** This exercise takes approximately 13–17 minutes across two steps. Step 1 should take 5–7 minutes. Step 2 runs until Checkpoint 2 at the 35-minute mark.

In Exercise 1 you proved the pipeline works. Now let's make the data meaningful — and introduce something unexpected in our fleet.

### Step 1: Start sending real latency

Your Codespace is already running a FastAPI that responds to requests and measures how long each one takes. Paste the following into `exercise2a.py` and click **Run**:

```python
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
    response = requests.get("http://localhost:8000/hello")
    latency_ms = (time.time() - start) * 1000

    send_latency(latency_ms)
    print(f"Sent: {latency_ms:.1f}ms")
    time.sleep(10)
```

You should see output like:

```
Sending real latency metrics for sarah.jones@example.com...
Press Ctrl+C to stop.

Sent: 142.3ms
Sent: 138.7ms
Sent: 145.1ms
```

Leave this running. Open a second terminal in your Codespace for Step 2.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The `send_latency()` function**
Rather than writing the ingest call directly in the loop, we've wrapped it in a function. A function is a named, reusable block of code — you define it once with `def` and call it by name whenever you need it. This keeps the loop readable and separates the "measure" step from the "send" step clearly.

**Error handling**
`send_latency()` checks the response status code and prints a warning if something goes wrong. Without this check, a failed send would be silent — the script would keep printing latency values while sending nothing. This version tells you immediately if your credentials or connection are the problem.

**Measuring latency**
`time.time()` captures the moment before the API call and again immediately after it returns. The difference — converted to milliseconds by multiplying by 1000 — is the real round-trip time for that request. This is exactly how production monitoring agents measure latency.

**The loop**
`while True` runs forever until you stop it with Ctrl+C. Every 10 seconds it measures a new latency value and sends it. The 10-second interval gives Splunk Observability Cloud enough data points for meaningful aggregations without flooding the ingest API.

**The second terminal**
`exercise2a.py` runs continuously, so it occupies the terminal. Opening a second terminal lets you run the next script alongside it without stopping the metric flow.

</details>

### Step 2: Investigate the fleet

With everyone's metrics flowing, let's look at the whole picture. Paste the following into `exercise2b.py` in your second terminal and click **Run**:

```python
import signalfx
from config import TOKEN, REALM

program = """
latency = data('workshop.api.latency').mean(by='participant_id', over='1m')
latency.publish('avg_latency_by_participant')
"""

with signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
) as sfx:

    with sfx.signalflow(TOKEN) as flow:
        computation = flow.execute(program)
        results = {}

        for msg in computation.stream():
            if msg.kind == 'data':
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    participant = meta.get('participant_id', 'unknown')
                    results[participant] = value

                if results:
                    print("\n--- Fleet Latency (1-minute average) ---")
                    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
                    for participant, latency in sorted_results:
                        bar = "█" * int(latency / 10)
                        print(f"{participant:<40} {latency:>8.1f}ms  {bar}")
```

You should see output like:

```
--- Fleet Latency (1-minute average) ---
chaos-bot@conf26.splunk.com              847.3ms  ████████████████████████████████████████████████████████████
sarah.jones@example.com                  143.2ms  ██████████████
michael.chen@example.com                 138.9ms  █████████████
...
```

One participant stands out. That's not a coincidence.

Now open the Fleet Dashboard in Splunk Observability Cloud to see the same data visualized live.

> 🔲 **Placeholder:** O11y Fleet Dashboard navigation steps — to be added once the workshop instance is provisioned.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The SignalFlow program**
The string assigned to `program` is a SignalFlow program — the same language running behind every chart in Splunk Observability Cloud. `data()` selects your metric stream. `.mean(by='participant_id', over='1m')` computes the 1-minute average latency for each participant separately. `.publish()` makes the results available to read.

**The SignalFlow client**
`signalfx.SignalFx()` connects to your Splunk Observability Cloud instance using your realm and token. `sfx.signalflow()` opens a streaming connection to the SignalFlow engine. Unlike the `requests.post()` calls in earlier exercises — which send a single request and receive a single response — this connection stays open and streams results continuously as SignalFlow computes them.

**Reading the stream**
`computation.stream()` returns messages as they arrive from SignalFlow. We only care about `data` messages — those contain actual metric values. Each data message contains one or more time series identifiers (`tsid`) and their current values.

**Getting the participant name**
The `tsid` is an internal identifier — a short string that SignalFlow uses to track each time series. `computation.get_metadata(tsid)` translates it back into the dimensions we know — in this case, `participant_id`. That's how we connect a raw number to a name.

**The bar chart**
Each `█` character represents 10ms of latency. It makes the outlier immediately obvious without needing to open a separate tool. The console output is a confidence check that your code is working — the Fleet Dashboard in Splunk Observability Cloud is the full visual.

</details>

---

**What just happened?**

You wrote and executed a SignalFlow program directly — the same computation engine that powers every chart in Splunk Observability Cloud. But instead of clicking through the UI to build a chart, you expressed the computation in code, ran it from your Codespace, and streamed the results in real time.

One participant — `chaos-bot@conf26.splunk.com` — is running significantly slower than everyone else. In Exercise 3 we're going to quantify exactly how much slower, using a metric that Splunk Observability Cloud doesn't give you out of the box.

> 🔵 **Checkpoint 2** — Look up when you reach this point. We'll discuss what you found, why one participant stands out, and what it means before moving on to Exercise 3.

---

## Exercise 3: Computing Apdex — Beyond What O11y Gives You

> ⏱ **Timing:** This exercise takes approximately 13–17 minutes. Paste and run the script early — the 5-minute rolling window means it needs a few minutes of data before scores appear. Use that time to read the intro and the code explainer.

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

Splunk Observability Cloud can show you latency. It can't compute Apdex — at least not without SignalFlow. Paste the following into `exercise3.py` and click **Run**:

```python
import signalfx
from config import TOKEN, REALM

T = 300           # Satisfied threshold in ms
T_tolerating = T * 4  # 1200ms — frustrated threshold

program = f"""
latency = data('workshop.api.latency', rollup='count')

satisfied = latency.map(lambda x: 1 if x < {T} else 0).sum(by='participant_id', over='5m')
tolerating = latency.map(lambda x: 1 if {T} <= x < {T_tolerating} else 0).sum(by='participant_id', over='5m')
total = latency.sum(by='participant_id', over='5m')

apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""

with signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
) as sfx:

    with sfx.signalflow(TOKEN) as flow:
        computation = flow.execute(program)
        results = {}

        for msg in computation.stream():
            if msg.kind == 'data':
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    participant = meta.get('participant_id', 'unknown')
                    results[participant] = value

                if results:
                    print("\n--- Apdex Scores (T=300ms) ---")
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
```

> ⏳ **Note:** It may take 2–3 minutes before scores appear. The computation needs enough data to fill the 5-minute rolling window. If you see no output yet, the script is working — just wait.

You should see output like:

```
--- Apdex Scores (T=300ms) ---
chaos-bot@conf26.splunk.com              0.52  Poor          ██████████
sarah.jones@example.com                  0.96  Excellent     ███████████████████
michael.chen@example.com                 0.95  Excellent     ███████████████████
...
```

The chaos-bot's Apdex score tells a clearer story than its raw latency alone. It's not just slow — by an industry-standard measure, it's delivering a poor experience.

Now open the Apdex Dashboard in Splunk Observability Cloud.

> 🔲 **Placeholder:** O11y Apdex Dashboard navigation steps — to be added once the workshop instance is provisioned.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The thresholds**
`T = 300` and `T_tolerating = T * 4` define the Apdex boundaries in milliseconds. These are Python variables — they get substituted into the SignalFlow program string before it's sent to Splunk Observability Cloud. Changing `T` here changes the entire computation. This is a preview of the abstraction we'll build properly in Take-home Exercise 1.

**The SignalFlow program**
This is more involved than Exercise 2, but it follows the Apdex formula directly:

- `data('workshop.api.latency', rollup='count')` retrieves the latency stream. The `rollup='count'` argument tells SignalFlow to treat each data point as an individual measurement rather than averaging them — which is what we need for counting requests in each bucket.
- `latency.map(lambda x: 1 if x < 300 else 0)` transforms each data point: if the latency was under 300ms it becomes 1 (satisfied); otherwise 0. This is how SignalFlow counts requests that meet a condition.
- `.sum(by='participant_id', over='5m')` adds up those 1s and 0s over a 5-minute window, grouped by participant. The result is a count of satisfied requests per participant over the last 5 minutes.
- The same pattern produces `tolerating` — requests between 300ms and 1200ms.
- `total` counts all requests regardless of latency.
- The final line is the Apdex formula expressed as stream arithmetic: `(satisfied + (tolerating / 2)) / total`. SignalFlow handles the division of two streams natively.

**Why this matters**
Every line of this SignalFlow program could be a column in a spreadsheet or a query in a BI tool — computed after the fact, on historical data. SignalFlow computes it live, on a continuous stream, updating every few seconds. That's what makes it suited to observability rather than reporting.

**The rating labels**
These are standard Apdex ratings defined by the Apdex Alliance. They're computed in Python after SignalFlow returns the score — simple comparisons on the number we received, nothing to do with SignalFlow itself.

</details>

---

**What just happened?**

You computed a metric that Splunk Observability Cloud doesn't ship — using the industry-standard formula, live, on streaming data, in a script you can run against any metric in any Splunk Observability Cloud instance.

That's what SignalFlow as an API unlocks. The UI gives you a powerful set of built-in analytics. The API gives you the engine underneath — and the engine can compute anything you can express mathematically. Apdex today. Error budget burn rate in the take-home exercises. A custom composite health score for your own business logic whenever you need one.

> 🔵 **Checkpoint 3** — Look up when you reach this point. We'll discuss the Apdex scores, confirm the chaos-bot is the culprit, and look at the Apdex Dashboard together before closing out the in-room exercises.

---

## Beyond the Workshop

The following exercises are designed to be completed at your own pace — during the workshop if you finish early, or on your own afterward. They build directly on everything you've done in the main exercises. There's no instructor pacing and no checkpoint pressure.

Each take-home exercise includes a timing estimate — not because you're racing, but so you know roughly what you're getting into before you start.

---

## Take-home Exercise 1: Make Your API Interesting

> ⏱ **Estimated time:** 20–30 minutes. The three-terminal setup and the 5-minute Apdex window are the main time variables.

So far your API returns your name from a local file. Real APIs call other services — and those downstream calls are often where latency problems hide. In this exercise you'll add a real downstream dependency to your API: GitHub's public user API. Then you'll measure how long GitHub takes to respond, send that as a metric, and watch how real-world network variability affects your Apdex score.

Along the way we'll introduce a small but important idea: pulling repeated logic into a reusable function. By the end of this exercise, computing Apdex for any metric is a single line of code.

You already have a GitHub account — you're using it right now for this Codespace. So this isn't a random downstream service. It's one you have a direct connection to.

### Step 1: Add your GitHub username to your config

Open your `.env` file and add one line:

```
GITHUB_USERNAME=your-github-username-here
```

### Step 2: Create a reusable Apdex function

In Exercise 3 you wrote the Apdex formula directly into your script. That works fine for one metric. Now that we're computing Apdex for a second metric, it makes sense to write the formula once and reuse it.

Paste the following into a new file called `apdex.py`:

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
latency = data('{metric_name}', rollup='count')
satisfied = latency.map(lambda x: 1 if x < {t} else 0).sum(by='participant_id', over='{window}')
tolerating = latency.map(lambda x: 1 if {t} <= x < {t_tolerating} else 0).sum(by='participant_id', over='{window}')
total = latency.sum(by='participant_id', over='{window}')
apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""
```

This file doesn't do anything on its own — it defines the function so other scripts can import and use it.

<details>
<summary><strong>What is a function, and why does this matter? (optional)</strong></summary>

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

</details>

### Step 3: Add a new endpoint to your FastAPI

Paste the following into `takehome1_api.py` and click **Run**:

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

Visit port `8001` in your Codespace's Ports tab and add `/github` to the URL. You should see something like:

```json
{
  "username": "sarahj",
  "name": "Sarah Jones",
  "public_repos": 23,
  "followers": 41,
  "downstream_latency_ms": 187.4
}
```

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The `/github` endpoint**
`@app.get("/github")` adds a new route to the FastAPI application alongside the existing `/hello` route. When a browser or script calls this URL, the function beneath it runs. It calls the GitHub API, measures how long that takes, and returns the result along with the measured latency.

**Why port 8001**
The original FastAPI runs on port 8000. Running this one on port 8001 means both can run simultaneously without conflicting. You'll see both listed in your Codespace's Ports tab.

**`time.time()` before and after**
The latency measurement is identical to what `exercise2a.py` does — capture the time before the call, capture it again after, subtract to get the duration. The difference is that here we're measuring a real external HTTP call to GitHub rather than a local call to our own API. That's what makes the latency real and variable.

**`data.get("name")`**
`.get()` is a safe way to read a value from a dictionary in Python. If the key doesn't exist — for example if a GitHub user hasn't set a display name — it returns `None` rather than crashing. This matters when calling external APIs you don't control.

</details>

### Step 4: Send GitHub latency as a metric

Open a second terminal and paste the following into `takehome1_sender.py`, then click **Run**:

```python
import os
import time
import requests
from dotenv import load_dotenv
from config import TOKEN, REALM, PARTICIPANT_ID

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
            "X-SF-TOKEN": TOKEN
        },
        json=payload
    )

    if response.status_code != 200:
        print(f"Warning: metric send failed ({response.status_code}) — check your credentials in .env")
    else:
        print(f"Sent: {latency_ms:.1f}ms  (github_username: {GITHUB_USERNAME})")

    time.sleep(10)
```

You should see output like:

```
Sending GitHub latency metrics for sarah.jones@example.com...
Press Ctrl+C to stop.

Sent: 187.4ms  (github_username: sarahj)
Sent: 203.1ms  (github_username: sarahj)
Sent: 191.8ms  (github_username: sarahj)
```

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

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

</details>

### Step 5: Compute Apdex for your GitHub metric

Open a third terminal and paste the following into `takehome1_apdex.py`, then click **Run**:

```python
import signalfx
from config import TOKEN, REALM
from apdex import build_apdex_program

program = build_apdex_program('workshop.github.latency')

with signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
) as sfx:

    with sfx.signalflow(TOKEN) as flow:
        computation = flow.execute(program)
        results = {}

        for msg in computation.stream():
            if msg.kind == 'data':
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    participant = meta.get('participant_id', 'unknown')
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
```

> ⏳ **Note:** As with Exercise 3, it may take 2–3 minutes before scores appear while the 5-minute window fills with data.

You should see Apdex scores for `workshop.github.latency` — and unlike the synthetic API, these will vary based on real network conditions between your Codespace and GitHub's servers.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**`from apdex import build_apdex_program`**
This line imports the function you created in Step 2. Python looks for a file called `apdex.py` in the same folder and loads the function from it.

**`program = build_apdex_program('workshop.github.latency')`**
This single line replaces the entire SignalFlow program string from Exercise 3. The function takes the metric name, fills in the formula, and returns the complete program. Notice how much shorter and more readable this script is compared to `exercise3.py` — the Apdex computation is identical, just expressed more cleanly.

**Everything else is identical to Exercise 3**
The SignalFlow client setup, the message loop, the result printing — all unchanged. Only the metric name changed. That's the practical value of the abstraction: write the computation once, apply it to anything.

</details>

---

**What just happened?**

You instrumented a real downstream dependency and applied Apdex to it with a single function call. The formula didn't change — only the metric name did. In production this pattern scales directly: one `build_apdex_program()` function, applied across as many services as you need, each producing a consistent and comparable Apdex score.

---

## Take-home Exercise 2: Build a Detector That Pages You

> ⏱ **Estimated time:** 20–30 minutes. The `lasting='5m'` condition on the detector means you'll need to leave the spike script running for several minutes before the alert fires.

Every detector you've ever created in Splunk Observability Cloud — every threshold, every alert condition, every notification rule — was created by making REST API calls. The UI you normally use is a convenient front end for those same calls.

That means anything that can make an HTTP request can do what the UI does. Python can. curl can. Terraform can. A CI/CD pipeline can. A bash script running on a cron job can. Splunk Observability Cloud isn't a web application with an API bolted on — it's an API platform with a web application built on top of it. The UI and your Python scripts have exactly equal access to everything the platform can do.

In this exercise you'll create a detector programmatically using the REST API directly — no UI, no clicks. Then you'll trigger it intentionally and watch the alert fire in Splunk Observability Cloud.

### Step 1: Create the detector

Paste the following into `takehome2_detector.py` and click **Run**:

```python
import requests
from config import TOKEN, REALM, PARTICIPANT_ID

API_URL = f"https://api.{REALM}.observability.splunkcloud.com"

# The SignalFlow program that powers this detector.
# This is identical to what the UI generates when you build a detector manually.
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
```

You should see output like:

```
Detector created successfully.
Name:        Apdex Monitor — sarah.jones@example.com
ID:          Ab1Cd2EfGhI
View it at:  https://app.us1.observability.splunkcloud.com/#/detector/v2/Ab1Cd2EfGhI
```

Click that URL. Your detector is live in Splunk Observability Cloud — created entirely in code, visible in the UI, watching your metrics right now.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

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

</details>

### Step 2: Trigger the detector intentionally

Now let's make the alert fire. Paste the following into `takehome2_spike.py` and run it in a second terminal:

```python
import time
import requests
from config import TOKEN, REALM, PARTICIPANT_ID

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
```

Leave this running. Within a few minutes your Apdex score will drop below 0.85 and your detector will fire.

> 🔲 **Placeholder:** O11y Alerts navigation steps — to be added once the workshop instance is provisioned.

> ⏳ **Note:** The detector uses `lasting='5m'` — it won't fire until the condition has been true for 5 continuous minutes. Leave `takehome2_spike.py` running and check back after a few minutes.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The hardcoded latency value**
Unlike `exercise2a.py` which measured real latency, this script sends a fixed value of 1800ms — well above the 1200ms frustrated threshold. This is intentional. We're not measuring anything real here; we're injecting bad data to prove the detector works. In production this technique is called fault injection, and it's a standard way to validate that alerting is correctly configured before you need it in a real incident.

**Why 1800ms specifically**
At 1800ms every single data point lands in the frustrated bucket — scoring zero in the Apdex formula. This guarantees the Apdex score drops to zero quickly and the detector fires within the 5-minute `lasting` window. A more subtle spike might take longer to trigger, making the exercise frustrating rather than instructive.

**Why 5 seconds instead of 10**
Normal senders use `time.sleep(10)`. This script uses 5 seconds — faster — because we want to fill the 5-minute detection window with frustrated requests as quickly as possible. The comment in the code makes that reasoning explicit, which is good practice: future-you (or a colleague) should understand why a number was chosen.

**The same ingest pattern, again**
This is the third script in this workshop that sends metrics via `requests.post()` to the ingest endpoint. The pattern is identical every time — because it is identical. Once you know it, it works everywhere in Splunk Observability Cloud.

</details>

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

### Step 1: Compute your burn rate

Paste the following into `takehome3_slo.py` and click **Run**:

```python
import signalfx
from config import TOKEN, REALM, PARTICIPANT_ID

SLO_TARGET = 0.995              # 99.5% of requests must be satisfied
ALLOWED_ERROR_RATE = 1 - SLO_TARGET  # 0.005
WINDOW = '1h'                   # Rolling window for the computation
BURN_RATE_THRESHOLD = 2.0       # Alert when burning budget twice as fast as sustainable

program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='count')

total = latency.sum(over='{WINDOW}')
frustrated = latency.map(lambda x: 1 if x >= 1200 else 0).sum(over='{WINDOW}')
current_error_rate = frustrated / total
burn_rate = current_error_rate / {ALLOWED_ERROR_RATE}

burn_rate.publish('burn_rate')
current_error_rate.publish('current_error_rate')
"""

with signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
) as sfx:

    with sfx.signalflow(TOKEN) as flow:
        computation = flow.execute(program)
        latest = {}

        for msg in computation.stream():
            if msg.kind == 'data':
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    label = meta.get('sf_metric', 'unknown')
                    latest[label] = value

                if len(latest) == 2:
                    error_rate = latest.get('current_error_rate', 0)
                    burn_rate = latest.get('burn_rate', 0)

                    if burn_rate >= BURN_RATE_THRESHOLD:
                        status = f"⚠️  BURNING TOO FAST — {burn_rate:.2f}x"
                    elif burn_rate >= 1.0:
                        status = f"⚡ Elevated — {burn_rate:.2f}x"
                    else:
                        status = f"✓  Healthy — {burn_rate:.2f}x"

                    print(f"\n--- SLO Status for {PARTICIPANT_ID} ---")
                    print(f"SLO target:         {SLO_TARGET * 100:.1f}%")
                    print(f"Allowed error rate: {ALLOWED_ERROR_RATE * 100:.2f}%")
                    print(f"Current error rate: {error_rate * 100:.3f}%")
                    print(f"Burn rate:          {status}")
```

> ⏳ **Note:** This computation uses a 1-hour rolling window. If you haven't been sending metrics for close to an hour, the burn rate will be based on a partial window. It will still work — just keep that context in mind when reading the results.

You should see output like:

```
--- SLO Status for sarah.jones@example.com ---
SLO target:         99.5%
Allowed error rate: 0.50%
Current error rate: 0.031%
Burn rate:          ✓  Healthy — 0.06x
```

If you still have `takehome2_spike.py` running from the previous exercise, your output will look quite different:

```
--- SLO Status for sarah.jones@example.com ---
SLO target:         99.5%
Allowed error rate: 0.50%
Current error rate: 100.000%
Burn rate:          ⚠️  BURNING TOO FAST — 200.00x
```

A burn rate of 200x means you'd exhaust your entire hourly error budget in about 18 seconds.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

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

</details>

### Step 2: Create a burn rate detector

Now let's make Splunk Observability Cloud watch this for you automatically. Paste the following into `takehome3_detector.py` and click **Run**:

```python
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
```

You should see output like:

```
Burn rate detector created successfully.
Name:        SLO Burn Rate — sarah.jones@example.com
ID:          Xy9Gh3JkLmN
View it at:  https://app.us1.observability.splunkcloud.com/#/detector/v2/Xy9Gh3JkLmN
```

Click the URL. Your burn rate detector is live — watching your error budget in real time, ready to fire the moment your service starts consuming it too fast.

<details>
<summary><strong>What does this code do? (optional)</strong></summary>

**The `lasting='10m'` condition**
In Take-home Exercise 2 the detector used `lasting='5m'`. Here we use 10 minutes. Burn rate can spike briefly and recover without indicating a real problem. Requiring the condition to persist for 10 minutes filters out transient spikes and ensures the alert represents a sustained trend. In production you'd tune this duration based on how quickly your team can respond and how much budget a 10-minute spike actually consumes.

**Severity: Critical**
Take-home Exercise 2 used Warning severity. This detector uses Critical — a sustained 2x burn rate is a more serious condition than Apdex dropping below the Good threshold. Splunk Observability Cloud uses severity to prioritize alerts and route them to different notification channels. The `notifications` array is where you'd configure that routing.

**The same REST pattern, again**
This is the same `requests.post()` call to the detectors endpoint from Take-home Exercise 2. The payload structure is identical — different SignalFlow, different name, different severity. Once you know the pattern, every Splunk Observability Cloud detector follows it.

**What you'd add for production**
The `notifications` array is empty here for simplicity. In a real deployment you'd add your PagerDuty integration ID, your Slack webhook, or your email address. The detector you just created is one JSON field away from being fully production-ready.

</details>

---

**What just happened?**

You implemented a complete SLO monitoring stack in Python:

- A SignalFlow computation that measures error budget burn rate in real time
- A detector that fires when that burn rate exceeds a sustainable threshold
- Both tied to your own SLO commitment, expressed as constants at the top of each script

This is the full arc of what SignalFlow as an API makes possible. The chaos-bot that was causing problems at the start of this workshop? With a burn rate detector in place, you'd have known about it within minutes — not because someone noticed a chart, but because the system told you automatically, with enough context to act.

---

## Running These Exercises on Your Own Instance

The workshop used a shared Splunk Observability Cloud instance provisioned via Splunk Show. Once you're back at your desk, you can run these exercises — or build on them — against your own instance.

### If you already have a Splunk Observability Cloud org

Open your `.env` file and replace the workshop values with your own:

```
SPLUNK_ACCESS_TOKEN=your-own-access-token
SPLUNK_REALM=your-own-realm
PARTICIPANT_ID=your-email-here
```

Your access token and realm are available in your Splunk Observability Cloud account under **Settings → Access Tokens** and **Settings → My Profile** respectively. Everything else stays the same — the scripts, the SignalFlow programs, and the detector definitions all work against any Splunk Observability Cloud org without modification.

### If you don't have a Splunk Observability Cloud org yet

Splunk offers a free trial that gives you full access to Splunk Observability Cloud. You can sign up at:

**[https://www.splunk.com/en_us/download/splunk-observability-cloud-free-trial.html](https://www.splunk.com/en_us/download/splunk-observability-cloud-free-trial.html)**

Once your trial is provisioned, find your access token and realm in the account settings and update your `.env` file as described above.

### If your Codespace has expired

GitHub Codespaces remain active for up to 30 days of inactivity. If yours has expired, you can relaunch it from the GitHub repository page — your files will still be there. The environment will rebuild automatically using the same devcontainer configuration.

If you'd prefer to run the exercises outside of a Codespace entirely, see the appendix below.

---

## Appendix: If You Can't Use GitHub Codespaces

If GitHub is unavailable or restricted in your environment, the following alternatives work with all of the exercises in this document. All three connect to the same Splunk Observability Cloud instance using the same credentials — you won't miss any functionality.

### Option 1: Google Colab (recommended fallback)

Google Colab runs Python notebooks in your browser with no installation required. A Google account is all you need.

> 🔲 **Placeholder:** Link to pre-built Colab notebook — to be added once the workshop exercises are finalized and tested.

Once open, run the first cell to install dependencies, then follow the exercise steps as written. The code is identical — Colab runs it in notebook cells rather than a terminal.

### Option 2: Replit

Replit runs Python in your browser and supports multiple files and terminals, making it the closest experience to Codespaces of the browser-based alternatives.

> 🔲 **Placeholder:** Link to pre-built Replit project — to be added once the workshop exercises are finalized and tested.

### Option 3: Local Python

If you have admin rights on your laptop, a single command installs everything you need:

**Mac:**
```bash
brew install python && pip install requests python-dotenv signalfx fastapi uvicorn
```

**Windows:**
```bash
winget install Python.Python.3 && pip install requests python-dotenv signalfx fastapi uvicorn
```

Once installed, clone the workshop repository and run the exercises from the repo folder as normal.

---

*SignalFlow 101: Build Your First App for Splunk Observability Cloud — .conf26*
*Exercise Guide v0.1 — Pre-production draft. Placeholders to be resolved against live Splunk Show instance.*
