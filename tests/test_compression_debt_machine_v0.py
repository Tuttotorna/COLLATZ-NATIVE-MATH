import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "build_compression_debt_machine_v0.py"


def load_module():
    module_name = "build_compression_debt_machine_v0"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)

    assert spec.loader is not None

    # Required for Python 3.12 dataclasses when postponed annotations are enabled.
    # dataclasses resolves string annotations through sys.modules[cls.__module__].
    sys.modules[module_name] = module

    spec.loader.exec_module(module)
    return module


def test_v2_basic_values():
    m = load_module()

    assert m.v2(1) == 0
    assert m.v2(2) == 1
    assert m.v2(4) == 2
    assert m.v2(12) == 2
    assert m.v2(40) == 3


def test_odd_step_seed_1_terminates_to_1():
    m = load_module()

    next_n, a, delta = m.odd_step(1)

    assert next_n == 1
    assert a == 2
    assert delta == 0.0


def test_odd_step_seed_3():
    m = load_module()

    next_n, a, delta = m.odd_step(3)

    assert next_n == 5
    assert a == 1
    assert delta > 0


def test_measure_odd_trajectory_boundary_fields():
    m = load_module()

    record, steps = m.measure_odd_trajectory(3, odd_steps=10)

    assert record.seed == 3
    assert record.odd_steps >= 1
    assert isinstance(record.debt_peak, float)
    assert isinstance(record.cheap_chain_epsilon_0, bool)
    assert all(step.n % 2 == 1 for step in steps)
    assert all(step.next_n % 2 == 1 for step in steps)


def test_build_summary_has_non_proof_boundary():
    m = load_module()

    summary = m.build(max_odd_seed=21, odd_steps=20)

    assert summary["boundary"]["proof_status"] == "not_a_proof"
    assert summary["boundary"]["collatz_status"] == "not_claimed_solved"
    assert summary["boundary"]["bounded_evidence_status"] == "measurement_only"
    assert summary["counts"]["odd_seeds_measured"] == 11


def test_pearson_returns_none_for_constant_vector():
    m = load_module()

    assert m.pearson([1.0, 1.0, 1.0], [2.0, 3.0, 4.0]) is None
