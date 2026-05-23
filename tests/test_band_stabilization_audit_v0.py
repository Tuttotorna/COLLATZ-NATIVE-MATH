import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_band_stabilization_audit_v0.py"


def load_module():
    module_name = "build_band_stabilization_audit_v0"
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

    ranges = m.make_block_ranges(block_size=9, max_end=29)

    assert ranges[0]["label"] == "1..9"
    assert ranges[1]["label"] == "11..19"
    assert ranges[2]["label"] == "21..29"


def test_rolling_mean():
    m = load_module()

    assert m.rolling([1.0, 2.0, 3.0], 2, m.mean) == [1.5, 2.5]


def test_measure_seed_has_band_fields():
    m = load_module()

    record = m.measure_seed(seed=3, odd_steps=20, post_peak_horizon=10)

    assert record["seed"] == 3
    assert "debt_peak" in record
    assert "response_delay" in record
    assert "post_peak_release_mass_h" in record
    assert record["odd_steps"] >= 1


def test_run_block_small():
    m = load_module()

    result = m.run_block(
        label="1..21",
        start=1,
        end=21,
        midpoint=11.0,
        odd_steps=30,
        post_peak_horizon=10,
    )

    assert result["label"] == "1..21"
    assert result["odd_seed_count"] == 11
    assert "primary_signal" in result["aggregate"]


def test_build_summary_has_boundary_and_band():
    m = load_module()

    old_ranges = m.BLOCK_RANGES
    old_steps = m.ODD_STEPS
    old_horizon = m.POST_PEAK_HORIZON

    try:
        m.ODD_STEPS = 30
        m.POST_PEAK_HORIZON = 10
        m.BLOCK_RANGES = [
            {"label": "1..21", "start": 1, "end": 21, "midpoint": 11.0},
            {"label": "23..41", "start": 23, "end": 41, "midpoint": 32.0},
            {"label": "43..61", "start": 43, "end": 61, "midpoint": 52.0},
        ]
        summary = m.build()
    finally:
        m.BLOCK_RANGES = old_ranges
        m.ODD_STEPS = old_steps
        m.POST_PEAK_HORIZON = old_horizon

    assert summary["version"] == "v5.4"
    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert "block_summary" in summary
    assert "band_status" in summary["block_summary"]


def test_pearson_constant_returns_none():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None
