#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "regeneration_scan.jsonl"

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
    value = 3 * n + 1
    a = v2(value)
    m = value // (2 ** a)
    return a, m

def trace_stats(n0: int, max_blocks: int = 10000):
    n = n0
    while n % 2 == 0:
        n //= 2

    total_debt = 0
    blocks = 0
    max_shadow = 0
    max_n = n
    escape_blocks = 0
    compression_blocks = 0
    regeneration_events = 0
    cheap_regeneration_events = 0

    previous_s = v2(n + 1)

    for _ in range(max_blocks):
        s = v2(n + 1)
        a, m = next_odd_block(n)
        s_next = v2(m + 1)

        total_debt += a
        blocks += 1
        max_shadow = max(max_shadow, s, s_next)
        max_n = max(max_n, n, m)

        if a == 1:
            escape_blocks += 1
        else:
            compression_blocks += 1

        if s_next > s:
            regeneration_events += 1
            produced_shadow = s_next - s
            cost = max(1, a - 1)
            cheapness = produced_shadow / cost
            if cheapness >= 1.7095:
                cheap_regeneration_events += 1

        n = m

        if n == 1:
            break

    return {
        "n0": n0,
        "odd_blocks": blocks,
        "reaches_1": n == 1,
        "total_debt": total_debt,
        "average_debt": total_debt / blocks if blocks else None,
        "escape_threshold_log2_3": math.log2(3),
        "average_debt_above_threshold": (total_debt / blocks) > math.log2(3) if blocks else None,
        "max_shadow": max_shadow,
        "max_n": max_n,
        "escape_blocks_a_eq_1": escape_blocks,
        "compression_blocks_a_ge_2": compression_blocks,
        "regeneration_events": regeneration_events,
        "cheap_regeneration_events": cheap_regeneration_events,
    }

def main():
    limit = 10000
    rows = []

    print("=" * 80)
    print("Regeneration scan")
    print("=" * 80)
    print(f"Scanning odd starts from 1 to {limit}")
    print("=" * 80)

    for n0 in range(1, limit + 1, 2):
        rows.append(trace_stats(n0))

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    max_blocks = max(rows, key=lambda r: r["odd_blocks"])
    max_shadow = max(rows, key=lambda r: r["max_shadow"])
    max_n = max(rows, key=lambda r: r["max_n"])
    most_regen = max(rows, key=lambda r: r["regeneration_events"])

    print()
    print("Top observations")
    print("-" * 80)
    print(f"max odd_blocks: n0={max_blocks['n0']} blocks={max_blocks['odd_blocks']}")
    print(f"max shadow: n0={max_shadow['n0']} max_shadow={max_shadow['max_shadow']}")
    print(f"max n reached: n0={max_n['n0']} max_n={max_n['max_n']}")
    print(f"most regeneration events: n0={most_regen['n0']} events={most_regen['regeneration_events']}")
    print()
    print(f"Wrote scan results to: {RESULTS_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
