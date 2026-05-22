#!/usr/bin/env python3

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "collapse_cause_classification.jsonl"
SUMMARY_PATH = ROOT / "results" / "collapse_cause_summary.json"

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

def trace_blocks(n0: int, max_blocks: int = 2000000):
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

def collapse_episodes(n0: int, rows, segments):
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
        collapse_segment = segments[i] if i < len(segments) else None

        chain_start_block = chain_segments[0]["segment_start_block"]
        chain_end_block = chain_segments[-1]["segment_end_block"]

        chain_rows = [
            row for row in rows
            if chain_start_block <= row["block"] <= chain_end_block
        ]
        chain_debt = sum(row["a"] for row in chain_rows)
        chain_blocks = len(chain_rows)
        chain_avg = chain_debt / chain_blocks if chain_blocks else None

        if collapse_segment is not None:
            collapse_start = collapse_segment["segment_start_block"]
            collapse_end = collapse_segment["segment_end_block"]
            collapse_rows = [
                row for row in rows
                if collapse_start <= row["block"] <= collapse_end
            ]
            collapse_debt = sum(row["a"] for row in collapse_rows)
            collapse_blocks = len(collapse_rows)
            collapse_avg = collapse_debt / collapse_blocks if collapse_blocks else None
            collapse_max_a = max(row["a"] for row in collapse_rows) if collapse_rows else None
            collapse_end_shadow = collapse_rows[-1]["s_next"] if collapse_rows else None
            collapse_cause = (
                "debt_break"
                if collapse_avg is not None and collapse_avg > LOG2_3
                else "non_chain_compatible"
            )
            next_is_locally_cheap = collapse_segment["is_locally_cheap"]
            next_reaches_regeneration = collapse_segment["reaches_next_regeneration"]
        else:
            collapse_start = None
            collapse_end = None
            collapse_debt = None
            collapse_blocks = None
            collapse_avg = None
            collapse_max_a = None
            collapse_end_shadow = None
            collapse_cause = "trajectory_end"
            next_is_locally_cheap = False
            next_reaches_regeneration = False
            collapse_rows = []

        post_start = chain_start_block
        post_end = collapse_end if collapse_end is not None else chain_end_block
        post_rows = [
            row for row in rows
            if post_start <= row["block"] <= post_end
        ]
        post_debt = sum(row["a"] for row in post_rows)
        post_blocks = len(post_rows)
        post_avg = post_debt / post_blocks if post_blocks else None
        compensation_surplus = post_avg - LOG2_3 if post_avg is not None else None

        reaches_1 = rows[-1]["next_odd"] == 1 if rows else False

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
            "chain_average_debt_below_or_equal_threshold": chain_avg <= LOG2_3 if chain_avg is not None else None,
            "chain_max_cheapness_ratio": max(seg["cheapness_ratio"] for seg in chain_segments),
            "chain_total_regenerated_shadow": sum(seg["regenerated_shadow"] for seg in chain_segments),
            "collapse_start_block": collapse_start,
            "collapse_end_block": collapse_end,
            "collapse_blocks": collapse_blocks,
            "collapse_debt": collapse_debt,
            "collapse_average_debt": collapse_avg,
            "collapse_max_a": collapse_max_a,
            "collapse_end_shadow": collapse_end_shadow,
            "collapse_cause": collapse_cause,
            "next_is_locally_cheap": next_is_locally_cheap,
            "next_reaches_regeneration": next_reaches_regeneration,
            "post_chain_blocks": post_blocks,
            "post_chain_debt": post_debt,
            "post_chain_average_debt": post_avg,
            "post_chain_average_debt_above_threshold": post_avg > LOG2_3 if post_avg is not None else None,
            "compensation_surplus": compensation_surplus,
            "reaches_1": reaches_1,
            "trajectory_total_blocks": len(rows),
            "trajectory_total_debt": sum(row["a"] for row in rows),
            "trajectory_average_debt": sum(row["a"] for row in rows) / len(rows) if rows else None,
        })

    return episodes

def classify_episode(ep):
    flags = {
        "debt_spike": False,
        "shadow_exhaustion": False,
        "failed_regeneration": False,
        "post_chain_overcompensation": False,
        "terminal_descent": False,
    }

    if ep["collapse_max_a"] is not None and ep["collapse_max_a"] >= 4:
        flags["debt_spike"] = True

    if ep["collapse_end_shadow"] is not None and ep["collapse_end_shadow"] <= 1:
        flags["shadow_exhaustion"] = True

    if not ep["next_is_locally_cheap"] or not ep["next_reaches_regeneration"]:
        flags["failed_regeneration"] = True

    if ep["post_chain_average_debt_above_threshold"]:
        flags["post_chain_overcompensation"] = True

    if ep["reaches_1"] and ep["collapse_cause"] == "trajectory_end":
        flags["terminal_descent"] = True

    priority = [
        "terminal_descent",
        "post_chain_overcompensation",
        "debt_spike",
        "failed_regeneration",
        "shadow_exhaustion",
    ]

    primary = "unclassified"
    for key in priority:
        if flags[key]:
            primary = key
            break

    return flags, primary

