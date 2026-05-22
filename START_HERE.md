# START HERE

This repository starts from one principle:

    the problem should generate the mathematics needed to make it speak.

For Collatz, the problem-born language begins with the accelerated odd dynamics:

    3 n_i + 1 = 2^(a_i) n_(i+1)

where:

    a_i = v2(3 n_i + 1)

This turns Collatz into a sequence of compression debts:

    W = (a_0, a_1, a_2, ...)

The second native quantity is the 2-adic shadow of -1:

    s_i = v2(n_i + 1)

Escape steps consume this shadow.

Regeneration restores it.

The key open target here is:

    no infinite cheap regeneration chain in positive odd Collatz dynamics

Read in this order:

    CORE_IDEA.md
    MATH_COLLATZ.md
    CRC_CONJECTURE.md
    docs/DEBT_WORDS.md
    docs/TWO_ADIC_SHADOW.md
    docs/CHEAP_REGENERATION.md

## v0.2 step

After reading the core files, run:

    python examples/analyze_regeneration_epochs.py

This computes regeneration events and cheapness ratios.

The v0.2 target is:

    distinguish local cheap regeneration from infinite cheap regeneration chains.

## v0.3 step

After v0.2, run:

    python examples/analyze_cheap_regeneration_chains.py

This moves from single regeneration events to finite cheap regeneration chain diagnostics.

The v0.3 question is:

    does local cheap regeneration connect into a sustained low-debt chain,
    or is it broken by accumulated compression debt?

## v0.4 step

After v0.3, run:

    python examples/analyze_chain_collapse.py

This detects finite chain-compatible runs and measures where they collapse.

The v0.4 question is:

    are finite cheap regeneration chains followed by debt compensation?

## v0.5 step

After v0.4, run:

    python examples/analyze_collapse_causes.py

This classifies how detected cheap regeneration chains collapse.

The v0.5 question is:

    which native mechanism breaks the chain?

## v0.6 step

After v0.5, run:

    python examples/analyze_unclassified_collapses.py

This analyzes the unclassified collapse residue and applies a refined collapse taxonomy.

The v0.6 question is:

    can every finite cheap regeneration chain collapse be expressed in native Collatz terms?

## v0.7 step

After v0.6, run:

    python examples/analyze_compensation_law.py

This searches for recovery windows after low-debt cheap regeneration chains.

The v0.7 question is:

    can every low-debt chain be shown to recover above log2(3) in finite time?

## v0.8 step

After v0.7, run:

    python examples/analyze_post_chain_recovery.py

This compares:

    chain_start_recovery
    post_chain_recovery

The v0.8 question is:

    after a cheap regeneration chain ends, does the future path recover above log2(3)?

## v0.9 step

After v0.8, run:

    python examples/analyze_hard_recovery_cases.py

This isolates the hardest post-chain recovery cases.

The v0.9 question is:

    which recovered chains are closest to failing compensation?

## v1.0 step

After v0.9, run:

    python examples/analyze_critical_case.py

This dissects:

    n0 = 9780657630

The v1.0 question is:

    what exact block pattern produces the 114-block post-chain recovery distance?

## v1.1 step

After v1.0, run:

    python examples/scan_critical_frontier.py

This checks whether:

    n0 = 9780657630

remains the current frontier case, or whether a harder candidate appears.

## v1.2 frontier stability exact baseline

Run:

    python examples/scan_critical_frontier.py

Then check:

    results/critical_frontier_summary.json
    results/frontier_stability_certificate.json

Expected status:

    comparison_status = SAME_AS_PREVIOUS
    frontier_stable = true

## v1.3 compensation law candidate

Run:

    python examples/analyze_compensation_law_candidate.py

Then inspect:

    results/compensation_law_candidate_summary.json
    results/compensation_law_candidate_certificate.json

## v1.4 adversarial compensation

Run:

    python examples/adversarial_compensation_scan.py

Then inspect:

    results/adversarial_compensation_summary.json
    results/adversarial_compensation_certificate.json

## v1.5 hardness metrics

Run the metric report:

`python examples/build_hardness_metric_report.py`

Then inspect:

`results/hardness_metric_report.md`

This explains why the repository can contain multiple hardest cases under different measurement lenses.

## v1.5.1 hardness report check

Run:

    python examples/build_hardness_metric_report.py

Then check:

    results/hardness_metric_report.json

The `tightest_positive_surplus` metric must be non-null.

## v1.6 native method first

Start here before reading the computational scans:

docs/NATIVE_METHOD.md
docs/NATIVE_OBJECTS.md
docs/STANDARD_TRANSLATION_BOUNDARY.md
docs/NATIVE_RESEARCH_PROGRAM.md
docs/EVIDENCE_LAYER_STATUS.md

The scans are evidence layers.

The native method is the source layer.

The standard mathematical translation comes later.

## v1.7 obstruction before closure

Before trying to prove closure, define what obstruction means.

Read:

    docs/NATIVE_OBSTRUCTION_MODEL.md
    docs/NATIVE_FAILURE_CONDITION.md
    docs/NATIVE_REGENERATION.md
    docs/NATIVE_CLOSURE_OPPOSITE.md
    docs/NATIVE_HARDNESS_VS_OBSTRUCTION.md

Core rule:

    Hardness measures stress.
    Obstruction requires self-preserving unclosed debt.

## v1.8 closure before translation

After defining native obstruction, define native closure.

Read:

    docs/NATIVE_CLOSURE_CONDITIONS.md
    docs/NATIVE_CLOSURE_TEST.md
    docs/NATIVE_DEBT_ERASURE.md
    docs/NATIVE_SHADOW_ERASURE.md
    docs/NATIVE_COMPENSATION_SUFFICIENCY.md

Core rule:

    Native closure is the erasure of obstruction potential, not merely reaching 1.

## v1.9 evidence before translation

Before returning to standard mathematics, map the evidence into native objects.

Read:

    docs/NATIVE_EVIDENCE_MAPPING.md
    docs/EVIDENCE_TO_NATIVE_OBJECTS.md
    docs/NATIVE_EVIDENCE_STATUS.md
    docs/NATIVE_EVIDENCE_LIMITS.md
    docs/NATIVE_TO_STANDARD_PREPARATION.md

Then run:

    python examples/build_native_evidence_map.py

Core rule:

    The evidence layer supports the native research path.
    It does not replace proof.

## v2.0 controlled translation

After v1.9, standard mathematics may re-enter only under translation control.

Read:

text:
docs/NATIVE_TO_STANDARD_TRANSLATION_BOUNDARY.md
docs/TRANSLATION_TABLE.md
docs/TRANSLATION_VALIDITY_RULES.md
docs/STANDARD_PROOF_PREPARATION.md
docs/NATIVE_STANDARD_GLOSSARY.md

Core rule:

text:
Every standard statement must map back to a native object.
