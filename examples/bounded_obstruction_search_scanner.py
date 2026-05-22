#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v2.6

Bounded Obstruction Search Scanner.

This scanner searches for obstruction-preserving regeneration inside a bounded
finite domain.

It does not prove the Collatz conjecture.
It does not claim global closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VERSION = "v2.6"
ESCAPE_THRESHOLD = math.log2(3)

MAX_ODD_BLOCKS = 2048
MAX_BAD_WINDOW_BLOCKS = 64
MAX_RECOVERY_LOOKAHEAD_BLOCKS = 256
DANGEROUS_SURPLUS_THRESHOLD = 1e-3

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

ROWS_PATH = RESULTS_DIR / "bounded_obstruction_search_rows.jsonl"
SUMMARY_PATH = RESULTS_DIR / "bounded_obstruction_search_summary.json"
CERTIFICATE_PATH = RESULTS_DIR / "bounded_obstruction_search_certificate.json"

KNOWN_ANCHORS = [
    1,
    3,
    7,
    27,
    31,
    63,
    77031,
    131071,
    626331,
    837799,
    1117065,
    2298025,
    3542887,
    63728127,
    670617279,
    9780657630,
    989345275647,
    9007199254740991,
]


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 requires a positive integer")

    exponent = 0
    while n % 2 == 0:
        exponent += 1
        n //= 2
    return exponent


def odd_part(n: int) -> int:
    if n <= 0:
        raise ValueError("odd_part requires a positive integer")

    while n % 2 == 0:
        n //= 2
    return n


def odd_block_sequence(n0: int, max_odd_blocks: int = MAX_ODD_BLOCKS) -> Tuple[List[Dict[str, Any]], bool]:
    if n0 <= 0:
        raise ValueError("n0 must be positive")

    n = odd_part(n0)
    blocks: List[Dict[str, Any]] = []

    for index in range(max_odd_blocks):
        if n == 1:
            return blocks, True

        expanded = 3 * n + 1
        discharge = v2(expanded)
        next_odd = expanded // (2 ** discharge)

        blocks.append(
            {
                "index": index,
                "odd": n,
                "expanded": expanded,
                "discharge": discharge,
                "next_odd": next_odd,
                "local_debt": ESCAPE_THRESHOLD - discharge,
            }
        )

        n = next_odd

    return blocks, False


def interval_average(values: List[int], start: int, end: int) -> float:
    if end <= start:
        raise ValueError("empty interval")
    return sum(values[start:end]) / (end - start)


def detect_bad_windows(
    discharges: List[int],
    max_window_blocks: int = MAX_BAD_WINDOW_BLOCKS,
) -> List[Dict[str, Any]]:
    bad_windows: List[Dict[str, Any]] = []
    total = len(discharges)

    for start in range(total):
        stop_limit = min(total, start + max_window_blocks)
        running_sum = 0

        for end in range(start + 1, stop_limit + 1):
            running_sum += discharges[end - 1]
            blocks = end - start
            avg = running_sum / blocks

            if avg < ESCAPE_THRESHOLD:
                bad_windows.append(
                    {
                        "start": start,
                        "end": end,
                        "blocks": blocks,
                        "average_discharge": avg,
                        "debt": ESCAPE_THRESHOLD * blocks - running_sum,
                        "deficit": ESCAPE_THRESHOLD - avg,
                    }
                )

    return bad_windows


def find_compensation(
    discharges: List[int],
    bad_window: Dict[str, Any],
    max_lookahead_blocks: int = MAX_RECOVERY_LOOKAHEAD_BLOCKS,
) -> Optional[Dict[str, Any]]:
    start = int(bad_window["start"])
    bad_end = int(bad_window["end"])
    total = len(discharges)
    recovery_limit = min(total, bad_end + max_lookahead_blocks)

    for combined_end in range(bad_end + 1, recovery_limit + 1):
        avg = interval_average(discharges, start, combined_end)
        surplus = avg - ESCAPE_THRESHOLD

        if surplus > 0:
            post_blocks = combined_end - bad_end
            return {
                "recovered": True,
                "combined_start": start,
                "combined_end": combined_end,
                "combined_blocks": combined_end - start,
                "post_start": bad_end,
                "post_end": combined_end,
                "post_blocks": post_blocks,
                "combined_average_discharge": avg,
                "combined_surplus": surplus,
            }

    return None


