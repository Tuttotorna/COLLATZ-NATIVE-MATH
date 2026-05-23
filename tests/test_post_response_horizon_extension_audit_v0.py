import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_post_response_horizon_extension_audit_v0.py"


def load_module():
    module_name = "build_post_response_horizon_extension_audit_v0"
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


def test_measure_seed_has_horizon_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=30)

    assert record["seed"] == 3
    assert "debt_peak" in record
    assert "response_delay" in record
    assert "regeneration_ratio" in record
    assert "new_peak_after_release" in record
    assert "time_to_new_peak_if_any" in record


def test_summarize_records_basic():
    m = load_module()

    records = [
        {
            "has_response": True,
            "response_delay": 1,
            "response_reduced_below_peak": True,
            "survival_ratio": -0.5,
            "regeneration_ratio": 0.2,
            "new_peak_after_release": False,
            "time_to_new_peak_if_any": None,
            "any_post_response_regeneration": True,
        },
        {
            "has_response": True,
            "response_delay": 2,
            "response_reduced_below_peak": True,
            "survival_ratio": -0.1,
            "regeneration_ratio": 0.9,
            "new_peak_after_release": False,
            "time_to_new_peak_if_any": None,
            "any_post_response_regeneration": True,
        },
    ]

    summary = m.summarize_records(records)

    assert summary["record_count"] == 2
    assert summary["p_has_response"] == 1.0
    assert summary["p_reduced_below_peak"] == 1.0
    assert summary["p_new_peak_after_release"] == 0.0


def test_run_block_small():
    m = load_module()

    result = m.run_block(
        label="1..21",
        start=1,
        end=21,
        midpoint=11.0,
        odd_steps=30,
    )

    assert result["label"] == "1..21"
    assert result["odd_seed_count"] == 11
    assert "p_new_peak_after_release" in result["aggregate"]


def test_build_summary_has_boundary_and_horizon():
    m = load_module()

    old_ranges = m.BLOCK_RANGES
    old_configs = m.ODD_STEP_CONFIGS

    try:
        m.ODD_STEP_CONFIGS = [30, 40]
        m.BLOCK_RANGES = [
            {"label": "1..21", "start": 1, "end": 21, "midpoint": 11.0},
            {"label": "23..41", "start": 23, "end": 41, "midpoint": 32.0},
        ]
        summary = m.build()
    finally:
        m.BLOCK_RANGES = old_ranges
        m.ODD_STEP_CONFIGS = old_configs

    assert summary["version"] == "v5.8"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "horizon_summary" in summary
    assert "horizon_results" in summary


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
