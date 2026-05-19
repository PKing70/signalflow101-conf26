"""
apdex.py — reusable Apdex SignalFlow program builder
------------------------------------------------------
Introduced in Take-home Exercise 1.

Usage:
    from exercises.apdex import build_apdex_program
    program = build_apdex_program('workshop.api.latency')

Parameters:
    metric_name : str   — the Splunk O11y metric to analyze
    t           : int   — satisfied threshold in ms (default 300)
    window      : str   — rolling time window (default '5m')
"""


def build_apdex_program(metric_name, t=300, window='5m'):
    t_tolerating = t * 4
    return f"""
latency = data('{metric_name}', rollup='count')
satisfied = latency.map(lambda x: 1 if x < {t} else 0).sum(by='participant_id', over='{window}')
tolerating = latency.map(lambda x: 1 if {t} <= x < {t_tolerating} else 0).sum(by='participant_id', over='{window}')
total = latency.sum(by='participant_id', over='{window}')
apdex = (satisfied + (tolerating / 2)) / total
apdex.publish('apdex')
"""
