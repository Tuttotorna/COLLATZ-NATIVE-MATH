#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "cheap_regeneration_chains.jsonl"
SUMMARY_PATH = ROOT / "results" / "cheap_regeneration_chain_summary.json"

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
    837799,
]

CHEAPNESS_THRESHOLD = 1 / (math.log2(3) - 1)

def v2(n: int) -> int:
    if n == 0:
        raise ValueError("v2(0) is undefined here.")
    c = 0
    n = abs(n)
    while n % 2 == 0:
        c += 1
        n //= 2
    return c

def odd_start(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive.")
    while n % 2 == 0:
        n //= 2
    return n

def next_odd_block(n: int):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be positive odd.")
    value = 3 * n + 1
    a = v2(value)
    m = value // (2 ** a)
    return a, m

def trace_blocks(n0: int, max_blocks: int = 100000):
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
        cheapness_ratio = regenerated_shadow / compression_cost if regenerated_shadow > 0 else 0.0
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
            "is_locally_cheap_regeneration": cheapness_ratio >= CHEAPNESS_THRESHOLD,
            "cumulative_debt": total_debt,
            "average_debt": total_debt / (block + 1),
            "escape_threshold_log2_3": math.log2(3),
            "average_debt_above_threshold": (total_debt / (block + 1)) > math.log2(3),
        })

        n = m
        if n == 1:
            break

    return rows

def regeneration_indices(rows):
    return [i for i, row in enumerate(rows) if row["is_regeneration"]]

def segment_between(rows, start_idx, end_idx):
    segment = rows[start_idx:end_idx + 1]
    if not segment:
        raise ValueError("empty segment")

    debt = sum(row["a"] for row in segment)
    blocks = len(segment)
    avg_debt = debt / blocks
    max_n = max(max(row["n"], row["next_odd"]) for row in segment)

    return {
        "segment_start_block": segment[0]["block"],
        "segment_end_block": segment[-1]["block"],
        "segment_blocks": blocks,
        "segment_debt": debt,
        "segment_average_debt": avg_debt,
        "segment_average_debt_above_threshold": avg_debt > math.log2(3),
        "segment_average_debt_at_or_below_threshold": avg_debt <= math.log2(3),
        "segment_max_n": max_n,
        "segment_escape_blocks": sum(1 for row in segment if row["a"] == 1),
        "segment_compression_blocks": sum(1 for row in segment if row["a"] >= 2),
    }

def analyze_chains_for_start(n0: int):
    rows = trace_blocks(n0)
    regen = regeneration_indices(rows)
    chain_rows = []

    if not regen:
        return rows, chain_rows

    for j, idx in enumerate(regen):
        event = rows[idx]
        next_idx = regen[j + 1] if j + 1 < len(regen) else len(rows) - 1
        segment = segment_between(rows, idx, next_idx)

        is_locally_cheap = event["cheapness_ratio"] >= CHEAPNESS_THRESHOLD
        reaches_next_regen = j + 1 < len(regen)
        chain_compatible = (
            is_locally_cheap
            and reaches_next_regen
            and segment["segment_average_debt_at_or_below_threshold"]
        )

        breaks_by_debt = (
            is_locally_cheap
            and segment["segment_average_debt_above_threshold"]
        )

        chain_rows.append({
            "n0": n0,
            "odd_start": odd_start(n0),
            "event_index": j,
            "event_block": idx,
            "event_n": event["n"],
            "event_a": event["a"],
            "event_s": event["s"],
            "event_next_odd": event["next_odd"],
            "event_s_next": event["s_next"],
            "regenerated_shadow": event["regenerated_shadow"],
            "compression_cost": event["compression_cost"],
            "cheapness_ratio": event["cheapness_ratio"],
            "cheapness_threshold": CHEAPNESS_THRESHOLD,
            "is_locally_cheap": is_locally_cheap,
            "reaches_next_regeneration": reaches_next_regen,
            "chain_compatible": chain_compatible,
            "breaks_by_debt": breaks_by_debt,
            **segment,
        })

    return rows, chain_rows