def detect_regeneration_after(
    discharges: List[int],
    after_index: int,
    max_window_blocks: int = MAX_BAD_WINDOW_BLOCKS,
) -> List[Dict[str, Any]]:
    if after_index >= len(discharges):
        return []

    suffix = discharges[after_index:]
    regenerated = detect_bad_windows(suffix, max_window_blocks=max_window_blocks)

    for item in regenerated:
        item["start"] += after_index
        item["end"] += after_index

    return regenerated


def classify_trajectory(n0: int) -> Dict[str, Any]:
    blocks, reaches_1 = odd_block_sequence(n0)
    discharges = [int(block["discharge"]) for block in blocks]

    bad_windows = detect_bad_windows(discharges)

    recovered_count = 0
    unrecovered_count = 0
    regeneration_count = 0
    dangerous_regeneration_count = 0
    obstruction_candidate_count = 0

    min_surplus: Optional[float] = None
    max_post_recovery_blocks = 0
    hardest_recovery_score = 0.0

    sample_bad_windows: List[Dict[str, Any]] = []
    sample_dangerous_regenerations: List[Dict[str, Any]] = []

    for bad in bad_windows:
        recovery = find_compensation(discharges, bad)

        if recovery is None:
            unrecovered_count += 1

            if not reaches_1:
                obstruction_candidate_count += 1

            if len(sample_bad_windows) < 5:
                sample_bad_windows.append(
                    {
                        "start": bad["start"],
                        "end": bad["end"],
                        "blocks": bad["blocks"],
                        "deficit": bad["deficit"],
                        "recovered": False,
                    }
                )

            continue

        recovered_count += 1

        surplus = float(recovery["combined_surplus"])
        if min_surplus is None or surplus < min_surplus:
            min_surplus = surplus

        post_blocks = int(recovery["post_blocks"])
        if post_blocks > max_post_recovery_blocks:
            max_post_recovery_blocks = post_blocks

        deficit = float(bad["deficit"])
        score = (bad["blocks"] * max(1, post_blocks)) / max(surplus, 1e-12)
        if score > hardest_recovery_score:
            hardest_recovery_score = score

        regenerated = detect_regeneration_after(discharges, int(recovery["combined_end"]))
        if regenerated:
            regeneration_count += 1

            dangerous = (
                surplus < DANGEROUS_SURPLUS_THRESHOLD
                or post_blocks >= 32
                or deficit < 1e-3
            )

            if dangerous:
                dangerous_regeneration_count += 1

                if len(sample_dangerous_regenerations) < 5:
                    first_regen = regenerated[0]
                    sample_dangerous_regenerations.append(
                        {
                            "bad_start": bad["start"],
                            "bad_end": bad["end"],
                            "recovery_end": recovery["combined_end"],
                            "post_recovery_blocks": post_blocks,
                            "combined_surplus": surplus,
                            "regeneration_start": first_regen["start"],
                            "regeneration_end": first_regen["end"],
                            "regeneration_deficit": first_regen["deficit"],
                        }
                    )

        if len(sample_bad_windows) < 5:
            sample_bad_windows.append(
                {
                    "start": bad["start"],
                    "end": bad["end"],
                    "blocks": bad["blocks"],
                    "deficit": bad["deficit"],
                    "recovered": True,
                    "post_recovery_blocks": post_blocks,
                    "combined_surplus": surplus,
                }
            )

    if not bad_windows:
        result_type = "NO_DEBT_DETECTED"
    elif obstruction_candidate_count > 0:
        result_type = "OBSTRUCTION_CANDIDATE_DETECTED"
    elif dangerous_regeneration_count > 0:
        result_type = "DANGEROUS_REGENERATION_DETECTED"
    elif regeneration_count > 0:
        result_type = "REGENERATED_BUT_COMPENSATED"
    elif unrecovered_count == 0:
        result_type = "DEBT_LOCALLY_RECOVERED"
    else:
        result_type = "UNDECIDED"

    return {
        "version": VERSION,
        "n0": n0,
        "odd_start": odd_part(n0),
        "reaches_1": reaches_1,
        "odd_blocks": len(blocks),
        "debt_window_count": len(bad_windows),
        "recovered_debt_window_count": recovered_count,
        "unrecovered_debt_window_count": unrecovered_count,
        "regeneration_count": regeneration_count,
        "dangerous_regeneration_count": dangerous_regeneration_count,
        "obstruction_candidate_count": obstruction_candidate_count,
        "closure_result_type": result_type,
        "min_positive_surplus": min_surplus,
        "max_post_recovery_blocks": max_post_recovery_blocks,
        "hardest_recovery_score": hardest_recovery_score,
        "sample_bad_windows": sample_bad_windows,
        "sample_dangerous_regenerations": sample_dangerous_regenerations,
    }


