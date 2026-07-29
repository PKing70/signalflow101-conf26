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

from config import TOKEN, REALM, PARTICIPANT_ID
from signalflow_rest import stream_signalflow

DISPLAY_LIMIT = 15

program = """
latency = data('workshop.api.latency').mean(over='1m').mean(by=['participant_id'])
latency.publish('avg_latency_by_participant')
"""

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
            sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
            display_results = sorted_results[:DISPLAY_LIMIT]
            own_result = next(
                (item for item in sorted_results if item[0] == PARTICIPANT_ID),
                None,
            )

            if own_result and own_result not in display_results:
                display_results.append(("...", None))
                display_results.append(own_result)

            print(f"\n--- Fleet Latency (top {min(DISPLAY_LIMIT, len(sorted_results))} of {len(sorted_results)}) ---")
            for participant, latency in display_results:
                if latency is None:
                    print(f"... {len(sorted_results)} participants reporting ...")
                    continue
                bar = "█" * int(latency / 10)
                print(f"{participant:<40} {latency:>8.1f}ms  {bar}")
except KeyboardInterrupt:
    print("\nStopped.")
