import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_distributed_release_pressure_v0.py"


def load_module():
    module_name = "build_distributed_release_pressure_v0"
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
    assert m.v2(8) == 3
    assert m.v2(48) == 4


def test_odd_step_seed_3():
    m = load_module()

    next_n, a, delta = m.odd_step(3)

    assert next_n == 5
    assert a == 1
    assert delta > 0


def test_measure_seed_has_pressure_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=20, post_peak_horizon=10)

    assert record["seed"] == 3
    assert "debt_peak" in record
    assert "peak_index" in record
    assert "response_delay" in record
    assert "post_peak_release_count_h" in record
    assert "post_peak_release_mass_h" in record
    assert record["odd_steps"] >= 1


def test_build_summary_has_boundary():
    m = load_module()

    summary = m.build(max_odd_seed=21, odd_steps=30, post_peak_horizon=10)

    assert summary["version"] == "v4.9"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert summary["counts"]["odd_seeds_measured"] == 11


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
