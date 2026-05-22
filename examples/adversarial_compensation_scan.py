from __future__ import annotations

import json
import math
from pathlib import Path

VERSION = "v1.4"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

ROWS_PATH = RESULTS / "adversarial_compensation_rows.jsonl"
SUMMARY_PATH = RESULTS / "adversarial_compensation_summary.json"
CERTIFICATE_PATH = RESULTS / "adversarial_compensation_certificate.json"

PREVIOUS_COMPENSATION_SUMMARY = RESULTS / "compensation_law_candidate_summary.json"
PREVIOUS_COMPENSATION_ROWS = RESULTS / "compensation_law_candidate_rows.jsonl"
PREVIOUS_FRONTIER_SUMMARY = RESULTS / "critical_frontier_summary.json"

ESCAPE_THRESHOLD = math.log2(3)
TOLERANCE = 1e-12

MAX_ODD_BLOCKS = 20000
MAX_BAD_WINDOW_BLOCKS = 256
MAX_CANDIDATES = 520

ANCHOR_SEEDS = [
    27,
    31,
    63,
    77031,
    131069,
    627355,
    670617279,
    9780657630,
    9780657631,
    989345275647,
]

def line():
    print("=" * 80)

def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_jsonl(path: Path, rows):
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )

def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

def v2(x: int) -> int:
    if x <= 0:
        raise ValueError("v2 expects a positive integer.")
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count

def odd_part(x: int) -> int:
    if x <= 0:
        raise ValueError("odd_part expects a positive integer.")
    while x % 2 == 0:
        x //= 2
    return x

def odd_debt_word(n0: int, max_blocks: int = MAX_ODD_BLOCKS):
    if n0 <= 0:
        raise ValueError("n0 must be positive.")

    n = odd_part(n0)
    word = []
    odd_values = [n]

    if n == 1:
        return {
            "n0": n0,
            "odd_start": n,
            "reaches_1": True,
            "truncated": False,
            "debt_word": [2],
            "odd_values": [1],
        }

    for _ in range(max_blocks):
        a = v2(3 * n + 1)
        word.append(a)
        n = (3 * n + 1) // (2 ** a)
        odd_values.append(n)
        if n == 1:
            return {
                "n0": n0,
                "odd_start": odd_part(n0),
                "reaches_1": True,
                "truncated": False,
                "debt_word": word,
                "odd_values": odd_values,
            }

    return {
        "n0": n0,
        "odd_start": odd_part(n0),
        "reaches_1": False,
        "truncated": True,
        "debt_word": word,
        "odd_values": odd_values,
    }

def window_average(total: int, blocks: int) -> float:
    if blocks <= 0:
        return 0.0
    return total / blocks

