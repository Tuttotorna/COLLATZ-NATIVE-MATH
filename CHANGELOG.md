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
