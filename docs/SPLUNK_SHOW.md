# Splunk Show SSH/CLI Setup

Use this path if your instructor provides access to the shared Splunk Show Python environment.

The exact SSH host, username, and login method will come from the workshop credential instructions. After you connect, you will run the exercises from a terminal.

## Get The Workshop Files

Your instructor will tell you whether the repo is already present in the shared
Splunk Show Python environment.

If the repo is already present, change into that folder. If not, clone it:

```bash
git clone https://github.com/PKing70/signalflow101-conf26.git
cd signalflow101-conf26
```

If dependencies are not already installed in the Splunk Show environment, run:

```bash
python -m pip install -r requirements.txt
```

## Configure Workshop Values

From the repo directory, create your `.env` file:

```bash
[ -f .env ] || cp .env.example .env
```

Open `.env` in a text editor. Use VS Code, another IDE, or any editor you
already know. If you are working only in a terminal, `nano .env` opens it there.

```bash
nano .env
```

If you use `nano`, use the arrow keys to move around and replace the placeholder
values with the values from the workshop credential instructions. When you are
finished, press **Ctrl+O**, press **Enter** to write the file, then press
**Ctrl+X** to exit.

Your `.env` file should look like this after you edit it:

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

Open a second terminal for the one-shot metric and sender:

```bash
python exercises/exercise1.py
python workshop.py send
```

Open a third terminal for the queries:

```bash
python workshop.py fleet
python workshop.py apdex
```

Stop `python workshop.py fleet` before running `python workshop.py apdex`.

Stop long-running commands with `Ctrl+C`.

If your instructor provides a URL or port-forwarding instructions for your API, add `/hello` to that URL to view the API response.