def find_bad_windows_and_recoveries(debt_word):
    bad_windows = []
    recovered = 0
    unrecovered = 0
    hardest = None
    longest = None
    tightest = None
    min_surplus = None
    max_post_recovery_blocks = 0

    length = len(debt_word)
    if length <= 1:
        return {
            "bad_windows": bad_windows,
            "bad_window_count": 0,
            "recovered_bad_windows": 0,
            "unrecovered_bad_windows": 0,
            "all_bad_windows_recovered": True,
            "max_post_recovery_blocks": 0,
            "min_combined_surplus": None,
            "max_hardness_score": 0.0,
            "hardest_recovery": None,
            "longest_recovery": None,
            "tightest_recovery": None,
        }

    prefix = [0]
    for value in debt_word:
        prefix.append(prefix[-1] + value)

    for start in range(length):
        max_end = min(length - 1, start + MAX_BAD_WINDOW_BLOCKS)
        for end in range(start, max_end):
            blocks = end - start + 1
            debt = prefix[end + 1] - prefix[start]
            avg = window_average(debt, blocks)

            if avg >= ESCAPE_THRESHOLD - TOLERANCE:
                continue

            if end + 1 >= length:
                continue

            recovered_here = False
            recovery = None

            for post_end in range(end + 1, length):
                combined_blocks = post_end - start + 1
                combined_debt = prefix[post_end + 1] - prefix[start]
                combined_avg = window_average(combined_debt, combined_blocks)

                if combined_avg >= ESCAPE_THRESHOLD - TOLERANCE:
                    post_blocks = post_end - end
                    post_debt = prefix[post_end + 1] - prefix[end + 1]
                    post_avg = window_average(post_debt, post_blocks)
                    surplus = combined_avg - ESCAPE_THRESHOLD

                    hardness = (blocks + post_blocks) / max(abs(surplus), 1e-15)

                    recovery = {
                        "bad_start": start,
                        "bad_end": end,
                        "bad_blocks": blocks,
                        "bad_debt": debt,
                        "bad_average_debt": avg,
                        "bad_deficit": ESCAPE_THRESHOLD - avg,
                        "post_start": end + 1,
                        "post_end": post_end,
                        "post_blocks": post_blocks,
                        "post_debt": post_debt,
                        "post_average_debt": post_avg,
                        "combined_start": start,
                        "combined_end": post_end,
                        "combined_blocks": combined_blocks,
                        "combined_debt": combined_debt,
                        "combined_average_debt": combined_avg,
                        "combined_surplus": surplus,
                        "recovered": True,
                        "hardness_score": hardness,
                    }

                    recovered_here = True
                    recovered += 1
                    max_post_recovery_blocks = max(max_post_recovery_blocks, post_blocks)

                    if min_surplus is None or surplus < min_surplus:
                        min_surplus = surplus

                    if hardest is None or hardness > hardest["hardness_score"]:
                        hardest = recovery

                    if longest is None or post_blocks > longest["post_blocks"]:
                        longest = recovery

                    if tightest is None or surplus < tightest["combined_surplus"]:
                        tightest = recovery

                    break

            if not recovered_here:
                unrecovered += 1
                recovery = {
                    "bad_start": start,
                    "bad_end": end,
                    "bad_blocks": blocks,
                    "bad_debt": debt,
                    "bad_average_debt": avg,
                    "bad_deficit": ESCAPE_THRESHOLD - avg,
                    "post_start": end + 1,
                    "post_end": length - 1,
                    "post_blocks": max(0, length - 1 - end),
                    "combined_start": start,
                    "combined_end": length - 1,
                    "combined_blocks": length - start,
                    "combined_debt": prefix[length] - prefix[start],
                    "combined_average_debt": window_average(prefix[length] - prefix[start], length - start),
                    "combined_surplus": window_average(prefix[length] - prefix[start], length - start) - ESCAPE_THRESHOLD,
                    "recovered": False,
                    "hardness_score": float("inf"),
                }

                if hardest is None or hardest.get("recovered", True):
                    hardest = recovery

            bad_windows.append(recovery)

    max_hardness = 0.0
    if hardest is not None:
        raw = hardest.get("hardness_score", 0.0)
        max_hardness = raw if math.isfinite(raw) else 1e999

    return {
        "bad_windows": bad_windows,
        "bad_window_count": len(bad_windows),
        "recovered_bad_windows": recovered,
        "unrecovered_bad_windows": unrecovered,
        "all_bad_windows_recovered": unrecovered == 0,
        "max_post_recovery_blocks": max_post_recovery_blocks,
        "min_combined_surplus": min_surplus,
        "max_hardness_score": max_hardness,
        "hardest_recovery": hardest,
        "longest_recovery": longest,
        "tightest_recovery": tightest,
    }

def sorted_unique_positive(values):
    return sorted({int(v) for v in values if isinstance(v, int) and v > 0})

def extract_seed_candidates():
    seeds = set(ANCHOR_SEEDS)

    comp_summary = load_json(PREVIOUS_COMPENSATION_SUMMARY)
    if isinstance(comp_summary, dict):
        for key in ["hardest_case", "longest_recovery_case", "tightest_surplus_case"]:
            value = comp_summary.get(key)
            if isinstance(value, dict) and isinstance(value.get("n0"), int):
                seeds.add(value["n0"])

    frontier_summary = load_json(PREVIOUS_FRONTIER_SUMMARY)
    if isinstance(frontier_summary, dict):
        value = frontier_summary.get("current_hardest")
        if isinstance(value, dict) and isinstance(value.get("n0"), int):
            seeds.add(value["n0"])

    previous_rows = load_jsonl(PREVIOUS_COMPENSATION_ROWS)
    ranked = sorted(
        [row for row in previous_rows if isinstance(row.get("max_hardness_score"), (int, float))],
        key=lambda row: row.get("max_hardness_score", 0.0),
        reverse=True,
    )

    for row in ranked[:40]:
        if isinstance(row.get("n0"), int):
            seeds.add(row["n0"])

    return sorted_unique_positive(seeds)

