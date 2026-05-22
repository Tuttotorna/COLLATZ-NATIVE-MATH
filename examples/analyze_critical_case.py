#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DISSECTION_PATH = ROOT / "results" / "critical_case_dissection.json"
BLOCKS_PATH = ROOT / "results" / "critical_case_blocks.jsonl"
WINDOW_PATH = ROOT / "results" / "critical_case_window.jsonl"
SUMMARY_PATH = ROOT / "results" / "critical_case_summary.json"

CRITICAL_N0 = 9780657630

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

def trace_blocks(n0: int, max_blocks: int = 5000000):
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
            "recovery_min_a": None,
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
                "recovery_min_a": min(r["a"] for r in window),
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
        "recovery_min_a": None,
    }

def hardness_score(row):
    if not row["post_chain_recovery_found"]:
        return float("inf")

    distance = row["post_chain_recovery_distance_blocks"] or 0
    gap = row["recovery_distance_gap"] or 0
    deficit = row["chain_deficit_below_threshold"] or 0
    chain_len = row["chain_length_segments"] or 0
    surplus = row["post_chain_recovery_surplus"]

    surplus_term = 1 / (1 + 1000 * surplus) if surplus is not None and surplus >= 0 else 10

    return (
        math.log2(1 + distance)
        + math.log2(1 + max(0, gap))
        + deficit
        + chain_len
        + surplus_term
    )

def enrich_episode(rows, ep):
    chain_start = ep["chain_start_block"]
    chain_end = ep["chain_end_block"]
    post_start = chain_end + 1

    chain_start_recovery = find_recovery(rows, chain_start)
    post_chain_recovery = find_recovery(rows, post_start)

    enriched = dict(ep)

    for k, v in chain_start_recovery.items():
        enriched[f"chain_start_{k}"] = v

    for k, v in post_chain_recovery.items():
        enriched[f"post_chain_{k}"] = v

    enriched["post_chain_start_block"] = post_start

    if chain_start_recovery["recovery_distance_blocks"] is not None and post_chain_recovery["recovery_distance_blocks"] is not None:
        enriched["recovery_distance_gap"] = (
            post_chain_recovery["recovery_distance_blocks"]
            - chain_start_recovery["recovery_distance_blocks"]
        )
    else:
        enriched["recovery_distance_gap"] = None

    enriched["post_chain_unrecovered"] = not post_chain_recovery["recovery_found"]
    enriched["hardness_score"] = hardness_score(enriched)

    return enriched

def focused_window(rows, episode):
    start = episode["chain_start_block"]
    end = episode["post_chain_recovery_end_block"]

    if end is None:
        end = len(rows) - 1

    window = rows[start:end + 1]
    post_start = episode["post_chain_start_block"]

    post_debt = 0
    post_blocks = 0
    chain_debt = 0
    chain_blocks = 0

    focused = []

    for row in window:
        block = row["block"]

        in_chain = episode["chain_start_block"] <= block <= episode["chain_end_block"]
        in_post_recovery = post_start <= block <= episode["post_chain_recovery_end_block"]

        if in_chain:
            chain_debt += row["a"]
            chain_blocks += 1

        if block >= post_start:
            post_debt += row["a"]
            post_blocks += 1
            post_avg = post_debt / post_blocks
            post_surplus = post_avg - LOG2_3
            post_deficit = LOG2_3 - post_avg
        else:
            post_avg = None
            post_surplus = None
            post_deficit = None

        chain_avg = chain_debt / chain_blocks if chain_blocks else None

        focused.append({
            **row,
            "in_chain": in_chain,
            "in_post_recovery": in_post_recovery,
            "relative_to_chain_start": block - episode["chain_start_block"],
            "relative_to_post_start": block - post_start,
            "chain_partial_blocks": chain_blocks,
            "chain_partial_debt": chain_debt,
            "chain_partial_average": chain_avg,
            "chain_partial_surplus": chain_avg - LOG2_3 if chain_avg is not None else None,
            "post_partial_blocks": post_blocks if block >= post_start else 0,
            "post_partial_debt": post_debt if block >= post_start else 0,
            "post_partial_average": post_avg,
            "post_partial_surplus": post_surplus,
            "post_partial_deficit": post_deficit,
            "post_crossed_threshold": post_avg is not None and post_avg > LOG2_3,
        })

    return focused

