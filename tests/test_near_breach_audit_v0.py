import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_near_breach_audit_v0.py"


def load_module():
    module_name = "build_near_breach_audit_v0"
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


def test_classify_seed_band():
    m = load_module()

    assert m.classify_seed_band(1) == "000001..000999"
    assert m.classify_seed_band(999) == "000001..000999"
    assert m.classify_seed_band(1001) == "000001..009999"
    assert m.classify_seed_band(15000) == "010001..019999"


def test_measure_seed_has_near_breach_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=30)

    assert record["seed"] == 3
    assert "regeneration_ratio" in record
    assert "gap_to_breach" in record
    assert "new_peak_after_release" in record
    assert "time_to_post_response_max" in record


def test_build_small_summary_has_boundary():
    m = load_module()

    old_max = m.MAX_ODD_SEED
    old_steps = m.ODD_STEPS
    old_top = m.TOP_K

    try:
        m.MAX_ODD_SEED = 99
        m.ODD_STEPS = 60
        m.TOP_K = 10
        summary = m.build()
    finally:
        m.MAX_ODD_SEED = old_max
        m.ODD_STEPS = old_steps
        m.TOP_K = old_top

    assert summary["version"] == "v5.9"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "near_breach_candidates" in summary
    assert "summary" in summary


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