def summarize_start(n0: int, rows, episodes):
    debt_word = [row["a"] for row in rows]
    classified = []
    for ep in episodes:
        flags, primary = classify_episode(ep)
        classified.append((ep, flags, primary))

    primary_counts = Counter(primary for _, _, primary in classified)

    return {
        "n0": n0,
        "odd_start": odd_start(n0),
        "odd_blocks": len(rows),
        "reaches_1": rows[-1]["next_odd"] == 1 if rows else False,
        "total_debt": sum(debt_word),
        "average_debt": sum(debt_word) / len(debt_word) if debt_word else None,
        "average_debt_above_threshold": (sum(debt_word) / len(debt_word)) > LOG2_3 if debt_word else None,
        "collapse_episodes": len(episodes),
        "primary_cause_counts": dict(primary_counts),
        "max_chain_length_segments": max([ep["chain_length_segments"] for ep in episodes], default=0),
        "max_chain_cheapness_ratio": max([ep["chain_max_cheapness_ratio"] for ep in episodes], default=0.0),
        "max_collapse_debt_spike": max([ep["collapse_max_a"] for ep in episodes if ep["collapse_max_a"] is not None], default=None),
    }

def main():
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    classified_rows = []
    summaries = []

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v0.5")
    print("=" * 80)
    print("Classifying collapse causes.")
    print("=" * 80)
    print(f"escape threshold log2(3): {LOG2_3:.6f}")
    print(f"cheapness threshold: {CHEAPNESS_THRESHOLD:.6f}")
    print("=" * 80)

    for n0 in SAMPLES:
        rows = trace_blocks(n0)
        segments = build_regeneration_segments(n0, rows)
        episodes = collapse_episodes(n0, rows, segments)

        for ep in episodes:
            flags, primary = classify_episode(ep)
            enriched = dict(ep)
            enriched["cause_flags"] = flags
            enriched["primary_cause"] = primary
            classified_rows.append(enriched)

        summary = summarize_start(n0, rows, episodes)
        summaries.append(summary)

        print()
        print(f"n0: {n0}")
        print(f"odd_blocks: {summary['odd_blocks']}")
        print(f"reaches_1: {str(summary['reaches_1']).lower()}")
        print(f"average_debt: {summary['average_debt']:.6f}")
        print(f"average_debt_above_threshold: {str(summary['average_debt_above_threshold']).lower()}")
        print(f"collapse_episodes: {summary['collapse_episodes']}")
        print(f"primary_cause_counts: {summary['primary_cause_counts']}")
        print(f"max_chain_length_segments: {summary['max_chain_length_segments']}")
        print(f"max_chain_cheapness_ratio: {summary['max_chain_cheapness_ratio']:.6f}")
        print(f"max_collapse_debt_spike: {summary['max_collapse_debt_spike']}")

    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in classified_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    global_cause_counts = Counter(row["primary_cause"] for row in classified_rows)
    flag_counts = Counter()
    for row in classified_rows:
        for key, val in row["cause_flags"].items():
            if val:
                flag_counts[key] += 1

    global_summary = {
        "version": "v0.5",
        "sample_count": len(SAMPLES),
        "escape_threshold_log2_3": LOG2_3,
        "cheapness_threshold": CHEAPNESS_THRESHOLD,
        "total_classified_episodes": len(classified_rows),
        "primary_cause_counts": dict(global_cause_counts),
        "flag_counts": dict(flag_counts),
        "all_reach_1_in_sample": all(s["reaches_1"] for s in summaries),
        "all_average_debt_above_threshold_in_sample": all(s["average_debt_above_threshold"] for s in summaries),
        "max_chain_length_episode": max(classified_rows, key=lambda x: x["chain_length_segments"]) if classified_rows else None,
        "max_cheapness_episode": max(classified_rows, key=lambda x: x["chain_max_cheapness_ratio"]) if classified_rows else None,
        "max_debt_spike_episode": max(
            classified_rows,
            key=lambda x: x["collapse_max_a"] if x["collapse_max_a"] is not None else -1,
        ) if classified_rows else None,
        "case_summaries": summaries,
    }

    SUMMARY_PATH.write_text(
        json.dumps(global_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print("Global primary cause counts:")
    for key, value in sorted(global_cause_counts.items()):
        print(f"{key}: {value}")
    print()
    print("Global flag counts:")
    for key, value in sorted(flag_counts.items()):
        print(f"{key}: {value}")
    print("=" * 80)
    print(f"Wrote classified episodes to: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
