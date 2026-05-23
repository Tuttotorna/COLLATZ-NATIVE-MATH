import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_fuzzy_rebound_anatomy_v0.py"


def load_module():
    module_name = "build_fuzzy_rebound_anatomy_v0"
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


def test_hamming_and_similarity():
    m = load_module()

    assert m.hamming_distance([1, 2, 3], [1, 2, 3]) == 0
    assert m.hamming_distance([1, 2, 3], [1, 9, 3]) == 1
    assert m.similarity([1, 2, 3], [1, 2, 3]) == 1.0
    assert round(m.similarity([1, 2, 3], [1, 9, 3]), 6) == round(2 / 3, 6)


def test_classify_rebound():
    m = load_module()

    assert m.classify_rebound(1.01, True) == "breach_after_fuzzy_pattern"
    assert m.classify_rebound(0.96, True) == "second_near_breach_candidate"
    assert m.classify_rebound(0.85, True) == "near_peak_rebound"
    assert m.classify_rebound(0.50, True) == "harmless_rebound"
    assert m.classify_rebound(0.50, False) == "no_rebound"


def test_analyze_seed_has_rebound_fields():
    m = load_module()

    result = m.analyze_seed(3)

    assert result["seed"] == 3
    assert "fuzzy_instance_count" in result
    assert "rebound_instance_count" in result
    assert "instances" in result
    assert "rebound_instances" in result


def test_build_small_summary_has_boundary():
    m = load_module()

    old_max = m.MAX_ODD_SEED
    old_steps = m.ODD_STEPS
    old_a = m.PATTERN_A
    old_b = m.PATTERN_B
    old_threshold = m.SIMILARITY_THRESHOLD

    try:
        m.MAX_ODD_SEED = 99
        m.ODD_STEPS = 60
        m.PATTERN_A = [1, 2]
        m.PATTERN_B = [2, 1]
        m.SIMILARITY_THRESHOLD = 0.5
        summary = m.build()
    finally:
        m.MAX_ODD_SEED = old_max
        m.ODD_STEPS = old_steps
        m.PATTERN_A = old_a
        m.PATTERN_B = old_b
        m.SIMILARITY_THRESHOLD = old_threshold

    assert summary["version"] == "v6.3"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "summary" in summary
    assert "rebound_instances" in summary


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
