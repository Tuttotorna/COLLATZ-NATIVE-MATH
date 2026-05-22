#!/usr/bin/env python3

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "compensation_law_search.jsonl"
SUMMARY_PATH = ROOT / "results" / "compensation_law_summary.json"

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
    9780657630,
    63728127,
    670617279,
    989345275647,
    871,
    6171,
    77031,
    156159,
]

LOG2_3 = math.log2(3)
CHEAPNESS_THRESHOLD = 1 / (LOG2_3 - 1)

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

def trace_blocks(n0: int, max_blocks: int = 3000000):
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
            "is_locally_cheap_regeneration": cheapness_ratio >= CHEAPNESS_THRESHOLD,
            "cumulative_debt": total_debt,
            "average_debt": total_debt / (block + 1),
            "average_debt_above_threshold": (total_debt / (block + 1)) > LOG2_3,
        })

        n = m
        if n == 1:
            break

    return rows

def regeneration_indices(rows):
    return [i for i, row in enumerate(rows) if row["is_regeneration"]]

def segment_stats(rows, start_idx, end_idx):
    segment = rows[start_idx:end_idx + 1]
    if not segment:
        raise ValueError("empty segment")

    debt = sum(row["a"] for row in segment)
    blocks = len(segment)
    avg = debt / blocks

    return {
        "start_block": segment[0]["block"],
        "end_block": segment[-1]["block"],
        "blocks": blocks,
        "debt": debt,
        "average_debt": avg,
        "average_debt_above_threshold": avg > LOG2_3,
        "average_debt_at_or_below_threshold": avg <= LOG2_3,
        "escape_blocks": sum(1 for row in segment if row["a"] == 1),
        "compression_blocks": sum(1 for row in segment if row["a"] >= 2),
        "max_a": max(row["a"] for row in segment),
        "end_shadow": segment[-1]["s_next"],
        "max_n": max(max(row["n"], row["next_odd"]) for row in segment),
        "max_shadow": max(max(row["s"], row["s_next"]) for row in segment),
    }

def build_regeneration_segments(n0: int, rows):
    regen = regeneration_indices(rows)
    segments = []

    for j, idx in enumerate(regen):
        event = rows[idx]
        next_idx = regen[j + 1] if j + 1 < len(regen) else len(rows) - 1
        stats = segment_stats(rows, idx, next_idx)

        is_locally_cheap = event["cheapness_ratio"] >= CHEAPNESS_THRESHOLD
        reaches_next_regen = j + 1 < len(regen)
        chain_compatible = (
            is_locally_cheap
            and reaches_next_regen
            and stats["average_debt_at_or_below_threshold"]
        )

        segments.append({
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
            "is_locally_cheap": is_locally_cheap,
            "reaches_next_regeneration": reaches_next_regen,
            "chain_compatible": chain_compatible,
            **{f"segment_{k}": v for k, v in stats.items()},
        })

    return segments

def chain_episodes(n0: int, rows, segments):
    episodes = []
    i = 0

    while i < len(segments):
        if not segments[i]["chain_compatible"]:
            i += 1
            continue

        start_i = i
        chain_segments = []

        while i < len(segments) and segments[i]["chain_compatible"]:
            chain_segments.append(segments[i])
            i += 1

        end_i = i - 1

        chain_start_block = chain_segments[0]["segment_start_block"]
        chain_end_block = chain_segments[-1]["segment_end_block"]

        chain_rows = [
            row for row in rows
            if chain_start_block <= row["block"] <= chain_end_block
        ]

        chain_debt = sum(row["a"] for row in chain_rows)
        chain_blocks = len(chain_rows)
        chain_avg = chain_debt / chain_blocks if chain_blocks else None
        chain_deficit = LOG2_3 - chain_avg if chain_avg is not None else None

        episodes.append({
            "n0": n0,
            "odd_start": odd_start(n0),
            "chain_start_event_index": segments[start_i]["event_index"],
            "chain_end_event_index": segments[end_i]["event_index"],
            "chain_length_segments": len(chain_segments),
            "chain_start_block": chain_start_block,
            "chain_end_block": chain_end_block,
            "chain_blocks": chain_blocks,
            "chain_debt": chain_debt,
            "chain_average_debt": chain_avg,
            "chain_deficit_below_threshold": chain_deficit,
            "chain_total_regenerated_shadow": sum(seg["regenerated_shadow"] for seg in chain_segments),
            "chain_max_cheapness_ratio": max(seg["cheapness_ratio"] for seg in chain_segments),
        })

    return episodes

