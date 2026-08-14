# Splunk Show SSH/CLI Setup

Use this fallback path if Replit is blocked by your laptop, browser, or company
policy, or if your instructor tells you to use the shared Splunk Show Python
environment.

The exact SSH host, Web SSH URL, username, and login method will come from the
workshop credential instructions. After you connect, you will run the exercises
from a terminal in the browser or from your own SSH client.

## Get The Workshop Files

The workshop Show environment is intended to have the repo and Python
dependencies preloaded.

After you sign in, start here:

```bash
cd ~/signalflow101-conf26
```

If `cd ~/signalflow101-conf26` says the folder does not exist, clone the repo:

```bash
git clone https://github.com/PKing70/signalflow101-conf26.git
cd signalflow101-conf26
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
If the credential sheet provides only one workshop token secret, use that same
value for both `SPLUNK_INGEST_TOKEN` and `SPLUNK_API_TOKEN`.

## Verify Setup

Before starting the exercises, check your setup:

```bash
cd ~/signalflow101-conf26
python workshop.py check
```

If `python workshop.py check` says packages are missing, install them, then run
the setup check again:

```bash
python -m pip install -r requirements.txt
python workshop.py check
```

After setup passes, go to [`docs/EXERCISE_GUIDE.md`](EXERCISE_GUIDE.md). The
exercise guide tells you which CLI command to run for each timed step.
