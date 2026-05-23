import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_post_response_debt_survival_audit_v0.py"


def load_module():
    module_name = "build_post_response_debt_survival_audit_v0"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)

    assert spec.loader is not None

    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def test_v2_basic_values():
    m = load_module()

    assert m.v2(1) == 0
    assert m.v2(2) == 1
    assert m.v2(64) == 6
    assert m.v2(96) == 5


def test_make_block_ranges_small():
    m = load_module()

    ranges = m.make_block_ranges(block_size=9, max_end=49)

    assert ranges[0]["label"] == "1..9"
    assert ranges[1]["label"] == "11..19"
    assert ranges[-1]["label"] == "41..49"


def test_measure_seed_has_survival_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=20, post_peak_horizon=10)

    assert record["seed"] == 3
    assert "debt_peak" in record
    assert "response_delay" in record
    assert "debt_after_first_release" in record
    assert "debt_drop_after_first_release" in record
    assert "survival_ratio" in record
    assert "new_peak_after_release" in record


def test_summarize_records_basic():
    m = load_module()

    records = [
        {
            "debt_peak": 2.0,
            "has_response": True,
            "response_delay": 1,
            "debt_drop_after_first_release": 1.0,
            "survival_ratio": 0.5,
            "response_reduced_below_peak": True,
            "response_overdischarged_below_zero": False,
            "new_peak_after_release": False,
        },
        {
            "debt_peak": 3.0,
            "has_response": True,
            "response_delay": 2,
            "debt_drop_after_first_release": 4.0,
            "survival_ratio": -0.3333333333,
            "response_reduced_below_peak": True,
            "response_overdischarged_below_zero": True,
            "new_peak_after_release": False,
        },
    ]

    summary = m.summarize_records(records)

    assert summary["record_count"] == 2
    assert summary["p_has_response"] == 1.0
    assert summary["p_reduced_below_peak"] == 1.0
    assert summary["p_survival_ratio_lt_1"] == 1.0


def test_run_block_small():
    m = load_module()

    result = m.run_block(
        label="1..21",
        start=1,
        end=21,
        midpoint=11.0,
        odd_steps=30,
        post_peak_horizon=10,
    )

    assert result["label"] == "1..21"
    assert result["odd_seed_count"] == 11
    assert "p_reduced_below_peak" in result["aggregate"]
    assert "median_survival_ratio" in result["aggregate"]


def test_build_summary_has_boundary_and_survival():
    m = load_module()

    old_ranges = m.BLOCK_RANGES
    old_steps = m.ODD_STEPS
    old_horizon = m.POST_PEAK_HORIZON

    try:
        m.ODD_STEPS = 30
        m.POST_PEAK_HORIZON = 10
        m.BLOCK_RANGES = [
            {"label": "1..21", "start": 1, "end": 21, "midpoint": 11.0},
            {"label": "23..41", "start": 23, "end": 41, "midpoint": 32.0},
            {"label": "43..61", "start": 43, "end": 61, "midpoint": 52.0},
        ]
        summary = m.build()
    finally:
        m.BLOCK_RANGES = old_ranges
        m.ODD_STEPS = old_steps
        m.POST_PEAK_HORIZON = old_horizon

    assert summary["version"] == "v5.7"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "survival_summary" in summary
    assert "survival_status" in summary["survival_summary"]


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