def summarize_start(n0: int, rows, chain_rows):
    debt_word = [row["a"] for row in rows]
    locally_cheap = [row for row in chain_rows if row["is_locally_cheap"]]
    chain_compatible = [row for row in chain_rows if row["chain_compatible"]]
    debt_breaks = [row for row in chain_rows if row["breaks_by_debt"]]

    return {
        "n0": n0,
        "odd_start": odd_start(n0),
        "odd_blocks": len(rows),
        "reaches_1": rows[-1]["next_odd"] == 1 if rows else False,
        "total_debt": sum(debt_word),
        "average_debt": sum(debt_word) / len(debt_word) if debt_word else None,
        "escape_threshold_log2_3": math.log2(3),
        "average_debt_above_threshold": (sum(debt_word) / len(debt_word)) > math.log2(3) if debt_word else None,
        "max_n": max(max(row["n"], row["next_odd"]) for row in rows) if rows else None,
        "max_shadow": max(max(row["s"], row["s_next"]) for row in rows) if rows else None,
        "regeneration_events": len(chain_rows),
        "locally_cheap_regeneration_events": len(locally_cheap),
        "chain_compatible_events": len(chain_compatible),
        "debt_break_events": len(debt_breaks),
        "max_cheapness_ratio": max([row["cheapness_ratio"] for row in chain_rows], default=0.0),
        "max_segment_average_debt": max([row["segment_average_debt"] for row in chain_rows], default=0.0),
        "min_segment_average_debt": min([row["segment_average_debt"] for row in chain_rows], default=0.0),
        "top_chain_compatible_events": sorted(
            chain_compatible,
            key=lambda x: x["cheapness_ratio"],
            reverse=True,
        )[:5],
        "top_locally_cheap_events": sorted(
            locally_cheap,
            key=lambda x: x["cheapness_ratio"],
            reverse=True,
        )[:5],
    }

def main():
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_chain_rows = []
    summaries = []

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v0.3")
    print("=" * 80)
    print("Analyzing cheap regeneration chains.")
    print("=" * 80)
    print(f"cheapness threshold: {CHEAPNESS_THRESHOLD:.6f}")
    print(f"escape threshold log2(3): {math.log2(3):.6f}")
    print("=" * 80)

    for n0 in SAMPLES:
        rows, chain_rows = analyze_chains_for_start(n0)
        summary = summarize_start(n0, rows, chain_rows)
        summaries.append(summary)
        all_chain_rows.extend(chain_rows)

        print()
        print(f"n0: {n0}")
        print(f"odd_blocks: {summary['odd_blocks']}")
        print(f"reaches_1: {str(summary['reaches_1']).lower()}")
        print(f"average_debt: {summary['average_debt']:.6f}")
        print(f"average_debt_above_threshold: {str(summary['average_debt_above_threshold']).lower()}")
        print(f"regeneration_events: {summary['regeneration_events']}")
        print(f"locally_cheap_events: {summary['locally_cheap_regeneration_events']}")
        print(f"chain_compatible_events: {summary['chain_compatible_events']}")
        print(f"debt_break_events: {summary['debt_break_events']}")
        print(f"max_cheapness_ratio: {summary['max_cheapness_ratio']:.6f}")

        if summary["top_locally_cheap_events"]:
            top = summary["top_locally_cheap_events"][0]
            print(
                "top_local_cheap: "
                f"block={top['event_block']} "
                f"n={top['event_n']} "
                f"a={top['event_a']} "
                f"s={top['event_s']} "
                f"next={top['event_next_odd']} "
                f"s_next={top['event_s_next']} "
                f"regen={top['regenerated_shadow']} "
                f"cost={top['compression_cost']} "
                f"Q={top['cheapness_ratio']:.6f} "
                f"seg_avg={top['segment_average_debt']:.6f}"
            )

        if summary["top_chain_compatible_events"]:
            top = summary["top_chain_compatible_events"][0]
            print(
                "top_chain_compatible: "
                f"block={top['event_block']} "
                f"Q={top['cheapness_ratio']:.6f} "
                f"seg_avg={top['segment_average_debt']:.6f}"
            )

    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in all_chain_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    all_locally_cheap = [row for row in all_chain_rows if row["is_locally_cheap"]]
    all_chain_compatible = [row for row in all_chain_rows if row["chain_compatible"]]
    all_debt_breaks = [row for row in all_chain_rows if row["breaks_by_debt"]]

    global_summary = {
        "version": "v0.3",
        "sample_count": len(SAMPLES),
        "escape_threshold_log2_3": math.log2(3),
        "cheapness_threshold": CHEAPNESS_THRESHOLD,
        "total_regeneration_events": len(all_chain_rows),
        "total_locally_cheap_events": len(all_locally_cheap),
        "total_chain_compatible_events": len(all_chain_compatible),
        "total_debt_break_events": len(all_debt_breaks),
        "all_reach_1_in_sample": all(s["reaches_1"] for s in summaries),
        "all_average_debt_above_threshold_in_sample": all(s["average_debt_above_threshold"] for s in summaries),
        "max_cheapness_event": max(all_chain_rows, key=lambda x: x["cheapness_ratio"]) if all_chain_rows else None,
        "max_chain_compatible_event": max(all_chain_compatible, key=lambda x: x["cheapness_ratio"]) if all_chain_compatible else None,
        "lowest_average_debt_case": min(summaries, key=lambda x: x["average_debt"]),
        "highest_average_debt_case": max(summaries, key=lambda x: x["average_debt"]),
        "max_chain_compatible_case": max(summaries, key=lambda x: x["chain_compatible_events"]),
    }

    SUMMARY_PATH.write_text(
        json.dumps(global_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print(f"Wrote chain rows to: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
