"""Pareto analysis for model evaluation."""

from __future__ import annotations


def get_pareto_frontier(results: list[dict]) -> list[dict]:
    """Compute the Pareto frontier for model evaluation results.

    We want to:
      - Maximize robustness
      - Minimize latency
      - Minimize parameter count

    A model A dominates model B if:
      - A.robustness >= B.robustness
      - A.latency <= B.latency
      - A.params <= B.params
    AND at least one of these inequalities is strict.

    Args:
        results: List of dictionaries, each containing:
            'model': str,
            'robustness': float,
            'latency': float,
            'params': int or float

    Returns:
        List of dictionaries that are on the Pareto frontier.
    """
    pareto_front = []

    for i, candidate in enumerate(results):
        dominated = False
        for j, other in enumerate(results):
            if i == j:
                continue

            # Check if other dominates candidate
            rob_better_or_eq = other["robustness"] >= candidate["robustness"]
            lat_better_or_eq = other["latency"] <= candidate["latency"]
            param_better_or_eq = other["params"] <= candidate["params"]

            rob_strict = other["robustness"] > candidate["robustness"]
            lat_strict = other["latency"] < candidate["latency"]
            param_strict = other["params"] < candidate["params"]

            is_better_or_equal = rob_better_or_eq and lat_better_or_eq and param_better_or_eq
            is_strictly_better = rob_strict or lat_strict or param_strict

            if is_better_or_equal and is_strictly_better:
                dominated = True
                break

        if not dominated:
            pareto_front.append(candidate)

    return pareto_front
