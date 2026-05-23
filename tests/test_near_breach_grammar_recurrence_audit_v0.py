import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_near_breach_grammar_recurrence_audit_v0.py"


def load_module():
    module_name = "build_near_breach_grammar_recurrence_audit_v0"
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


def test_find_pattern_positions():
    m = load_module()

    assert m.find_pattern_positions([1, 2, 3, 1, 2, 3], [1, 2]) == [0, 3]
    assert m.find_pattern_positions([1, 2, 3], [2, 3]) == [1]
    assert m.find_pattern_positions([1, 2, 3], [4]) == []


def test_min_distance_between_positions():
    m = load_module()

    assert m.min_distance_between_positions([3]) is None
    assert m.min_distance_between_positions([3, 10, 15]) == 5


def test_analyze_seed_has_recurrence_fields():
    m = load_module()

    result = m.analyze_seed(3)

    assert result["seed"] == 3
    assert "pattern_A_count" in result
    assert "pattern_B_count" in result
    assert "combined_pattern_count" in result
    assert "instance_metrics" in result


def test_build_small_summary_has_boundary():
    m = load_module()

    old_max = m.MAX_ODD_SEED
    old_steps = m.ODD_STEPS
    old_top = m.TOP_SEEDS_TO_REPORT
    old_a = m.PATTERN_A
    old_b = m.PATTERN_B

    try:
        m.MAX_ODD_SEED = 99
        m.ODD_STEPS = 60
        m.TOP_SEEDS_TO_REPORT = 5
        m.PATTERN_A = [1, 2]
        m.PATTERN_B = [2, 1]
        summary = m.build()
    finally:
        m.MAX_ODD_SEED = old_max
        m.ODD_STEPS = old_steps
        m.TOP_SEEDS_TO_REPORT = old_top
        m.PATTERN_A = old_a
        m.PATTERN_B = old_b

    assert summary["version"] == "v6.1"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "summary" in summary
    assert "top_pattern_hits" in summary


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
