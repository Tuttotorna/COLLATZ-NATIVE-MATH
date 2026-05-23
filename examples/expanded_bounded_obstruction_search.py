#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v2.8

Expanded Bounded Obstruction Search.

This is not brute force.
This scanner expands around near-obstruction evidence from v2.6 and v2.7.

It searches for obstruction-preserving regeneration, not merely:
- long trajectories
- high hardness
- many bad windows
- tight surplus
- repeated regeneration

It does not prove the Collatz conjecture.
It does not prove global closure.
It emits bounded evidence only.
"""

from __future__ import annotations

import bisect
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VERSION = "v2.8"
SOURCE_VERSION = "v2.6/v2.7"

ESCAPE_THRESHOLD = math.log2(3)

MAX_ODD_BLOCKS = 4096
MAX_BAD_WINDOW_BLOCKS = 64
MAX_RECOVERY_LOOKAHEAD_BLOCKS = 384
DANGEROUS_SURPLUS_THRESHOLD = 1e-3
MAX_EXPANDED_CANDIDATES = 320

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

V26_ROWS_PATH = RESULTS_DIR / "bounded_obstruction_search_rows.jsonl"
V26_CERTIFICATE_PATH = RESULTS_DIR / "bounded_obstruction_search_certificate.json"
V27_CERTIFICATE_PATH = RESULTS_DIR / "obstruction_scanner_evidence_certificate.json"

ROWS_PATH = RESULTS_DIR / "expanded_bounded_obstruction_search_rows.jsonl"
SUMMARY_PATH = RESULTS_DIR / "expanded_bounded_obstruction_search_summary.json"
CERTIFICATE_PATH = RESULTS_DIR / "expanded_bounded_obstruction_search_certificate.json"


BASE_ANCHORS = [
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


def odd_block_sequence(n0: int, max_odd_blocks: int = MAX_ODD_BLOCKS) -> Tuple[List[int], bool]:
    if n0 <= 0:
        raise ValueError("n0 must be positive")

    n = odd_part(n0)
    discharges: List[int] = []

    for _ in range(max_odd_blocks):
        if n == 1:
            return discharges, True

        expanded = 3 * n + 1
        discharge = v2(expanded)
        n = expanded // (2 ** discharge)
        discharges.append(discharge)

    return discharges, False


def prefix_sums(values: List[int]) -> List[int]:
    prefix = [0]
    total = 0
    for value in values:
        total += value
        prefix.append(total)
    return prefix


def interval_sum(prefix: List[int], start: int, end: int) -> int:
    return prefix[end] - prefix[start]


def interval_average(prefix: List[int], start: int, end: int) -> float:
    blocks = end - start
    if blocks <= 0:
        raise ValueError("empty interval")
    return interval_sum(prefix, start, end) / blocks


def detect_bad_windows(discharges: List[int]) -> List[Dict[str, Any]]:
    bad_windows: List[Dict[str, Any]] = []
    prefix = prefix_sums(discharges)
    total = len(discharges)

    for start in range(total):
        stop_limit = min(total, start + MAX_BAD_WINDOW_BLOCKS)
        for end in range(start + 1, stop_limit + 1):
            blocks = end - start
            avg = interval_average(prefix, start, end)
            if avg < ESCAPE_THRESHOLD:
                bad_windows.append(
                    {
                        "start": start,
                        "end": end,
                        "blocks": blocks,
                        "average_discharge": avg,
                        "debt": ESCAPE_THRESHOLD * blocks - interval_sum(prefix, start, end),
                        "deficit": ESCAPE_THRESHOLD - avg,
                    }
                )

    return bad_windows


def find_compensation(
    discharges: List[int],
    prefix: List[int],
    bad_window: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    start = int(bad_window["start"])
    bad_end = int(bad_window["end"])
    total = len(discharges)
    recovery_limit = min(total, bad_end + MAX_RECOVERY_LOOKAHEAD_BLOCKS)

    for combined_end in range(bad_end + 1, recovery_limit + 1):
        avg = interval_average(prefix, start, combined_end)
        surplus = avg - ESCAPE_THRESHOLD

        if surplus > 0:
            return {
                "recovered": True,
                "combined_start": start,
                "combined_end": combined_end,
                "combined_blocks": combined_end - start,
                "post_blocks": combined_end - bad_end,
                "combined_average_discharge": avg,
                "combined_surplus": surplus,
            }

    return None


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def select_near_obstruction_seeds() -> List[int]:
    seeds = set(BASE_ANCHORS)
    rows = load_jsonl(V26_ROWS_PATH)

    if not rows:
        return sorted(seeds)

    by_dangerous = sorted(
        rows,
        key=lambda row: (
            int(row.get("dangerous_regeneration_count", 0)),
            int(row.get("regeneration_count", 0)),
            int(row.get("debt_window_count", 0)),
        ),
        reverse=True,
    )

    by_debt_windows = sorted(
        rows,
        key=lambda row: int(row.get("debt_window_count", 0)),
        reverse=True,
    )

    by_recovery = sorted(
        rows,
        key=lambda row: float(row.get("hardest_recovery_score", 0.0)),
        reverse=True,
    )

    rows_with_surplus = [
        row for row in rows if row.get("min_positive_surplus") is not None
    ]

    by_tight_surplus = sorted(
        rows_with_surplus,
        key=lambda row: float(row.get("min_positive_surplus")),
    )

    for group in [by_dangerous[:20], by_debt_windows[:20], by_recovery[:20], by_tight_surplus[:20]]:
        for row in group:
            n0 = int(row["n0"])
            if n0 > 0:
                seeds.add(n0)

    return sorted(seeds)


def expanded_candidate_numbers() -> List[int]:
    seeds = select_near_obstruction_seeds()
    candidates = set()

    local_offsets = list(range(-16, 17))
    wider_offsets = [
        -1024,
        -512,
        -256,
        -128,
        -64,
        -32,
        32,
        64,
        128,
        256,
        512,
        1024,
    ]

    for seed in seeds:
        for delta in local_offsets:
            value = seed + delta
            if value > 0:
                candidates.add(value)

        for delta in wider_offsets:
            value = seed + delta
            if value > 0:
                candidates.add(value)

        if seed > 4:
            candidates.add(seed * 2 - 1)
            candidates.add(seed * 2 + 1)

    for power in range(8, 64, 4):
        base = 2 ** power
        for delta in range(-8, 9):
            value = base + delta
            if value > 0:
                candidates.add(value)

    ordered = sorted(candidates)

    if len(ordered) <= MAX_EXPANDED_CANDIDATES:
        return ordered

    priority = set(BASE_ANCHORS)
    for seed in seeds:
        for delta in range(-8, 9):
            value = seed + delta
            if value > 0:
                priority.add(value)

    priority_ordered = [n for n in sorted(priority) if n in candidates]
    remainder = [n for n in ordered if n not in priority]

    selected = priority_ordered[:MAX_EXPANDED_CANDIDATES]
    remaining_slots = MAX_EXPANDED_CANDIDATES - len(selected)

    if remaining_slots > 0:
        step = max(1, len(remainder) // remaining_slots)
        selected.extend(remainder[::step][:remaining_slots])

    return sorted(set(selected))


def classify_trajectory(n0: int) -> Dict[str, Any]:
    discharges, reaches_1 = odd_block_sequence(n0)
    prefix = prefix_sums(discharges)
    bad_windows = detect_bad_windows(discharges)
    bad_starts = sorted(int(item["start"]) for item in bad_windows)

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
        recovery = find_compensation(discharges, prefix, bad)

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
        score = (int(bad["blocks"]) * max(1, post_blocks)) / max(surplus, 1e-12)
        if score > hardest_recovery_score:
            hardest_recovery_score = score

        recovery_end = int(recovery["combined_end"])
        regen_index = bisect.bisect_left(bad_starts, recovery_end)
        has_regeneration = regen_index < len(bad_starts)

        if has_regeneration:
            regeneration_count += 1

            dangerous = (
                surplus < DANGEROUS_SURPLUS_THRESHOLD
                or post_blocks >= 32
                or deficit < 1e-3
            )

            if dangerous:
                dangerous_regeneration_count += 1

                if len(sample_dangerous_regenerations) < 5:
                    regen_start = bad_starts[regen_index]
                    sample_dangerous_regenerations.append(
                        {
                            "bad_start": bad["start"],
                            "bad_end": bad["end"],
                            "recovery_end": recovery_end,
                            "post_recovery_blocks": post_blocks,
                            "combined_surplus": surplus,
                            "regeneration_start": regen_start,
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
        "source_version": SOURCE_VERSION,
        "n0": n0,
        "odd_start": odd_part(n0),
        "reaches_1": reaches_1,
        "odd_blocks": len(discharges),
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


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    closure_result_counts: Dict[str, int] = {}
    for row in rows:
        result_type = str(row["closure_result_type"])
        closure_result_counts[result_type] = closure_result_counts.get(result_type, 0) + 1

    rows_with_surplus = [row for row in rows if row["min_positive_surplus"] is not None]

    hardest_by_recovery = max(rows, key=lambda row: float(row["hardest_recovery_score"])) if rows else None
    tightest_surplus = min(rows_with_surplus, key=lambda row: float(row["min_positive_surplus"])) if rows_with_surplus else None
    max_debt_windows = max(rows, key=lambda row: int(row["debt_window_count"])) if rows else None
    max_dangerous_regeneration = max(rows, key=lambda row: int(row["dangerous_regeneration_count"])) if rows else None

    obstruction_candidate_count = sum(int(row["obstruction_candidate_count"]) for row in rows)

    if obstruction_candidate_count > 0:
        native_interpretation = "OBSTRUCTION_CANDIDATE_DETECTED_IN_EXPANDED_BOUNDED_SEARCH"
    elif sum(int(row["dangerous_regeneration_count"]) for row in rows) > 0:
        native_interpretation = "DANGEROUS_REGENERATION_FOUND_BUT_NO_OBSTRUCTION_CANDIDATE"
    else:
        native_interpretation = "NO_OBSTRUCTION_SIGNATURE_DETECTED_IN_EXPANDED_BOUND"

    return {
        "version": VERSION,
        "scanner": "expanded_bounded_obstruction_search",
        "source_version": SOURCE_VERSION,
        "expansion_strategy": "targeted expansion around near-obstruction cases from prior bounded evidence",
        "search_domain": "finite targeted expansion around v2.6/v2.7 stress cases, known anchors, and power-of-two neighborhoods",
        "tested_candidate_count": len(rows),
        "debt_window_count": sum(int(row["debt_window_count"]) for row in rows),
        "regeneration_count": sum(int(row["regeneration_count"]) for row in rows),
        "dangerous_regeneration_count": sum(int(row["dangerous_regeneration_count"]) for row in rows),
        "obstruction_candidate_count": obstruction_candidate_count,
        "obstruction_detected": obstruction_candidate_count > 0,
        "closure_result_counts": closure_result_counts,
        "native_interpretation": native_interpretation,
        "hardest_by_recovery": None if hardest_by_recovery is None else {
            "n0": hardest_by_recovery["n0"],
            "hardest_recovery_score": hardest_by_recovery["hardest_recovery_score"],
            "max_post_recovery_blocks": hardest_by_recovery["max_post_recovery_blocks"],
            "min_positive_surplus": hardest_by_recovery["min_positive_surplus"],
            "closure_result_type": hardest_by_recovery["closure_result_type"],
        },
        "tightest_positive_surplus": None if tightest_surplus is None else {
            "n0": tightest_surplus["n0"],
            "min_positive_surplus": tightest_surplus["min_positive_surplus"],
            "closure_result_type": tightest_surplus["closure_result_type"],
        },
        "max_debt_windows": None if max_debt_windows is None else {
            "n0": max_debt_windows["n0"],
            "debt_window_count": max_debt_windows["debt_window_count"],
            "closure_result_type": max_debt_windows["closure_result_type"],
        },
        "max_dangerous_regeneration": None if max_dangerous_regeneration is None else {
            "n0": max_dangerous_regeneration["n0"],
            "dangerous_regeneration_count": max_dangerous_regeneration["dangerous_regeneration_count"],
            "closure_result_type": max_dangerous_regeneration["closure_result_type"],
        },
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction detected in a finite expanded bounded domain is not the same as no obstruction can exist.",
        "next_recommended_version": "v2.9 Shadow Persistence Instrumentation",
    }


def make_certificate(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "expanded_bounded_obstruction_search_certificate",
        "source_version": SOURCE_VERSION,
        "expansion_strategy": summary["expansion_strategy"],
        "search_domain": summary["search_domain"],
        "tested_candidate_count": summary["tested_candidate_count"],
        "debt_window_count": summary["debt_window_count"],
        "regeneration_count": summary["regeneration_count"],
        "dangerous_regeneration_count": summary["dangerous_regeneration_count"],
        "obstruction_candidate_count": summary["obstruction_candidate_count"],
        "obstruction_detected": summary["obstruction_detected"],
        "native_interpretation": summary["native_interpretation"],
        "closure_result_counts": summary["closure_result_counts"],
        "hardest_by_recovery": summary["hardest_by_recovery"],
        "tightest_positive_surplus": summary["tightest_positive_surplus"],
        "max_debt_windows": summary["max_debt_windows"],
        "max_dangerous_regeneration": summary["max_dangerous_regeneration"],
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": summary["negative_result_boundary"],
        "next_recommended_version": summary["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v2.8")
    print("=" * 80)
    print("Expanded Bounded Obstruction Search")
    print("=" * 80)
    print(f"escape threshold log2(3): {ESCAPE_THRESHOLD}")
    print(f"max odd blocks: {MAX_ODD_BLOCKS}")
    print(f"max bad window blocks: {MAX_BAD_WINDOW_BLOCKS}")
    print(f"max recovery lookahead blocks: {MAX_RECOVERY_LOOKAHEAD_BLOCKS}")
    print(f"dangerous surplus threshold: {DANGEROUS_SURPLUS_THRESHOLD}")
    print(f"max expanded candidates: {MAX_EXPANDED_CANDIDATES}")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    candidates = expanded_candidate_numbers()
    rows = [classify_trajectory(n0) for n0 in candidates]

    summary = summarize_rows(rows)
    certificate = make_certificate(summary)

    with ROWS_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"tested_candidate_count: {summary['tested_candidate_count']}")
    print(f"debt_window_count: {summary['debt_window_count']}")
    print(f"regeneration_count: {summary['regeneration_count']}")
    print(f"dangerous_regeneration_count: {summary['dangerous_regeneration_count']}")
    print(f"obstruction_candidate_count: {summary['obstruction_candidate_count']}")
    print(f"obstruction_detected: {summary['obstruction_detected']}")
    print(f"native_interpretation: {summary['native_interpretation']}")
    print(f"proof_status: {summary['proof_status']}")
    print(f"negative_result_boundary: {summary['negative_result_boundary']}")

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