def candidate_numbers() -> List[int]:
    candidates = set()

    for n in range(1, 128):
        candidates.add(n)

    for anchor in KNOWN_ANCHORS:
        for delta in range(-8, 9):
            value = anchor + delta
            if value > 0:
                candidates.add(value)

    for power in range(4, 54, 4):
        base = 2 ** power
        for delta in range(-4, 5):
            value = base + delta
            if value > 0:
                candidates.add(value)

    return sorted(candidates)


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    closure_result_counts: Dict[str, int] = {}

    for row in rows:
        result_type = str(row["closure_result_type"])
        closure_result_counts[result_type] = closure_result_counts.get(result_type, 0) + 1

    tested_candidate_count = len(rows)
    debt_window_count = sum(int(row["debt_window_count"]) for row in rows)
    regeneration_count = sum(int(row["regeneration_count"]) for row in rows)
    dangerous_regeneration_count = sum(int(row["dangerous_regeneration_count"]) for row in rows)
    obstruction_candidate_count = sum(int(row["obstruction_candidate_count"]) for row in rows)

    hardest_by_recovery = max(rows, key=lambda row: float(row["hardest_recovery_score"])) if rows else None

    rows_with_surplus = [row for row in rows if row["min_positive_surplus"] is not None]
    tightest_surplus_row = min(rows_with_surplus, key=lambda row: float(row["min_positive_surplus"])) if rows_with_surplus else None

    max_bad_windows_row = max(rows, key=lambda row: int(row["debt_window_count"])) if rows else None
    max_dangerous_regeneration_row = max(rows, key=lambda row: int(row["dangerous_regeneration_count"])) if rows else None

    return {
        "version": VERSION,
        "scanner": "bounded_obstruction_search_scanner",
        "search_domain": "deterministic finite candidate set: small integers, known anchors, local neighborhoods, and power-of-two neighborhoods",
        "candidate_generation_rule": "range(1,128) plus neighborhoods around known anchors plus neighborhoods around powers of two",
        "tested_candidate_count": tested_candidate_count,
        "debt_window_count": debt_window_count,
        "regeneration_count": regeneration_count,
        "dangerous_regeneration_count": dangerous_regeneration_count,
        "obstruction_candidate_count": obstruction_candidate_count,
        "closure_result_counts": closure_result_counts,
        "hardest_by_recovery": None if hardest_by_recovery is None else {
            "n0": hardest_by_recovery["n0"],
            "hardest_recovery_score": hardest_by_recovery["hardest_recovery_score"],
            "max_post_recovery_blocks": hardest_by_recovery["max_post_recovery_blocks"],
            "min_positive_surplus": hardest_by_recovery["min_positive_surplus"],
            "closure_result_type": hardest_by_recovery["closure_result_type"],
        },
        "tightest_positive_surplus": None if tightest_surplus_row is None else {
            "n0": tightest_surplus_row["n0"],
            "min_positive_surplus": tightest_surplus_row["min_positive_surplus"],
            "closure_result_type": tightest_surplus_row["closure_result_type"],
        },
        "max_bad_windows": None if max_bad_windows_row is None else {
            "n0": max_bad_windows_row["n0"],
            "debt_window_count": max_bad_windows_row["debt_window_count"],
            "closure_result_type": max_bad_windows_row["closure_result_type"],
        },
        "max_dangerous_regeneration": None if max_dangerous_regeneration_row is None else {
            "n0": max_dangerous_regeneration_row["n0"],
            "dangerous_regeneration_count": max_dangerous_regeneration_row["dangerous_regeneration_count"],
            "closure_result_type": max_dangerous_regeneration_row["closure_result_type"],
        },
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction detected in a finite domain is not the same as no obstruction can exist.",
    }