def main():
    rows = trace_blocks(CRITICAL_N0)
    segments = build_regeneration_segments(CRITICAL_N0, rows)
    episodes = chain_episodes(CRITICAL_N0, rows, segments)
    enriched = [enrich_episode(rows, ep) for ep in episodes]

    recovered = [ep for ep in enriched if ep["post_chain_recovery_found"]]
    if not recovered:
        raise RuntimeError("No recovered post-chain episode found for critical case.")

    critical = max(recovered, key=lambda ep: ep["hardness_score"])
    window_rows = focused_window(rows, critical)

    trajectory_total_debt = sum(row["a"] for row in rows)
    trajectory_average = trajectory_total_debt / len(rows)

    first_crossing = None
    for row in window_rows:
        if row["post_crossed_threshold"]:
            first_crossing = row
            break

    post_rows = [
        row for row in window_rows
        if row["in_post_recovery"]
    ]

    debt_word = [row["a"] for row in post_rows]
    shadow_word = [row["s"] for row in post_rows]
    n_word = [row["n"] for row in post_rows]

    longest_a1_run = 0
    current_a1_run = 0
    for a in debt_word:
        if a == 1:
            current_a1_run += 1
            longest_a1_run = max(longest_a1_run, current_a1_run)
        else:
            current_a1_run = 0

    dissection = {
        "version": "v1.0",
        "n0": CRITICAL_N0,
        "odd_start": odd_start(CRITICAL_N0),
        "escape_threshold_log2_3": LOG2_3,
        "cheapness_threshold": CHEAPNESS_THRESHOLD,
        "trajectory_odd_blocks": len(rows),
        "trajectory_total_debt": trajectory_total_debt,
        "trajectory_average_debt": trajectory_average,
        "reaches_1": rows[-1]["next_odd"] == 1 if rows else False,
        "critical_episode": critical,
        "first_crossing_block": first_crossing["block"] if first_crossing else None,
        "first_crossing_relative_to_post_start": first_crossing["relative_to_post_start"] if first_crossing else None,
        "first_crossing_post_average": first_crossing["post_partial_average"] if first_crossing else None,
        "first_crossing_post_surplus": first_crossing["post_partial_surplus"] if first_crossing else None,
        "post_recovery_debt_word": debt_word,
        "post_recovery_shadow_word": shadow_word,
        "post_recovery_n_word_prefix": n_word[:25],
        "post_recovery_blocks": len(post_rows),
        "post_recovery_escape_blocks": sum(1 for row in post_rows if row["a"] == 1),
        "post_recovery_compression_blocks": sum(1 for row in post_rows if row["a"] >= 2),
        "post_recovery_longest_a1_run": longest_a1_run,
        "post_recovery_max_a": max(debt_word) if debt_word else None,
        "post_recovery_min_a": min(debt_word) if debt_word else None,
        "post_recovery_sum_a": sum(debt_word),
        "post_recovery_average_a": sum(debt_word) / len(debt_word) if debt_word else None,
    }

    summary = {
        "version": "v1.0",
        "n0": CRITICAL_N0,
        "critical_chain_start_block": critical["chain_start_block"],
        "critical_chain_end_block": critical["chain_end_block"],
        "post_chain_recovery_start_block": critical["post_chain_start_block"],
        "post_chain_recovery_end_block": critical["post_chain_recovery_end_block"],
        "post_chain_recovery_distance_blocks": critical["post_chain_recovery_distance_blocks"],
        "post_chain_recovery_average_debt": critical["post_chain_recovery_average_debt"],
        "post_chain_recovery_surplus": critical["post_chain_recovery_surplus"],
        "chain_deficit_below_threshold": critical["chain_deficit_below_threshold"],
        "hardness_score": critical["hardness_score"],
        "first_crossing_block": dissection["first_crossing_block"],
        "first_crossing_relative_to_post_start": dissection["first_crossing_relative_to_post_start"],
        "post_recovery_longest_a1_run": longest_a1_run,
        "post_recovery_escape_blocks": dissection["post_recovery_escape_blocks"],
        "post_recovery_compression_blocks": dissection["post_recovery_compression_blocks"],
        "post_recovery_debt_word_prefix": debt_word[:60],
    }

    DISSECTION_PATH.parent.mkdir(parents=True, exist_ok=True)

    DISSECTION_PATH.write_text(
        json.dumps(dissection, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with BLOCKS_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with WINDOW_PATH.open("w", encoding="utf-8") as f:
        for row in window_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v1.0")
    print("=" * 80)
    print("Critical case dissection")
    print("=" * 80)
    print(f"n0: {CRITICAL_N0}")
    print(f"odd_start: {odd_start(CRITICAL_N0)}")
    print(f"trajectory odd blocks: {len(rows)}")
    print(f"trajectory average debt: {trajectory_average:.6f}")
    print(f"reaches_1: {str(rows[-1]['next_odd'] == 1).lower()}")
    print("-" * 80)
    print(f"critical chain start: {critical['chain_start_block']}")
    print(f"critical chain end: {critical['chain_end_block']}")
    print(f"chain average debt: {critical['chain_average_debt']:.6f}")
    print(f"chain deficit below log2(3): {critical['chain_deficit_below_threshold']:.6f}")
    print("-" * 80)
    print(f"post-chain recovery start: {critical['post_chain_start_block']}")
    print(f"post-chain recovery end: {critical['post_chain_recovery_end_block']}")
    print(f"post-chain recovery distance: {critical['post_chain_recovery_distance_blocks']}")
    print(f"post-chain recovery average: {critical['post_chain_recovery_average_debt']:.6f}")
    print(f"post-chain recovery surplus: {critical['post_chain_recovery_surplus']:.6f}")
    print(f"hardness score: {critical['hardness_score']:.6f}")
    print("-" * 80)
    print(f"first crossing block: {dissection['first_crossing_block']}")
    print(f"first crossing relative to post start: {dissection['first_crossing_relative_to_post_start']}")
    print(f"post recovery debt sum: {dissection['post_recovery_sum_a']}")
    print(f"post recovery blocks: {dissection['post_recovery_blocks']}")
    print(f"post recovery escape blocks a=1: {dissection['post_recovery_escape_blocks']}")
    print(f"post recovery compression blocks a>=2: {dissection['post_recovery_compression_blocks']}")
    print(f"post recovery longest a=1 run: {dissection['post_recovery_longest_a1_run']}")
    print("-" * 80)
    print("post recovery debt word prefix:")
    print(debt_word[:80])
    print("=" * 80)
    print(f"Wrote dissection to: {DISSECTION_PATH.relative_to(ROOT)}")
    print(f"Wrote full blocks to: {BLOCKS_PATH.relative_to(ROOT)}")
    print(f"Wrote focused window to: {WINDOW_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
