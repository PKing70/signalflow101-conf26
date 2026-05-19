"""
Take-home Exercise 1: Make Your API Interesting — Step 3
---------------------------------------------------------
Adds a /github endpoint to your FastAPI that calls GitHub's
public user API and measures real downstream latency.

Runs on port 8001 alongside the original API on port 8000.
Visit port 8001 in your Codespace Ports tab, then add /github.

Requires GITHUB_USERNAME in your .env file.
"""

import os
import time
import requests
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
PARTICIPANT_ID = os.getenv("PARTICIPANT_ID")

if not GITHUB_USERNAME:
    raise EnvironmentError(
        "GITHUB_USERNAME not set in .env — add it before running this script."
    )

app = FastAPI()


@app.get("/hello")
def hello():
    return {"participant": PARTICIPANT_ID}


@app.get("/github")
def github_profile():
    start = time.time()
    response = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}",
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    latency_ms = (time.time() - start) * 1000
    data = response.json()
    return {
        "username": GITHUB_USERNAME,
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "downstream_latency_ms": round(latency_ms, 1)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
