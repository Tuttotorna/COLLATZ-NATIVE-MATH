from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

VERSION = "v1.3"
ESCAPE_THRESHOLD = math.log2(3)
COMPARISON_TOLERANCE = 1e-12

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

ROWS_PATH = RESULTS / "compensation_law_candidate_rows.jsonl"
SUMMARY_PATH = RESULTS / "compensation_law_candidate_summary.json"
CERTIFICATE_PATH = RESULTS / "compensation_law_candidate_certificate.json"

PREVIOUS_CRITICAL_N0 = 9780657630


def line() -> None:
    print("=" * 80)


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 expects a positive integer.")
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    return count


def odd_start(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive.")
    while n % 2 == 0:
        n //= 2
    return n


def odd_blocks(n0: int, max_blocks: int = 10000) -> List[Dict[str, int]]:
    n = odd_start(n0)
    rows: List[Dict[str, int]] = []

    # Convention:
    # - n0 = 1 has one native block: 1 -> 1 with a = v2(4) = 2.
    # - for n0 > 1, stop immediately after the first block whose next odd value is 1.
    #   Do not append an extra artificial terminal 1 -> 1 block.
    for block_index in range(max_blocks):
        a = v2(3 * n + 1)
        next_n = (3 * n + 1) // (2 ** a)

        rows.append(
            {
                "block": block_index,
                "n": n,
                "a": a,
                "next": next_n,
            }
        )

        if next_n == 1:
            return rows

        n = next_n

    raise RuntimeError(f"max_blocks exceeded for n0={n0}")


def candidate_frontier() -> List[int]:
    candidates = set()

    seeds = [
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
        626331,
        1117065,
        1501353,
        1723519,
        2298025,
        3542887,
    ]

    for n in seeds:
        candidates.add(n)

    for k in range(2, 54):
        base = (2 ** k) - 1
        for delta in (-2, 0, 2):
            n = base + delta
            if n > 0:
                candidates.add(n)

    centers = [
        626331,
        1117065,
        3542887,
        9780657630,
        989345275647,
    ]

    for center in centers:
        for radius_power in range(0, 13):
            step = 2 ** radius_power
            for delta in (-step, step):
                n = center + delta
                if n > 0:
                    candidates.add(n)

    return sorted(candidates)


def prefix_sums(values: List[int]) -> List[int]:
    sums = [0]
    total = 0
    for value in values:
        total += value
        sums.append(total)
    return sums


def window_sum(prefix: List[int], start: int, end_exclusive: int) -> int:
    return prefix[end_exclusive] - prefix[start]


def window_avg(prefix: List[int], start: int, end_exclusive: int) -> float:
    length = end_exclusive - start
    if length <= 0:
        raise ValueError("empty window")
    return window_sum(prefix, start, end_exclusive) / length


def is_bad_window(prefix: List[int], start: int, end_exclusive: int) -> bool:
    return window_avg(prefix, start, end_exclusive) < ESCAPE_THRESHOLD - COMPARISON_TOLERANCE


def find_maximal_bad_windows(debt_word: List[int]) -> List[dict]:
    prefix = prefix_sums(debt_word)
    n = len(debt_word)
    bad = []

    for start in range(n):
        best_end = None
        best_avg = None

        for end in range(start + 1, n + 1):
            avg = window_avg(prefix, start, end)
            if avg < ESCAPE_THRESHOLD - COMPARISON_TOLERANCE:
                best_end = end
                best_avg = avg

        if best_end is not None:
            previous_bad = False
            if start > 0:
                previous_bad = is_bad_window(prefix, start - 1, best_end)

            next_bad = False
            if best_end < n:
                next_bad = is_bad_window(prefix, start, best_end + 1)

            if not previous_bad and not next_bad:
                bad.append(
                    {
                        "bad_start": start,
                        "bad_end": best_end - 1,
                        "bad_blocks": best_end - start,
                        "bad_debt": window_sum(prefix, start, best_end),
                        "bad_average_debt": best_avg,
                        "bad_deficit": ESCAPE_THRESHOLD - best_avg,
                    }
                )

    unique = {}
    for row in bad:
        key = (row["bad_start"], row["bad_end"])
        unique[key] = row

    return [unique[key] for key in sorted(unique)]


def find_post_bad_recovery(debt_word: List[int], bad_start: int, bad_end: int) -> Optional[dict]:
    prefix = prefix_sums(debt_word)
    n = len(debt_word)
    post_start = bad_end + 1

    if post_start >= n:
        return None

    for recovery_end in range(post_start, n):
        combined_avg = window_avg(prefix, bad_start, recovery_end + 1)
        post_avg = window_avg(prefix, post_start, recovery_end + 1)

        if combined_avg >= ESCAPE_THRESHOLD - COMPARISON_TOLERANCE:
            return {
                "post_start": post_start,
                "post_end": recovery_end,
                "post_blocks": recovery_end - post_start + 1,
                "post_debt": window_sum(prefix, post_start, recovery_end + 1),
                "post_average_debt": post_avg,
                "combined_start": bad_start,
                "combined_end": recovery_end,
                "combined_blocks": recovery_end - bad_start + 1,
                "combined_debt": window_sum(prefix, bad_start, recovery_end + 1),
                "combined_average_debt": combined_avg,
                "combined_surplus": combined_avg - ESCAPE_THRESHOLD,
            }

    return None


def analyze_one(n0: int) -> dict:
    blocks = odd_blocks(n0)
    debt_word = [row["a"] for row in blocks]
    trajectory_total_debt = sum(debt_word)
    trajectory_average_debt = trajectory_total_debt / len(debt_word)

    bad_windows = find_maximal_bad_windows(debt_word)

    recovered = 0
    unrecovered = 0
    recovery_rows = []

    for bad in bad_windows:
        recovery = find_post_bad_recovery(
            debt_word,
            bad_start=bad["bad_start"],
            bad_end=bad["bad_end"],
        )

        if recovery is None:
            unrecovered += 1
            recovery_rows.append(
                {
                    **bad,
                    "recovered": False,
                    "post_start": None,
                    "post_end": None,
                    "post_blocks": None,
                    "combined_surplus": None,
                    "hardness_score": None,
                }
            )
        else:
            recovered += 1

            hardness_score = (
                bad["bad_deficit"]
                * (bad["bad_blocks"] + recovery["post_blocks"])
                / max(recovery["combined_surplus"], 1e-15)
            )

            recovery_rows.append(
                {
                    **bad,
                    **recovery,
                    "recovered": True,
                    "hardness_score": hardness_score,
                }
            )

    hardest_recovery = None
    recovered_rows = [row for row in recovery_rows if row["recovered"]]
    if recovered_rows:
        hardest_recovery = max(recovered_rows, key=lambda row: row["hardness_score"])

    max_post_recovery_blocks = 0
    min_combined_surplus = None
    max_hardness_score = 0.0

    if recovered_rows:
        max_post_recovery_blocks = max(row["post_blocks"] for row in recovered_rows)
        min_combined_surplus = min(row["combined_surplus"] for row in recovered_rows)
        max_hardness_score = max(row["hardness_score"] for row in recovered_rows)

    return {
        "version": VERSION,
        "n0": n0,
        "odd_start": odd_start(n0),
        "reaches_1": blocks[-1]["next"] == 1,
        "odd_blocks": len(blocks),
        "trajectory_total_debt": trajectory_total_debt,
        "trajectory_average_debt": trajectory_average_debt,
        "trajectory_average_above_threshold": trajectory_average_debt >= ESCAPE_THRESHOLD,
        "bad_windows": len(bad_windows),
        "recovered_bad_windows": recovered,
        "unrecovered_bad_windows": unrecovered,
        "all_bad_windows_recovered": unrecovered == 0,
        "max_post_recovery_blocks": max_post_recovery_blocks,
        "min_combined_surplus": min_combined_surplus,
        "max_hardness_score": max_hardness_score,
        "hardest_recovery": hardest_recovery,
        "recovery_rows": recovery_rows,
    }


def main() -> None:
    RESULTS.mkdir(exist_ok=True)

    line()
    print("COLLATZ-NATIVE-MATH v1.3")
    line()
    print("Compensation law candidate finite scan")
    print(f"escape threshold log2(3): {ESCAPE_THRESHOLD:.15f}")
    print(f"comparison tolerance: {COMPARISON_TOLERANCE}")
    line()

    candidates = candidate_frontier()
    rows = []

    for n0 in candidates:
        row = analyze_one(n0)
        rows.append(row)
        print(
            "n0: {n0} odd_blocks: {odd_blocks} bad_windows: {bad_windows} "
            "recovered: {recovered_bad_windows} unrecovered: {unrecovered_bad_windows} "
            "max_post_recovery_blocks: {max_post_recovery_blocks} "
            "min_surplus: {min_combined_surplus} hardness: {max_hardness_score:.6f}".format(**row)
        )

    unrecovered_rows = [row for row in rows if row["unrecovered_bad_windows"] > 0]
    rows_with_bad = [row for row in rows if row["bad_windows"] > 0]

    hardest = max(rows, key=lambda row: row["max_hardness_score"])
    longest = max(rows, key=lambda row: row["max_post_recovery_blocks"])
    tightest_candidates = [
        row for row in rows
        if row["min_combined_surplus"] is not None
    ]
    tightest = min(tightest_candidates, key=lambda row: row["min_combined_surplus"]) if tightest_candidates else None

    total_bad_windows = sum(row["bad_windows"] for row in rows)
    total_recovered = sum(row["recovered_bad_windows"] for row in rows)
    total_unrecovered = sum(row["unrecovered_bad_windows"] for row in rows)

    summary = {
        "version": VERSION,
        "candidate_count": len(candidates),
        "escape_threshold_log2_3": ESCAPE_THRESHOLD,
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "total_bad_windows": total_bad_windows,
        "total_recovered_bad_windows": total_recovered,
        "total_unrecovered_bad_windows": total_unrecovered,
        "all_bad_windows_recovered": total_unrecovered == 0,
        "cases_with_bad_windows": len(rows_with_bad),
        "cases_with_unrecovered_bad_windows": len(unrecovered_rows),
        "hardest_case": {
            "n0": hardest["n0"],
            "odd_blocks": hardest["odd_blocks"],
            "bad_windows": hardest["bad_windows"],
            "max_post_recovery_blocks": hardest["max_post_recovery_blocks"],
            "min_combined_surplus": hardest["min_combined_surplus"],
            "max_hardness_score": hardest["max_hardness_score"],
            "hardest_recovery": hardest["hardest_recovery"],
        },
        "longest_recovery_case": {
            "n0": longest["n0"],
            "odd_blocks": longest["odd_blocks"],
            "bad_windows": longest["bad_windows"],
            "max_post_recovery_blocks": longest["max_post_recovery_blocks"],
            "min_combined_surplus": longest["min_combined_surplus"],
            "max_hardness_score": longest["max_hardness_score"],
            "hardest_recovery": longest["hardest_recovery"],
        },
        "tightest_surplus_case": None if tightest is None else {
            "n0": tightest["n0"],
            "odd_blocks": tightest["odd_blocks"],
            "bad_windows": tightest["bad_windows"],
            "max_post_recovery_blocks": tightest["max_post_recovery_blocks"],
            "min_combined_surplus": tightest["min_combined_surplus"],
            "max_hardness_score": tightest["max_hardness_score"],
            "hardest_recovery": tightest["hardest_recovery"],
        },
    }

    certificate = {
        "version": VERSION,
        "certificate_type": "finite_compensation_law_candidate_certificate",
        "claim_tested": (
            "Every detected maximal bad debt window in the selected finite frontier "
            "has a later finite recovery window whose combined average debt reaches "
            "or exceeds log2(3)."
        ),
        "candidate_count": len(candidates),
        "total_bad_windows": total_bad_windows,
        "total_recovered_bad_windows": total_recovered,
        "total_unrecovered_bad_windows": total_unrecovered,
        "all_bad_windows_recovered": total_unrecovered == 0,
        "escape_threshold_log2_3": ESCAPE_THRESHOLD,
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "hardest_case_n0": summary["hardest_case"]["n0"],
        "hardest_case_score": summary["hardest_case"]["max_hardness_score"],
        "longest_recovery_case_n0": summary["longest_recovery_case"]["n0"],
        "longest_recovery_blocks": summary["longest_recovery_case"]["max_post_recovery_blocks"],
        "tightest_surplus_case_n0": None if tightest is None else tightest["n0"],
        "tightest_surplus": None if tightest is None else tightest["min_combined_surplus"],
        "meaning": (
            "This supports the compensation-law candidate on the selected finite frontier. "
            "It is a falsifiable computational certificate, not a proof."
        ),
        "limits": (
            "The scan is finite. A proof would require showing that every structurally possible "
            "bad window must admit finite compensation by arithmetic necessity."
        ),
    }

    write_jsonl(ROWS_PATH, rows)
    write_json(SUMMARY_PATH, summary)
    write_json(CERTIFICATE_PATH, certificate)

    line()
    print("Compensation law candidate summary")
    line()
    print(f"candidate count: {len(candidates)}")
    print(f"total bad windows: {total_bad_windows}")
    print(f"total recovered bad windows: {total_recovered}")
    print(f"total unrecovered bad windows: {total_unrecovered}")
    print(f"all bad windows recovered: {str(total_unrecovered == 0).lower()}")
    print(
        "hardest case: n0={n0} hardness={hardness:.6f}".format(
            n0=summary["hardest_case"]["n0"],
            hardness=summary["hardest_case"]["max_hardness_score"],
        )
    )
    print(
        "longest recovery: n0={n0} blocks={blocks}".format(
            n0=summary["longest_recovery_case"]["n0"],
            blocks=summary["longest_recovery_case"]["max_post_recovery_blocks"],
        )
    )
    print(f"Wrote rows to: {ROWS_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    line()


if __name__ == "__main__":
    main()
