#!/usr/bin/env python3
"""
Distributed Release Pressure V0.

This is a bounded measurement layer after Compression Debt Machine V0.

It does not prove Collatz.
It does not claim Collatz is solved.
It measures post-peak release timing and distributed discharge pressure.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

DEFAULT_MAX_ODD_SEED = 999
DEFAULT_ODD_STEPS = 120
DEFAULT_POST_PEAK_HORIZON = 20


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
            "pre_peak_release_count": 0,
            "total_release_count": 0,
            "total_strong_release_count": 0,
            "mean_delta": 0.0,
            "cumulative_debt": 0.0,
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
    pre_peak_releases = [s for s in steps if s["index"] <= peak_index and s["is_release"]]
    total_releases = [s for s in steps if s["is_release"]]
    total_strong_releases = [s for s in steps if s["is_strong_release"]]
    deltas = [s["delta"] for s in steps]

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
        "pre_peak_release_count": len(pre_peak_releases),
        "total_release_count": len(total_releases),
        "total_strong_release_count": len(total_strong_releases),
        "mean_delta": mean(deltas),
        "cumulative_debt": sum(deltas),
    }


def build(
    max_odd_seed: int = DEFAULT_MAX_ODD_SEED,
    odd_steps: int = DEFAULT_ODD_STEPS,
    post_peak_horizon: int = DEFAULT_POST_PEAK_HORIZON,
) -> dict:
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

    high_debt = sorted(records, key=lambda r: r["debt_peak"], reverse=True)[:20]
    fastest_response_after_peak = sorted(
        [r for r in records if r["response_delay"] is not None and r["debt_peak"] > 0],
        key=lambda r: (r["response_delay"], -r["debt_peak"]),
    )[:20]
    strongest_post_peak_pressure = sorted(
        records,
        key=lambda r: (r["post_peak_release_mass_h"], r["post_peak_release_count_h"]),
        reverse=True,
    )[:20]

    return {
        "version": "v4.9",
        "machine": "Distributed Release Pressure V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
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
            "debt_peak_vs_post_peak_release_count_h_pearson": pearson(debt_peaks, post_peak_release_counts),
            "debt_peak_vs_post_peak_strong_release_count_h_pearson": pearson(debt_peaks, post_peak_strong_counts),
            "debt_peak_vs_post_peak_release_mass_h_pearson": pearson(debt_peaks, post_peak_masses),
            "debt_peak_vs_total_release_count_pearson": pearson(debt_peaks, total_release_counts),
        },
        "samples": {
            "highest_debt_peak": high_debt,
            "fastest_response_after_peak": fastest_response_after_peak,
            "strongest_post_peak_pressure": strongest_post_peak_pressure,
        },
        "interpretation": {
            "bounded_claim": "The machine measures how release events are distributed after debt peaks.",
            "native_hypothesis": "Debt may generate local distributed release pressure rather than a single maximal discharge.",
            "main_falsifiable_question": "After a debt peak, how quickly and how strongly does release pressure appear?",
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
    lines.append("# Distributed Release Pressure V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded measurement result.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Parameters")
    lines.append("")

    for key, value in summary["parameters"].items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")
    lines.append("## Counts")
    lines.append("")

    for key, value in summary["counts"].items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")
    lines.append("## Aggregate measurements")
    lines.append("")

    for key, value in summary["aggregate"].items():
        lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Highest debt-peak samples")
    lines.append("")

    for item in summary["samples"]["highest_debt_peak"][:10]:
        lines.append(
            f"- seed `{item['seed']}`: debt_peak=`{fmt(item['debt_peak'])}`, "
            f"peak_index=`{item['peak_index']}`, response_delay=`{fmt(item['response_delay'])}`, "
            f"post_peak_release_count_h=`{item['post_peak_release_count_h']}`, "
            f"post_peak_release_mass_h=`{fmt(item['post_peak_release_mass_h'])}`"
        )

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The machine tests whether debt peaks are followed by distributed release pressure.")
    lines.append("")
    lines.append("The target signal is not one maximal discharge, but timing and density of release after peak.")
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

    json_path = RESULTS / "distributed_release_pressure_v0.json"
    md_path = RESULTS / "distributed_release_pressure_v0.md"
    cert_path = RESULTS / "distributed_release_pressure_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v4.9",
        "artifact": "Distributed Release Pressure V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "boundary": summary["boundary"],
    }

    cert_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"WROTE: {json_path}")
    print(f"WROTE: {md_path}")
    print(f"WROTE: {cert_path}")
    print("")
    print("AGGREGATE:")

    for key, value in summary["aggregate"].items():
        print(f"  {key}: {fmt(value)}")

    print("")
    print("BOUNDARY:")

    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
