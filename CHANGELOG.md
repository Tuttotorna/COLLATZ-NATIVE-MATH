# Changelog

## v0.1.0

Initial repository structure.

Added:

- problem-born framing
- Math_Collatz core language
- debt words
- 2-adic shadow
- cheap regeneration chain conjecture
- trace demo
- regeneration scan
- tests
- GitHub Actions CI

## v0.2.0

Added regeneration epoch analysis.

New files:

- docs/REGENERATION_EPOCHS.md
- docs/CHEAPNESS_RATIO.md
- docs/EPOCH_ANALYSIS_NOTES.md
- examples/analyze_regeneration_epochs.py
- tests/test_regeneration_epochs.py
- results/regeneration_epochs_sample.jsonl
- results/regeneration_epochs_summary.json

Core addition:

    regeneration events
    regenerated shadow
    compression cost
    cheapness ratio
    future escape capacity

v0.2 clarifies that local cheap regeneration exists, so the real target is not:

    no cheap regeneration exists

but:

    no infinite cheap regeneration chain exists in positive odd Collatz dynamics.

## v0.3.0

Added cheap regeneration chain analysis.

New files:

- docs/CHAIN_ANALYSIS.md
- docs/CRC_CHAIN_MODEL.md
- docs/CHAIN_RESULTS.md
- examples/analyze_cheap_regeneration_chains.py
- tests/test_cheap_regeneration_chains.py
- results/cheap_regeneration_chains.jsonl
- results/cheap_regeneration_chain_summary.json

Core addition:

    chain-compatible regeneration events
    segment average debt
    debt break detection
    finite cheap regeneration chain diagnostics

v0.3 moves the project from local cheap regeneration to chain sustainability.

The target is now operationally phrased as:

    local cheap regeneration exists,
    but no infinite cheap regeneration chain should exist in positive odd Collatz dynamics.

## v0.4.0

Added chain collapse analysis.

New files:

- docs/CHAIN_COLLAPSE.md
- docs/POST_CHAIN_COMPENSATION.md
- docs/COLLAPSE_RESULTS.md
- examples/analyze_chain_collapse.py
- tests/test_chain_collapse.py
- results/chain_collapse_analysis.jsonl
- results/chain_collapse_summary.json

Core addition:

    chain collapse episodes
    post-chain compensation
    compensation surplus
    collapse cause
    chain length
    chain average debt

v0.4 moves from detecting chain-compatible segments to asking where and why those chains break.

## v0.5.0

Added collapse cause classification.

New files:

- docs/COLLAPSE_CAUSE_CLASSIFICATION.md
- docs/COLLAPSE_MECHANISMS.md
- docs/CLASSIFICATION_RESULTS.md
- examples/analyze_collapse_causes.py
- tests/test_collapse_cause_classification.py
- results/collapse_cause_classification.jsonl
- results/collapse_cause_summary.json

Core addition:

    debt spike classification
    shadow exhaustion classification
    failed regeneration classification
    post-chain overcompensation classification
    terminal descent classification
    primary collapse cause

v0.5 moves from detecting that chains collapse to classifying how they collapse.
