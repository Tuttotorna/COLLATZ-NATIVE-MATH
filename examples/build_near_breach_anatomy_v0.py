#!/usr/bin/env python3
"""
Near-Breach Anatomy V0.

This bounded audit extracts the internal trajectory grammar of the strongest
near-breach candidates.

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
TOP_K = 20
WINDOW_RADIUS = 8

CONTROL_SEEDS = [
    927, 2067, 4095, 8191, 9999,
    12345, 22223, 33333, 44445, 55555,
    66667, 77777, 88889, 99999,
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


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_median(values: list[float]) -> float | None:
    return median(values) if values else None


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


def trajectory(seed: int, odd_steps: int = ODD_STEPS) -> dict:
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

        record = {
            "index": i,
            "n": n,
            "next_n": next_n,
            "a": a,
            "delta": delta,
            "prefix_debt": prefix,
            "is_expansion": delta > 0,
            "is_release": delta < -1,
            "is_strong_release": delta < -2,
        }

        steps.append(record)
        prefixes.append(prefix)
        n = next_n

    if not steps:
        return {
            "seed": seed,
            "terminated": True,
            "final_n": n,
            "odd_steps": 0,
            "steps": [],
            "debt_peak": 0.0,
            "peak_index": None,
            "response_index": None,
            "post_response_max_index": None,
            "response_delay": None,
            "time_to_post_response_max": None,
            "regeneration_ratio": None,
            "gap_to_breach": None,
            "survival_ratio": None,
            "new_peak_after_release": False,
        }

    debt_peak = max(prefixes)
    peak_index = prefixes.index(debt_peak)

    later_steps = [s for s in steps if s["index"] > peak_index]
    later_releases = [s for s in later_steps if s["is_release"]]

    if not later_releases:
        return {
            "seed": seed,
            "terminated": n == 1,
            "final_n": n,
            "odd_steps": len(steps),
            "steps": steps,
            "debt_peak": debt_peak,
            "peak_index": peak_index,
            "response_index": None,
            "post_response_max_index": None,
            "response_delay": None,
            "time_to_post_response_max": None,
            "regeneration_ratio": None,
            "gap_to_breach": None,
            "survival_ratio": None,
            "new_peak_after_release": False,
        }

    first_release = later_releases[0]
    response_index = first_release["index"]
    response_delay = response_index - peak_index
    debt_after_first_release = first_release["prefix_debt"]
    survival_ratio = debt_after_first_release / debt_peak if debt_peak > 0 else None

    post_response_steps = [s for s in steps if s["index"] > response_index]

    if post_response_steps:
        post_response_max_step = max(post_response_steps, key=lambda s: s["prefix_debt"])
        post_response_max_debt = post_response_max_step["prefix_debt"]
        post_response_max_index = post_response_max_step["index"]
        time_to_post_response_max = post_response_max_index - response_index
        regeneration_ratio = post_response_max_debt / debt_peak if debt_peak > 0 else None
        gap_to_breach = 1.0 - regeneration_ratio if regeneration_ratio is not None else None
        new_peak_after_release = regeneration_ratio is not None and regeneration_ratio > 1.0
    else:
        post_response_max_debt = None
        post_response_max_index = None
        time_to_post_response_max = None
        regeneration_ratio = None
        gap_to_breach = None
        new_peak_after_release = False

    return {
        "seed": seed,
        "terminated": n == 1,
        "final_n": n,
        "odd_steps": len(steps),
        "steps": steps,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_index": response_index,
        "post_response_max_debt": post_response_max_debt,
        "post_response_max_index": post_response_max_index,
        "response_delay": response_delay,
        "time_to_post_response_max": time_to_post_response_max,
        "regeneration_ratio": regeneration_ratio,
        "gap_to_breach": gap_to_breach,
        "survival_ratio": survival_ratio,
        "new_peak_after_release": new_peak_after_release,
    }


def slice_window(steps: list[dict], center: int | None, radius: int = WINDOW_RADIUS) -> list[dict]:
    if center is None:
        return []

    start = max(0, center - radius)
    end = min(len(steps), center + radius + 1)

    return steps[start:end]


def summarize_steps(steps: list[dict]) -> dict:
    if not steps:
        return {
            "count": 0,
            "mean_a": None,
            "median_a": None,
            "a1_rate": None,
            "a2_rate": None,
            "a_ge_3_rate": None,
            "positive_delta_rate": None,
            "release_rate": None,
            "strong_release_rate": None,
            "mean_delta": None,
            "sum_delta": None,
            "max_prefix_debt": None,
            "min_prefix_debt": None,
        }

    a_values = [s["a"] for s in steps]
    deltas = [s["delta"] for s in steps]
    prefixes = [s["prefix_debt"] for s in steps]
    n = len(steps)

    return {
        "count": n,
        "mean_a": safe_mean([float(x) for x in a_values]),
        "median_a": safe_median([float(x) for x in a_values]),
        "a1_rate": sum(1 for x in a_values if x == 1) / n,
        "a2_rate": sum(1 for x in a_values if x == 2) / n,
        "a_ge_3_rate": sum(1 for x in a_values if x >= 3) / n,
        "positive_delta_rate": sum(1 for x in deltas if x > 0) / n,
        "release_rate": sum(1 for x in deltas if x < -1) / n,
        "strong_release_rate": sum(1 for x in deltas if x < -2) / n,
        "mean_delta": safe_mean(deltas),
        "sum_delta": sum(deltas),
        "max_prefix_debt": max(prefixes),
        "min_prefix_debt": min(prefixes),
    }


def compress_steps(steps: list[dict]) -> list[dict]:
    return [
        {
            "index": s["index"],
            "n": s["n"],
            "next_n": s["next_n"],
            "a": s["a"],
            "delta": s["delta"],
            "prefix_debt": s["prefix_debt"],
        }
        for s in steps
    ]


def anatomy(seed: int) -> dict:
    t = trajectory(seed)
    steps = t["steps"]

    pre_peak = slice_window(steps, t["peak_index"])
    peak_to_response = [
        s for s in steps
        if t["peak_index"] is not None
        and t["response_index"] is not None
        and t["peak_index"] <= s["index"] <= t["response_index"]
    ]
    response_to_post_max = [
        s for s in steps
        if t["response_index"] is not None
        and t["post_response_max_index"] is not None
        and t["response_index"] <= s["index"] <= t["post_response_max_index"]
    ]

    full_summary = summarize_steps(steps)
    pre_peak_summary = summarize_steps(pre_peak)
    peak_to_response_summary = summarize_steps(peak_to_response)
    response_to_post_max_summary = summarize_steps(response_to_post_max)

    a_sequence = [s["a"] for s in steps]
    delta_sequence = [s["delta"] for s in steps]
    prefix_sequence = [s["prefix_debt"] for s in steps]

    return {
        "seed": seed,
        "terminated": t["terminated"],
        "odd_steps": t["odd_steps"],
        "debt_peak": t["debt_peak"],
        "peak_index": t["peak_index"],
        "response_index": t["response_index"],
        "post_response_max_index": t["post_response_max_index"],
        "response_delay": t["response_delay"],
        "time_to_post_response_max": t["time_to_post_response_max"],
        "regeneration_ratio": t["regeneration_ratio"],
        "gap_to_breach": t["gap_to_breach"],
        "survival_ratio": t["survival_ratio"],
        "new_peak_after_release": t["new_peak_after_release"],
        "full_summary": full_summary,
        "pre_peak_summary": pre_peak_summary,
        "peak_to_response_summary": peak_to_response_summary,
        "response_to_post_max_summary": response_to_post_max_summary,
        "a_sequence": a_sequence,
        "delta_sequence": delta_sequence,
        "prefix_debt_sequence": prefix_sequence,
        "pre_peak_window": compress_steps(pre_peak),
        "peak_to_response_window": compress_steps(peak_to_response),
        "response_to_post_max_window": compress_steps(response_to_post_max),
    }


def discover_near_breach_seeds(max_odd_seed: int = MAX_ODD_SEED, top_k: int = TOP_K) -> list[int]:
    candidates = []

    for seed in range(1, max_odd_seed + 1, 2):
        t = trajectory(seed)

        if t["gap_to_breach"] is None:
            continue

        candidates.append(
            {
                "seed": seed,
                "gap_to_breach": t["gap_to_breach"],
                "regeneration_ratio": t["regeneration_ratio"],
            }
        )

    candidates.sort(key=lambda x: x["gap_to_breach"])

    return [c["seed"] for c in candidates[:top_k]]


def group_summary(items: list[dict]) -> dict:
    if not items:
        return {}

    return {
        "count": len(items),
        "mean_seed": safe_mean([float(x["seed"]) for x in items]),
        "mean_gap_to_breach": safe_mean([x["gap_to_breach"] for x in items if x["gap_to_breach"] is not None]),
        "min_gap_to_breach": min([x["gap_to_breach"] for x in items if x["gap_to_breach"] is not None]),
        "mean_regeneration_ratio": safe_mean([x["regeneration_ratio"] for x in items if x["regeneration_ratio"] is not None]),
        "max_regeneration_ratio": max([x["regeneration_ratio"] for x in items if x["regeneration_ratio"] is not None]),
        "mean_response_delay": safe_mean([float(x["response_delay"]) for x in items if x["response_delay"] is not None]),
        "mean_time_to_post_response_max": safe_mean([float(x["time_to_post_response_max"]) for x in items if x["time_to_post_response_max"] is not None]),
        "mean_survival_ratio": safe_mean([x["survival_ratio"] for x in items if x["survival_ratio"] is not None]),
        "mean_full_a1_rate": safe_mean([x["full_summary"]["a1_rate"] for x in items if x["full_summary"]["a1_rate"] is not None]),
        "mean_full_a_ge_3_rate": safe_mean([x["full_summary"]["a_ge_3_rate"] for x in items if x["full_summary"]["a_ge_3_rate"] is not None]),
        "mean_response_to_post_max_a1_rate": safe_mean([x["response_to_post_max_summary"]["a1_rate"] for x in items if x["response_to_post_max_summary"]["a1_rate"] is not None]),
        "mean_response_to_post_max_a_ge_3_rate": safe_mean([x["response_to_post_max_summary"]["a_ge_3_rate"] for x in items if x["response_to_post_max_summary"]["a_ge_3_rate"] is not None]),
        "mean_response_to_post_max_sum_delta": safe_mean([x["response_to_post_max_summary"]["sum_delta"] for x in items if x["response_to_post_max_summary"]["sum_delta"] is not None]),
    }


def build() -> dict:
    near_breach_seeds = discover_near_breach_seeds()
    near_breach_set = set(near_breach_seeds)

    clean_control_seeds = [
        s for s in CONTROL_SEEDS
        if s % 2 == 1 and s not in near_breach_set and s <= MAX_ODD_SEED
    ]

    near_breach_anatomies = [anatomy(seed) for seed in near_breach_seeds]
    control_anatomies = [anatomy(seed) for seed in clean_control_seeds]

    near_summary = group_summary(near_breach_anatomies)
    control_summary = group_summary(control_anatomies)

    response_delay_histogram = {}
    time_to_post_max_histogram = {}

    for item in near_breach_anatomies:
        rd = str(item["response_delay"])
        tm = str(item["time_to_post_response_max"])
        response_delay_histogram[rd] = response_delay_histogram.get(rd, 0) + 1
        time_to_post_max_histogram[tm] = time_to_post_max_histogram.get(tm, 0) + 1

    first_a_sequences = [
        item["response_to_post_max_window"][0:12]
        for item in near_breach_anatomies[:10]
    ]

    comparison = {
        "near_breach_count": len(near_breach_anatomies),
        "control_count": len(control_anatomies),
        "near_breach_response_delay_histogram": response_delay_histogram,
        "near_breach_time_to_post_max_histogram": time_to_post_max_histogram,
        "near_breach_mean_gap": near_summary.get("mean_gap_to_breach"),
        "control_mean_gap": control_summary.get("mean_gap_to_breach"),
        "near_breach_mean_regeneration_ratio": near_summary.get("mean_regeneration_ratio"),
        "control_mean_regeneration_ratio": control_summary.get("mean_regeneration_ratio"),
        "near_breach_mean_response_to_post_max_a1_rate": near_summary.get("mean_response_to_post_max_a1_rate"),
        "control_mean_response_to_post_max_a1_rate": control_summary.get("mean_response_to_post_max_a1_rate"),
        "near_breach_mean_response_to_post_max_a_ge_3_rate": near_summary.get("mean_response_to_post_max_a_ge_3_rate"),
        "control_mean_response_to_post_max_a_ge_3_rate": control_summary.get("mean_response_to_post_max_a_ge_3_rate"),
        "near_breach_mean_response_to_post_max_sum_delta": near_summary.get("mean_response_to_post_max_sum_delta"),
        "control_mean_response_to_post_max_sum_delta": control_summary.get("mean_response_to_post_max_sum_delta"),
    }

    if (
        comparison["near_breach_mean_response_to_post_max_a1_rate"] is not None
        and comparison["control_mean_response_to_post_max_a1_rate"] is not None
        and comparison["near_breach_mean_response_to_post_max_a1_rate"]
        > comparison["control_mean_response_to_post_max_a1_rate"]
    ):
        bounded_assessment = "near_breach_expansion_rich_regeneration_grammar"
    else:
        bounded_assessment = "near_breach_anatomy_measured"

    return {
        "version": "v6.0",
        "machine": "Near-Breach Anatomy V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "max_odd_seed": MAX_ODD_SEED,
            "top_k": TOP_K,
            "window_radius": WINDOW_RADIUS,
            "control_seeds": clean_control_seeds,
        },
        "near_breach_seeds": near_breach_seeds,
        "near_breach_anatomies": near_breach_anatomies,
        "control_anatomies": control_anatomies,
        "near_breach_summary": near_summary,
        "control_summary": control_summary,
        "comparison": comparison,
        "first_response_to_post_max_windows_top10": first_a_sequences,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit extracts the internal sequence grammar of strongest near-breach trajectories.",
            "primary_anatomy_signal": "response_to_post_max_window",
            "native_hypothesis": "Near-breach trajectories share a repeated regeneration grammar between first response and post-response maximum.",
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

    lines.append("# Near-Breach Anatomy V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded near-breach anatomy audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Near-breach seeds")
    lines.append("")
    lines.append("`" + ", ".join(str(x) for x in summary["near_breach_seeds"]) + "`")
    lines.append("")
    lines.append("## Comparison")
    lines.append("")

    for key, value in summary["comparison"].items():
        lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Top near-breach anatomy")
    lines.append("")

    for item in summary["near_breach_anatomies"][:10]:
        lines.append(f"### seed `{item['seed']}`")
        lines.append("")
        lines.append(f"- regeneration_ratio: `{fmt(item['regeneration_ratio'])}`")
        lines.append(f"- gap_to_breach: `{fmt(item['gap_to_breach'])}`")
        lines.append(f"- debt_peak: `{fmt(item['debt_peak'])}`")
        lines.append(f"- peak_index: `{fmt(item['peak_index'])}`")
        lines.append(f"- response_index: `{fmt(item['response_index'])}`")
        lines.append(f"- post_response_max_index: `{fmt(item['post_response_max_index'])}`")
        lines.append(f"- response_delay: `{fmt(item['response_delay'])}`")
        lines.append(f"- time_to_post_response_max: `{fmt(item['time_to_post_response_max'])}`")
        lines.append(f"- survival_ratio: `{fmt(item['survival_ratio'])}`")
        lines.append("")
        lines.append("response_to_post_max a-sequence:")
        lines.append("")
        a_seq = [str(s["a"]) for s in item["response_to_post_max_window"]]
        lines.append("`" + ", ".join(a_seq) + "`")
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit shifts from magnitude measurement to sequence anatomy.")
    lines.append("")
    lines.append("The critical question is whether near-breach cases share a repeatable grammar between response and post-response maximum.")
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

    json_path = RESULTS / "near_breach_anatomy_v0.json"
    md_path = RESULTS / "near_breach_anatomy_v0.md"
    cert_path = RESULTS / "near_breach_anatomy_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v6.0",
        "artifact": "Near-Breach Anatomy V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "comparison": summary["comparison"],
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
    print("NEAR-BREACH SEEDS:")
    print(f"  {summary['near_breach_seeds']}")
    print("")
    print("COMPARISON:")
    for key, value in summary["comparison"].items():
        print(f"  {key}: {value}")
    print("")
    print("TOP 10 RESPONSE->POST-MAX A-SEQUENCES:")
    for item in summary["near_breach_anatomies"][:10]:
        a_seq = [s["a"] for s in item["response_to_post_max_window"]]
        print(
            f"  seed={item['seed']} | "
            f"gap={item['gap_to_breach']} | "
            f"ratio={item['regeneration_ratio']} | "
            f"delay={item['response_delay']} | "
            f"time_to_max={item['time_to_post_response_max']} | "
            f"a_seq={a_seq}"
        )
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
