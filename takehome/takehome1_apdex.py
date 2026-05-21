"""
Take-home Exercise 1: Make Your API Interesting — Step 5
---------------------------------------------------------
Computes Apdex for workshop.github.latency using the reusable
build_apdex_program() function from exercises/apdex.py.

Note: wait 2–3 minutes before scores appear — the computation
needs enough data to fill the 5-minute rolling window.
"""

import signalfx
from config import TOKEN, REALM
from exercises.apdex import build_apdex_program

program = build_apdex_program('workshop.github.latency')

sfx = signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
)

with sfx.signalflow(TOKEN) as flow:
    computation = flow.execute(program)
    results = {}

    try:
        for msg in computation.stream():
            if hasattr(msg, 'data'):
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    participant = meta.get('participant_id', 'unknown')
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
