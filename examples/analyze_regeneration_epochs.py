#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "regeneration_epochs_sample.jsonl"
SUMMARY_PATH = ROOT / "results" / "regeneration_epochs_summary.json"

SAMPLES = [
    1,
    3,
    7,
    9,
    27,
    31,
    63,
    127,
    255,
    1023,
    2047,
    2729,
    4255,
    6171,
    9663,
    77031,
]

def v2(n: int) -> int:
    if n == 0:
        raise ValueError("v2(0) is undefined here.")
    c = 0
    n = abs(n)
    while n % 2 == 0:
        c += 1
        n //= 2
    return c

def next_odd_block(n: int):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be positive odd.")
    value = 3 * n + 1
    a = v2(value)
    m = value // (2 ** a)
    return a, m

def odd_start(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive.")
    while n % 2 == 0:
        n //= 2
    return n

def trace_blocks(n0: int, max_blocks: int = 10000):
    n = odd_start(n0)
    rows = []
    total_debt = 0

    for block in range(max_blocks):
        s = v2(n + 1)
        a, m = next_odd_block(n)
        s_next = v2(m + 1)
        total_debt += a

        regenerated_shadow = max(0, s_next - s)
        compression_cost = max(1, a - 1)
        cheapness_ratio = (
            regenerated_shadow / compression_cost
            if regenerated_shadow > 0
            else 0.0
        )
        future_escape_capacity = max(0, s_next - 1)

        rows.append({
            "block": block,
            "n": n,
            "s": s,
            "a": a,
            "next_odd": m,
            "s_next": s_next,
            "shadow_delta": s_next - s,
            "is_escape_block": a == 1,
            "is_compression_block": a >= 2,
            "is_regeneration": s_next > s,
            "regenerated_shadow": regenerated_shadow,
            "compression_cost": compression_cost,
            "cheapness_ratio": cheapness_ratio,
            "future_escape_capacity": future_escape_capacity,
            "cumulative_debt": total_debt,
            "average_debt": total_debt / (block + 1),
            "escape_threshold_log2_3": math.log2(3),
            "average_debt_above_threshold": (total_debt / (block + 1)) > math.log2(3),
        })

        n = m
        if n == 1:
            break

    return rows

def summarize(n0: int, rows):
    if not rows:
        return {
            "n0": n0,
            "odd_start": odd_start(n0),
            "odd_blocks": 0,
            "reaches_1": False,
        }

    regenerations = [r for r in rows if r["is_regeneration"]]
    cheap_regens = [r for r in regenerations if r["cheapness_ratio"] >= 1.7095]
    debt_word = [r["a"] for r in rows]
    shadow_word = [r["s"] for r in rows]

    return {
        "n0": n0,
        "odd_start": rows[0]["n"],
        "odd_blocks": len(rows),
        "reaches_1": rows[-1]["next_odd"] == 1,
        "total_debt": sum(debt_word),
        "average_debt": sum(debt_word) / len(debt_word),
        "escape_threshold_log2_3": math.log2(3),
        "average_debt_above_threshold": (sum(debt_word) / len(debt_word)) > math.log2(3),
        "max_n": max(max(r["n"], r["next_odd"]) for r in rows),
        "max_shadow": max(max(r["s"], r["s_next"]) for r in rows),
        "escape_blocks_a_eq_1": sum(1 for a in debt_word if a == 1),
        "compression_blocks_a_ge_2": sum(1 for a in debt_word if a >= 2),
        "regeneration_events": len(regenerations),
        "cheap_regeneration_events_q_ge_1_7095": len(cheap_regens),
        "max_cheapness_ratio": max([r["cheapness_ratio"] for r in regenerations], default=0.0),
        "max_regenerated_shadow": max([r["regenerated_shadow"] for r in regenerations], default=0),
        "debt_word_prefix": debt_word[:80],
        "shadow_word_prefix": shadow_word[:80],
        "top_regeneration_events": sorted(
            [
                {
                    "block": r["block"],
                    "n": r["n"],
                    "a": r["a"],
                    "s": r["s"],
                    "next_odd": r["next_odd"],
                    "s_next": r["s_next"],
                    "regenerated_shadow": r["regenerated_shadow"],
                    "compression_cost": r["compression_cost"],
                    "cheapness_ratio": r["cheapness_ratio"],
                    "future_escape_capacity": r["future_escape_capacity"],
                }
                for r in regenerations
            ],
            key=lambda x: x["cheapness_ratio"],
            reverse=True,
        )[:10],
    }

def main():
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    summaries = []
    epoch_rows = []

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v0.2")
    print("=" * 80)
    print("Analyzing regeneration epochs and cheapness ratios.")
    print("=" * 80)

    for n0 in SAMPLES:
        rows = trace_blocks(n0)
        summary = summarize(n0, rows)
        summaries.append(summary)

        for row in rows:
            enriched = dict(row)
            enriched["n0"] = n0
            enriched["odd_start"] = summary["odd_start"]
            epoch_rows.append(enriched)

        print()
        print(f"n0: {n0}")
        print(f"odd_blocks: {summary['odd_blocks']}")
        print(f"reaches_1: {str(summary['reaches_1']).lower()}")
        print(f"average_debt: {summary['average_debt']:.6f}")
        print(f"log2(3): {summary['escape_threshold_log2_3']:.6f}")
        print(f"average_debt_above_threshold: {str(summary['average_debt_above_threshold']).lower()}")
        print(f"max_shadow: {summary['max_shadow']}")
        print(f"regeneration_events: {summary['regeneration_events']}")
        print(f"cheap_regeneration_events_q_ge_1_7095: {summary['cheap_regeneration_events_q_ge_1_7095']}")
        print(f"max_cheapness_ratio: {summary['max_cheapness_ratio']:.6f}")
        print(f"max_regenerated_shadow: {summary['max_regenerated_shadow']}")

        if summary["top_regeneration_events"]:
            top = summary["top_regeneration_events"][0]
            print(
                "top_regeneration: "
                f"block={top['block']} "
                f"n={top['n']} "
                f"a={top['a']} "
                f"s={top['s']} "
                f"next={top['next_odd']} "
                f"s_next={top['s_next']} "
                f"regen={top['regenerated_shadow']} "
                f"cost={top['compression_cost']} "
                f"Q={top['cheapness_ratio']:.6f}"
            )

    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in epoch_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    global_summary = {
        "version": "v0.2",
        "sample_count": len(SAMPLES),
        "escape_threshold_log2_3": math.log2(3),
        "cheapness_warning_threshold": 1.7095,
        "max_average_debt_case": max(summaries, key=lambda x: x["average_debt"]),
        "min_average_debt_case": min(summaries, key=lambda x: x["average_debt"]),
        "max_shadow_case": max(summaries, key=lambda x: x["max_shadow"]),
        "max_cheapness_case": max(summaries, key=lambda x: x["max_cheapness_ratio"]),
        "max_regeneration_events_case": max(summaries, key=lambda x: x["regeneration_events"]),
        "all_reach_1_in_sample": all(s["reaches_1"] for s in summaries),
        "all_average_debt_above_threshold_in_sample": all(s["average_debt_above_threshold"] for s in summaries),
    }

    SUMMARY_PATH.write_text(
        json.dumps(global_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print(f"Wrote epoch rows to: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
