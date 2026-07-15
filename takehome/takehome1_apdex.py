"""
Take-home Exercise 1: Make Your API Interesting — Step 5
---------------------------------------------------------
Computes Apdex for workshop.github.latency using the reusable
build_apdex_program() function from apdex.py.

Note: wait 2–3 minutes before scores appear — the computation
needs enough data to fill the 5-minute rolling window.
"""

from config import TOKEN, REALM
from apdex import build_apdex_program
from signalflow_rest import stream_signalflow

program = build_apdex_program('workshop.github.latency')

results = {}

try:
    for event_name, payload, metadata in stream_signalflow(program, TOKEN, REALM):
        if event_name != "data":
            continue

        for point in payload.get("data", []):
            tsid = point.get("tsId")
            value = point.get("value")
            if not tsid or value is None:
                continue
            participant = metadata.get(tsid, {}).get("participant_id", "unknown")
            results[participant] = value

        if results:
            print("\n--- GitHub Apdex Scores (T=300ms) ---")
            sorted_results = sorted(results.items(), key=lambda x: x[1])
            for participant, score in sorted_results:
                if score >= 0.94:
                    rating = "Excellent"
                elif score >= 0.85:
                    rating = "Good"
                elif score >= 0.70:
                    rating = "Fair"
                elif score >= 0.50:
                    rating = "Poor"
                else:
                    rating = "Unacceptable"
                bar = "█" * int(score * 20)
                print(f"{participant:<40} {score:.2f}  {rating:<12}  {bar}")
except KeyboardInterrupt:
    print("\nStopped.")
