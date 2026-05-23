#!/usr/bin/env python3
"""
Compression Debt Machine V0.

This script is a bounded measurement builder.

It does not prove Collatz.
It does not claim Collatz is solved.
It measures compression debt, release, and cheap regeneration
inside finite odd-step windows.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

DEFAULT_MAX_ODD_SEED = 999
DEFAULT_ODD_STEPS = 80
DEFAULT_EPSILON = 0.0

LOG2_3 = math.log2(3.0)


def v2(x: int) -> int:
    """Return the exponent of 2 in x. Requires x > 0."""
    if x <= 0:
        raise ValueError("v2 requires a positive integer")

    count = 0

    while x % 2 == 0:
        x //= 2
        count += 1

    return count


def odd_step(n: int) -> tuple[int, int, float]:
    """Return next odd value, a=v2(3n+1), and exact log2 drift."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("odd_step requires a positive odd integer")

    m = 3 * n + 1
    a = v2(m)
    next_n = m // (2 ** a)
    delta = math.log2(next_n / n)

    return next_n, a, delta


@dataclass(frozen=True)
class StepRecord:
    index: int
    n: int
    next_n: int
    a: int
    delta: float
    kind: str


@dataclass(frozen=True)
class TrajectoryRecord:
    seed: int
    odd_steps: int
    terminated: bool
    final_n: int
    mean_delta: float
    cumulative_debt: float
    debt_peak: float
    min_prefix_debt: float
    max_a: int
    release_count: int
    strong_release_count: int
    cheap_chain_epsilon_0: bool
    regeneration_capable: bool


def classify_step(delta: float) -> str:
    if delta > 0:
        return "debt_creation"
    if delta < -2:
        return "strong_release"
    if delta < -1:
        return "release"
    if delta < 0:
        return "mild_discharge"
    return "balanced"


def measure_odd_trajectory(
    seed: int,
    odd_steps: int = DEFAULT_ODD_STEPS,
    epsilon: float = DEFAULT_EPSILON,
) -> tuple[TrajectoryRecord, list[StepRecord]]:
    """Measure bounded odd-step compression debt for a positive odd seed."""
    if seed <= 0 or seed % 2 == 0:
        raise ValueError("seed must be a positive odd integer")

    if odd_steps <= 0:
        raise ValueError("odd_steps must be positive")

    n = seed
    steps: list[StepRecord] = []
    deltas: list[float] = []

    prefix = 0.0
    debt_peak = 0.0
    min_prefix = 0.0

    saw_positive_before_release = False
    saw_release_after_positive = False
    regeneration_capable = False

    for i in range(odd_steps):
        if n == 1:
            break

        next_n, a, delta = odd_step(n)
        kind = classify_step(delta)

        steps.append(
            StepRecord(
                index=i,
                n=n,
                next_n=next_n,
                a=a,
                delta=delta,
                kind=kind,
            )
        )

        deltas.append(delta)
        prefix += delta

        debt_peak = max(debt_peak, prefix)
        min_prefix = min(min_prefix, prefix)

        if prefix > 0 and not saw_release_after_positive:
            saw_positive_before_release = True

        if saw_positive_before_release and delta < -1:
            saw_release_after_positive = True

        if saw_release_after_positive and prefix > 0:
            regeneration_capable = True

        n = next_n

    release_count = sum(1 for s in steps if s.delta < -1)
    strong_release_count = sum(1 for s in steps if s.delta < -2)

    if deltas:
        mean_delta = mean(deltas)
        cumulative_debt = sum(deltas)
        max_a = max(s.a for s in steps)
    else:
        mean_delta = 0.0
        cumulative_debt = 0.0
        max_a = 0

    record = TrajectoryRecord(
        seed=seed,
        odd_steps=len(steps),
        terminated=(n == 1),
        final_n=n,
        mean_delta=mean_delta,
        cumulative_debt=cumulative_debt,
        debt_peak=debt_peak,
        min_prefix_debt=min_prefix,
        max_a=max_a,
        release_count=release_count,
        strong_release_count=strong_release_count,
        cheap_chain_epsilon_0=(mean_delta >= -epsilon),
        regeneration_capable=regeneration_capable,
    )

    return record, steps


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None

    mx = mean(xs)
    my = mean(ys)

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))

    if den_x == 0 or den_y == 0:
        return None

    return num / (den_x * den_y)


