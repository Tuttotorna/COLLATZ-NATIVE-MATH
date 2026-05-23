import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_finding_summary_v0.py"


def load_module():
    module_name = "build_finding_summary_v0"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)

    assert spec.loader is not None

    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def test_get_nested_present_and_default():
    m = load_module()

    obj = {"a": {"b": {"c": 7}}}

    assert m.get_nested(obj, ["a", "b", "c"]) == 7
    assert m.get_nested(obj, ["a", "x"], default="missing") == "missing"
    assert m.get_nested(None, ["a"], default="missing") == "missing"


def test_fmt_handles_core_types():
    m = load_module()

    assert m.fmt(None) == "None"
    assert m.fmt(True) == "true"
    assert m.fmt(False) == "false"
    assert m.fmt(1.23456789) == "1.234567890000"
    assert m.fmt("x") == "x"


def test_build_returns_summary_shape():
    m = load_module()

    result = m.build()

    assert result["version"] == "v6.5"
    assert result["machine"] == "Finding Summary V0"
    assert len(result["findings"]) == 10
    assert result["boundary"]["proof_status"] == "not_a_proof"
    assert result["boundary"]["collatz_status"] == "not_claimed_solved"
    assert "one_sentence" in result["concise_thesis"]


def test_findings_have_required_fields():
    m = load_module()

    result = m.build()

    for finding in result["findings"]:
        assert "id" in finding
        assert "name" in finding
        assert "status" in finding
        assert "evidence" in finding
        assert "interpretation" in finding
        assert "boundary" in finding


def test_markdown_contains_non_claims_and_boundary():
    m = load_module()

    result = m.build()
    markdown = m.write_markdown(result)

    assert "# COLLATZ-NATIVE-MATH v6.x Finding Summary V0" in markdown
    assert "It is not a proof of Collatz." in markdown
    assert "not_claimed_solved" in markdown
    assert "No persistent mature low-compression regeneration chain observed." in markdown
