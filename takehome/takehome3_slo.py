"""
Take-home Exercise 3: The SLO Error Budget — Step 1
----------------------------------------------------
Computes error budget burn rate for your workshop API using SignalFlow.

SLO:    99.5% of requests must complete under 300ms (satisfied)
Window: 1 hour rolling (production standard is 30 days — same math)
Alert:  2x burn rate means you'll exhaust your budget in half the window

Burn rate = current_error_rate / allowed_error_rate
  1.0x = consuming budget at exactly the sustainable pace
  2.0x = consuming it twice as fast — alert threshold
  0.5x = well within budget

Note: uses a 1-hour window. If you haven't been sending metrics for
close to an hour, results will reflect a partial window — still valid,
just keep that context in mind.
"""

import signalfx
from config import TOKEN, REALM, PARTICIPANT_ID

SLO_TARGET = 0.995               # 99.5% of requests must be satisfied
ALLOWED_ERROR_RATE = 1 - SLO_TARGET  # 0.005
WINDOW = '1h'                    # Rolling computation window
BURN_RATE_THRESHOLD = 2.0        # Alert when burning twice as fast as sustainable

program = f"""
latency = data('workshop.api.latency',
    filter=filter('participant_id', '{PARTICIPANT_ID}'),
    rollup='count')

total = latency.sum(over='{WINDOW}')
frustrated = latency.map(lambda x: 1 if x >= 1200 else 0).sum(over='{WINDOW}')
current_error_rate = frustrated / total
burn_rate = current_error_rate / {ALLOWED_ERROR_RATE}

burn_rate.publish('burn_rate')
current_error_rate.publish('current_error_rate')
"""

sfx = signalfx.SignalFx(
    api_endpoint=f"https://api.{REALM}.observability.splunkcloud.com",
    ingest_endpoint=f"https://ingest.{REALM}.observability.splunkcloud.com",
    stream_endpoint=f"https://stream.{REALM}.observability.splunkcloud.com"
)

with sfx.signalflow(TOKEN) as flow:
    computation = flow.execute(program)
    latest = {}

    try:
        for msg in computation.stream():
            if hasattr(msg, 'data'):
                for tsid, value in msg.data.items():
                    meta = computation.get_metadata(tsid)
                    label = meta.get('sf_metric', 'unknown')
                    latest[label] = value

                if len(latest) == 2:
                    error_rate = latest.get('current_error_rate', 0)
                    burn_rate = latest.get('burn_rate', 0)

                    if burn_rate >= BURN_RATE_THRESHOLD:
                        status = f"⚠️  BURNING TOO FAST — {burn_rate:.2f}x"
                    elif burn_rate >= 1.0:
                        status = f"⚡ Elevated — {burn_rate:.2f}x"
                    else:
                        status = f"✓  Healthy — {burn_rate:.2f}x"

                    print(f"\n--- SLO Status for {PARTICIPANT_ID} ---")
                    print(f"SLO target:         {SLO_TARGET * 100:.1f}%")
                    print(f"Allowed error rate: {ALLOWED_ERROR_RATE * 100:.2f}%")
                    print(f"Current error rate: {error_rate * 100:.3f}%")
                    print(f"Burn rate:          {status}")
    except KeyboardInterrupt:
        print("\nStopped.")
