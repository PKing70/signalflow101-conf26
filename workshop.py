"""
workshop.py - small command helper for workshop Python environments.

Replit workflows and CLI terminals call into this file so attendees can run
short, named commands instead of copying longer shell commands.
"""

import argparse
import importlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request


API_URL = "http://localhost:8000/hello"
PLACEHOLDERS = {
    "your-access-token-here",
    "your-ingest-token-secret-here",
    "your-api-token-secret-here",
    "your-realm-here",
    "participant-your-number",
    "your-github-username-here",
}


def is_present(value):
    return bool(value and value.strip() and value.strip() not in PLACEHOLDERS)


def load_environment():
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass
    return {
        "SPLUNK_REALM": os.getenv("SPLUNK_REALM", "").strip(),
        "SPLUNK_INGEST_TOKEN": os.getenv("SPLUNK_INGEST_TOKEN", "").strip(),
        "SPLUNK_API_TOKEN": os.getenv("SPLUNK_API_TOKEN", "").strip(),
        "SPLUNK_ACCESS_TOKEN": os.getenv("SPLUNK_ACCESS_TOKEN", "").strip(),
        "PARTICIPANT_ID": os.getenv("PARTICIPANT_ID", "").strip(),
    }


def package_status():
    packages = [
        ("requests", "requests"),
        ("dotenv", "python-dotenv"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
    ]
    results = []
    for module_name, package_name in packages:
        try:
            importlib.import_module(module_name)
            results.append((package_name, True))
        except ImportError:
            results.append((package_name, False))
    return results


def check_setup(_args):
    values = load_environment()
    packages = package_status()

    print("SignalFlow 101 setup check\n")
    print(f"Python: {sys.version.split()[0]}")

    print("\nPackages:")
    packages_ok = True
    for package_name, installed in packages:
        status = "OK" if installed else "MISSING"
        print(f"  {status:<7} {package_name}")
        packages_ok = packages_ok and installed

    ingest_token = values["SPLUNK_INGEST_TOKEN"] or values["SPLUNK_ACCESS_TOKEN"]
    api_token = values["SPLUNK_API_TOKEN"] or values["SPLUNK_ACCESS_TOKEN"]
    checks = [
        ("SPLUNK_REALM", values["SPLUNK_REALM"]),
        ("SPLUNK_INGEST_TOKEN or SPLUNK_ACCESS_TOKEN", ingest_token),
        ("SPLUNK_API_TOKEN or SPLUNK_ACCESS_TOKEN", api_token),
        ("PARTICIPANT_ID", values["PARTICIPANT_ID"]),
    ]

    print("\nWorkshop values:")
    values_ok = True
    for label, value in checks:
        status = "OK" if is_present(value) else "MISSING"
        print(f"  {status:<7} {label}")
        values_ok = values_ok and status == "OK"

    participant_id = values["PARTICIPANT_ID"]
    if is_present(participant_id) and not participant_id.startswith("participant-"):
        print("\nWarning: PARTICIPANT_ID should look like participant-042.")
        values_ok = False

    if packages_ok and values_ok:
        print("\nReady. Start the API, then start sending latency metrics.")
        return 0

    print("\nNot ready yet.")
    print("In Replit, add these values in Tools > Secrets.")
    print("In Splunk Show SSH/CLI or local Python, copy .env.example to .env and fill it in.")
    return 1


def wait_for_api(args):
    deadline = time.monotonic() + args.timeout
    print(f"Waiting for API at {API_URL}...")

    last_error = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(API_URL, timeout=3) as response:
                payload = json.loads(response.read().decode("utf-8"))
            print("API is reachable.")
            print(json.dumps(payload, indent=2))
            return 0
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            time.sleep(2)

    print(f"API did not become ready within {args.timeout} seconds.")
    if last_error:
        print(f"Last error: {last_error}")
    print("Start the API workflow or run the API serve command from the guide.")
    return 1


def serve_api(_args):
    os.execv(
        sys.executable,
        [
            sys.executable,
            "-m",
            "uvicorn",
            "workshop_api:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
    )


def run_script(script_path):
    os.execv(sys.executable, [sys.executable, script_path])


def send_latency(args):
    if wait_for_api(args) != 0:
        return 1
    run_script("exercises/exercise2a.py")
    return 0


def view_fleet(_args):
    run_script("exercises/exercise2b.py")
    return 0


def compute_apdex(_args):
    run_script("exercises/exercise3.py")
    return 0


def install_dependencies(_args):
    return subprocess.call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )


def build_parser():
    parser = argparse.ArgumentParser(description="SignalFlow 101 workshop helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="check packages and workshop values")
    check.set_defaults(func=check_setup)

    install = subparsers.add_parser("install", help="install Python dependencies")
    install.set_defaults(func=install_dependencies)

    serve = subparsers.add_parser("serve", help="start the workshop API")
    serve.set_defaults(func=serve_api)

    wait = subparsers.add_parser("wait-api", help="wait until the API is reachable")
    wait.add_argument("--timeout", type=int, default=60)
    wait.set_defaults(func=wait_for_api)

    send = subparsers.add_parser(
        "send", help="wait for the API, then send latency metrics"
    )
    send.add_argument("--timeout", type=int, default=60)
    send.set_defaults(func=send_latency)

    fleet = subparsers.add_parser("fleet", help="view fleet latency")
    fleet.set_defaults(func=view_fleet)

    apdex = subparsers.add_parser("apdex", help="compute Apdex scores")
    apdex.set_defaults(func=compute_apdex)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
