#!/usr/bin/env python3

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "sample_results.jsonl"
DATA_PATH = ROOT / "data" / "sample_traces.jsonl"

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

def trace_odd(n0: int, max_blocks: int = 10000):
    if n0 <= 0:
        raise ValueError("n0 must be positive.")
    n = n0
    while n % 2 == 0:
        n //= 2
    rows = []
    total_debt = 0

    for i in range(max_blocks):
        s = v2(n + 1)
        a, m = next_odd_block(n)
        s_next = v2(m + 1)
        total_debt += a
        avg_debt = total_debt / (i + 1)
        local_factor = 3 / (2 ** a)

        rows.append({
            "block": i,
            "n": n,
            "a": a,
            "s": s,
            "next_odd": m,
            "s_next": s_next,
            "shadow_delta": s_next - s,
            "local_factor": local_factor,
            "cumulative_debt": total_debt,
            "average_debt": avg_debt,
            "escape_threshold_log2_3": math.log2(3),
            "above_escape_threshold": avg_debt > math.log2(3),
        })

        n = m
        if n == 1:
            break

    return rows

def summarize_trace(n0: int, rows):
    if not rows:
        return {
            "n0": n0,
            "odd_blocks": 0,
            "reaches_1": False,
        }

    debt_word = [r["a"] for r in rows]
    shadow_word = [r["s"] for r in rows]
    reaches_1 = rows[-1]["next_odd"] == 1

    return {
        "n0": n0,
        "odd_start": rows[0]["n"],
        "odd_blocks": len(rows),
        "reaches_1": reaches_1,
        "debt_word_prefix": debt_word[:80],
        "shadow_word_prefix": shadow_word[:80],
        "total_debt": sum(debt_word),
        "average_debt": sum(debt_word) / len(debt_word),
        "escape_threshold_log2_3": math.log2(3),
        "average_debt_above_threshold": (sum(debt_word) / len(debt_word)) > math.log2(3),
        "max_shadow": max(shadow_word),
        "max_n": max(max(r["n"], r["next_odd"]) for r in rows),
        "local_escape_blocks_a_eq_1": sum(1 for a in debt_word if a == 1),
        "compression_blocks_a_ge_2": sum(1 for a in debt_word if a >= 2),
    }

def main():
    samples = [
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
        6171,
        77031,
    ]

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    summaries = []
    full_trace_rows = []

    print("=" * 80)
    print("COLLATZ-NATIVE-MATH")
    print("=" * 80)
    print("Tracing odd debt words, 2-adic shadow, and regeneration behavior.")
    print("=" * 80)

    for n0 in samples:
        rows = trace_odd(n0)
        summary = summarize_trace(n0, rows)
        summaries.append(summary)

        print()
        print(f"n0: {n0}")
        print(f"odd_blocks: {summary['odd_blocks']}")
        print(f"reaches_1: {str(summary['reaches_1']).lower()}")
        print(f"total_debt: {summary['total_debt']}")
        print(f"average_debt: {summary['average_debt']:.6f}")
        print(f"log2(3): {summary['escape_threshold_log2_3']:.6f}")
        print(f"average_debt_above_threshold: {str(summary['average_debt_above_threshold']).lower()}")
        print(f"max_shadow: {summary['max_shadow']}")
        print(f"max_n: {summary['max_n']}")
        print(f"a=1 blocks: {summary['local_escape_blocks_a_eq_1']}")
        print(f"a>=2 blocks: {summary['compression_blocks_a_ge_2']}")
        print(f"debt_word_prefix: {summary['debt_word_prefix'][:30]}")
        print(f"shadow_word_prefix: {summary['shadow_word_prefix'][:30]}")

        for row in rows:
            full = dict(row)
            full["n0"] = n0
            full_trace_rows.append(full)

    with RESULTS_PATH.open("w", encoding="utf-8") as f:
        for row in summaries:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with DATA_PATH.open("w", encoding="utf-8") as f:
        for row in full_trace_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print()
    print("=" * 80)
    print(f"Wrote summaries to: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote trace data to: {DATA_PATH.relative_to(ROOT)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
