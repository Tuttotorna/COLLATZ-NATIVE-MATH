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

## v0.6.0

Added unclassified collapse analysis and refined collapse taxonomy.

New files:

- docs/UNCLASSIFIED_COLLAPSE_ANALYSIS.md
- docs/REFINED_COLLAPSE_TAXONOMY.md
- docs/UNCLASSIFIED_RESULTS.md
- examples/analyze_unclassified_collapses.py
- tests/test_unclassified_collapse_analysis.py
- results/unclassified_collapse_analysis.jsonl
- results/unclassified_collapse_summary.json

Core addition:

    soft_debt_break
    weak_regeneration
    delayed_compensation
    end_of_chain_without_escape
    refined v0.6 primary collapse cause

v0.6 targets the unclassified residue left by v0.5.

## v0.7.0

Added compensation law search.

New files:

- docs/COMPENSATION_LAW_SEARCH.md
- docs/RECOVERY_WINDOW.md
- docs/COMPENSATION_RESULTS.md
- examples/analyze_compensation_law.py
- tests/test_compensation_law_search.py
- results/compensation_law_search.jsonl
- results/compensation_law_summary.json

Core addition:

    chain deficit
    recovery window
    recovery distance
    recovery debt
    recovery surplus
    compensation law candidate search

v0.7 moves from classifying collapse to measuring how fast low-debt chains are compensated.

## v0.8.0

Added post-chain recovery analysis.

New files:

- docs/POST_CHAIN_RECOVERY.md
- docs/RECOVERY_COMPARISON.md
- docs/POST_CHAIN_RESULTS.md
- examples/analyze_post_chain_recovery.py
- tests/test_post_chain_recovery.py
- results/post_chain_recovery_analysis.jsonl
- results/post_chain_recovery_summary.json

Core addition:

    chain-start recovery vs post-chain recovery
    recovery distance gap
    instant post-chain recovery
    post-chain unrecovered episodes

v0.8 corrects v0.7 by measuring recovery after the chain has ended, not only from the chain start.

## v0.9.0

Added hard recovery case analysis.

New files:

- docs/HARD_RECOVERY_CASES.md
- docs/HARDNESS_SCORE.md
- docs/HARD_RECOVERY_RESULTS.md
- examples/analyze_hard_recovery_cases.py
- tests/test_hard_recovery_cases.py
- results/hard_recovery_cases.jsonl
- results/hard_recovery_summary.json

Core addition:

    hardness score
    top hard recovery cases
    longest post-chain recovery cases
    tightest recovery surplus cases
    largest chain deficit cases
    largest recovery gap cases

v0.9 identifies the structurally hardest recovered compensation cases.

## v1.0.0

Added critical case dissection.

New files:

- docs/CRITICAL_CASE_DISSECTION.md
- docs/CRITICAL_CASE_RESULTS.md
- docs/CRITICAL_PATTERN_NOTES.md
- examples/analyze_critical_case.py
- tests/test_critical_case.py
- results/critical_case_dissection.json
- results/critical_case_blocks.jsonl
- results/critical_case_window.jsonl
- results/critical_case_summary.json

Core addition:

    hard case n0 = 9780657630
    block-by-block post-chain recovery window
    first crossing above log2(3)
    focused debt word
    recovery surplus dissection
    critical pattern notes

v1.0 turns the hardest sampled recovered case into a concrete object for inspection.

## v1.1.0

Added critical frontier scan.

New files:

- docs/CRITICAL_FRONTIER_SCAN.md
- docs/FRONTIER_RESULTS.md
- docs/FRONTIER_LIMITS.md
- examples/scan_critical_frontier.py
- tests/test_critical_frontier_scan.py
- results/critical_frontier_scan.jsonl
- results/critical_frontier_summary.json

Core addition:

    bounded frontier scan around hard cases
    local neighborhood scan around known frontier centers
    structured near-Mersenne candidates
    automatic hardest-case ranking
    automatic comparison against the v1.0 critical case

v1.1 tests whether the v1.0 hard case is isolated or part of a wider frontier.

## v1.2 - Frontier stability certificate exact baseline

- Preserves the v1.1 critical frontier scanner as deterministic core.
- Adds a v1.2 wrapper that emits a frontier stability certificate.
- Uses the exact previous critical hardness baseline: 15.100955299032181.
- Avoids false HARDER_THAN_PREVIOUS classification caused by rounded baseline 15.100955.
- Records comparison_status, frontier_stable, and harder_than_previous_critical.
- Adds regression tests for exact frontier stability.

