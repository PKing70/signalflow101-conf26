# Splunk Show SSH/CLI Setup

Use this fallback path if Replit is blocked by your laptop, browser, or company
policy, or if your instructor tells you to use the shared Splunk Show Python
environment.

You will use the email address you registered with to retrieve your Splunk Show
password, then SSH to the shared workshop host.

## Sign In To Splunk Show

1. Go to [https://show.splunk.com/](https://show.splunk.com/).
2. Sign in with the email address you used to register for this workshop.
3. Find your Splunk Show password.
4. Open Terminal, Windows Terminal, PowerShell, or another SSH-capable terminal.
5. Connect to the workshop host:

```bash
ssh -p 2222 splunk@100.53.232.167
```

6. Enter your Splunk Show password when prompted.

After you connect, you will run the exercises from that SSH terminal.

## Get The Workshop Files

The workshop Show environment is intended to have the repo and Python
dependencies preloaded.

After you connect over SSH, start here:

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
SPLUNK_INGEST_TOKEN=<workshop ingest token secret>
SPLUNK_API_TOKEN=<workshop API token secret>
PARTICIPANT_ID=<participant ID assigned by workshop staff>
```

Use token secrets, not token IDs. Your participant ID is not copied from O11y or
Splunk Show; it is assigned by the workshop staff and should look like
`participant-042`.
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
