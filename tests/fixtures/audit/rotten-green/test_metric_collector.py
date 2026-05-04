"""Metric collector tests.

Fixture for the SLOBAC audit's `rotten-green` scenario. Two planted positives
exercise the canonical signals: empty body with TODO comment, and a SUT call
followed by a `print` where an assertion was intended. One negative control
asserts on a real return value.
"""

from __future__ import annotations


class MetricCollector:
    """SUT — collects metric samples and reports their average."""

    def __init__(self):
        self._samples: list[float] = []

    def record(self, value: float) -> None:
        self._samples.append(value)

    def average(self) -> float:
        if not self._samples:
            return 0.0
        return sum(self._samples) / len(self._samples)


# --- positive 1: empty body with TODO; reports green.                       -
#     The runner counts this as a passing test. There is no assertion,   -
#     no SUT call. The only signal that work is missing is a comment    -
#     that no aggregator surfaces.                                       -

def test_record_handles_negative_values():
    
    pass


# --- positive 2: `print` where assertion was intended.                      -
#     The SUT runs (record + average), the result is computed and       -
#     bound, and then `print(avg)` is called. No assertion. The test   -
#     reports green regardless of what `average()` returns — even     -
#     `def average(self): return 999` would still print and pass.    -

def test_average_after_three_samples():
    collector = MetricCollector()
    collector.record(10.0)
    collector.record(20.0)
    collector.record(30.0)
    avg = collector.average()
    print("computed average:", avg)


# --- negative control: real assertion on real SUT output.                   -

def test_average_of_three_samples_is_their_arithmetic_mean():
    collector = MetricCollector()
    collector.record(10.0)
    collector.record(20.0)
    collector.record(30.0)
    assert collector.average() == 20.0
