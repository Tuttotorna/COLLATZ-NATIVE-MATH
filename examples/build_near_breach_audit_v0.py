#!/usr/bin/env python3
"""
Near-Breach Audit V0.

This bounded audit finds trajectories that come closest to regenerating
a new post-response debt peak.

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

ODD_STEPS = 960
MAX_ODD_SEED = 99999
TOP_K = 50


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


def measure_seed(seed: int, odd_steps: int = ODD_STEPS) -> dict:
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
            "has_response": False,
            "has_post_response_window": False,
            "debt_peak": 0.0,
            "peak_index": None,
            "response_index": None,
            "response_delay": None,
            "debt_after_first_release": None,
            "survival_ratio": None,
            "post_response_max_debt": None,
            "post_response_max_index": None,
            "time_to_post_response_max": None,
            "regeneration_ratio": None,
            "gap_to_breach": None,
            "new_peak_after_release": False,
        }

    debt_peak = max(prefixes)
    peak_index = prefixes.index(debt_peak)

    later_steps = [s for s in steps if s["index"] > peak_index]
    later_releases = [s for s in later_steps if s["is_release"]]

    if not later_releases:
        return {
            "seed": seed,
            "odd_steps": len(steps),
            "terminated": n == 1,
            "has_response": False,
            "has_post_response_window": False,
            "debt_peak": debt_peak,
            "peak_index": peak_index,
            "response_index": None,
            "response_delay": None,
            "debt_after_first_release": None,
            "survival_ratio": None,
            "post_response_max_debt": None,
            "post_response_max_index": None,
            "time_to_post_response_max": None,
            "regeneration_ratio": None,
            "gap_to_breach": None,
            "new_peak_after_release": False,
        }

    first_release = later_releases[0]
    response_index = first_release["index"]
    response_delay = response_index - peak_index
    debt_after_first_release = first_release["prefix_debt"]

    survival_ratio = debt_after_first_release / debt_peak if debt_peak > 0 else None

    post_response_steps = [s for s in steps if s["index"] > response_index]

    if not post_response_steps:
        return {
            "seed": seed,
            "odd_steps": len(steps),
            "terminated": n == 1,
            "has_response": True,
            "has_post_response_window": False,
            "debt_peak": debt_peak,
            "peak_index": peak_index,
            "response_index": response_index,
            "response_delay": response_delay,
            "debt_after_first_release": debt_after_first_release,
            "survival_ratio": survival_ratio,
            "post_response_max_debt": None,
            "post_response_max_index": None,
            "time_to_post_response_max": None,
            "regeneration_ratio": None,
            "gap_to_breach": None,
            "new_peak_after_release": False,
        }

    post_response_max_step = max(post_response_steps, key=lambda s: s["prefix_debt"])
    post_response_max_debt = post_response_max_step["prefix_debt"]
    post_response_max_index = post_response_max_step["index"]
    time_to_post_response_max = post_response_max_index - response_index

    regeneration_ratio = post_response_max_debt / debt_peak if debt_peak > 0 else None
    gap_to_breach = 1.0 - regeneration_ratio if regeneration_ratio is not None else None
    new_peak_after_release = regeneration_ratio is not None and regeneration_ratio > 1.0

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "has_response": True,
        "has_post_response_window": True,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_index": response_index,
        "response_delay": response_delay,
        "debt_after_first_release": debt_after_first_release,
        "survival_ratio": survival_ratio,
        "post_response_max_debt": post_response_max_debt,
        "post_response_max_index": post_response_max_index,
        "time_to_post_response_max": time_to_post_response_max,
        "regeneration_ratio": regeneration_ratio,
        "gap_to_breach": gap_to_breach,
        "new_peak_after_release": new_peak_after_release,
    }


def classify_seed_band(seed: int) -> str:
    if seed <= 999:
        return "000001..000999"
    start = ((seed - 1) // 10000) * 10000 + 1
    end = start + 9998
    return f"{start:06d}..{end:06d}"


def build() -> dict:
    records = [measure_seed(seed) for seed in range(1, MAX_ODD_SEED + 1, 2)]

    analyzable = [
        r for r in records
        if r["regeneration_ratio"] is not None
        and r["gap_to_breach"] is not None
    ]

    breaches = [r for r in analyzable if r["new_peak_after_release"]]
    near_breaches = sorted(analyzable, key=lambda r: r["gap_to_breach"])[:TOP_K]

    ratios = [float(r["regeneration_ratio"]) for r in analyzable]
    gaps = [float(r["gap_to_breach"]) for r in analyzable]
    seeds = [float(r["seed"]) for r in analyzable]
    log_seeds = [math.log10(float(r["seed"])) for r in analyzable if r["seed"] > 0]
    gaps_for_log = [float(r["gap_to_breach"]) for r in analyzable if r["seed"] > 0]
    ratios_for_log = [float(r["regeneration_ratio"]) for r in analyzable if r["seed"] > 0]

    near_breach_gap_min = min(gaps) if gaps else None
    near_breach_ratio_max = max(ratios) if ratios else None

    gap_vs_log_seed_corr = pearson(log_seeds, gaps_for_log)
    gap_vs_log_seed_slope = linear_slope(log_seeds, gaps_for_log)
    ratio_vs_log_seed_corr = pearson(log_seeds, ratios_for_log)
    ratio_vs_log_seed_slope = linear_slope(log_seeds, ratios_for_log)

    band_counts = {}
    band_best = {}

    for r in analyzable:
        band = classify_seed_band(r["seed"])
        band_counts[band] = band_counts.get(band, 0) + 1

        if band not in band_best or r["gap_to_breach"] < band_best[band]["gap_to_breach"]:
            band_best[band] = {
                "seed": r["seed"],
                "gap_to_breach": r["gap_to_breach"],
                "regeneration_ratio": r["regeneration_ratio"],
                "debt_peak": r["debt_peak"],
                "response_delay": r["response_delay"],
                "survival_ratio": r["survival_ratio"],
                "time_to_post_response_max": r["time_to_post_response_max"],
            }

    near_breach_seeds = [r["seed"] for r in near_breaches]
    near_breach_bands = [classify_seed_band(seed) for seed in near_breach_seeds]

    near_breach_band_histogram = {}
    for band in near_breach_bands:
        near_breach_band_histogram[band] = near_breach_band_histogram.get(band, 0) + 1

    last_half_threshold = MAX_ODD_SEED // 2
    last_half_records = [r for r in analyzable if r["seed"] > last_half_threshold]
    first_half_records = [r for r in analyzable if r["seed"] <= last_half_threshold]

    first_half_best_gap = min([r["gap_to_breach"] for r in first_half_records]) if first_half_records else None
    last_half_best_gap = min([r["gap_to_breach"] for r in last_half_records]) if last_half_records else None

    top10 = near_breaches[:10]
    top10_mean_seed = safe_mean([float(r["seed"]) for r in top10])
    top10_min_gap = min([r["gap_to_breach"] for r in top10]) if top10 else None
    top10_max_ratio = max([r["regeneration_ratio"] for r in top10]) if top10 else None

    summary = {
        "records_measured": len(records),
        "analyzable_records": len(analyzable),
        "breach_count": len(breaches),
        "breach_rate": len(breaches) / len(analyzable) if analyzable else None,
        "max_regeneration_ratio": near_breach_ratio_max,
        "min_gap_to_breach": near_breach_gap_min,
        "mean_gap_to_breach": safe_mean(gaps),
        "median_gap_to_breach": safe_median(gaps),
        "mean_regeneration_ratio": safe_mean(ratios),
        "median_regeneration_ratio": safe_median(ratios),
        "gap_vs_log_seed_correlation": gap_vs_log_seed_corr,
        "gap_vs_log_seed_slope": gap_vs_log_seed_slope,
        "regeneration_ratio_vs_log_seed_correlation": ratio_vs_log_seed_corr,
        "regeneration_ratio_vs_log_seed_slope": ratio_vs_log_seed_slope,
        "first_half_best_gap": first_half_best_gap,
        "last_half_best_gap": last_half_best_gap,
        "top10_mean_seed": top10_mean_seed,
        "top10_min_gap": top10_min_gap,
        "top10_max_regeneration_ratio": top10_max_ratio,
        "near_breach_band_histogram": near_breach_band_histogram,
        "band_best_candidates": band_best,
    }

    if breaches:
        bounded_assessment = "breach_detected"
    elif near_breach_gap_min is not None and near_breach_gap_min < 0.01:
        bounded_assessment = "near_breach_below_one_percent_gap"
    elif near_breach_gap_min is not None and near_breach_gap_min < 0.05:
        bounded_assessment = "near_breach_below_five_percent_gap"
    else:
        bounded_assessment = "no_close_breach_detected"

    return {
        "version": "v5.9",
        "machine": "Near-Breach Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "max_odd_seed": MAX_ODD_SEED,
            "top_k": TOP_K,
        },
        "summary": summary,
        "near_breach_candidates": near_breaches,
        "breach_candidates": breaches[:TOP_K],
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit identifies trajectories closest to post-response new-peak breach.",
            "primary_breach_signal": "gap_to_breach = 1 - regeneration_ratio",
            "native_hypothesis": "Near-breach candidates expose the hardest local cases for the debt-response grammar.",
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

    lines.append("# Near-Breach Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded near-breach audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    for key, value in summary["summary"].items():
        if isinstance(value, dict):
            lines.append(f"- {key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  - {sub_key}: `{sub_value}`")
        else:
            lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Top near-breach candidates")
    lines.append("")

    for item in summary["near_breach_candidates"][:20]:
        lines.append(
            f"- seed `{item['seed']}`: "
            f"regeneration_ratio=`{fmt(item['regeneration_ratio'])}`, "
            f"gap_to_breach=`{fmt(item['gap_to_breach'])}`, "
            f"debt_peak=`{fmt(item['debt_peak'])}`, "
            f"response_delay=`{fmt(item['response_delay'])}`, "
            f"survival_ratio=`{fmt(item['survival_ratio'])}`, "
            f"time_to_post_response_max=`{fmt(item['time_to_post_response_max'])}`"
        )

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit does not search for average behavior.")
    lines.append("")
    lines.append("It searches for the hardest bounded cases: trajectories closest to regenerating a new post-response peak.")
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

    json_path = RESULTS / "near_breach_audit_v0.json"
    md_path = RESULTS / "near_breach_audit_v0.md"
    cert_path = RESULTS / "near_breach_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.9",
        "artifact": "Near-Breach Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "summary": summary["summary"],
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
    print("NEAR-BREACH SUMMARY:")
    keys = [
        "records_measured",
        "analyzable_records",
        "breach_count",
        "max_regeneration_ratio",
        "min_gap_to_breach",
        "mean_gap_to_breach",
        "median_gap_to_breach",
        "gap_vs_log_seed_correlation",
        "gap_vs_log_seed_slope",
        "regeneration_ratio_vs_log_seed_correlation",
        "regeneration_ratio_vs_log_seed_slope",
        "first_half_best_gap",
        "last_half_best_gap",
        "top10_mean_seed",
    ]
    for key in keys:
        print(f"  {key}: {summary['summary'][key]}")
    print("")
    print("TOP 10 NEAR-BREACH CANDIDATES:")
    for item in summary["near_breach_candidates"][:10]:
        print(
            "  "
            f"seed={item['seed']} | "
            f"ratio={item['regeneration_ratio']} | "
            f"gap={item['gap_to_breach']} | "
            f"debt_peak={item['debt_peak']} | "
            f"response_delay={item['response_delay']} | "
            f"survival_ratio={item['survival_ratio']} | "
            f"time_to_post_response_max={item['time_to_post_response_max']}"
        )
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
