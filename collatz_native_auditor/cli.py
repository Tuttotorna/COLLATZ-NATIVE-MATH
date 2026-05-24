import argparse
import sys
from pathlib import Path

from .core import audit_many, generate_seeds, write_all_reports


def main():
    parser = argparse.ArgumentParser(
        prog="collatz-native-audit",
        description="Audit Collatz trajectories using native structural measurements.",
    )

    parser.add_argument("--seed", type=int, default=None, help="Audit one positive seed.")
    parser.add_argument("--start", type=int, default=None, help="Start seed for range mode.")
    parser.add_argument("--end", type=int, default=None, help="End seed for range mode.")
    parser.add_argument("--input", default=None, help="CSV file with a 'seed' column.")
    parser.add_argument("--out-dir", default="collatz_native_report", help="Output directory.")
    parser.add_argument("--max-steps", type=int, default=10000, help="Maximum Collatz steps per seed.")
    parser.add_argument("--near-breach-ratio", type=float, default=0.98, help="Near-breach threshold ratio.")
    parser.add_argument("--fail-on-near-breach", action="store_true", help="Exit with code 2 if near-breach cases are found.")
    parser.add_argument("--fail-on-bound-exceeded", action="store_true", help="Exit with code 3 if any seed exceeds max steps.")

    args = parser.parse_args()

    seeds = generate_seeds(
        seed=args.seed,
        start=args.start,
        end=args.end,
        input_path=args.input,
    )

    result = audit_many(
        seeds=seeds,
        max_steps=args.max_steps,
        near_breach_ratio=args.near_breach_ratio,
    )

    write_all_reports(args.out_dir, result)

    s = result["summary"]

    print("")
    print("COLLATZ NATIVE AUDIT")
    print("====================")
    print(f"total_seeds:         {s['total_seeds']}")
    print(f"terminated:          {s['terminated']}")
    print(f"bound_exceeded:      {s['bound_exceeded']}")
    print(f"near_breach_cases:   {s['near_breach_cases']}")
    print(f"near_breach_rate:    {s['near_breach_rate']:.6f}")
    print(f"max_peak_debt:       {s['max_peak_debt']}")
    print(f"max_steps:           {s['max_steps']}")
    print(f"max_odd_steps:       {s['max_odd_steps']}")
    print(f"max_value_seen:      {s['max_value_seen']}")
    print("")
    print(f"WROTE: {Path(args.out_dir) / 'report.json'}")
    print(f"WROTE: {Path(args.out_dir) / 'report.csv'}")
    print(f"WROTE: {Path(args.out_dir) / 'report.html'}")
    print(f"WROTE: {Path(args.out_dir) / 'near_breach_cases.jsonl'}")
    print(f"WROTE: {Path(args.out_dir) / 'certificate.json'}")
    print("")

    if args.fail_on_bound_exceeded and s["bound_exceeded"] > 0:
        sys.exit(3)

    if args.fail_on_near_breach and s["near_breach_cases"] > 0:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
