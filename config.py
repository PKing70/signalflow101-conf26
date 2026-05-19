"""
config.py — loads workshop credentials from .env

Every script in this repo imports from here:
    from config import TOKEN, REALM, PARTICIPANT_ID

Set your credentials in the .env file at the root of the repo.
Copy .env.example to .env and fill in the values.
"""

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SPLUNK_ACCESS_TOKEN")
REALM = os.getenv("SPLUNK_REALM")
PARTICIPANT_ID = os.getenv("PARTICIPANT_ID")

# Validate on import so every script fails fast with a clear message
_missing = [k for k, v in {
    "SPLUNK_ACCESS_TOKEN": TOKEN,
    "SPLUNK_REALM": REALM,
    "PARTICIPANT_ID": PARTICIPANT_ID,
}.items() if not v]

if _missing:
    raise EnvironmentError(
        f"\n\nMissing required values in your .env file: {', '.join(_missing)}\n"
        "Copy .env.example to .env and fill in your workshop credentials.\n"
    )