def make_certificate(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "bounded_obstruction_search_certificate",
        "search_domain": summary["search_domain"],
        "candidate_generation_rule": summary["candidate_generation_rule"],
        "tested_candidate_count": summary["tested_candidate_count"],
        "debt_window_count": summary["debt_window_count"],
        "regeneration_count": summary["regeneration_count"],
        "dangerous_regeneration_count": summary["dangerous_regeneration_count"],
        "obstruction_candidate_count": summary["obstruction_candidate_count"],
        "obstruction_detected": summary["obstruction_candidate_count"] > 0,
        "closure_result_counts": summary["closure_result_counts"],
        "hardest_by_recovery": summary["hardest_by_recovery"],
        "tightest_positive_surplus": summary["tightest_positive_surplus"],
        "max_bad_windows": summary["max_bad_windows"],
        "max_dangerous_regeneration": summary["max_dangerous_regeneration"],
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": summary["negative_result_boundary"],
        "minimum_report_fields_present": True,
        "next_recommended_version": "v2.7 Obstruction Scanner Evidence Report",
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v2.6")
    print("=" * 80)
    print("Bounded obstruction search scanner")
    print("=" * 80)
    print(f"escape threshold log2(3): {ESCAPE_THRESHOLD}")
    print(f"max odd blocks: {MAX_ODD_BLOCKS}")
    print(f"max bad window blocks: {MAX_BAD_WINDOW_BLOCKS}")
    print(f"max recovery lookahead blocks: {MAX_RECOVERY_LOOKAHEAD_BLOCKS}")
    print(f"dangerous surplus threshold: {DANGEROUS_SURPLUS_THRESHOLD}")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    candidates = candidate_numbers()
    rows = [classify_trajectory(n0) for n0 in candidates]
    summary = summarize_rows(rows)
    certificate = make_certificate(summary)

    with ROWS_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"candidate count: {summary['tested_candidate_count']}")
    print(f"debt windows: {summary['debt_window_count']}")
    print(f"regenerations: {summary['regeneration_count']}")
    print(f"dangerous regenerations: {summary['dangerous_regeneration_count']}")
    print(f"obstruction candidates: {summary['obstruction_candidate_count']}")
    print(f"obstruction detected: {certificate['obstruction_detected']}")
    print(f"proof status: {summary['proof_status']}")
    print(f"negative result boundary: {summary['negative_result_boundary']}")

    hardest = summary["hardest_by_recovery"]
    if hardest:
        print(
            "hardest by recovery: "
            f"n0={hardest['n0']} score={hardest['hardest_recovery_score']}"
        )

    tightest = summary["tightest_positive_surplus"]
    if tightest:
        print(
            "tightest positive surplus: "
            f"n0={tightest['n0']} surplus={tightest['min_positive_surplus']}"
        )

    print(f"Wrote rows to: {ROWS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
