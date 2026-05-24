import csv
import json
import subprocess
import sys

from collatz_native_auditor.core import (
    audit_many,
    audit_seed,
    collatz_odd_step,
    generate_seeds,
    read_seed_csv,
    v2,
)


def test_v2():
    assert v2(1) == 0
    assert v2(2) == 1
    assert v2(8) == 3
    assert v2(40) == 3


def test_collatz_odd_step():
    nxt, a = collatz_odd_step(5)
    assert nxt == 1
    assert a == 4


def test_audit_seed_terminates_for_27():
    result = audit_seed(27, max_steps=1000)
    assert result.seed == 27
    assert result.bounded is True
    assert result.terminal_value == 1
    assert result.steps > 0
    assert result.peak_debt >= 0


def test_audit_many_range():
    result = audit_many(range(1, 11), max_steps=1000)
    assert result["summary"]["total_seeds"] == 10
    assert result["summary"]["terminated"] == 10
    assert "certificate" in result
    assert len(result["audits"]) == 10


def test_generate_single_seed():
    assert generate_seeds(seed=27, start=None, end=None, input_path=None) == [27]


def test_generate_range():
    assert generate_seeds(seed=None, start=3, end=5, input_path=None) == [3, 4, 5]


def test_read_seed_csv(tmp_path):
    p = tmp_path / "seeds.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["seed"])
        writer.writeheader()
        writer.writerow({"seed": "27"})
        writer.writerow({"seed": "31"})

    assert read_seed_csv(str(p)) == [27, 31]


def test_cli_range_writes_reports(tmp_path):
    out_dir = tmp_path / "report"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "collatz_native_auditor.cli",
            "--start",
            "1",
            "--end",
            "20",
            "--out-dir",
            str(out_dir),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert (out_dir / "report.json").exists()
    assert (out_dir / "report.csv").exists()
    assert (out_dir / "report.html").exists()
    assert (out_dir / "near_breach_cases.jsonl").exists()
    assert (out_dir / "certificate.json").exists()


def test_cli_seed_mode(tmp_path):
    out_dir = tmp_path / "seed_report"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "collatz_native_auditor.cli",
            "--seed",
            "27",
            "--out-dir",
            str(out_dir),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    report = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert report["summary"]["total_seeds"] == 1
    assert report["audits"][0]["seed"] == 27
