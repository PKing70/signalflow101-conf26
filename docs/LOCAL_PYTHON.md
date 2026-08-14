# Existing Local Python Setup

Use this path only if your own Python environment was already working before
the workshop. Replit is the recommended in-room path. Splunk Show SSH/CLI is the
fallback if Replit is blocked.

We will not troubleshoot laptop-specific Python, firewall, package manager, or
IDE issues during the 60-minute session.

## Get The Workshop Files

Choose where you want the workshop folder to live. The example below creates a
parent folder called `workshops` in your home directory, then clones the repo
inside it:

```bash
mkdir -p ~/workshops
cd ~/workshops
if [ ! -d signalflow101-conf26 ]; then git clone https://github.com/PKing70/signalflow101-conf26.git; fi
cd signalflow101-conf26
python -m venv .venv
.venv/bin/python -c "import sys; print(sys.executable)"
.venv/bin/python -m pip install -r requirements.txt
```

The `.venv/bin/python -c ...` command should print a path inside `.venv`.

If `pip` says it cannot find a package such as `requests`, your Python
environment may be pointed at a private company package index. If your laptop
is allowed to reach public PyPI, retry with:

```bash
.venv/bin/python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

If that is blocked by your laptop or network policy, use Replit or the Splunk
Show SSH/CLI environment instead.

Because these commands call `.venv/bin/python` directly, you do not need to
activate the virtual environment first.

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
SPLUNK_INGEST_TOKEN=<workshop ingest token secret>
SPLUNK_API_TOKEN=<workshop API token secret>
PARTICIPANT_ID=<participant ID assigned by workshop staff>
```

Use token secrets, not token IDs. Your participant ID is not copied from O11y or
Splunk Show; it is assigned by the workshop staff and should look like
`participant-042`.
If the credential sheet provides only one workshop token secret, use that same
value for both `SPLUNK_INGEST_TOKEN` and `SPLUNK_API_TOKEN`.

## Run The Exercises

Follow [`docs/EXERCISE_GUIDE.md`](EXERCISE_GUIDE.md).

For local Python on Mac/Linux, use `.venv/bin/python` for the exercise commands
in the guide. On Windows, use `.venv\Scripts\python` instead.
