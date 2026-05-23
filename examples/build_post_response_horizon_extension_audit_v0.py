#!/usr/bin/env python3
"""
Post-Response Horizon Extension Audit V0.

This bounded audit tests whether post-response new-peak regeneration appears
only when the odd-step observation horizon is extended.

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

ODD_STEP_CONFIGS = [160, 240, 320, 480, 640, 960]
BLOCK_SIZE = 999
MAX_END = 49999


def make_block_ranges(block_size: int = BLOCK_SIZE, max_end: int = MAX_END) -> list[dict]:
    ranges = []
    start = 1

    while start <= max_end:
        end = min(start + block_size - 1, max_end)
        ranges.append(
            {
                "label": f"{start}..{end}",
                "start": start,
                "end": end,
                "midpoint": (start + end) / 2.0,
            }
        )
        start = end + 2

    return ranges


BLOCK_RANGES = make_block_ranges()


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


def odd_seeds(start: int, end: int) -> list[int]:
    first = start if start % 2 == 1 else start + 1
    return list(range(first, end + 1, 2))


def measure_seed(seed: int, odd_steps: int) -> dict:
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
            "response_index": None,
            "has_response": False,
            "debt_after_first_release": None,
            "survival_ratio": None,
            "response_reduced_below_peak": False,
            "post_response_max_debt": None,
            "regeneration_ratio": None,
            "new_peak_after_release": False,
            "time_to_new_peak_if_any": None,
            "any_post_response_regeneration": False,
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
            "debt_peak": debt_peak,
            "peak_index": peak_index,
            "response_delay": None,
            "response_index": None,
            "has_response": False,
            "debt_after_first_release": None,
            "survival_ratio": None,
            "response_reduced_below_peak": False,
            "post_response_max_debt": None,
            "regeneration_ratio": None,
            "new_peak_after_release": False,
            "time_to_new_peak_if_any": None,
            "any_post_response_regeneration": False,
        }

    first_release = later_releases[0]
    response_index = first_release["index"]
    response_delay = response_index - peak_index
    debt_after_first_release = first_release["prefix_debt"]

    if debt_peak > 0:
        survival_ratio = debt_after_first_release / debt_peak
    else:
        survival_ratio = None

    response_reduced_below_peak = debt_after_first_release < debt_peak

    post_response_steps = [s for s in steps if s["index"] > response_index]
    post_response_prefixes = [s["prefix_debt"] for s in post_response_steps]

    if post_response_prefixes:
        post_response_max_debt = max(post_response_prefixes)

        if debt_peak > 0:
            regeneration_ratio = post_response_max_debt / debt_peak
        else:
            regeneration_ratio = None

        new_peak_after_release = post_response_max_debt > debt_peak
        any_post_response_regeneration = post_response_max_debt > debt_after_first_release

        if new_peak_after_release:
            first_new_peak_step = next(
                s for s in post_response_steps
                if s["prefix_debt"] > debt_peak
            )
            time_to_new_peak_if_any = first_new_peak_step["index"] - response_index
        else:
            time_to_new_peak_if_any = None
    else:
        post_response_max_debt = None
        regeneration_ratio = None
        new_peak_after_release = False
        any_post_response_regeneration = False
        time_to_new_peak_if_any = None

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_delay": response_delay,
        "response_index": response_index,
        "has_response": True,
        "debt_after_first_release": debt_after_first_release,
        "survival_ratio": survival_ratio,
        "response_reduced_below_peak": response_reduced_below_peak,
        "post_response_max_debt": post_response_max_debt,
        "regeneration_ratio": regeneration_ratio,
        "new_peak_after_release": new_peak_after_release,
        "time_to_new_peak_if_any": time_to_new_peak_if_any,
        "any_post_response_regeneration": any_post_response_regeneration,
    }


def summarize_records(records: list[dict]) -> dict:
    n = len(records)

    if n == 0:
        raise ValueError("No records to summarize")

    response_records = [r for r in records if r["has_response"]]
    ratio_records = [r for r in response_records if r["survival_ratio"] is not None]
    regen_ratio_records = [r for r in response_records if r["regeneration_ratio"] is not None]
    new_peak_records = [r for r in records if r["new_peak_after_release"]]

    delays = [float(r["response_delay"]) for r in response_records]
    survival_ratios = [float(r["survival_ratio"]) for r in ratio_records]
    regeneration_ratios = [float(r["regeneration_ratio"]) for r in regen_ratio_records]
    times_to_new_peak = [float(r["time_to_new_peak_if_any"]) for r in new_peak_records]

    p_has_response = len(response_records) / n
    no_response_rate = 1.0 - p_has_response
    p_reduced_below_peak = sum(1 for r in records if r["response_reduced_below_peak"]) / n
    p_new_peak_after_release = len(new_peak_records) / n
    p_any_post_response_regeneration = sum(1 for r in records if r["any_post_response_regeneration"]) / n

    return {
        "record_count": n,
        "response_count": len(response_records),
        "no_response_rate": no_response_rate,
        "p_has_response": p_has_response,
        "median_response_delay": safe_median(delays),
        "mean_response_delay": safe_mean(delays),
        "p_reduced_below_peak": p_reduced_below_peak,
        "median_survival_ratio": safe_median(survival_ratios),
        "mean_survival_ratio": safe_mean(survival_ratios),
        "max_survival_ratio": max(survival_ratios) if survival_ratios else None,
        "p_new_peak_after_release": p_new_peak_after_release,
        "p_any_post_response_regeneration": p_any_post_response_regeneration,
        "median_regeneration_ratio": safe_median(regeneration_ratios),
        "mean_regeneration_ratio": safe_mean(regeneration_ratios),
        "max_post_response_regeneration_ratio": max(regeneration_ratios) if regeneration_ratios else None,
        "median_time_to_new_peak_if_any": safe_median(times_to_new_peak),
        "min_time_to_new_peak_if_any": min(times_to_new_peak) if times_to_new_peak else None,
        "max_time_to_new_peak_if_any": max(times_to_new_peak) if times_to_new_peak else None,
    }


def run_block(label: str, start: int, end: int, midpoint: float, odd_steps: int) -> dict:
    seeds = odd_seeds(start, end)
    records = [measure_seed(seed, odd_steps) for seed in seeds]
    aggregate = summarize_records(records)

    return {
        "label": label,
        "start": start,
        "end": end,
        "midpoint": midpoint,
        "odd_seed_count": len(seeds),
        "aggregate": aggregate,
    }


def summarize_horizon(block_results: list[dict], odd_steps: int) -> dict:
    p_new_peak_values = [r["aggregate"]["p_new_peak_after_release"] for r in block_results]
    p_reduced_values = [r["aggregate"]["p_reduced_below_peak"] for r in block_results]
    no_response_rates = [r["aggregate"]["no_response_rate"] for r in block_results]
    median_survival_values = [r["aggregate"]["median_survival_ratio"] for r in block_results]
    max_regen_values = [r["aggregate"]["max_post_response_regeneration_ratio"] for r in block_results]
    p_any_regen_values = [r["aggregate"]["p_any_post_response_regeneration"] for r in block_results]
    median_delay_values = [r["aggregate"]["median_response_delay"] for r in block_results]

    valid_survival = [x for x in median_survival_values if x is not None]
    valid_max_regen = [x for x in max_regen_values if x is not None]

    return {
        "odd_steps": odd_steps,
        "block_count": len(block_results),
        "p_new_peak_after_release_values": p_new_peak_values,
        "p_new_peak_after_release_max": max(p_new_peak_values) if p_new_peak_values else None,
        "p_new_peak_after_release_mean": safe_mean(p_new_peak_values),
        "p_reduced_below_peak_min": min(p_reduced_values) if p_reduced_values else None,
        "p_reduced_below_peak_mean": safe_mean(p_reduced_values),
        "no_response_rate_max": max(no_response_rates) if no_response_rates else None,
        "median_survival_ratio_mean": safe_mean(valid_survival),
        "median_survival_ratio_max": max(valid_survival) if valid_survival else None,
        "max_post_response_regeneration_ratio_max": max(valid_max_regen) if valid_max_regen else None,
        "max_post_response_regeneration_ratio_mean": safe_mean(valid_max_regen),
        "p_any_post_response_regeneration_mean": safe_mean(p_any_regen_values),
        "p_any_post_response_regeneration_max": max(p_any_regen_values) if p_any_regen_values else None,
        "median_delay_all_1": all(x == 1 for x in median_delay_values if x is not None),
    }


def build() -> dict:
    horizon_results = []

    for odd_steps in ODD_STEP_CONFIGS:
        block_results = [
            run_block(
                label=r["label"],
                start=r["start"],
                end=r["end"],
                midpoint=r["midpoint"],
                odd_steps=odd_steps,
            )
            for r in BLOCK_RANGES
        ]

        horizon_summary = summarize_horizon(block_results, odd_steps)

        horizon_results.append(
            {
                "odd_steps": odd_steps,
                "block_results": block_results,
                "horizon_summary": horizon_summary,
            }
        )

    odd_steps_values = [float(x["odd_steps"]) for x in horizon_results]
    p_new_peak_max_values = [
        x["horizon_summary"]["p_new_peak_after_release_max"]
        for x in horizon_results
    ]
    p_reduced_min_values = [
        x["horizon_summary"]["p_reduced_below_peak_min"]
        for x in horizon_results
    ]
    max_regen_values = [
        x["horizon_summary"]["max_post_response_regeneration_ratio_max"]
        for x in horizon_results
    ]

    zero_new_peak_all_horizons = all(x == 0 for x in p_new_peak_max_values)
    reduced_floor_all_horizons = min(p_reduced_min_values) if p_reduced_min_values else None
    max_regen_ratio_all_horizons = max(max_regen_values) if max_regen_values else None

    p_new_peak_slope = linear_slope(odd_steps_values, p_new_peak_max_values)
    p_new_peak_corr = pearson(odd_steps_values, p_new_peak_max_values)

    horizon_summary = {
        "odd_step_configs": ODD_STEP_CONFIGS,
        "max_end": MAX_END,
        "block_size": BLOCK_SIZE,
        "horizon_count": len(horizon_results),
        "p_new_peak_after_release_max_values": p_new_peak_max_values,
        "p_reduced_below_peak_min_values": p_reduced_min_values,
        "max_post_response_regeneration_ratio_max_values": max_regen_values,
        "zero_new_peak_all_horizons": zero_new_peak_all_horizons,
        "reduced_floor_all_horizons": reduced_floor_all_horizons,
        "max_regen_ratio_all_horizons": max_regen_ratio_all_horizons,
        "p_new_peak_slope_by_odd_steps": p_new_peak_slope,
        "p_new_peak_corr_by_odd_steps": p_new_peak_corr,
    }

    if (
        zero_new_peak_all_horizons
        and reduced_floor_all_horizons is not None
        and reduced_floor_all_horizons >= 0.98
    ):
        bounded_assessment = "extended_horizon_no_new_peak_with_strong_reduction"
    elif zero_new_peak_all_horizons:
        bounded_assessment = "extended_horizon_no_new_peak_detected"
    else:
        bounded_assessment = "new_peak_detected_under_extended_horizon"

    return {
        "version": "v5.8",
        "machine": "Post-Response Horizon Extension Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_step_configs": ODD_STEP_CONFIGS,
            "block_size": BLOCK_SIZE,
            "max_end": MAX_END,
        },
        "block_ranges": BLOCK_RANGES,
        "horizon_results": horizon_results,
        "horizon_summary": horizon_summary,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether post-response new-peak regeneration appears under longer odd-step horizons.",
            "primary_regeneration_signal": "p_new_peak_after_release",
            "native_hypothesis": "First post-peak release closes the local debt episode across extended bounded horizons.",
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

    lines.append("# Post-Response Horizon Extension Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded post-response horizon extension audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Horizon summary")
    lines.append("")

    for key, value in summary["horizon_summary"].items():
        if isinstance(value, list):
            formatted = ", ".join(fmt(v) for v in value)
            lines.append(f"- {key}: `{formatted}`")
        else:
            lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Per-horizon summaries")
    lines.append("")

    for item in summary["horizon_results"]:
        hs = item["horizon_summary"]
        lines.append(f"### odd_steps={item['odd_steps']}")
        lines.append("")
        for key, value in hs.items():
            lines.append(f"- {key}: `{fmt(value)}`")
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit tests whether new post-response peaks appear only when the observation horizon is extended.")
    lines.append("")
    lines.append("No new peak inside the tested horizon is bounded evidence only, not a global theorem.")
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

    json_path = RESULTS / "post_response_horizon_extension_audit_v0.json"
    md_path = RESULTS / "post_response_horizon_extension_audit_v0.md"
    cert_path = RESULTS / "post_response_horizon_extension_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.8",
        "artifact": "Post-Response Horizon Extension Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "horizon_summary": summary["horizon_summary"],
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
    print("HORIZON SUMMARY:")
    for key, value in summary["horizon_summary"].items():
        print(f"  {key}: {value}")
    print("")
    print("PER-HORIZON CORE:")
    for item in summary["horizon_results"]:
        hs = item["horizon_summary"]
        print(
            f"  odd_steps={item['odd_steps']} | "
            f"p_new_peak_max={hs['p_new_peak_after_release_max']} | "
            f"p_reduced_min={hs['p_reduced_below_peak_min']} | "
            f"max_regen_ratio={hs['max_post_response_regeneration_ratio_max']} | "
            f"median_delay_all_1={hs['median_delay_all_1']}"
        )
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
