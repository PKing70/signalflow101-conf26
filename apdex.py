"""
Reusable Apdex SignalFlow program builder.
"""


def build_apdex_program(metric_name, t=300, window="5m"):
    """
    Build a SignalFlow program that computes Apdex for any latency metric.

    metric_name: Splunk O11y metric to analyze
    t: satisfied threshold in milliseconds
    window: rolling time window for the computation
    """
    t_tolerating = t * 4
    return f"""
latency = data('{metric_name}', rollup='count')
satisfied = latency.map(lambda x: 1 if x < {t} else 0).sum(over='{window}').sum(by=['participant_id'])
tolerating = latency.map(lambda x: 1 if x >= {t} and x < {t_tolerating} else 0).sum(over='{window}').sum(by=['participant_id'])
total = latency.sum(over='{window}').sum(by=['participant_id'])
apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""
