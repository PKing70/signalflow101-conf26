# Splunk Show SSH/CLI Setup

Use this path if your instructor provides access to the shared Splunk Show Python environment.

The exact SSH host, username, and login method will come from the workshop credential instructions. After you connect, you will run the exercises from a terminal.

## Configure Workshop Values

From the repo directory, create your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and fill in the values from the workshop credential instructions:

```text
SPLUNK_REALM=us1
SPLUNK_INGEST_TOKEN=<token secret>
SPLUNK_API_TOKEN=<token secret>
PARTICIPANT_ID=<your assigned alias>
```

Use token secrets, not token IDs. Your participant ID should look like `participant-042`.

## Run The CLI Flow

Check your setup:

```bash
python workshop.py check
```

Start your API:

```bash
python workshop.py serve
```

Open a second terminal for the sender and queries:

```bash
python workshop.py send
python workshop.py fleet
python workshop.py apdex
```

Stop long-running commands with `Ctrl+C`.

If your instructor provides a URL or port-forwarding instructions for your API, add `/hello` to that URL to view the API response.
