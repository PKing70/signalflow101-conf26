# Replit Setup

Use this path if GitHub Codespaces or Splunk Show's Python environment is not available on your laptop.

Replit runs Python in your browser. You do not need to install Python locally, but you do need a Replit account and your workshop credentials.

## Start From The Workshop Repo

1. Go to [https://tinyurl.com/DEV1942](https://tinyurl.com/DEV1942).
2. In Replit, open [https://replit.com/import](https://replit.com/import), choose GitHub, and paste the repo URL: `https://github.com/PKing70/signalflow101-conf26`.
3. If your browser allows Replit's rapid import URL, this shortcut may also work: [https://replit.com/github.com/PKing70/signalflow101-conf26](https://replit.com/github.com/PKing70/signalflow101-conf26).
4. Wait for Replit to finish opening the workspace.

If you already imported the repo earlier, use Replit's Git tools to pull the latest `main` branch before continuing.

## Add Your Workshop Values

In Replit, use **Tools > Secrets**. Add these values exactly as named:

| Secret | Value |
|---|---|
| `SPLUNK_REALM` | The workshop realm from the instructor |
| `SPLUNK_INGEST_TOKEN` | The workshop ingest token secret |
| `SPLUNK_API_TOKEN` | The workshop API token secret |
| `PARTICIPANT_ID` | Your assigned alias, such as `participant-042` |

Do not paste secrets into Python files, chat windows, screenshots, or the public repo.

## Run The Workshop Workflows

Open **Tools > Workflows**. You should see these workflows:

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
2. Run `1 - Start API`.
3. Confirm the API works by opening the Replit web preview and adding `/hello` to the URL.
4. Run `2 - Send latency metrics` and leave it running.
5. Run `3 - View fleet latency` when the instructor asks you to investigate the fleet.
6. Run `4 - Compute Apdex` when the instructor asks you to compute Apdex.

After `0 - Check setup` succeeds, `In-room - API + sender` is a shortcut that starts the API and latency sender together. Use the separate workflows if you want clearer output while learning the flow.

The long-running workflows print continuously. Stop them with the Replit Stop button or `Ctrl+C` in the console.

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

**You see `participant-unconfigured`:** `PARTICIPANT_ID` is missing or still set to a placeholder. Set it to your assigned alias, such as `participant-042`.

**The workflows do not appear:** Replit sometimes needs a workspace reload after importing `.replit`. Reload the browser tab or restart the workspace, then open **Tools > Workflows** again.