## v1.3 - Compensation law candidate

- Adds a finite compensation-law candidate scanner.
- Detects maximal bad debt windows where average debt is below log2(3).
- Searches shortest post-window recovery restoring the combined average to log2(3).
- Emits a finite compensation-law candidate certificate.
- Adds regression tests for the v1.3 outputs.

## v1.4 - Adversarial compensation scan

- Adds an adversarial scanner for the compensation-law candidate.
- Expands around known hard cases using local neighborhoods, powers-of-two offsets, and bit-flip perturbations.
- Searches for unrecovered bad compensation windows.
- Emits finite rows, summary, and certificate artifacts.
- Adds regression tests for the adversarial certificate.

## v1.5 - Hardness metric report

- Adds a metric-unification report for Collatz hardness.
- Separates frontier recovery hardness, compensation-window hardness, adversarial compensation hardness, tightest surplus, and known trajectory anchors.
- Adds `examples/build_hardness_metric_report.py`.
- Adds `docs/HARDNESS_METRICS.md`.
- Adds generated reports in `results/hardness_metric_report.json` and `results/hardness_metric_report.md`.
- Adds regression tests proving that multiple hardest cases are not treated as contradictions.

## v1.5.1 - Fix tightest positive surplus extraction

- Fixes `tightest_positive_surplus` in the hardness metric report.
- Ensures the metric extracts a real positive value instead of `None`.
- Adds regression coverage for the expected current value:
  `n0 = 63728127`, `min_surplus = 1.7736432994075457e-05`.

## v1.6 - Native Method Boundary

- Adds a native-method boundary layer.
- Separates native method from computational evidence.
- Defines native primitives: debt, discharge, shadow, regeneration, compensation, obstruction candidate, and native closure.
- Adds a standard translation boundary.
- Clarifies that previous scans are evidence layers, not the native theory itself.
- Defines the next research step as v1.7 Native Obstruction Model.

## v1.7 - Native Obstruction Model

- Defines what a native obstruction would have to be.
- Separates obstruction from long trajectory, hardness, tight surplus, and local instability.
- Defines native failure condition.
- Defines native regeneration.
- Defines the opposite of native closure.
- Adds hardness-vs-obstruction boundary.
- Sets v1.8 as Native Closure Conditions.

## v1.8 - Native Closure Conditions

- Defines native closure as structural erasure of obstruction potential.
- Separates native closure from reaching 1.
- Defines the native closure test.
- Defines debt erasure, shadow erasure, and compensation sufficiency.
- Clarifies that local recovery is not automatically closure.
- Sets v1.9 as Native Evidence Mapping.

## v1.9 - Native Evidence Mapping

- Adds a native evidence mapping layer.
- Maps existing computational artifacts into native objects.
- Separates evidence from proof.
- Separates hardness from obstruction.
- Separates local recovery from native closure.
- Adds a native evidence map builder.
- Writes results/native_evidence_map.json and results/native_evidence_map.md.
- Prepares v2.0 Native-to-Standard Translation Boundary.

## v2.0 - Native-to-Standard Translation Boundary

- Defines the controlled boundary where standard mathematics may re-enter.
- Adds reversible translation rule: native object -> standard expression -> native meaning retained.
- Adds translation table for expansion, discharge, debt, bad window, compensation, shadow, regeneration, obstruction, and closure.
- Prevents premature theorem/proof claims.
- Separates native closure from reaching 1.
- Separates hardness from obstruction.
- Sets v2.1 as Standard Definition Candidates.

## v2.1 - Standard Definition Candidates

- Adds candidate standard definitions for native objects.
- Keeps standard mathematics under the reversibility rule.
- Defines stable candidates: odd block, discharge exponent, expansion pressure, debt, bad window, compensation, surplus.
- Marks shadow, regeneration, obstruction, and closure as open candidates.
- Adds definition status and next standardization steps.
- Sets v2.2 as Local Debt Lemma Candidates.

## v2.2 - Local Debt Lemma Candidates

- Adds reversible local debt lemma candidates.
- Converts stable v2.1 definitions into lemma candidates.
- Adds bad-window, compensation, surplus, and hardness-obstruction lemma candidate documents.
- Separates stable, boundary, and open lemma candidates.
- Keeps proof_status = not_a_proof.
- Keeps theorem_status = no_theorems_introduced.
- Sets v2.3 as Shadow and Regeneration Definition Refinement.

