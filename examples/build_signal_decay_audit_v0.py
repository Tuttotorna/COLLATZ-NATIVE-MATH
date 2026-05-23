#!/usr/bin/env python3
"""
Signal Decay Audit V0.

This bounded audit tests whether the distributed release pressure signal
decays toward zero or remains above a positive floor candidate.

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

CONFIGS = [
    {"max_odd_seed": 99, "odd_steps": 80, "post_peak_horizon": 10},
    {"max_odd_seed": 199, "odd_steps": 80, "post_peak_horizon": 10},
    {"max_odd_seed": 499, "odd_steps": 100, "post_peak_horizon": 15},
    {"max_odd_seed": 999, "odd_steps": 120, "post_peak_horizon": 20},
    {"max_odd_seed": 1499, "odd_steps": 140, "post_peak_horizon": 20},
    {"max_odd_seed": 1999, "odd_steps": 160, "post_peak_horizon": 25},
    {"max_odd_seed": 2999, "odd_steps": 180, "post_peak_horizon": 25},
    {"max_odd_seed": 3999, "odd_steps": 200, "post_peak_horizon": 30},
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


def build() -> dict:
    config_results = [
        run_config(
            max_odd_seed=c["max_odd_seed"],
            odd_steps=c["odd_steps"],
            post_peak_horizon=c["post_peak_horizon"],
        )
        for c in CONFIGS
    ]

    scales = [float(r["config"]["max_odd_seed"]) for r in config_results]
    log_scales = [math.log10(x) for x in scales]

    primary_values = [
        r["aggregate"]["primary_signal"]
        for r in config_results
        if r["aggregate"]["primary_signal"] is not None
    ]

    primary_scales = [
        float(r["config"]["max_odd_seed"])
        for r in config_results
        if r["aggregate"]["primary_signal"] is not None
    ]

    primary_log_scales = [math.log10(x) for x in primary_scales]

    early_count = max(1, len(primary_values) // 2)
    early_values = primary_values[:early_count]
    late_values = primary_values[early_count:]

    early_mean = safe_mean(early_values)
    late_mean = safe_mean(late_values)

    if early_mean is not None and early_mean != 0 and late_mean is not None:
        late_to_early_ratio = late_mean / early_mean
    else:
        late_to_early_ratio = None

    slope_per_seed = linear_slope(primary_scales, primary_values)
    slope_per_log10_scale = linear_slope(primary_log_scales, primary_values)
    scale_corr = pearson(primary_log_scales, primary_values)

    first_signal = primary_values[0] if primary_values else None
    last_signal = primary_values[-1] if primary_values else None

    if first_signal is not None and last_signal is not None:
        total_drop = first_signal - last_signal
        relative_drop = total_drop / first_signal if first_signal != 0 else None
    else:
        total_drop = None
        relative_drop = None

    floor_window = primary_values[-3:] if len(primary_values) >= 3 else primary_values
    floor_estimate = safe_mean(floor_window)
    floor_min = min(floor_window) if floor_window else None

    zero_crossing_observed = any(x <= 0 for x in primary_values)
    all_positive = all(x > 0 for x in primary_values) if primary_values else False

    floor_candidate = (
        all_positive
        and floor_estimate is not None
        and floor_min is not None
        and floor_estimate > 0.5
        and floor_min > 0.45
    )

    decay_detected = (
        slope_per_log10_scale is not None
        and slope_per_log10_scale < 0
        and scale_corr is not None
        and scale_corr < -0.5
    )

    if floor_candidate and decay_detected:
        bounded_assessment = "positive_floor_candidate_with_decay"
    elif floor_candidate:
        bounded_assessment = "positive_floor_candidate"
    elif decay_detected and not zero_crossing_observed:
        bounded_assessment = "positive_but_decaying_under_tested_scales"
    elif zero_crossing_observed:
        bounded_assessment = "signal_crossed_zero_under_tested_scales"
    else:
        bounded_assessment = "inconclusive_decay_pattern"

    median_response_delays = [
        r["aggregate"]["median_response_delay"]
        for r in config_results
        if r["aggregate"]["median_response_delay"] is not None
    ]

    decay = {
        "configs_tested": len(config_results),
        "primary_signal_name": "debt_peak_vs_post_peak_release_mass_h_pearson",
        "scales": primary_scales,
        "log10_scales": primary_log_scales,
        "primary_signal_values": primary_values,
        "first_signal": first_signal,
        "last_signal": last_signal,
        "total_drop": total_drop,
        "relative_drop": relative_drop,
        "slope_per_seed": slope_per_seed,
        "slope_per_log10_scale": slope_per_log10_scale,
        "scale_vs_primary_signal_correlation": scale_corr,
        "early_window_mean": early_mean,
        "late_window_mean": late_mean,
        "late_to_early_ratio": late_to_early_ratio,
        "signal_floor_estimate_last3_mean": floor_estimate,
        "signal_floor_min_last3": floor_min,
        "zero_crossing_observed": zero_crossing_observed,
        "all_positive": all_positive,
        "floor_candidate": floor_candidate,
        "decay_detected": decay_detected,
        "median_response_delay_values": median_response_delays,
        "median_response_delay_all_at_most_1": all(x <= 1 for x in median_response_delays) if median_response_delays else False,
    }

    return {
        "version": "v5.1",
        "machine": "Signal Decay Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "configs": CONFIGS,
        "config_results": config_results,
        "decay": decay,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether the primary distributed release pressure signal decays toward zero or preserves a positive bounded floor candidate.",
            "primary_signal": "debt_peak_vs_post_peak_release_mass_h_pearson",
            "native_hypothesis": "Debt peaks continue to produce visible post-peak release pressure under increasing bounded scale.",
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

    lines.append("# Signal Decay Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded decay audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Decay summary")
    lines.append("")

    for key, value in summary["decay"].items():
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
        lines.append(f"- primary_signal: `{fmt(agg['primary_signal'])}`")
        lines.append(f"- median_response_delay: `{fmt(agg['median_response_delay'])}`")
        lines.append(f"- mean_response_delay: `{fmt(agg['mean_response_delay'])}`")
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit checks whether the release-pressure signal is collapsing toward zero or preserving a positive bounded floor candidate.")
    lines.append("")
    lines.append("A positive floor candidate is not a theorem.")
    lines.append("")
    lines.append("It is a bounded reproducibility signal.")
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

    json_path = RESULTS / "signal_decay_audit_v0.json"
    md_path = RESULTS / "signal_decay_audit_v0.md"
    cert_path = RESULTS / "signal_decay_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.1",
        "artifact": "Signal Decay Audit V0",
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
    for value in summary["decay"]["primary_signal_values"]:
        print(f"  {fmt(value)}")
    print("")
    print("DECAY:")
    for key, value in summary["decay"].items():
        print(f"  {key}: {value}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