def find_recovery(rows, start_block):
    debt = 0
    blocks = 0

    for row in rows[start_block:]:
        debt += row["a"]
        blocks += 1
        avg = debt / blocks

        if avg > LOG2_3:
            return {
                "recovery_found": True,
                "recovery_end_block": row["block"],
                "recovery_distance_blocks": blocks,
                "recovery_debt": debt,
                "recovery_average_debt": avg,
                "recovery_surplus": avg - LOG2_3,
                "recovery_max_a": max(r["a"] for r in rows[start_block:row["block"] + 1]),
                "recovery_max_shadow": max(max(r["s"], r["s_next"]) for r in rows[start_block:row["block"] + 1]),
            }

    return {
        "recovery_found": False,
        "recovery_end_block": None,
        "recovery_distance_blocks": None,
        "recovery_debt": None,
        "recovery_average_debt": None,
        "recovery_surplus": None,
        "recovery_max_a": None,
        "recovery_max_shadow": None,
    }

def analyze_start(n0: int):
    rows = trace_blocks(n0)
    segments = build_regeneration_segments(n0, rows)
    episodes = chain_episodes(n0, rows, segments)

    out = []
    trajectory_debt = sum(row["a"] for row in rows)
    trajectory_blocks = len(rows)
    trajectory_average = trajectory_debt / trajectory_blocks if trajectory_blocks else None

    for ep in episodes:
        recovery = find_recovery(rows, ep["chain_start_block"])
        enriched = dict(ep)
        enriched.update(recovery)
        enriched["trajectory_blocks"] = trajectory_blocks
        enriched["trajectory_total_debt"] = trajectory_debt
        enriched["trajectory_average_debt"] = trajectory_average
        enriched["trajectory_average_debt_above_threshold"] = trajectory_average > LOG2_3 if trajectory_average is not None else None
        enriched["reaches_1"] = rows[-1]["next_odd"] == 1 if rows else False

        if recovery["recovery_found"]:
            enriched["recovery_to_chain_length_ratio"] = (
                recovery["recovery_distance_blocks"] / ep["chain_blocks"]
                if ep["chain_blocks"] else None
            )
        else:
            enriched["recovery_to_chain_length_ratio"] = None

        out.append(enriched)

    summary = {
        "n0": n0,
        "odd_start": odd_start(n0),
        "odd_blocks": len(rows),
        "reaches_1": rows[-1]["next_odd"] == 1 if rows else False,
        "trajectory_total_debt": trajectory_debt,
        "trajectory_average_debt": trajectory_average,
        "trajectory_average_debt_above_threshold": trajectory_average > LOG2_3 if trajectory_average is not None else None,
        "chain_episodes": len(out),
        "all_chains_recovered": all(row["recovery_found"] for row in out) if out else True,
        "max_recovery_distance_blocks": max([row["recovery_distance_blocks"] for row in out if row["recovery_distance_blocks"] is not None], default=0),
        "max_chain_deficit": max([row["chain_deficit_below_threshold"] for row in out], default=0),
        "max_recovery_to_chain_length_ratio": max([row["recovery_to_chain_length_ratio"] for row in out if row["recovery_to_chain_length_ratio"] is not None], default=0),
    }

    return out, summary

