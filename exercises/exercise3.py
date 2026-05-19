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

import signalfx
from config import TOKEN, REALM

T = 300            # Satisfied threshold in ms
T_tolerating = T * 4  # 1200ms — frustrated threshold

program = f"""
latency = data('workshop.api.latency', rollup='count')

satisfied = latency.map(lambda x: 1 if x < {T} else 0).sum(by='participant_id', over='5m')
tolerating = latency.map(lambda x: 1 if {T} <= x < {T_tolerating} else 0).sum(by='participant_id', over='5m')
total = latency.sum(by='participant_id', over='5m')

apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""

with signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
) as sfx:

    with sfx.signalflow(TOKEN) as flow:
        computation = flow.execute(program)
        results = {}

        for msg in computation.stream():
            if msg.kind == 'data':
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    participant = meta.get('participant_id', 'unknown')
                    results[participant] = value

                if results:
                    print("\n--- Apdex Scores (T=300ms) ---")
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
