#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "post_chain_recovery_analysis.jsonl"
SUMMARY_PATH = ROOT / "results" / "post_chain_recovery_summary.json"

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
    156159,
    106239,
    230631,
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
    if start_block is None or start_block >= len(rows):
        return {
            "recovery_found": False,
            "recovery_start_block": start_block,
            "recovery_end_block": None,
            "recovery_distance_blocks": None,
            "recovery_debt": None,
            "recovery_average_debt": None,
            "recovery_surplus": None,
            "recovery_max_a": None,
        }

    debt = 0
    blocks = 0

    for row in rows[start_block:]:
        debt += row["a"]
        blocks += 1
        avg = debt / blocks

        if avg > LOG2_3:
            window = rows[start_block:row["block"] + 1]
            return {
                "recovery_found": True,
                "recovery_start_block": start_block,
                "recovery_end_block": row["block"],
                "recovery_distance_blocks": blocks,
                "recovery_debt": debt,
                "recovery_average_debt": avg,
                "recovery_surplus": avg - LOG2_3,
                "recovery_max_a": max(r["a"] for r in window),
            }

    return {
        "recovery_found": False,
        "recovery_start_block": start_block,
        "recovery_end_block": None,
        "recovery_distance_blocks": None,
        "recovery_debt": None,
        "recovery_average_debt": None,
        "recovery_surplus": None,
        "recovery_max_a": None,
    }

def prefix_keys(prefix, data):
    return {f"{prefix}_{k}": v for k, v in data.items()}

def analyze_start(n0: int):
    rows = trace_blocks(n0)
    segments = build_regeneration_segments(n0, rows)
    episodes = chain_episodes(n0, rows, segments)

    out = []
    trajectory_debt = sum(row["a"] for row in rows)
    trajectory_blocks = len(rows)
    trajectory_average = trajectory_debt / trajectory_blocks if trajectory_blocks else None

    for ep in episodes:
        chain_start = ep["chain_start_block"]
        chain_end = ep["chain_end_block"]
        post_start = chain_end + 1

        chain_start_recovery = find_recovery(rows, chain_start)
        post_chain_recovery = find_recovery(rows, post_start)

        enriched = dict(ep)
        enriched.update(prefix_keys("chain_start", chain_start_recovery))
        enriched.update(prefix_keys("post_chain", post_chain_recovery))

        enriched["post_chain_start_block"] = post_start
        enriched["post_chain_available_blocks"] = max(0, len(rows) - post_start)
        enriched["trajectory_blocks"] = trajectory_blocks
        enriched["trajectory_total_debt"] = trajectory_debt
        enriched["trajectory_average_debt"] = trajectory_average
        enriched["trajectory_average_debt_above_threshold"] = trajectory_average > LOG2_3 if trajectory_average is not None else None
        enriched["reaches_1"] = rows[-1]["next_odd"] == 1 if rows else False

        if chain_start_recovery["recovery_distance_blocks"] is not None and post_chain_recovery["recovery_distance_blocks"] is not None:
            enriched["recovery_distance_gap"] = (
                post_chain_recovery["recovery_distance_blocks"]
                - chain_start_recovery["recovery_distance_blocks"]
            )
        else:
            enriched["recovery_distance_gap"] = None

        enriched["instant_chain_start_recovery"] = (
            chain_start_recovery["recovery_found"]
            and chain_start_recovery["recovery_distance_blocks"] == 1
        )

        enriched["instant_post_chain_recovery"] = (
            post_chain_recovery["recovery_found"]
            and post_chain_recovery["recovery_distance_blocks"] == 1
        )

        enriched["post_chain_unrecovered"] = not post_chain_recovery["recovery_found"]

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
        "chain_start_recovered": sum(1 for row in out if row["chain_start_recovery_found"]),
        "post_chain_recovered": sum(1 for row in out if row["post_chain_recovery_found"]),
        "post_chain_unrecovered": sum(1 for row in out if row["post_chain_unrecovered"]),
        "max_post_chain_recovery_distance": max(
            [row["post_chain_recovery_distance_blocks"] for row in out if row["post_chain_recovery_distance_blocks"] is not None],
            default=0,
        ),
        "max_recovery_distance_gap": max(
            [row["recovery_distance_gap"] for row in out if row["recovery_distance_gap"] is not None],
            default=0,
        ),
    }

    return out, summary

