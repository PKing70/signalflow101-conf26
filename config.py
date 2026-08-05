"""
config.py - loads workshop credentials from environment or .env

Every script in this repo imports from here:
    from config import INGEST_TOKEN, API_TOKEN, REALM, PARTICIPANT_ID

Set your credentials in Replit Secrets, environment variables, or a .env file
at the root of the repo. For Splunk Show SSH/CLI or local Python, copy
.env.example to .env.
"""

import os
from dotenv import load_dotenv

load_dotenv()

_LEGACY_TOKEN = (os.getenv("SPLUNK_ACCESS_TOKEN") or "").strip()
INGEST_TOKEN = (os.getenv("SPLUNK_INGEST_TOKEN") or _LEGACY_TOKEN).strip()
API_TOKEN = (os.getenv("SPLUNK_API_TOKEN") or _LEGACY_TOKEN).strip()
REALM = (os.getenv("SPLUNK_REALM") or "").strip()
PARTICIPANT_ID = (os.getenv("PARTICIPANT_ID") or "").strip()

_PLACEHOLDERS = {
    "your-access-token-here",
    "your-ingest-token-secret-here",
    "your-api-token-secret-here",
    "your-realm-here",
    "participant-your-number",
    "your-github-username-here",
}

# Validate on import so every script fails fast with a clear message
_missing = [k for k, v in {
    "SPLUNK_INGEST_TOKEN or SPLUNK_ACCESS_TOKEN": INGEST_TOKEN,
    "SPLUNK_API_TOKEN or SPLUNK_ACCESS_TOKEN": API_TOKEN,
    "SPLUNK_REALM": REALM,
    "PARTICIPANT_ID": PARTICIPANT_ID,
}.items() if not v or v in _PLACEHOLDERS]

if _missing:
    raise EnvironmentError(
        f"\n\nMissing required workshop values: {', '.join(_missing)}\n"
        "In Replit, add them in Tools > Secrets.\n"
        "In Splunk Show SSH/CLI or local Python, copy .env.example to .env and fill it in.\n"
        "Your PARTICIPANT_ID should look like participant-042, not an email address.\n"
    )
