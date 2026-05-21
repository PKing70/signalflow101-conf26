"""
Exercise 2b: Investigate the Fleet
------------------------------------
Runs a SignalFlow program that computes 1-minute average latency
for every participant in the workshop, sorted by latency descending.

Run this in a second terminal while exercise2a.py is still running.
One participant will stand out. That's not a coincidence.

Then open the Fleet Dashboard in Splunk Observability Cloud to see
the same data visualized live.
"""

import signalfx
from config import TOKEN, REALM

program = """
latency = data('workshop.api.latency').mean(over='1m').mean(by=['participant_id'])
latency.publish('avg_latency_by_participant')
"""

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
                    print("\n--- Fleet Latency (1-minute average) ---")
                    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
                    for participant, latency in sorted_results:
                        bar = "█" * int(latency / 10)
                        print(f"{participant:<40} {latency:>8.1f}ms  {bar}")
    except KeyboardInterrupt:
        print("\nStopped.")