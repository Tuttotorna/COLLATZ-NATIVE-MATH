#!/usr/bin/env python3
"""
Scale Stability Audit V0.

This is a bounded reproducibility audit for the Distributed Release Pressure signal.

It does not prove Collatz.
It does not claim Collatz is solved.
It tests whether the debt_peak -> post_peak_release_mass signal survives
changes in N, odd_steps, and post_peak_horizon.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

CONFIGS = [
    {"max_odd_seed": 99, "odd_steps": 80, "post_peak_horizon": 10},
    {"max_odd_seed": 199, "odd_steps": 80, "post_peak_horizon": 10},
    {"max_odd_seed": 499, "odd_steps": 100, "post_peak_horizon": 15},
    {"max_odd_seed": 999, "odd_steps": 120, "post_peak_horizon": 20},
    {"max_odd_seed": 1499, "odd_steps": 140, "post_peak_horizon": 20},
    {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 25},
]


def v2(x: int) -> int:
    if x <= 0:
        raise ValueError("v2 requires a positive integer")
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def odd_step(n: int) -> tuple[int, int, float]:
    if n <= 0 or n % 2 == 0:
        raise ValueError("odd_step requires a positive odd integer")
    m = 3 * n + 1
    a = v2(m)
    next_n = m // (2 ** a)
    delta = math.log2(next_n / n)
    return next_n, a, delta


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None

    mx = mean(xs)
    my = mean(ys)

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))

    if den_x == 0 or den_y == 0:
        return None

    return num / (den_x * den_y)


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_median(values: list[float]) -> float | None:
    return median(values) if values else None


def measure_seed(seed: int, odd_steps: int, post_peak_horizon: int) -> dict:
    if seed <= 0 or seed % 2 == 0:
        raise ValueError("seed must be a positive odd integer")

    n = seed
    steps = []
    prefix = 0.0
    prefixes = []

    for i in range(odd_steps):
        if n == 1:
            break

        next_n, a, delta = odd_step(n)
        prefix += delta

        steps.append(
            {
                "index": i,
                "n": n,
                "next_n": next_n,
                "a": a,
                "delta": delta,
                "prefix_debt": prefix,
                "is_release": delta < -1,
                "is_strong_release": delta < -2,
            }
        )

        prefixes.append(prefix)
        n = next_n

    if not steps:
        return {
            "seed": seed,
            "odd_steps": 0,
            "terminated": True,
            "final_n": n,
            "debt_peak": 0.0,
            "peak_index": None,
            "response_delay": None,
            "has_post_peak_release": False,
            "post_peak_release_count_h": 0,
            "post_peak_strong_release_count_h": 0,
            "post_peak_release_mass_h": 0.0,
            "total_release_count": 0,
            "total_strong_release_count": 0,
        }

    debt_peak = max(prefixes)
    peak_index = prefixes.index(debt_peak)

    later_steps = [s for s in steps if s["index"] > peak_index]
    later_releases = [s for s in later_steps if s["is_release"]]

    if later_releases:
        response_delay = later_releases[0]["index"] - peak_index
        has_post_peak_release = True
    else:
        response_delay = None
        has_post_peak_release = False

    horizon_end = peak_index + post_peak_horizon
    post_peak_window = [
        s for s in steps
        if s["index"] > peak_index and s["index"] <= horizon_end
    ]

    post_peak_releases = [s for s in post_peak_window if s["is_release"]]
    post_peak_strong_releases = [s for s in post_peak_window if s["is_strong_release"]]
    total_releases = [s for s in steps if s["is_release"]]
    total_strong_releases = [s for s in steps if s["is_strong_release"]]

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "final_n": n,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_delay": response_delay,
        "has_post_peak_release": has_post_peak_release,
        "post_peak_release_count_h": len(post_peak_releases),
        "post_peak_strong_release_count_h": len(post_peak_strong_releases),
        "post_peak_release_mass_h": sum(abs(s["delta"]) for s in post_peak_releases),
        "total_release_count": len(total_releases),
        "total_strong_release_count": len(total_strong_releases),
    }


def run_config(max_odd_seed: int, odd_steps: int, post_peak_horizon: int) -> dict:
    seeds = list(range(1, max_odd_seed + 1, 2))

    records = [
        measure_seed(seed, odd_steps, post_peak_horizon)
        for seed in seeds
    ]

    debt_peaks = [r["debt_peak"] for r in records]
    post_peak_release_counts = [float(r["post_peak_release_count_h"]) for r in records]
    post_peak_strong_counts = [float(r["post_peak_strong_release_count_h"]) for r in records]
    post_peak_masses = [float(r["post_peak_release_mass_h"]) for r in records]
    total_release_counts = [float(r["total_release_count"]) for r in records]

    response_records = [r for r in records if r["response_delay"] is not None]
    response_delays = [float(r["response_delay"]) for r in response_records]

    nonzero_debt_records = [r for r in records if r["debt_peak"] > 0]
    nonzero_with_response = [
        r for r in nonzero_debt_records
        if r["response_delay"] is not None
    ]

    primary = pearson(debt_peaks, post_peak_masses)
    strong = pearson(debt_peaks, post_peak_strong_counts)
    count = pearson(debt_peaks, post_peak_release_counts)
    total = pearson(debt_peaks, total_release_counts)

    return {
        "config": {
            "max_odd_seed": max_odd_seed,
            "odd_steps": odd_steps,
            "post_peak_horizon": post_peak_horizon,
        },
        "counts": {
            "odd_seeds_measured": len(records),
            "terminated_within_bound": sum(1 for r in records if r["terminated"]),
            "not_terminated_within_bound": sum(1 for r in records if not r["terminated"]),
            "records_with_positive_debt_peak": len(nonzero_debt_records),
            "records_with_post_peak_release": sum(1 for r in records if r["has_post_peak_release"]),
            "positive_debt_records_with_post_peak_release": len(nonzero_with_response),
        },
        "aggregate": {
            "mean_debt_peak": safe_mean(debt_peaks),
            "max_debt_peak": max(debt_peaks) if debt_peaks else None,
            "mean_response_delay": safe_mean(response_delays),
            "median_response_delay": safe_median(response_delays),
            "min_response_delay": min(response_delays) if response_delays else None,
            "max_response_delay": max(response_delays) if response_delays else None,
            "mean_post_peak_release_count_h": safe_mean(post_peak_release_counts),
            "mean_post_peak_strong_release_count_h": safe_mean(post_peak_strong_counts),
            "mean_post_peak_release_mass_h": safe_mean(post_peak_masses),
            "debt_peak_vs_post_peak_release_count_h_pearson": count,
            "debt_peak_vs_post_peak_strong_release_count_h_pearson": strong,
            "debt_peak_vs_post_peak_release_mass_h_pearson": primary,
            "debt_peak_vs_total_release_count_pearson": total,
        },
    }


def sign_label(x: float | None) -> str:
    if x is None:
        return "none"
    if x > 0:
        return "positive"
    if x < 0:
        return "negative"
    return "zero"


def build() -> dict:
    config_results = [
        run_config(
            max_odd_seed=c["max_odd_seed"],
            odd_steps=c["odd_steps"],
            post_peak_horizon=c["post_peak_horizon"],
        )
        for c in CONFIGS
    ]

    primary_values = [
        r["aggregate"]["debt_peak_vs_post_peak_release_mass_h_pearson"]
        for r in config_results
        if r["aggregate"]["debt_peak_vs_post_peak_release_mass_h_pearson"] is not None
    ]

    strong_values = [
        r["aggregate"]["debt_peak_vs_post_peak_strong_release_count_h_pearson"]
        for r in config_results
        if r["aggregate"]["debt_peak_vs_post_peak_strong_release_count_h_pearson"] is not None
    ]

    count_values = [
        r["aggregate"]["debt_peak_vs_post_peak_release_count_h_pearson"]
        for r in config_results
        if r["aggregate"]["debt_peak_vs_post_peak_release_count_h_pearson"] is not None
    ]

    response_medians = [
        r["aggregate"]["median_response_delay"]
        for r in config_results
        if r["aggregate"]["median_response_delay"] is not None
    ]

    primary_signs = [sign_label(x) for x in primary_values]
    primary_positive_count = sum(1 for s in primary_signs if s == "positive")

    if primary_values:
        primary_min = min(primary_values)
        primary_max = max(primary_values)
        primary_mean = mean(primary_values)
        primary_spread = primary_max - primary_min
    else:
        primary_min = None
        primary_max = None
        primary_mean = None
        primary_spread = None

    stability = {
        "configs_tested": len(config_results),
        "primary_signal_name": "debt_peak_vs_post_peak_release_mass_h_pearson",
        "primary_signal_values": primary_values,
        "primary_signal_positive_count": primary_positive_count,
        "primary_signal_all_positive": primary_positive_count == len(primary_values) and len(primary_values) > 0,
        "primary_signal_min": primary_min,
        "primary_signal_max": primary_max,
        "primary_signal_mean": primary_mean,
        "primary_signal_spread": primary_spread,
        "primary_signal_min_above_0_5": primary_min is not None and primary_min > 0.5,
        "primary_signal_mean_above_0_6": primary_mean is not None and primary_mean > 0.6,
        "strong_release_signal_values": strong_values,
        "release_count_signal_values": count_values,
        "median_response_delay_values": response_medians,
        "median_response_delay_all_at_most_1": all(x <= 1 for x in response_medians) if response_medians else False,
    }

    if (
        stability["primary_signal_all_positive"]
        and stability["primary_signal_min_above_0_5"]
        and stability["primary_signal_mean_above_0_6"]
    ):
        bounded_assessment = "scale_stable_positive_signal"
    elif stability["primary_signal_all_positive"]:
        bounded_assessment = "positive_but_scale_strength_varies"
    else:
        bounded_assessment = "not_scale_stable_under_tested_configs"

    return {
        "version": "v5.0",
        "machine": "Scale Stability Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "configs": CONFIGS,
        "config_results": config_results,
        "stability": stability,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether distributed release pressure remains stable across parameter scales.",
            "primary_signal": "debt_peak_vs_post_peak_release_mass_h_pearson",
            "native_hypothesis": "Debt peaks generate scale-stable post-peak release pressure in bounded odd-step Collatz dynamics.",
        },
        "boundary": {
            "proof_status": "not_a_proof",
            "collatz_status": "not_claimed_solved",
            "theorem_status": "no_theorem_claimed",
            "global_closure_status": "not_claimed",
            "global_invariant_status": "not_claimed",
            "bounded_evidence_status": "measurement_only",
        },
    }


def fmt(x):
    if x is None:
        return "None"
    if isinstance(x, float):
        return f"{x:.12f}"
    return str(x)


def write_markdown(summary: dict) -> str:
    lines = []

    lines.append("# Scale Stability Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded reproducibility audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Stability summary")
    lines.append("")

    for key, value in summary["stability"].items():
        if isinstance(value, list):
            formatted = ", ".join(fmt(v) for v in value)
            lines.append(f"- {key}: `{formatted}`")
        else:
            lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Configuration results")
    lines.append("")

    for item in summary["config_results"]:
        cfg = item["config"]
        agg = item["aggregate"]
        lines.append(
            f"### max_odd_seed={cfg['max_odd_seed']}, "
            f"odd_steps={cfg['odd_steps']}, "
            f"post_peak_horizon={cfg['post_peak_horizon']}"
        )
        lines.append("")
        lines.append(f"- median_response_delay: `{fmt(agg['median_response_delay'])}`")
        lines.append(f"- mean_response_delay: `{fmt(agg['mean_response_delay'])}`")
        lines.append(
            "- debt_peak_vs_post_peak_release_mass_h_pearson: "
            f"`{fmt(agg['debt_peak_vs_post_peak_release_mass_h_pearson'])}`"
        )
        lines.append(
            "- debt_peak_vs_post_peak_strong_release_count_h_pearson: "
            f"`{fmt(agg['debt_peak_vs_post_peak_strong_release_count_h_pearson'])}`"
        )
        lines.append(
            "- debt_peak_vs_post_peak_release_count_h_pearson: "
            f"`{fmt(agg['debt_peak_vs_post_peak_release_count_h_pearson'])}`"
        )
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit checks whether the post-peak release pressure signal survives scale changes.")
    lines.append("")
    lines.append("If the primary signal remains positive and strong, the debt/release language is not only descriptive in one run.")
    lines.append("")
    lines.append("It becomes a bounded reproducible measurement pattern.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")

    for key, value in summary["boundary"].items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    summary = build()

    json_path = RESULTS / "scale_stability_audit_v0.json"
    md_path = RESULTS / "scale_stability_audit_v0.md"
    cert_path = RESULTS / "scale_stability_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.0",
        "artifact": "Scale Stability Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "boundary": summary["boundary"],
    }

    cert_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"WROTE: {json_path}")
    print(f"WROTE: {md_path}")
    print(f"WROTE: {cert_path}")
    print("")
    print("BOUNDED ASSESSMENT:")
    print(f"  {summary['bounded_assessment']}")
    print("")
    print("PRIMARY SIGNAL VALUES:")
    for value in summary["stability"]["primary_signal_values"]:
        print(f"  {fmt(value)}")
    print("")
    print("STABILITY:")
    for key, value in summary["stability"].items():
        print(f"  {key}: {value}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
