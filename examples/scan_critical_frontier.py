#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAN_PATH = ROOT / "results" / "critical_frontier_scan.jsonl"
SUMMARY_PATH = ROOT / "results" / "critical_frontier_summary.json"

LOG2_3 = math.log2(3)
CHEAPNESS_THRESHOLD = 1 / (LOG2_3 - 1)

PREVIOUS_CRITICAL = {
    "n0": 9780657630,
    "distance": 114,
    "surplus": 0.002757,
    "hardness": 15.100955,
}

KNOWN_HARD_CASES = [
    27,
    31,
    63,
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
    626331,
    1117065,
    1501353,
    1723519,
    2298025,
    3542887,
]

FRONTIER_CENTERS = [
    9780657630,
    989345275647,
    626331,
    1117065,
    3542887,
]

def v2(n: int) -> int:
    if n == 0:
        raise ValueError("v2(0) is undefined here.")
    n = abs(n)
    c = 0
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

def trace_blocks(n0: int, max_blocks: int = 200000):
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
            "is_regeneration": s_next > s,
            "regenerated_shadow": regenerated_shadow,
            "compression_cost": compression_cost,
            "cheapness_ratio": cheapness_ratio,
            "is_locally_cheap_regeneration": cheapness_ratio >= CHEAPNESS_THRESHOLD,
            "cumulative_debt": total_debt,
            "average_debt": total_debt / (block + 1),
        })

        n = m
        if n == 1:
            break

    return rows

def segment_stats(rows, start_idx, end_idx):
    segment = rows[start_idx:end_idx + 1]
    debt = sum(row["a"] for row in segment)
    blocks = len(segment)
    avg = debt / blocks

    return {
        "start_block": segment[0]["block"],
        "end_block": segment[-1]["block"],
        "blocks": blocks,
        "debt": debt,
        "average_debt": avg,
        "average_debt_at_or_below_threshold": avg <= LOG2_3,
        "max_a": max(row["a"] for row in segment),
        "max_shadow": max(max(row["s"], row["s_next"]) for row in segment),
    }

