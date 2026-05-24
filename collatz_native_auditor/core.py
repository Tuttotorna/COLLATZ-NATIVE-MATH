import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class SeedAudit:
    seed: int
    status: str
    steps: int
    odd_steps: int
    max_value: int
    peak_debt: int
    final_debt: int
    release_count: int
    strong_release_count: int
    regeneration_count: int
    max_regeneration_ratio: float
    response_delay_after_peak: Optional[int]
    recovered_below_peak: bool
    near_breach: bool
    near_breach_gap: Optional[float]
    terminal_value: int
    bounded: bool


def v2(x: int) -> int:
    if x <= 0:
        raise ValueError("v2 is defined here only for positive integers.")
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count


def collatz_odd_step(n: int) -> Tuple[int, int]:
    if n <= 0:
        raise ValueError("seed values must be positive integers")
    if n % 2 == 0:
        raise ValueError("collatz_odd_step expects an odd integer")
    x = 3 * n + 1
    a = v2(x)
    return x // (2 ** a), a


def read_seed_csv(path: str) -> List[int]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    seeds = []

    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "seed" not in reader.fieldnames:
            raise ValueError("CSV input must contain a 'seed' column.")

        for row in reader:
            raw = str(row.get("seed", "")).strip()
            if not raw:
                continue
            seed = int(raw)
            if seed <= 0:
                raise ValueError("Seed must be positive: " + str(seed))
            seeds.append(seed)

    return seeds


def generate_seeds(seed: Optional[int], start: Optional[int], end: Optional[int], input_path: Optional[str]) -> List[int]:
    modes = 0
    if seed is not None:
        modes += 1
    if input_path is not None:
        modes += 1
    if start is not None or end is not None:
        modes += 1

    if modes != 1:
        raise ValueError("Choose exactly one input mode: --seed, --start/--end, or --input.")

    if seed is not None:
        if seed <= 0:
            raise ValueError("--seed must be positive")
        return [seed]

    if input_path is not None:
        return read_seed_csv(input_path)

    if start is None or end is None:
        raise ValueError("Range mode requires both --start and --end.")
    if start <= 0 or end <= 0:
        raise ValueError("--start and --end must be positive")
    if end < start:
        raise ValueError("--end must be >= --start")

    return list(range(start, end + 1))


def audit_seed(seed: int, max_steps: int = 10000, near_breach_ratio: float = 0.98) -> SeedAudit:
    if seed <= 0:
        raise ValueError("seed must be positive")

    n = seed
    steps = 0
    odd_steps = 0
    max_value = n

    debt = 0
    peak_debt = 0
    peak_debt_step = 0

    release_count = 0
    strong_release_count = 0
    regeneration_count = 0

    max_regeneration_ratio = 0.0
    response_delay_after_peak = None
    recovered_below_peak = False
    near_breach = False
    near_breach_gap = None

    while n != 1 and steps < max_steps:
        max_value = max(max_value, n)

        if n % 2 == 0:
            n = n // 2
            debt = max(0, debt - 1)
            steps += 1

            if debt < peak_debt and response_delay_after_peak is None and peak_debt > 0:
                response_delay_after_peak = steps - peak_debt_step

            if debt < peak_debt:
                recovered_below_peak = True

            continue

        previous_debt = debt
        next_odd, a = collatz_odd_step(n)
        odd_steps += 1

        debt += 1
        if a >= 2:
            debt = max(0, debt - (a - 1))

        if a >= 2:
            release_count += 1
        if a >= 3:
            strong_release_count += 1
        if debt > previous_debt:
            regeneration_count += 1

        if peak_debt > 0:
            ratio = debt / peak_debt
            if ratio > max_regeneration_ratio:
                max_regeneration_ratio = ratio
            if ratio >= near_breach_ratio and debt < peak_debt:
                near_breach = True
                gap = 1.0 - ratio
                if near_breach_gap is None or gap < near_breach_gap:
                    near_breach_gap = gap

        if debt > peak_debt:
            peak_debt = debt
            peak_debt_step = steps
            response_delay_after_peak = None

        n = next_odd
        steps += 1
        max_value = max(max_value, n)

    bounded = n == 1
    status = "TERMINATED" if bounded else "BOUND_EXCEEDED"

    if bounded and near_breach:
        status = "TERMINATED_NEAR_BREACH"

    if not bounded:
        near_breach = True
        if near_breach_gap is None:
            near_breach_gap = 0.0

    return SeedAudit(
        seed=seed,
        status=status,
        steps=steps,
        odd_steps=odd_steps,
        max_value=max_value,
        peak_debt=peak_debt,
        final_debt=debt,
        release_count=release_count,
        strong_release_count=strong_release_count,
        regeneration_count=regeneration_count,
        max_regeneration_ratio=round(max_regeneration_ratio, 12),
        response_delay_after_peak=response_delay_after_peak,
        recovered_below_peak=recovered_below_peak,
        near_breach=near_breach,
        near_breach_gap=None if near_breach_gap is None else round(near_breach_gap, 12),
        terminal_value=n,
        bounded=bounded,
    )


