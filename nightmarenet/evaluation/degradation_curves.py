"""Degradation curves calculation."""

from __future__ import annotations


def calculate_degradation_curves(model_results: dict[str, dict]) -> dict[str, list[dict]]:
    """Extract degradation curves from evaluation results per model.

    Args:
        model_results: A mapping from model name to its evaluation results.
            Expected format for each model's results:
            {
                "strengths": [
                    {
                        "strength": 0.1,
                        "dream_similarity": 0.95,
                        "nightmare_similarity": 0.90
                    },
                    ...
                ]
            }

    Returns:
        A dictionary mapping model names to a list of data points representing
        the degradation curve (strength vs perplexity).
    """
    curves = {}
    for model_name, results in model_results.items():
        curve = []
        strengths = results.get("strengths", [])
        perplexities = results.get("perplexities", [])

        for s, p in zip(strengths, perplexities):
            curve.append({
                "strength": s,
                "robustness": p  # Lower perplexity is better
            })
        curves[model_name] = curve
    return curves
