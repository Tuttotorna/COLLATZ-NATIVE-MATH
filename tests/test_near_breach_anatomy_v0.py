import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_near_breach_anatomy_v0.py"


def load_module():
    module_name = "build_near_breach_anatomy_v0"
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


def test_trajectory_has_anatomy_fields():
    m = load_module()

    record = m.trajectory(seed=3, odd_steps=30)

    assert record["seed"] == 3
    assert "steps" in record
    assert "debt_peak" in record
    assert "regeneration_ratio" in record
    assert "gap_to_breach" in record


def test_summarize_steps_basic():
    m = load_module()

    steps = [
        {"a": 1, "delta": 1.0, "prefix_debt": 1.0},
        {"a": 3, "delta": -2.0, "prefix_debt": -1.0},
    ]

    summary = m.summarize_steps(steps)

    assert summary["count"] == 2
    assert summary["a1_rate"] == 0.5
    assert summary["a_ge_3_rate"] == 0.5
    assert summary["release_rate"] == 0.5


def test_anatomy_has_windows():
    m = load_module()

    item = m.anatomy(3)

    assert item["seed"] == 3
    assert "pre_peak_window" in item
    assert "peak_to_response_window" in item
    assert "response_to_post_max_window" in item
    assert "full_summary" in item


def test_build_small_summary_has_boundary():
    m = load_module()

    old_max = m.MAX_ODD_SEED
    old_steps = m.ODD_STEPS
    old_top = m.TOP_K
    old_controls = m.CONTROL_SEEDS

    try:
        m.MAX_ODD_SEED = 99
        m.ODD_STEPS = 60
        m.TOP_K = 5
        m.CONTROL_SEEDS = [3, 5, 7, 9, 11, 13, 15]
        summary = m.build()
    finally:
        m.MAX_ODD_SEED = old_max
        m.ODD_STEPS = old_steps
        m.TOP_K = old_top
        m.CONTROL_SEEDS = old_controls

    assert summary["version"] == "v6.0"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "near_breach_anatomies" in summary
    assert "comparison" in summary


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