def main():
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_rows = []
    summaries = []

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v0.8")
    print("=" * 80)
    print("Analyzing post-chain recovery windows.")
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
        print(f"chain_episodes: {summary['chain_episodes']}")
        print(f"chain_start_recovered: {summary['chain_start_recovered']}")
        print(f"post_chain_recovered: {summary['post_chain_recovered']}")
        print(f"post_chain_unrecovered: {summary['post_chain_unrecovered']}")
        print(f"max_post_chain_recovery_distance: {summary['max_post_chain_recovery_distance']}")
        print(f"max_recovery_distance_gap: {summary['max_recovery_distance_gap']}")

        if rows:
            candidates = [r for r in rows if r["post_chain_recovery_found"]]
            if candidates:
                top = max(candidates, key=lambda r: r["post_chain_recovery_distance_blocks"])
                print(
                    "top_post_chain_recovery: "
                    f"chain_end={top['chain_end_block']} "
                    f"post_start={top['post_chain_start_block']} "
                    f"distance={top['post_chain_recovery_distance_blocks']} "
                    f"avg={top['post_chain_recovery_average_debt']:.6f} "
                    f"surplus={top['post_chain_recovery_surplus']:.6f}"
                )
            else:
                print("top_post_chain_recovery: none")

    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in all_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    post_recovered = [row for row in all_rows if row["post_chain_recovery_found"]]
    post_unrecovered = [row for row in all_rows if row["post_chain_unrecovered"]]
    chain_start_recovered = [row for row in all_rows if row["chain_start_recovery_found"]]

    global_summary = {
        "version": "v0.8",
        "sample_count": len(SAMPLES),
        "escape_threshold_log2_3": LOG2_3,
        "cheapness_threshold": CHEAPNESS_THRESHOLD,
        "total_chain_episodes": len(all_rows),
        "chain_start_recovered_episodes": len(chain_start_recovered),
        "post_chain_recovered_episodes": len(post_recovered),
        "post_chain_unrecovered_episodes": len(post_unrecovered),
        "all_post_chain_episodes_recovered": len(post_unrecovered) == 0,
        "max_post_chain_recovery_distance_episode": max(
            post_recovered,
            key=lambda r: r["post_chain_recovery_distance_blocks"],
        ) if post_recovered else None,
        "max_recovery_gap_episode": max(
            [r for r in all_rows if r["recovery_distance_gap"] is not None],
            key=lambda r: r["recovery_distance_gap"],
        ) if any(r["recovery_distance_gap"] is not None for r in all_rows) else None,
        "average_post_chain_recovery_distance": (
            sum(r["post_chain_recovery_distance_blocks"] for r in post_recovered) / len(post_recovered)
            if post_recovered else None
        ),
        "instant_post_chain_recovery_count": sum(1 for r in all_rows if r["instant_post_chain_recovery"]),
        "instant_chain_start_recovery_count": sum(1 for r in all_rows if r["instant_chain_start_recovery"]),
        "case_summaries": summaries,
        "post_chain_unrecovered_examples": post_unrecovered[:20],
    }

    SUMMARY_PATH.write_text(
        json.dumps(global_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print(f"total_chain_episodes: {len(all_rows)}")
    print(f"chain_start_recovered_episodes: {len(chain_start_recovered)}")
    print(f"post_chain_recovered_episodes: {len(post_recovered)}")
    print(f"post_chain_unrecovered_episodes: {len(post_unrecovered)}")
    print(f"all_post_chain_episodes_recovered: {str(len(post_unrecovered) == 0).lower()}")
    if post_recovered:
        max_rec = max(post_recovered, key=lambda r: r["post_chain_recovery_distance_blocks"])
        print(
            "max post-chain recovery distance: "
            f"n0={max_rec['n0']} "
            f"distance={max_rec['post_chain_recovery_distance_blocks']} "
            f"avg={max_rec['post_chain_recovery_average_debt']:.6f}"
        )
    print("=" * 80)
    print(f"Wrote post-chain rows to: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