## v2.3 - Shadow and Regeneration Definition Refinement

- Refines shadow as persistence of obstruction-relevant prior debt influence.
- Refines shadow erasure as loss of obstruction-carrying power.
- Separates regeneration, benign regeneration, dangerous regeneration, and obstruction-preserving regeneration.
- Clarifies that regeneration alone is not obstruction.
- Defines the obstruction threshold for regeneration chains.
- Keeps proof and theorem claims forbidden.
- Sets v2.4 as Native Closure Lemma Candidates.

## v2.4 - Native Closure Lemma Candidates

- Adds native closure lemma candidates.
- Defines closure result types: CLOSED, LOCALLY_RECOVERED_NOT_CLOSED, REGENERATED_BUT_COMPENSATED, DANGEROUS_REGENERATION, OBSTRUCTION_CANDIDATE, UNDECIDED.
- Defines debt erasure lemma candidates.
- Defines shadow erasure lemma candidates.
- Defines regeneration lemma candidates.
- Keeps all statements as candidates, not theorems.
- Sets v2.5 as Obstruction Search Protocol.

## v2.5 - Obstruction Search Protocol

- Defines the obstruction search protocol.
- Defines obstruction-preserving regeneration as the search target.
- Defines the six-part obstruction candidate signature.
- Defines negative finite-result boundaries.
- Defines obstruction search result types.
- Defines minimum reporting fields for future scanners.
- Sets v2.6 as Bounded Obstruction Search Scanner.

## v2.6 - Bounded Obstruction Search Scanner

- Adds a deterministic bounded scanner for obstruction-preserving regeneration.
- Searches for native obstruction signatures, not merely long or hard trajectories.
- Emits bounded rows, summary, and certificate artifacts.
- Adds negative-result boundary: no obstruction detected in a finite domain is not proof of impossibility.
- Adds tests for scanner artifacts, minimum report fields, known anchors, and result consistency.
- Sets v2.7 as Obstruction Scanner Evidence Report.

## v2.7 - Obstruction Scanner Evidence Report

- Adds an evidence report builder for v2.6 bounded obstruction scanner output.
- Interprets scanner results in native terms.
- Identifies hardest recovery, tightest surplus, most debt windows, most regeneration, most dangerous regeneration, and near-obstruction cases.
- Preserves the negative-result boundary.
- Clarifies that dangerous regeneration is stress, not obstruction.
- Sets v2.8 as Expanded Bounded Obstruction Search.

## v2.8 - Expanded Bounded Obstruction Search

- Adds a targeted expanded bounded obstruction scanner.
- Expands around near-obstruction evidence from v2.6 and v2.7.
- Avoids blind brute force.
- Searches for obstruction-preserving regeneration, not merely hard trajectories.
- Emits expanded bounded rows, summary, and certificate artifacts.
- Keeps negative-result boundary explicit.
- Sets v2.9 as Shadow Persistence Instrumentation.

## v2.9 - Shadow Persistence Instrumentation

- Adds shadow persistence instrumentation over v2.8 expanded bounded search output.
- Distinguishes recurring stress from prior-debt shadow carry.
- Classifies shadow signals into weak, persistent, and obstruction-candidate classes.
- Emits JSON report, Markdown report, and certificate artifacts.
- Keeps proof boundary explicit.
- Sets v3.0 as Formal Native-to-Standard Lemma Draft.

## v3.0 - Formal Native-to-Standard Lemma Draft

- Adds the first formal native-to-standard lemma draft layer.
- Converts stable native objects into formal lemma drafts.
- Keeps all drafts reversible to native meaning.
- Defines the central bridge statement: persistent shadow signal does not imply obstruction unless compensation fails and obstruction potential remains self-preserving.
- Adds proof obligations before any theorem attempt.
- Explicitly keeps proof status as not_a_proof.
- Sets v3.1 as Proof Obligation Tracker.

## v3.1 - Native Language Inversion

- Corrects the route from solving Collatz to learning what Collatz is.
- Defines the mother rule: No solution before native language.
- Defines the secondary rule: No proof before native description.
- Reclassifies termination as a classical translation endpoint, not the native source question.
- Reclassifies previous scans as native instrumentation and grammar probes.
- Reclassifies v3.0 formal lemma drafts as deferred translation layer.
- Adds the next step: v3.2 Native Grammar Map.

## v3.2 - Native Grammar Map