def build_regeneration_segments(n0: int, rows):
    regen = [i for i, row in enumerate(rows) if row["is_regeneration"]]
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
            "event_index": j,
            "event_block": idx,
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
        chain_avg = chain_debt / chain_blocks
        chain_deficit = LOG2_3 - chain_avg

        episodes.append({
            "n0": n0,
            "chain_start_event_index": segments[start_i]["event_index"],
            "chain_end_event_index": segments[end_i]["event_index"],
            "chain_length_segments": len(chain_segments),
            "chain_start_block": chain_start_block,
            "chain_end_block": chain_end_block,
            "chain_blocks": chain_blocks,
            "chain_debt": chain_debt,
            "chain_average_debt": chain_avg,
            "chain_deficit_below_threshold": chain_deficit,
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
            "recovery_average_debt": None,
            "recovery_surplus": None,
        }

    debt = 0
    blocks = 0

    for row in rows[start_block:]:
        debt += row["a"]
        blocks += 1
        avg = debt / blocks

        if avg > LOG2_3:
            return {
                "recovery_found": True,
                "recovery_start_block": start_block,
                "recovery_end_block": row["block"],
                "recovery_distance_blocks": blocks,
                "recovery_average_debt": avg,
                "recovery_surplus": avg - LOG2_3,
            }

    return {
        "recovery_found": False,
        "recovery_start_block": start_block,
        "recovery_end_block": None,
        "recovery_distance_blocks": None,
        "recovery_average_debt": None,
        "recovery_surplus": None,
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

    enriched["hardness_score"] = hardness_score(enriched)
    return enriched

def candidate_set():
    candidates = set()

    for n in KNOWN_HARD_CASES:
        if n > 0:
            candidates.add(n)

    # Local neighborhoods around frontier centers.
    # Keep bounded to avoid turning CI into a long exhaustive scan.
    offsets = [
        -4096, -2048, -1024, -512, -256, -128, -64, -32, -16, -8, -4, -2,
        0,
        2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096,
    ]

    for center in FRONTIER_CENTERS:
        for offset in offsets:
            n = center + offset
            if n > 0:
                candidates.add(n)

    # Structured near-Mersenne odd candidates.
    for k in range(5, 54):
        n = (2 ** k) - 1
        candidates.add(n)
        if n - 2 > 0:
            candidates.add(n - 2)
        candidates.add(n + 2)

    return sorted(candidates)

def analyze_n0(n0: int):
    rows = trace_blocks(n0)

    reaches_1 = bool(rows and rows[-1]["next_odd"] == 1)
    total_debt = sum(row["a"] for row in rows)
    avg_debt = total_debt / len(rows) if rows else None

    segments = build_regeneration_segments(n0, rows)
    episodes = chain_episodes(n0, rows, segments)
    enriched = [enrich_episode(rows, ep) for ep in episodes]

    recovered = [ep for ep in enriched if ep["post_chain_recovery_found"]]
    unrecovered = [ep for ep in enriched if not ep["post_chain_recovery_found"]]

    hardest = max(recovered, key=lambda ep: ep["hardness_score"]) if recovered else None
    longest = max(recovered, key=lambda ep: ep["post_chain_recovery_distance_blocks"]) if recovered else None

    tightest_candidates = [
        ep for ep in recovered
        if ep["post_chain_recovery_surplus"] is not None
    ]
    tightest = min(tightest_candidates, key=lambda ep: ep["post_chain_recovery_surplus"]) if tightest_candidates else None

    return {
        "n0": n0,
        "odd_start": odd_start(n0),
        "reaches_1": reaches_1,
        "odd_blocks": len(rows),
        "trajectory_total_debt": total_debt,
        "trajectory_average_debt": avg_debt,
        "chain_episodes": len(episodes),
        "post_chain_recovered": len(recovered),
        "post_chain_unrecovered": len(unrecovered),
        "max_post_chain_recovery_distance": longest["post_chain_recovery_distance_blocks"] if longest else 0,
        "min_post_chain_recovery_surplus": tightest["post_chain_recovery_surplus"] if tightest else None,
        "max_hardness_score": hardest["hardness_score"] if hardest else 0,
        "hardest_episode": hardest,
        "longest_recovery_episode": longest,
        "tightest_surplus_episode": tightest,
    }

def main():
    candidates = candidate_set()
    rows = []

    SCAN_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v1.1")
    print("=" * 80)
    print("Critical frontier scan")
    print("=" * 80)
    print(f"candidate count: {len(candidates)}")
    print(f"escape threshold log2(3): {LOG2_3:.6f}")
    print(f"cheapness threshold: {CHEAPNESS_THRESHOLD:.6f}")
    print("=" * 80)

    with SCAN_PATH.open("w", encoding="utf-8") as f:
        for index, n0 in enumerate(candidates, start=1):
            row = analyze_n0(n0)
            row["candidate_index"] = index
            rows.append(row)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

            print(
                "n0:",
                row["n0"],
                "odd_blocks:",
                row["odd_blocks"],
                "chains:",
                row["chain_episodes"],
                "max_distance:",
                row["max_post_chain_recovery_distance"],
                "min_surplus:",
                row["min_post_chain_recovery_surplus"],
                "hardness:",
                f"{row['max_hardness_score']:.6f}",
            )

    completed = [row for row in rows if row["reaches_1"]]
    recovered_rows = [row for row in rows if row["post_chain_recovered"] > 0]

    current_hardest = max(recovered_rows, key=lambda row: row["max_hardness_score"]) if recovered_rows else None
    current_longest = max(recovered_rows, key=lambda row: row["max_post_chain_recovery_distance"]) if recovered_rows else None

    surplus_rows = [
        row for row in recovered_rows
        if row["min_post_chain_recovery_surplus"] is not None
    ]
    current_tightest = min(surplus_rows, key=lambda row: row["min_post_chain_recovery_surplus"]) if surplus_rows else None

    harder_than_previous = (
        current_hardest is not None
        and current_hardest["max_hardness_score"] > PREVIOUS_CRITICAL["hardness"]
    )

    summary = {
        "version": "v1.1",
        "candidate_count": len(candidates),
        "completed_count": len(completed),
        "previous_critical_n0": PREVIOUS_CRITICAL["n0"],
        "previous_critical_distance": PREVIOUS_CRITICAL["distance"],
        "previous_critical_surplus": PREVIOUS_CRITICAL["surplus"],
        "previous_critical_hardness": PREVIOUS_CRITICAL["hardness"],
        "current_hardest": current_hardest,
        "current_longest_recovery": current_longest,
        "current_tightest_surplus": current_tightest,
        "harder_than_previous_critical": harder_than_previous,
    }

    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 80)
    print("Frontier summary")
    print("=" * 80)

    if current_hardest:
        print(
            "current hardest:",
            f"n0={current_hardest['n0']}",
            f"hardness={current_hardest['max_hardness_score']:.6f}",
            f"distance={current_hardest['max_post_chain_recovery_distance']}",
            f"min_surplus={current_hardest['min_post_chain_recovery_surplus']}",
        )

    if current_longest:
        print(
            "current longest recovery:",
            f"n0={current_longest['n0']}",
            f"distance={current_longest['max_post_chain_recovery_distance']}",
            f"hardness={current_longest['max_hardness_score']:.6f}",
        )

    if current_tightest:
        print(
            "current tightest surplus:",
            f"n0={current_tightest['n0']}",
            f"surplus={current_tightest['min_post_chain_recovery_surplus']}",
            f"distance={current_tightest['max_post_chain_recovery_distance']}",
        )

    print(f"harder than previous critical: {str(harder_than_previous).lower()}")
    print("=" * 80)
    print(f"Wrote scan rows to: {SCAN_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
