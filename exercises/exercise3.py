"""
Exercise 3: Computing Apdex — Beyond What O11y Gives You
---------------------------------------------------------
Runs a SignalFlow program that computes Apdex scores for every
participant in the workshop fleet.

Apdex = (Satisfied + Tolerating/2) / Total
T = 300ms for this workshop.

Scores:  0.94–1.00 Excellent  |  0.85–0.93 Good  |  0.70–0.84 Fair
         0.50–0.69 Poor       |  < 0.50 Unacceptable

Note: it may take 2–3 minutes before scores appear — the computation
needs enough data to fill the 5-minute rolling window.

Then open the Apdex Dashboard in Splunk Observability Cloud.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_TOKEN, REALM, PARTICIPANT_ID
from signalflow_rest import stream_signalflow

DISPLAY_LIMIT = 15

T = 300            # Satisfied threshold in ms
T_tolerating = T * 4  # 1200ms — frustrated threshold

program = f"""
latency = data('workshop.api.latency', rollup='latest')

satisfied = latency.map(lambda x: 1 if x is not None and x < {T} else 0).sum(by=['participant_id']).sum(over='5m')
tolerating = latency.map(lambda x: 1 if x is not None and x >= {T} and x < {T_tolerating} else 0).sum(by=['participant_id']).sum(over='5m')
total = latency.map(lambda x: 1 if x is not None else 0).sum(by=['participant_id']).sum(over='5m')

apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""

results = {}

try:
    for event_name, payload, metadata in stream_signalflow(program, API_TOKEN, REALM):
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
            sorted_results = sorted(results.items(), key=lambda x: x[1])
            display_results = sorted_results[:DISPLAY_LIMIT]
            own_result = next(
                (item for item in sorted_results if item[0] == PARTICIPANT_ID),
                None,
            )

            if own_result and own_result not in display_results:
                display_results.append(("...", None))
                display_results.append(own_result)

            print(f"\n--- Apdex Scores (lowest {min(DISPLAY_LIMIT, len(sorted_results))} of {len(sorted_results)}, T=300ms) ---")
            for participant, score in display_results:
                if score is None:
                    print(f"... {len(sorted_results)} participants reporting ...")
                    continue
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
