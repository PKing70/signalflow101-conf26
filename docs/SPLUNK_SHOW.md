# Splunk Show SSH/CLI Setup

Use this fallback path if Replit is blocked by your laptop, browser, or company
policy, or if your instructor tells you to use the Splunk Show Python
environment.

You will use the email address you registered with to retrieve your Splunk Show
password, then SSH to your assigned workshop instance.

Splunk Show SSH is only your Python terminal for the exercises. You will still
use Splunk Observability Cloud in your browser to view the shared workshop
dashboard.

## Sign In To Splunk Show

1. Go to [https://show.splunk.com/](https://show.splunk.com/).
2. Sign in with the email address you used to register for this workshop.
3. Find your Splunk Show password and SSH connection command.
4. Open Terminal, Windows Terminal, PowerShell, or another SSH-capable terminal.
   On Windows, open **Windows Terminal**. If it is not already using
   PowerShell, open a **PowerShell** tab.
5. Connect to your assigned workshop instance using the SSH command shown in
   Splunk Show. It will look similar to this:

```bash
ssh -p 2222 splunk@<your-show-host>
```

6. Enter your Splunk Show password when prompted.

After you connect, you will run the exercises from that SSH terminal.

## Get The Workshop Files

The workshop Show environment is intended to have the repo and Python
dependencies preloaded. Each attendee gets a separate Show instance, so it is
safe to sync your copy of the repo before you start.

After you connect over SSH, start here:

```bash
cd ~/signalflow101-conf26
git pull --ff-only origin main
```

If `cd ~/signalflow101-conf26` says the folder does not exist, clone the repo:

```bash
git clone https://github.com/PKing70/signalflow101-conf26.git
cd signalflow101-conf26
git pull --ff-only origin main
```

If `git pull --ff-only origin main` reports local changes, stop and ask the
instructor for help before continuing. The workshop files should match the
latest version in GitHub.

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
values. Copy the ingest and API token values from Splunk Observability Cloud
after signing in; see [`docs/O11Y.md`](O11Y.md). When you are finished, press
**Ctrl+O**, press **Enter** to write the file, then press **Ctrl+X** to exit.

Your `.env` file should look like this after you edit it:

```text
SPLUNK_REALM=us1
SPLUNK_INGEST_TOKEN=<workshop ingest token value copied from O11y>
SPLUNK_API_TOKEN=<workshop API token value copied from O11y>
PARTICIPANT_ID=<participant ID assigned by workshop staff>
```

Use token values/secrets, not token IDs. Your participant ID is not copied from
O11y or Splunk Show; it is assigned by the workshop staff and should look like
`participant-042`.
Use the ingest token value for `SPLUNK_INGEST_TOKEN` and the API token value for
`SPLUNK_API_TOKEN`. If you accidentally use the ingest token for both, Exercise
1 and Exercise 2a might send metrics, but Exercise 2b will fail with an
unauthorized SignalFlow error.

## Verify Setup

Before starting the exercises, check your setup:

```bash
cd ~/signalflow101-conf26
git pull --ff-only origin main
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
Use [`docs/O11Y.md`](O11Y.md) when the exercise guide tells you to verify your
metrics in Splunk Observability Cloud.