def main():
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_rows = []
    summaries = []

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v0.7")
    print("=" * 80)
    print("Searching for compensation law candidates.")
    print("=" * 80)
    print(f"escape threshold log2(3): {LOG2_3:.6f}")
    print(f"cheapness threshold: {CHEAPNESS_THRESHOLD:.6f}")
    print("=" * 80)

    for n0 in SAMPLES:
        rows, summary = analyze_start(n0)
        all_rows.extend(rows)
        summaries.append(summary)

        print()
        print(f"n0: {n0}")
        print(f"odd_blocks: {summary['odd_blocks']}")
        print(f"reaches_1: {str(summary['reaches_1']).lower()}")
        print(f"trajectory_average_debt: {summary['trajectory_average_debt']:.6f}")
        print(f"trajectory_average_debt_above_threshold: {str(summary['trajectory_average_debt_above_threshold']).lower()}")
        print(f"chain_episodes: {summary['chain_episodes']}")
        print(f"all_chains_recovered: {str(summary['all_chains_recovered']).lower()}")
        print(f"max_recovery_distance_blocks: {summary['max_recovery_distance_blocks']}")
        print(f"max_chain_deficit: {summary['max_chain_deficit']:.6f}")
        print(f"max_recovery_to_chain_length_ratio: {summary['max_recovery_to_chain_length_ratio']:.6f}")

        if rows:
            top = max(rows, key=lambda r: r["recovery_distance_blocks"] if r["recovery_distance_blocks"] is not None else -1)
            print(
                "top_recovery: "
                f"chain_start={top['chain_start_block']} "
                f"chain_len={top['chain_length_segments']} "
                f"chain_avg={top['chain_average_debt']:.6f} "
                f"deficit={top['chain_deficit_below_threshold']:.6f} "
                f"recovery_distance={top['recovery_distance_blocks']} "
                f"recovery_avg={top['recovery_average_debt']:.6f} "
                f"surplus={top['recovery_surplus']:.6f}"
            )

    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in all_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    recovered = [row for row in all_rows if row["recovery_found"]]
    unrecovered = [row for row in all_rows if not row["recovery_found"]]

    global_summary = {
        "version": "v0.7",
        "sample_count": len(SAMPLES),
        "escape_threshold_log2_3": LOG2_3,
        "cheapness_threshold": CHEAPNESS_THRESHOLD,
        "total_chain_episodes": len(all_rows),
        "recovered_chain_episodes": len(recovered),
        "unrecovered_chain_episodes": len(unrecovered),
        "all_chain_episodes_recovered": len(unrecovered) == 0,
        "max_recovery_distance_episode": max(recovered, key=lambda r: r["recovery_distance_blocks"]) if recovered else None,
        "max_chain_deficit_episode": max(all_rows, key=lambda r: r["chain_deficit_below_threshold"]) if all_rows else None,
        "max_recovery_ratio_episode": max(
            recovered,
            key=lambda r: r["recovery_to_chain_length_ratio"] if r["recovery_to_chain_length_ratio"] is not None else -1,
        ) if recovered else None,
        "average_recovery_distance": (
            sum(r["recovery_distance_blocks"] for r in recovered) / len(recovered)
            if recovered else None
        ),
        "average_chain_deficit": (
            sum(r["chain_deficit_below_threshold"] for r in all_rows) / len(all_rows)
            if all_rows else None
        ),
        "case_summaries": summaries,
        "unrecovered_examples": unrecovered[:20],
    }

    SUMMARY_PATH.write_text(
        json.dumps(global_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print(f"total_chain_episodes: {len(all_rows)}")
    print(f"recovered_chain_episodes: {len(recovered)}")
    print(f"unrecovered_chain_episodes: {len(unrecovered)}")
    print(f"all_chain_episodes_recovered: {str(len(unrecovered) == 0).lower()}")
    if recovered:
        max_rec = max(recovered, key=lambda r: r["recovery_distance_blocks"])
        print(
            "max recovery distance: "
            f"n0={max_rec['n0']} "
            f"distance={max_rec['recovery_distance_blocks']} "
            f"chain_avg={max_rec['chain_average_debt']:.6f} "
            f"recovery_avg={max_rec['recovery_average_debt']:.6f}"
        )
    print("=" * 80)
    print(f"Wrote compensation rows to: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
