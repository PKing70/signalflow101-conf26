#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  cp .env.example .env
fi

if pgrep -f "uvicorn workshop_api:app.*--port 8000" >/dev/null; then
  echo "Workshop API is already running on http://localhost:8000"
  exit 0
fi

nohup python -m uvicorn workshop_api:app --host 0.0.0.0 --port 8000 \
  >/tmp/signalflow101-workshop-api.log 2>&1 &

echo "Workshop API started on http://localhost:8000"
echo "Logs: /tmp/signalflow101-workshop-api.log"
