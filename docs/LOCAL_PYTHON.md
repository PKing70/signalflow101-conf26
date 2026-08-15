# Existing Local Python Setup

Use this path only if your own Python environment was already working before
the workshop. Replit is the recommended in-room path. Splunk Show SSH/CLI is the
fallback if Replit is blocked.

We will not troubleshoot laptop-specific Python, firewall, package manager, or
IDE issues during the 60-minute session.

On Windows, open **Windows Terminal**. If it is not already using PowerShell,
open a **PowerShell** tab. The Windows commands below assume PowerShell syntax.

## Get The Workshop Files

Choose where you want the workshop folder to live. The example below creates a
parent folder called `workshops` in your home directory, then clones the repo
inside it:

Mac/Linux:

```bash
mkdir -p ~/workshops
cd ~/workshops
if [ ! -d signalflow101-conf26 ]; then git clone https://github.com/PKing70/signalflow101-conf26.git; fi
cd signalflow101-conf26
python -m venv .venv
.venv/bin/python -c "import sys; print(sys.executable)"
.venv/bin/python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\workshops" | Out-Null
Set-Location "$HOME\workshops"
if (!(Test-Path signalflow101-conf26)) { git clone https://github.com/PKing70/signalflow101-conf26.git }
Set-Location signalflow101-conf26
py -3 -m venv .venv
.\.venv\Scripts\python -c "import sys; print(sys.executable)"
.\.venv\Scripts\python -m pip install -r requirements.txt
```

The Python path check should print a path inside `.venv`.

If `pip` says it cannot find a package such as `requests`, your Python
environment may be pointed at a private company package index. If your laptop
is allowed to reach public PyPI, retry with:

Mac/Linux:

```bash
.venv/bin/python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

If that is blocked by your laptop or network policy, use Replit or the Splunk
Show SSH/CLI environment instead.

Because these commands call the Python inside `.venv` directly, you do not need
to activate the virtual environment first.

## Configure Workshop Values

From the repo directory, create your `.env` file:

Mac/Linux:

```bash
[ -f .env ] || cp .env.example .env
```

Windows PowerShell:

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Open `.env` in a text editor. Use VS Code, another IDE, or any editor you
already know. If you are working only in a terminal on Mac/Linux, `nano .env`
opens it there. On Windows, Notepad is enough.

Mac/Linux:

```bash
nano .env
```

Windows PowerShell:

```powershell
notepad .env
```

If you use `nano`, use the arrow keys to move around and replace the placeholder
values with the values from the workshop credential instructions. When you are
finished, press **Ctrl+O**, press **Enter** to write the file, then press
**Ctrl+X** to exit. If you use Notepad, edit the values, save, and close the
file.

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
in the guide. On Windows PowerShell, use `.\.venv\Scripts\python` instead.