def audit_many(seeds: Iterable[int], max_steps: int = 10000, near_breach_ratio: float = 0.98) -> Dict[str, Any]:
    audits = [
        audit_seed(seed=s, max_steps=max_steps, near_breach_ratio=near_breach_ratio)
        for s in seeds
    ]

    total = len(audits)
    near = [a for a in audits if a.near_breach]
    unbounded = [a for a in audits if not a.bounded]

    peak_debts = [a.peak_debt for a in audits]
    steps = [a.steps for a in audits]
    odd_steps = [a.odd_steps for a in audits]
    max_values = [a.max_value for a in audits]

    summary = {
        "total_seeds": total,
        "terminated": sum(1 for a in audits if a.bounded),
        "bound_exceeded": len(unbounded),
        "near_breach_cases": len(near),
        "near_breach_rate": (len(near) / total) if total else 0.0,
        "max_peak_debt": max(peak_debts) if peak_debts else 0,
        "max_steps": max(steps) if steps else 0,
        "max_odd_steps": max(odd_steps) if odd_steps else 0,
        "max_value_seen": max(max_values) if max_values else 0,
        "problem_solved": "Produces reproducible native Collatz trajectory audits for seeds or seed ranges.",
    }

    certificate = {
        "audit_type": "collatz_native_audit",
        "summary": summary,
        "bounded_claim": "finite run only; no proof of Collatz is claimed",
        "measurement_language": [
            "compression_debt",
            "2_adic_shadow",
            "release_events",
            "strong_release_events",
            "regeneration_events",
            "near_breach_detection",
            "recovery_after_peak",
        ],
    }

    return {
        "summary": summary,
        "certificate": certificate,
        "audits": [asdict(a) for a in audits],
    }


def write_json(path: str, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv_report(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "seed",
        "status",
        "steps",
        "odd_steps",
        "max_value",
        "peak_debt",
        "final_debt",
        "release_count",
        "strong_release_count",
        "regeneration_count",
        "max_regeneration_ratio",
        "response_delay_after_peak",
        "recovered_below_peak",
        "near_breach",
        "near_breach_gap",
        "terminal_value",
        "bounded",
    ]

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in result["audits"]:
            writer.writerow({k: row.get(k, "") for k in fields})


def html_escape(x: Any) -> str:
    return (
        str(x)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write_html_report(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    summary = result["summary"]

    rows = []
    for a in result["audits"]:
        if not a["near_breach"] and a["bounded"]:
            continue
        rows.append(
            "<tr>"
            + "<td>" + html_escape(a["seed"]) + "</td>"
            + "<td>" + html_escape(a["status"]) + "</td>"
            + "<td>" + html_escape(a["steps"]) + "</td>"
            + "<td>" + html_escape(a["peak_debt"]) + "</td>"
            + "<td>" + html_escape(a["max_regeneration_ratio"]) + "</td>"
            + "<td>" + html_escape(a["near_breach_gap"]) + "</td>"
            + "<td>" + html_escape(a["bounded"]) + "</td>"
            + "</tr>"
        )

    html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Collatz Native Audit Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 32px;
      line-height: 1.45;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 8px;
      vertical-align: top;
    }}
    th {{
      background: #f2f2f2;
    }}
    pre {{
      white-space: pre-wrap;
      background: #f7f7f7;
      padding: 12px;
      border: 1px solid #eee;
    }}
    .box {{
      background: #f8f8f8;
      padding: 16px;
      margin-bottom: 24px;
      border: 1px solid #eee;
    }}
  </style>
</head>
<body>
  <h1>Collatz Native Audit Report</h1>

  <div class="box">
    <p><b>Total seeds:</b> {total_seeds}</p>
    <p><b>Terminated:</b> {terminated}</p>
    <p><b>Bound exceeded:</b> {bound_exceeded}</p>
    <p><b>Near-breach cases:</b> {near_breach_cases}</p>
    <p><b>Near-breach rate:</b> {near_breach_rate:.6f}</p>
    <p><b>Max peak debt:</b> {max_peak_debt}</p>
    <p><b>Max steps:</b> {max_steps}</p>
    <p><b>Max value seen:</b> {max_value_seen}</p>
  </div>

  <h2>Flagged Cases</h2>

  <table>
    <tr>
      <th>Seed</th>
      <th>Status</th>
      <th>Steps</th>
      <th>Peak Debt</th>
      <th>Max Regeneration Ratio</th>
      <th>Near-Breach Gap</th>
      <th>Bounded</th>
    </tr>
    {rows}
  </table>

  <h2>Boundary</h2>
  <pre>This is a finite audit. It does not prove the Collatz conjecture.</pre>
</body>
</html>
""".format(
        total_seeds=summary["total_seeds"],
        terminated=summary["terminated"],
        bound_exceeded=summary["bound_exceeded"],
        near_breach_cases=summary["near_breach_cases"],
        near_breach_rate=summary["near_breach_rate"],
        max_peak_debt=summary["max_peak_debt"],
        max_steps=summary["max_steps"],
        max_value_seen=summary["max_value_seen"],
        rows="".join(rows),
    )

    p.write_text(html, encoding="utf-8")


def write_near_breach_jsonl(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", encoding="utf-8") as f:
        for a in result["audits"]:
            if a["near_breach"]:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")


def write_all_reports(out_dir: str, result: Dict[str, Any]) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    write_json(str(out / "report.json"), result)
    write_csv_report(str(out / "report.csv"), result)
    write_html_report(str(out / "report.html"), result)
    write_near_breach_jsonl(str(out / "near_breach_cases.jsonl"), result)
    write_json(str(out / "certificate.json"), result["certificate"])