def build(
    max_odd_seed: int = DEFAULT_MAX_ODD_SEED,
    odd_steps: int = DEFAULT_ODD_STEPS,
    epsilon: float = DEFAULT_EPSILON,
) -> dict:
    seeds = [n for n in range(1, max_odd_seed + 1, 2)]

    records: list[TrajectoryRecord] = []

    samples: dict[str, list[dict]] = {
        "highest_debt_peak": [],
        "longest_nonterminated": [],
        "regeneration_capable": [],
        "cheap_chain_epsilon_0": [],
    }

    full_step_samples: dict[str, list[dict]] = {}

    for seed in seeds:
        record, steps = measure_odd_trajectory(seed, odd_steps=odd_steps, epsilon=epsilon)
        records.append(record)

        if record.regeneration_capable and len(samples["regeneration_capable"]) < 10:
            samples["regeneration_capable"].append(asdict(record))

        if record.cheap_chain_epsilon_0 and len(samples["cheap_chain_epsilon_0"]) < 10:
            samples["cheap_chain_epsilon_0"].append(asdict(record))

        if record.debt_peak > 0 and len(full_step_samples) < 10:
            full_step_samples[str(seed)] = [asdict(s) for s in steps[:20]]

    highest_debt = sorted(records, key=lambda r: r.debt_peak, reverse=True)[:10]
    longest_nonterminated = sorted(
        records,
        key=lambda r: (not r.terminated, r.odd_steps, r.debt_peak),
        reverse=True,
    )[:10]

    samples["highest_debt_peak"] = [asdict(r) for r in highest_debt]
    samples["longest_nonterminated"] = [asdict(r) for r in longest_nonterminated]

    debt_peaks = [r.debt_peak for r in records]
    max_as = [float(r.max_a) for r in records]
    release_counts = [float(r.release_count) for r in records]
    strong_release_counts = [float(r.strong_release_count) for r in records]

    terminated_count = sum(1 for r in records if r.terminated)
    cheap_count = sum(1 for r in records if r.cheap_chain_epsilon_0)
    regen_count = sum(1 for r in records if r.regeneration_capable)

    summary = {
        "version": "v4.8",
        "machine": "Compression Debt Machine V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "max_odd_seed": max_odd_seed,
            "odd_steps": odd_steps,
            "epsilon": epsilon,
            "log2_3": LOG2_3,
        },
        "counts": {
            "odd_seeds_measured": len(records),
            "terminated_within_bound": terminated_count,
            "not_terminated_within_bound": len(records) - terminated_count,
            "cheap_chain_epsilon_0_count": cheap_count,
            "regeneration_capable_count": regen_count,
        },
        "aggregate": {
            "mean_delta_mean": mean([r.mean_delta for r in records]) if records else 0.0,
            "cumulative_debt_mean": mean([r.cumulative_debt for r in records]) if records else 0.0,
            "debt_peak_mean": mean(debt_peaks) if records else 0.0,
            "max_debt_peak": max(debt_peaks) if records else 0.0,
            "max_a_seen": max([r.max_a for r in records]) if records else 0,
            "debt_peak_vs_max_a_pearson": pearson(debt_peaks, max_as),
            "debt_peak_vs_release_count_pearson": pearson(debt_peaks, release_counts),
            "debt_peak_vs_strong_release_count_pearson": pearson(debt_peaks, strong_release_counts),
        },
        "samples": samples,
        "step_samples": full_step_samples,
        "interpretation": {
            "bounded_claim": "The machine measures bounded compression debt, release, and cheap regeneration.",
            "native_reduction": "A divergent Collatz behavior would require unbounded persistence of low-compression regeneration grammar.",
            "main_falsifiable_question": "Do high-debt windows tend to be followed by stronger release events?",
        },
        "boundary": {
            "proof_status": "not_a_proof",
            "collatz_status": "not_claimed_solved",
            "theorem_status": "no_theorem_claimed",
            "global_closure_status": "not_claimed",
            "global_invariant_status": "not_claimed",
            "obstruction_status": "not_claimed",
            "bounded_evidence_status": "measurement_only",
        },
    }

    return summary


def write_markdown(summary: dict) -> str:
    counts = summary["counts"]
    aggregate = summary["aggregate"]
    params = summary["parameters"]

    def fmt(x):
        if x is None:
            return "None"
        if isinstance(x, float):
            return f"{x:.12f}"
        return str(x)

    lines = []

    lines.append("# Compression Debt Machine V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded measurement result.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("It is not a theorem layer.")
    lines.append("")
    lines.append("## Parameters")
    lines.append("")
    lines.append(f"- max_odd_seed: `{params['max_odd_seed']}`")
    lines.append(f"- odd_steps: `{params['odd_steps']}`")
    lines.append(f"- epsilon: `{params['epsilon']}`")
    lines.append(f"- log2_3: `{fmt(params['log2_3'])}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")

    for key, value in counts.items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")
    lines.append("## Aggregate measurements")
    lines.append("")

    for key, value in aggregate.items():
        lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Highest debt-peak samples")
    lines.append("")

    for item in summary["samples"]["highest_debt_peak"][:10]:
        lines.append(
            f"- seed `{item['seed']}`: "
            f"debt_peak=`{fmt(item['debt_peak'])}`, "
            f"mean_delta=`{fmt(item['mean_delta'])}`, "
            f"max_a=`{item['max_a']}`, "
            f"release_count=`{item['release_count']}`, "
            f"terminated=`{item['terminated']}`"
        )

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The machine makes the debt/release vocabulary computable.")
    lines.append("")
    lines.append("A possible divergent Collatz behavior would require more than local growth.")
    lines.append("")
    lines.append("It would require persistent low-compression regeneration.")
    lines.append("")
    lines.append("The V0 machine measures bounded approximations of that requirement.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")

    for key, value in summary["boundary"].items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")

    return "\n".join(lines)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    summary = build()

    json_path = RESULTS / "compression_debt_machine_v0.json"
    md_path = RESULTS / "compression_debt_machine_v0.md"
    cert_path = RESULTS / "compression_debt_machine_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v4.8",
        "artifact": "Compression Debt Machine V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "boundary": summary["boundary"],
    }

    cert_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"WROTE: {json_path}")
    print(f"WROTE: {md_path}")
    print(f"WROTE: {cert_path}")
    print("")
    print("BOUNDARY:")

    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
