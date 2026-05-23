import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_mature_rebound_guard_v0.py"


def load_module():
    module_name = "build_mature_rebound_guard_v0"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)

    assert spec.loader is not None

    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def test_classify_weak_prefix_false_breach():
    m = load_module()

    instance = {
        "prior_debt_peak": 0.5,
        "post_max_to_prior_peak_ratio": 10.0,
        "rebound_class": "breach_after_fuzzy_pattern",
    }

    assert m.classify_guarded_rebound(instance) == "weak_prefix_false_breach"


def test_classify_mature_breach():
    m = load_module()

    instance = {
        "prior_debt_peak": 5.0,
        "post_max_to_prior_peak_ratio": 1.1,
        "rebound_class": "breach_after_fuzzy_pattern",
    }

    assert m.classify_guarded_rebound(instance) == "mature_breach_after_fuzzy_pattern"


def test_classify_mature_second_near_breach():
    m = load_module()

    instance = {
        "prior_debt_peak": 5.0,
        "post_max_to_prior_peak_ratio": 0.97,
        "rebound_class": "near_peak_rebound",
    }

    assert m.classify_guarded_rebound(instance) == "mature_second_near_breach_candidate"


def test_enrich_instance_adds_guard_fields():
    m = load_module()

    instance = {
        "seed": 1,
        "pattern": "B",
        "prior_debt_peak": 1.0,
        "post_horizon_max_prefix": 3.0,
        "post_max_to_prior_peak_ratio": 3.0,
        "post_pattern_debt_gain": 2.0,
        "rebound_class": "breach_after_fuzzy_pattern",
        "breach_after_fuzzy_pattern": True,
    }

    enriched = m.enrich_instance(instance)

    assert enriched["mature_prior_peak"] is False
    assert enriched["guarded_rebound_class"] == "weak_prefix_false_breach"
    assert enriched["weak_prefix_artifact"] is True
    assert enriched["guarded_breach_after_fuzzy_pattern"] is False


def test_build_with_mock_input(tmp_path):
    m = load_module()

    old_input = m.INPUT_PATH
    old_results = m.RESULTS

    mock_results = tmp_path / "results"
    mock_results.mkdir()
    mock_input = mock_results / "fuzzy_rebound_anatomy_v0.json"

    mock_input.write_text(
        json.dumps(
            {
                "version": "v6.3",
                "machine": "Fuzzy Rebound Anatomy V0",
                "rebound_instances": [
                    {
                        "seed": 11,
                        "pattern": "B",
                        "prior_debt_peak": 0.5,
                        "post_horizon_max_prefix": 5.0,
                        "post_max_to_prior_peak_ratio": 10.0,
                        "post_pattern_debt_gain": 4.5,
                        "rebound_class": "breach_after_fuzzy_pattern",
                        "breach_after_fuzzy_pattern": True,
                    },
                    {
                        "seed": 13,
                        "pattern": "A",
                        "prior_debt_peak": 5.0,
                        "post_horizon_max_prefix": 4.0,
                        "post_max_to_prior_peak_ratio": 0.8,
                        "post_pattern_debt_gain": 0.1,
                        "rebound_class": "harmless_rebound",
                        "breach_after_fuzzy_pattern": False,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        m.RESULTS = mock_results
        m.INPUT_PATH = mock_input
        result = m.build()
    finally:
        m.INPUT_PATH = old_input
        m.RESULTS = old_results

    assert result["version"] == "v6.4"
    assert result["summary"]["rebound_instance_count"] == 2
    assert result["summary"]["weak_prefix_false_breach_count"] == 1
    assert result["summary"]["mature_rebound_count"] == 1
    assert result["boundary"]["proof_status"] == "not_a_proof"


def test_count_by():
    m = load_module()

    assert m.count_by(
        [
            {"x": "a"},
            {"x": "a"},
            {"x": "b"},
        ],
        "x",
    ) == {"a": 2, "b": 1}
