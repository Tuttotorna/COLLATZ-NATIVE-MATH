#!/usr/bin/env python3
"""
Residual Decay Audit V0.

This bounded audit separates the apparent decay of the distributed release
pressure signal by varying one axis at a time:

A. max_odd_seed
B. odd_steps
C. post_peak_horizon

It does not prove Collatz.
It does not claim Collatz is solved.
It is measurement only.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

AXIS_CONFIGS = {
    "seed_scale_axis": [
        {"max_odd_seed": 99, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 199, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 499, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 999, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 3999, "odd_steps": 160, "post_peak_horizon": 20},
    ],
    "odd_step_depth_axis": [
        {"max_odd_seed": 1999, "odd_steps": 40, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 80, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 120, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 200, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 240, "post_peak_horizon": 20},
    ],
    "post_peak_horizon_axis": [
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 5},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 10},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 15},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 20},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 25},
        {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 30},
    ],
}


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


def linear_slope(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mx = mean(xs)
    my = mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return num / den


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
            "debt_peak": 0.0,
            "peak_index": None,
            "response_delay": None,
            "has_post_peak_release": False,
            "post_peak_release_count_h": 0,
            "post_peak_strong_release_count_h": 0,
            "post_peak_release_mass_h": 0.0,
            "total_release_count": 0,
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

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_delay": response_delay,
        "has_post_peak_release": has_post_peak_release,
        "post_peak_release_count_h": len(post_peak_releases),
        "post_peak_strong_release_count_h": len(post_peak_strong_releases),
        "post_peak_release_mass_h": sum(abs(s["delta"]) for s in post_peak_releases),
        "total_release_count": len(total_releases),
    }


def run_config(max_odd_seed: int, odd_steps: int, post_peak_horizon: int) -> dict:
    seeds = list(range(1, max_odd_seed + 1, 2))
    records = [measure_seed(seed, odd_steps, post_peak_horizon) for seed in seeds]

    debt_peaks = [r["debt_peak"] for r in records]
    post_peak_masses = [float(r["post_peak_release_mass_h"]) for r in records]
    post_peak_counts = [float(r["post_peak_release_count_h"]) for r in records]
    post_peak_strong_counts = [float(r["post_peak_strong_release_count_h"]) for r in records]
    total_release_counts = [float(r["total_release_count"]) for r in records]

    response_delays = [
        float(r["response_delay"])
        for r in records
        if r["response_delay"] is not None
    ]

    primary = pearson(debt_peaks, post_peak_masses)

    return {
        "config": {
            "max_odd_seed": max_odd_seed,
            "odd_steps": odd_steps,
            "post_peak_horizon": post_peak_horizon,
        },
        "aggregate": {
            "primary_signal": primary,
            "debt_peak_vs_post_peak_release_mass_h_pearson": primary,
            "debt_peak_vs_post_peak_release_count_h_pearson": pearson(debt_peaks, post_peak_counts),
            "debt_peak_vs_post_peak_strong_release_count_h_pearson": pearson(debt_peaks, post_peak_strong_counts),
            "debt_peak_vs_total_release_count_pearson": pearson(debt_peaks, total_release_counts),
            "median_response_delay": safe_median(response_delays),
            "mean_response_delay": safe_mean(response_delays),
            "records": len(records),
            "terminated_within_bound": sum(1 for r in records if r["terminated"]),
        },
    }


def axis_value(axis_name: str, config: dict) -> float:
    if axis_name == "seed_scale_axis":
        return float(config["max_odd_seed"])
    if axis_name == "odd_step_depth_axis":
        return float(config["odd_steps"])
    if axis_name == "post_peak_horizon_axis":
        return float(config["post_peak_horizon"])
    raise ValueError(f"Unknown axis name: {axis_name}")


def summarize_axis(axis_name: str, config_results: list[dict]) -> dict:
    xs = [axis_value(axis_name, r["config"]) for r in config_results]
    log_xs = [math.log10(x) for x in xs]

    ys = [
        r["aggregate"]["primary_signal"]
        for r in config_results
        if r["aggregate"]["primary_signal"] is not None
    ]

    aligned_xs = [
        axis_value(axis_name, r["config"])
        for r in config_results
        if r["aggregate"]["primary_signal"] is not None
    ]

    aligned_log_xs = [math.log10(x) for x in aligned_xs]

    if ys:
        first_signal = ys[0]
        last_signal = ys[-1]
        total_drop = first_signal - last_signal
        relative_drop = total_drop / first_signal if first_signal != 0 else None
        min_signal = min(ys)
        max_signal = max(ys)
        mean_signal = mean(ys)
        zero_crossing_observed = any(y <= 0 for y in ys)
        all_positive = all(y > 0 for y in ys)
    else:
        first_signal = None
        last_signal = None
        total_drop = None
        relative_drop = None
        min_signal = None
        max_signal = None
        mean_signal = None
        zero_crossing_observed = False
        all_positive = False

    median_delays = [
        r["aggregate"]["median_response_delay"]
        for r in config_results
        if r["aggregate"]["median_response_delay"] is not None
    ]

    slope_linear = linear_slope(aligned_xs, ys)
    slope_log = linear_slope(aligned_log_xs, ys)
    corr_log = pearson(aligned_log_xs, ys)

    if corr_log is not None and corr_log < -0.5:
        direction = "decay"
    elif corr_log is not None and corr_log > 0.5:
        direction = "growth"
    else:
        direction = "flat_or_mixed"

    if all_positive and min_signal is not None and min_signal > 0.45:
        floor_status = "positive_floor_preserved"
    elif all_positive:
        floor_status = "positive_but_weak_floor"
    elif zero_crossing_observed:
        floor_status = "zero_crossing_observed"
    else:
        floor_status = "inconclusive"

    return {
        "axis_name": axis_name,
        "axis_values": aligned_xs,
        "axis_log10_values": aligned_log_xs,
        "primary_signal_values": ys,
        "first_signal": first_signal,
        "last_signal": last_signal,
        "total_drop": total_drop,
        "relative_drop": relative_drop,
        "min_signal": min_signal,
        "max_signal": max_signal,
        "mean_signal": mean_signal,
        "slope_per_axis_unit": slope_linear,
        "slope_per_log10_axis": slope_log,
        "axis_vs_signal_correlation_log10": corr_log,
        "direction": direction,
        "floor_status": floor_status,
        "zero_crossing_observed": zero_crossing_observed,
        "all_positive": all_positive,
        "median_response_delay_values": median_delays,
        "median_response_delay_all_at_most_1": all(x <= 1 for x in median_delays) if median_delays else False,
    }


def build() -> dict:
    axis_results = {}

    for axis_name, configs in AXIS_CONFIGS.items():
        config_results = [
            run_config(
                max_odd_seed=c["max_odd_seed"],
                odd_steps=c["odd_steps"],
                post_peak_horizon=c["post_peak_horizon"],
            )
            for c in configs
        ]

        axis_results[axis_name] = {
            "configs": configs,
            "config_results": config_results,
            "axis_summary": summarize_axis(axis_name, config_results),
        }

    summaries = {
        axis_name: data["axis_summary"]
        for axis_name, data in axis_results.items()
    }

    decay_axes = [
        axis_name
        for axis_name, summary in summaries.items()
        if summary["direction"] == "decay"
    ]

    growth_axes = [
        axis_name
        for axis_name, summary in summaries.items()
        if summary["direction"] == "growth"
    ]

    flat_axes = [
        axis_name
        for axis_name, summary in summaries.items()
        if summary["direction"] == "flat_or_mixed"
    ]

    floor_preserved_axes = [
        axis_name
        for axis_name, summary in summaries.items()
        if summary["floor_status"] == "positive_floor_preserved"
    ]

    zero_crossing_axes = [
        axis_name
        for axis_name, summary in summaries.items()
        if summary["zero_crossing_observed"]
    ]

    if zero_crossing_axes:
        bounded_assessment = "zero_crossing_observed_on_some_axis"
    elif decay_axes and len(floor_preserved_axes) == len(summaries):
        bounded_assessment = "axis_decay_with_positive_floor_preserved"
    elif decay_axes:
        bounded_assessment = "axis_decay_detected"
    elif growth_axes and not decay_axes:
        bounded_assessment = "no_decay_growth_or_horizon_accumulation"
    else:
        bounded_assessment = "flat_or_mixed_axis_response"

    return {
        "version": "v5.2",
        "machine": "Residual Decay Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "axis_results": axis_results,
        "axis_summaries": summaries,
        "residual_attribution": {
            "decay_axes": decay_axes,
            "growth_axes": growth_axes,
            "flat_axes": flat_axes,
            "floor_preserved_axes": floor_preserved_axes,
            "zero_crossing_axes": zero_crossing_axes,
        },
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit separates apparent signal decay by changing one measurement axis at a time.",
            "primary_signal": "debt_peak_vs_post_peak_release_mass_h_pearson",
            "native_hypothesis": "The weakening of release-pressure correlation can be attributed to specific measurement axes rather than treated as a single undifferentiated scale effect.",
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

    lines.append("# Residual Decay Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded residual decay audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Residual attribution")
    lines.append("")

    for key, value in summary["residual_attribution"].items():
        lines.append(f"- {key}: `{', '.join(value) if value else 'none'}`")

    lines.append("")
    lines.append("## Axis summaries")
    lines.append("")

    for axis_name, axis_summary in summary["axis_summaries"].items():
        lines.append(f"### {axis_name}")
        lines.append("")
        for key, value in axis_summary.items():
            if isinstance(value, list):
                formatted = ", ".join(fmt(v) for v in value)
                lines.append(f"- {key}: `{formatted}`")
            else:
                lines.append(f"- {key}: `{fmt(value)}`")
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit separates whether signal decay comes from seed scale, odd-step depth, or post-peak horizon.")
    lines.append("")
    lines.append("This prevents treating a mixed parameter effect as a single structural law.")
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

    json_path = RESULTS / "residual_decay_audit_v0.json"
    md_path = RESULTS / "residual_decay_audit_v0.md"
    cert_path = RESULTS / "residual_decay_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.2",
        "artifact": "Residual Decay Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "residual_attribution": summary["residual_attribution"],
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
    print("RESIDUAL ATTRIBUTION:")
    for key, value in summary["residual_attribution"].items():
        print(f"  {key}: {value}")
    print("")
    print("AXIS SUMMARIES:")
    for axis_name, axis_summary in summary["axis_summaries"].items():
        print(f"  {axis_name}:")
        print(f"    direction: {axis_summary['direction']}")
        print(f"    floor_status: {axis_summary['floor_status']}")
        print(f"    primary_signal_values: {axis_summary['primary_signal_values']}")
        print(f"    correlation_log10: {axis_summary['axis_vs_signal_correlation_log10']}")
        print(f"    slope_log10: {axis_summary['slope_per_log10_axis']}")
        print(f"    median_response_delay_values: {axis_summary['median_response_delay_values']}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
