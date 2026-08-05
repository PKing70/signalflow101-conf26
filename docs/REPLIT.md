# Replit Setup

Use this path if GitHub Codespaces or Splunk Show's Python environment is not available on your laptop.

Replit runs Python in your browser. You do not need to install Python locally, but you do need a Replit account and your workshop credentials.

## Start From The Workshop Repo

1. Sign in to Replit and go to your Replit home: [https://replit.com/~](https://replit.com/~).
2. Choose **Import code or design**.
3. Under **Import to Replit**, choose **GitHub**.
4. Under **Import from GitHub**, enter the workshop repo URL: `https://github.com/PKing70/signalflow101-conf26`.
5. Confirm the suggested Repl name is `signalflow101-conf26` and that you are the owner, then choose **Import from GitHub**.
6. Wait for Replit to finish importing the project.
7. When the project opens, Replit may show an Agent panel asking what you want to do with the project. Close the Agent panel with **X** or ignore it. Do not paste workshop secrets into the Agent chat.
8. The right side may say **Your app is not running**. That is expected. You are in the right place.

If you already imported the repo earlier, use Replit's Git tools to pull the latest `main` branch before continuing.

## Add Your Workshop Values

In Replit, use **Secrets**. Replit may already show a secret named `SESSION_SECRET`. Leave it alone. You will add four more secrets for this workshop.

1. From the left side of Replit, open **Tools**.
2. Choose **Secrets**.
3. Choose **+ New Secret**.
4. Add these secrets one at a time. For each one, fill out **Key** and **Value**, then choose **Add Secret**.

Important: copy token secrets/values, not token IDs. Token IDs identify the token in Splunk O11y; token secrets are the values Python uses to authenticate.

| Replit Secret | Value Source |
|---|---|
| `SPLUNK_REALM` | Everyone uses `us1` |
| `SPLUNK_INGEST_TOKEN` | Provided in the workshop credential instructions, or copied from O11y **Settings > Access Tokens** if your account can view it |
| `SPLUNK_API_TOKEN` | Provided in the workshop credential instructions, or copied from your O11y user profile/API access token page |
| `PARTICIPANT_ID` | Provided in your workshop email or credential page, for example `participant-345` |

Do not paste secrets into Python files, chat windows, screenshots, or the public repo.

The example `participant-345` is only an example. Use the exact `PARTICIPANT_ID` assigned to you.

## Run The Workshop Workflows

Replit's UI changes frequently. The most reliable way to open Workflows is:

1. Press **Cmd+K** on Mac or **Ctrl+K** on Windows.
2. Search for `Workflows`.
3. Choose **Workflows** from the results.

You should see these workflows:

| Workflow | What it does |
|---|---|
| `0 - Check setup` | Verifies packages and required workshop values |
| `1 - Start API` | Starts your personal FastAPI service on port 8000 |
| `2 - Send latency metrics` | Measures your API and sends latency to Splunk O11y |
| `3 - View fleet latency` | Runs the SignalFlow fleet query |
| `4 - Compute Apdex` | Runs the SignalFlow Apdex query |
| `In-room - API + sender` | Starts the API and sender together |

Recommended in-room flow:

1. Run `0 - Check setup`.
2. Press **Cmd+K** or **Ctrl+K**, search for `Console`, and open **Console** to see the workflow output.
3. Run `1 - Start API`.
4. Press **Cmd+K** or **Ctrl+K**, search for `Preview`, and open **Preview**.
5. If Preview opens to `/`, add `/hello` to the path. You should see JSON with your `participant_id`.
6. Run `2 - Send latency metrics` and leave it running.
7. Run `3 - View fleet latency` when the instructor asks you to investigate the fleet.
8. Stop `3 - View fleet latency` before starting the next query.
9. Run `4 - Compute Apdex` when the instructor asks you to compute Apdex.

After `0 - Check setup` succeeds, `In-room - API + sender` is a shortcut that starts the API and latency sender together. Use the separate workflows if you want clearer output while learning the flow.

The long-running workflows print continuously. Stop them with the Replit Stop button or `Ctrl+C` in the console.

Expected setup check output:

```text
SignalFlow 101 setup check

Python: 3.12.12

Packages:
  OK      requests
  OK      python-dotenv
  OK      fastapi
  OK      uvicorn

Workshop values:
  OK      SPLUNK_REALM
  OK      SPLUNK_INGEST_TOKEN or SPLUNK_ACCESS_TOKEN
  OK      SPLUNK_API_TOKEN or SPLUNK_ACCESS_TOKEN
  OK      PARTICIPANT_ID

Ready. Start the API, then start sending latency metrics.
```

Expected `/hello` output:

```json
{
  "participant_id": "participant-345",
  "message": "hello from participant-345",
  "simulated_processing_ms": 105.5
}
```

Expected sender output:

```text
API is reachable.
{
  "participant_id": "participant-345",
  "message": "hello from participant-345",
  "simulated_processing_ms": 92.3
}
Sending real latency metrics for participant-345...
Press Ctrl+C to stop.

Sent: 93.7ms
Sent: 112.0ms
```

Expected fleet output:

```text
--- Fleet Latency (top 2 of 2) ---
participant-1                               129.2ms  ████████████
participant-345                              96.1ms  █████████
```

Expected Apdex output:

```text
--- Apdex Scores (lowest 2 of 2, T=300ms) ---
participant-345                          1.00  Excellent     ████████████████████
participant-1                            1.00  Excellent     ████████████████████
```

## Shell Fallback

If the Workflows pane is unavailable, use the Shell:

```bash
python workshop.py check
python workshop.py serve
python workshop.py send
python workshop.py fleet
python workshop.py apdex
```

Keep `python workshop.py serve` running while you run the sender in another workflow or shell.

## Troubleshooting

**Setup check says values are missing:** Open **Tools > Secrets** and confirm the names match exactly. Replit Secrets are case-sensitive.

**API does not start:** Run `python workshop.py install`, then run `python workshop.py serve` again.

**Sender cannot reach `localhost:8000`:** Start `1 - Start API` first. If using the shell, keep the API command running in one shell and run the sender in a second shell.

**Preview shows `{"detail":"Not Found"}`:** The API is running, but Preview opened a path the API does not use. Add `/hello` to the Preview path.

**You see `participant-unconfigured`:** `PARTICIPANT_ID` is missing or still set to a placeholder. Set it to your assigned alias, such as `participant-042`.

**The workflows do not appear:** Replit sometimes needs a workspace reload after importing `.replit`. Reload the browser tab or restart the workspace, then press **Cmd+K** or **Ctrl+K** and search for `Workflows` again.