- Adds the native grammar map after the v3.1 route correction.
- Defines Collatz first as a native dynamical grammar, not as a conjecture to solve.
- Defines grammar objects: expansion, discharge, debt, shadow, regeneration, compensation, closure, obstruction.
- Defines grammar transitions and admissible native sequences.
- Reclassifies prior scans as grammar probes.
- Forbids premature translations from grammar to proof, closure to reaching 1, and dangerous regeneration to obstruction.
- Sets v3.3 as Native Sentence Extractor.

## v3.3 - Native Sentence Extractor

- Adds a native sentence extractor.
- Reads trajectory evidence as grammar utterances rather than proof attempts.
- Extracts sentence classes such as debt, compensation, regeneration, dangerous regeneration, and obstruction candidate sentences.
- Produces native sentence JSONL, summary, report, and certificate artifacts.
- Keeps the mother rule explicit: No solution before native language.
- Sets v3.4 as Native Sentence Atlas.

## v3.4 - Native Sentence Atlas

- Adds a native sentence atlas builder.
- Maps sentence classes, sentence families, native words, dangerous sentences, rare profiles, and dominant profiles.
- Treats trajectories as native utterances, not proof objects.
- Keeps the rule: No solution before native language.
- Adds atlas JSON, Markdown report, and certificate artifacts.
- Sets v3.5 as Native Grammar Recurrence Map.

## v3.5 - Native Grammar Recurrence Map

- Adds a native grammar recurrence builder.
- Maps sentence-class transitions and sentence-family transitions.
- Separates repeat, mutation, dangerous recurrence, and obstruction recurrence.
- Treats recurrence as native behavior, not proof evidence.
- Keeps the rule: No solution before native language.
- Emits recurrence map JSON, Markdown report, and certificate.
- Sets v3.6 as Native Grammar Mutation Atlas.

## v3.6 - Native Grammar Mutation Atlas

- Adds a native grammar mutation atlas builder.
- Maps how native sentence forms transform into other sentence forms.
- Separates dangerous release, dangerous persistence, recovery-to-regeneration, regeneration-to-recovery, and toward-obstruction mutation.
- Treats n0 = 9780657630 as a possible grammar node, not a proof object.
- Preserves the rule: No solution before native language.
- Emits mutation atlas JSON, Markdown report, and certificate.
- Sets v3.7 as Native Grammar Stability Map.

## v3.7 - Native Grammar Stability Map

- Adds a native grammar stability map builder.
- Distinguishes recurrence, mutation, and stability.
- Classifies stable, unstable, dangerous-stable, dangerous-unstable, release, and obstruction-relevant grammar behavior.
- Treats n0 = 9780657630 as a grammar stability node, not a proof object.
- Preserves the rule: No solution before native language.
- Emits stability map JSON, Markdown report, and certificate.
- Sets v3.8 as Native Conservation Map.

## v3.8 - Native Conservation Map

- Adds a native conservation map builder.
- Distinguishes recurrence, mutation, stability, and conservation.
- Maps what remains visible across recurrence, mutation, and stability.
- Classifies danger-release conservation, instability conservation, stability conservation, and obstruction-relevant conservation.
- Treats n0 = 9780657630 as a conservation probe, not a proof object.
- Preserves the rule: No solution before native language.
- Emits conservation map JSON, Markdown report, and certificate.
- Sets v3.9 as Native Invariant Candidate Map.

## v3.9 - Native Invariant Candidate Map

- Adds a native invariant candidate map builder.
- Converts bounded conservation behaviors into invariant candidates without theorem claims.
- Separates bounded invariant candidate from global invariant.
- Classifies danger-release, dangerous-stability, instability, weak, and obstruction-relevant invariant candidates.
- Treats n0 = 9780657630 as an invariant-candidate probe, not a proof object.
- Preserves the rule: No solution before native language.
- Emits invariant candidate map JSON, Markdown report, and certificate.
- Sets v4.0 as Native Language Summary.

## v4.0 - Native Language Summary

- Adds a native language summary builder.
- Summarizes the v3.1 to v3.9 native-language route.
- States the primary position: Collatz is not treated first as a conjecture to solve, but as a native dynamical language.
- Summarizes bounded native observations: dangerous forms, danger-release, dangerous-stability, no obstruction-relevant invariant candidate, and 9780657630 as stress node.
- Preserves the rule: No solution before native language.
- Preserves the non-proof boundary.
- Emits summary JSON, Markdown report, and certificate.
- Sets v4.1 as Native Language README Consolidation.
