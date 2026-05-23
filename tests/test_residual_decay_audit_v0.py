import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_residual_decay_audit_v0.py"


def load_module():
    module_name = "build_residual_decay_audit_v0"
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


def test_axis_value():
    m = load_module()

    cfg = {"max_odd_seed": 99, "odd_steps": 80, "post_peak_horizon": 10}

    assert m.axis_value("seed_scale_axis", cfg) == 99.0
    assert m.axis_value("odd_step_depth_axis", cfg) == 80.0
    assert m.axis_value("post_peak_horizon_axis", cfg) == 10.0


def test_measure_seed_has_residual_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=20, post_peak_horizon=10)

    assert record["seed"] == 3
    assert "debt_peak" in record
    assert "response_delay" in record
    assert "post_peak_release_mass_h" in record
    assert record["odd_steps"] >= 1


def test_run_config_small():
    m = load_module()

    result = m.run_config(max_odd_seed=21, odd_steps=30, post_peak_horizon=10)

    assert result["config"]["max_odd_seed"] == 21
    assert result["aggregate"]["records"] == 11
    assert "primary_signal" in result["aggregate"]


def test_build_summary_has_boundary_and_axes():
    m = load_module()

    old_configs = m.AXIS_CONFIGS
    try:
        m.AXIS_CONFIGS = {
            "seed_scale_axis": [
                {"max_odd_seed": 21, "odd_steps": 30, "post_peak_horizon": 10},
                {"max_odd_seed": 31, "odd_steps": 30, "post_peak_horizon": 10},
            ],
            "odd_step_depth_axis": [
                {"max_odd_seed": 31, "odd_steps": 20, "post_peak_horizon": 10},
                {"max_odd_seed": 31, "odd_steps": 30, "post_peak_horizon": 10},
            ],
            "post_peak_horizon_axis": [
                {"max_odd_seed": 31, "odd_steps": 30, "post_peak_horizon": 5},
                {"max_odd_seed": 31, "odd_steps": 30, "post_peak_horizon": 10},
            ],
        }
        summary = m.build()
    finally:
        m.AXIS_CONFIGS = old_configs

    assert summary["version"] == "v5.2"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "seed_scale_axis" in summary["axis_summaries"]
    assert "odd_step_depth_axis" in summary["axis_summaries"]
    assert "post_peak_horizon_axis" in summary["axis_summaries"]


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