def adversarial_neighborhood(seed: int):
    values = set()
    values.add(seed)

    for delta in range(-32, 33):
        values.add(seed + delta)

    for k in range(0, 18):
        step = 2 ** k
        values.add(seed - step)
        values.add(seed + step)

    for k in range(0, min(54, max(1, seed.bit_length() + 1))):
        values.add(seed ^ (2 ** k))

    if seed > 2:
        values.add(2 * seed - 1)
        values.add(2 * seed + 1)
        values.add(seed // 2)
        values.add(seed // 2 + 1)

    return sorted_unique_positive(values)

def build_candidate_set():
    seeds = extract_seed_candidates()
    candidates = set()

    for seed in seeds:
        for value in adversarial_neighborhood(seed):
            candidates.add(value)

    candidates = sorted_unique_positive(candidates)

    if len(candidates) > MAX_CANDIDATES:
        protected = sorted_unique_positive(ANCHOR_SEEDS + seeds)
        protected_set = set(protected)
        remaining = [x for x in candidates if x not in protected_set]

        def priority(x):
            return (
                min(abs(x - seed) for seed in protected),
                x.bit_length(),
                x,
            )

        remaining = sorted(remaining, key=priority)
        candidates = sorted_unique_positive(protected + remaining[: max(0, MAX_CANDIDATES - len(protected))])

    return candidates

def analyze_candidate(n0: int):
    trace = odd_debt_word(n0)
    debt_word = trace["debt_word"]
    compensation = find_bad_windows_and_recoveries(debt_word)

    row = {
        "version": VERSION,
        "n0": n0,
        "odd_start": trace["odd_start"],
        "reaches_1": trace["reaches_1"],
        "truncated": trace["truncated"],
        "odd_blocks": len(debt_word),
        "total_debt": sum(debt_word),
        "average_debt": window_average(sum(debt_word), len(debt_word)) if debt_word else 0.0,
        "escape_threshold": ESCAPE_THRESHOLD,
        "bad_windows": compensation["bad_window_count"],
        "recovered_bad_windows": compensation["recovered_bad_windows"],
        "unrecovered_bad_windows": compensation["unrecovered_bad_windows"],
        "all_bad_windows_recovered": compensation["all_bad_windows_recovered"],
        "max_post_recovery_blocks": compensation["max_post_recovery_blocks"],
        "min_combined_surplus": compensation["min_combined_surplus"],
        "max_hardness_score": compensation["max_hardness_score"],
        "hardest_recovery": compensation["hardest_recovery"],
        "longest_recovery": compensation["longest_recovery"],
        "tightest_recovery": compensation["tightest_recovery"],
    }

    return row

def main():
    RESULTS.mkdir(exist_ok=True)

    line()
    print("COLLATZ-NATIVE-MATH v1.4")
    line()
    print("Adversarial compensation scan")
    print(f"escape threshold log2(3): {ESCAPE_THRESHOLD}")
    print(f"comparison tolerance: {TOLERANCE}")
    print(f"max bad window blocks: {MAX_BAD_WINDOW_BLOCKS}")
    print(f"max candidates: {MAX_CANDIDATES}")
    line()

    candidates = build_candidate_set()
    rows = []

    for n0 in candidates:
        row = analyze_candidate(n0)
        rows.append(row)

        print(
            "n0: {n0} odd_blocks: {odd_blocks} bad_windows: {bad_windows} "
            "recovered: {recovered_bad_windows} unrecovered: {unrecovered_bad_windows} "
            "max_post_recovery_blocks: {max_post_recovery_blocks} "
            "min_surplus: {min_combined_surplus} hardness: {max_hardness_score:.6f}".format(**row)
        )

    total_bad = sum(row["bad_windows"] for row in rows)
    total_recovered = sum(row["recovered_bad_windows"] for row in rows)
    total_unrecovered = sum(row["unrecovered_bad_windows"] for row in rows)
    all_recovered = total_unrecovered == 0

    rows_with_bad = [row for row in rows if row["bad_windows"] > 0]
    rows_with_hardness = [row for row in rows if row["max_hardness_score"] > 0]

    hardest_case = max(rows_with_hardness, key=lambda row: row["max_hardness_score"]) if rows_with_hardness else None
    longest_case = max(rows_with_bad, key=lambda row: row["max_post_recovery_blocks"]) if rows_with_bad else None

    rows_with_surplus = [
        row for row in rows
        if row["min_combined_surplus"] is not None
    ]
    tightest_case = min(rows_with_surplus, key=lambda row: row["min_combined_surplus"]) if rows_with_surplus else None

    counterexamples = [
        {
            "n0": row["n0"],
            "odd_blocks": row["odd_blocks"],
            "bad_windows": row["bad_windows"],
            "unrecovered_bad_windows": row["unrecovered_bad_windows"],
            "hardest_recovery": row["hardest_recovery"],
        }
        for row in rows
        if row["unrecovered_bad_windows"] > 0
    ]

    summary = {
        "version": VERSION,
        "scan_type": "adversarial_compensation_scan",
        "generated_candidate_count": len(candidates),
        "escape_threshold": ESCAPE_THRESHOLD,
        "comparison_tolerance": TOLERANCE,
        "max_bad_window_blocks": MAX_BAD_WINDOW_BLOCKS,
        "total_bad_windows": total_bad,
        "total_recovered_bad_windows": total_recovered,
        "total_unrecovered_bad_windows": total_unrecovered,
        "all_bad_windows_recovered": all_recovered,
        "counterexample_candidate_count": len(counterexamples),
        "counterexample_candidates": counterexamples,
        "hardest_case": hardest_case,
        "longest_recovery_case": longest_case,
        "tightest_surplus_case": tightest_case,
        "anchor_seeds": ANCHOR_SEEDS,
    }

    certificate = {
        "version": VERSION,
        "certificate_type": "adversarial_compensation_certificate",
        "claim": (
            "No unrecovered bad compensation window was found in the finite adversarial scan domain."
            if all_recovered
            else "At least one unrecovered bad compensation window was found in the finite adversarial scan domain."
        ),
        "finite_domain_only": True,
        "not_a_collatz_proof": True,
        "generated_candidate_count": len(candidates),
        "total_bad_windows": total_bad,
        "total_recovered_bad_windows": total_recovered,
        "total_unrecovered_bad_windows": total_unrecovered,
        "all_bad_windows_recovered": all_recovered,
        "counterexample_candidate_count": len(counterexamples),
        "counterexample_candidates": counterexamples,
        "hardest_case_n0": hardest_case["n0"] if hardest_case else None,
        "hardest_case_score": hardest_case["max_hardness_score"] if hardest_case else None,
        "tightest_surplus_n0": tightest_case["n0"] if tightest_case else None,
        "tightest_surplus": tightest_case["min_combined_surplus"] if tightest_case else None,
        "limits": (
            "This certificate is computational and finite. It covers only the generated adversarial candidate set "
            "and only the configured maximum bad-window length. It is not a proof of the Collatz conjecture."
        ),
    }

    write_jsonl(ROWS_PATH, rows)
    write_json(SUMMARY_PATH, summary)
    write_json(CERTIFICATE_PATH, certificate)

    line()
    print("Adversarial compensation summary")
    line()
    print(f"candidate count: {len(candidates)}")
    print(f"total bad windows: {total_bad}")
    print(f"total recovered bad windows: {total_recovered}")
    print(f"total unrecovered bad windows: {total_unrecovered}")
    print(f"all bad windows recovered: {str(all_recovered).lower()}")

    if hardest_case:
        print(
            "hardest case: n0={n0} hardness={max_hardness_score:.6f}".format(**hardest_case)
        )

    if tightest_case:
        print(
            "tightest surplus: n0={n0} surplus={min_combined_surplus}".format(**tightest_case)
        )

    if counterexamples:
        print("counterexample candidates found: true")
    else:
        print("counterexample candidates found: false")

    print(f"Wrote rows to: {ROWS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    line()

if __name__ == "__main__":
    main()
