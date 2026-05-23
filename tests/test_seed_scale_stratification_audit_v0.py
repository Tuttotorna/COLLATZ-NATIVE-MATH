import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_seed_scale_stratification_audit_v0.py"


def load_module():
    module_name = "build_seed_scale_stratification_audit_v0"
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


def test_odd_seeds():
    m = load_module()

    assert m.odd_seeds(1, 9) == [1, 3, 5, 7, 9]
    assert m.odd_seeds(2, 10) == [3, 5, 7, 9]


def test_measure_seed_has_stratification_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=20, post_peak_horizon=10)

    assert record["seed"] == 3
    assert "debt_peak" in record
    assert "response_delay" in record
    assert "post_peak_release_mass_h" in record
    assert record["odd_steps"] >= 1


def test_run_range_small():
    m = load_module()

    result = m.run_range(
        label="1..21",
        start=1,
        end=21,
        odd_steps=30,
        post_peak_horizon=10,
    )

    assert result["label"] == "1..21"
    assert result["odd_seed_count"] == 11
    assert "primary_signal" in result["aggregate"]


def test_build_summary_has_boundary_and_comparison():
    m = load_module()

    old_cumulative = m.CUMULATIVE_RANGES
    old_blocks = m.BLOCK_RANGES
    old_steps = m.ODD_STEPS
    old_horizon = m.POST_PEAK_HORIZON

    try:
        m.ODD_STEPS = 30
        m.POST_PEAK_HORIZON = 10
        m.CUMULATIVE_RANGES = [
            {"label": "1..21", "start": 1, "end": 21},
            {"label": "1..41", "start": 1, "end": 41},
        ]
        m.BLOCK_RANGES = [
            {"label": "1..21", "start": 1, "end": 21},
            {"label": "23..41", "start": 23, "end": 41},
        ]
        summary = m.build()
    finally:
        m.CUMULATIVE_RANGES = old_cumulative
        m.BLOCK_RANGES = old_blocks
        m.ODD_STEPS = old_steps
        m.POST_PEAK_HORIZON = old_horizon

    assert summary["version"] == "v5.3"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "comparison" in summary
    assert "cumulative_summary" in summary
    assert "block_summary" in summary


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
