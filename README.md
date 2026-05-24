<!-- COLLATZ_NATIVE_AUDITOR_TOP_START -->

# COLLATZ-NATIVE-MATH

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20365748.svg)](https://doi.org/10.5281/zenodo.20365748)

## Concrete entrypoint: Collatz Native Auditor

This repository now has a direct operational tool:

    python -m collatz_native_auditor.cli --start 1 --end 10000 --out-dir report

It does not claim to prove the Collatz conjecture.

It solves a narrower and concrete problem:

    given one seed or a range of seeds,
    produce a reproducible native audit of Collatz trajectories
    using compression debt, 2-adic shadow, regeneration behavior,
    near-breach detection, and recovery certificates.

In short:

    Collatz input -> native measurements -> audit report

## What problem does it solve?

It turns the native language developed in this repository into an executable audit tool.

Instead of asking the reader to understand the whole research path first, the tool lets them run a concrete measurement:

    Which seeds accumulate high compression debt?
    Which seeds approach near-breach behavior?
    Which seeds recover after peak debt?
    Which trajectories show regeneration pressure?
    Which cases deserve inspection?

The rest of this repository explains how this native measurement language was developed.

The auditor is the practical entrypoint.

## Install

Clone the repository:

    git clone https://github.com/Tuttotorna/COLLATZ-NATIVE-MATH.git
    cd COLLATZ-NATIVE-MATH

Install locally:

    pip install -e .

The auditor only uses the Python standard library.

## Run

Audit a range:

    python -m collatz_native_auditor.cli --start 1 --end 10000 --out-dir report

Audit one seed:

    python -m collatz_native_auditor.cli --seed 77031 --out-dir report_seed_77031

Audit seeds from CSV:

    python -m collatz_native_auditor.cli --input examples/sample_seeds.csv --out-dir report_csv

## Input

The auditor accepts three input modes.

Single seed:

    --seed 77031

Range:

    --start 1 --end 10000

CSV file:

    seed
    27
    31
    77031

## Output

The auditor writes:

    report.json
    report.csv
    report.html
    near_breach_cases.jsonl
    certificate.json

Meaning:

    report.json
    Full structured audit.

    report.csv
    Spreadsheet-friendly per-seed summary.

    report.html
    Human-readable inspection report.

    near_breach_cases.jsonl
    One JSON object per near-breach case.

    certificate.json
    Reproducibility certificate with parameters and aggregate results.

## CI gate

The auditor can fail automatically when near-breach cases are detected:

    python -m collatz_native_auditor.cli --start 1 --end 10000 --out-dir report --fail-on-near-breach

Exit codes:

    0 = audit completed, no blocking condition
    2 = near-breach cases detected
    3 = non-terminating-within-bound cases detected

## What this is not

This is not a proof of Collatz.

It does not claim infinite coverage.

It does not replace the full research path in this repository.

It provides one concrete, reproducible operation:

    run Collatz seeds
    measure native trajectory structure
    produce a report
    optionally fail CI when critical cases appear

## Why the rest of the repository still matters

The rest of the repository documents how this operational tool was reached:

    compression debt
    2-adic shadow
    release pressure
    response time
    near-breach anatomy
    rebound guards
    native structural interpretation

The code above is the entrypoint.

The repository below is the derivation path.

<!-- COLLATZ_NATIVE_AUDITOR_TOP_END -->

---

<!-- V4.6_PUBLIC_README_SHORTFORM -->
## Public shortform

COLLATZ-NATIVE-MATH is a native structural reading of Collatz dynamics.

**Central question:**

```text
What is Collatz before it becomes a conjecture?
```

**Core rule:**

```text
No solution before native language.
```

**What this is:**

- a native-language description program
- a bounded artifact system
- a grammar mapping of Collatz-generated structures
- a public non-proof research route

**What this is not:**

- not a proof of Collatz
- not a claim that Collatz is solved
- not a theorem layer
- not a global closure claim
- not a global invariant claim

**Current bounded status:**

- artifact consistency audit passes
- native language index contains 101 indexed items
- bounded invariant candidate map contains 45 candidates
- danger-release invariant candidates are present
- dangerous-stability invariant candidates are present
- no obstruction-relevant invariant candidate is detected in the current bounded maps

**Read next:**

- `results/native_public_research_brief.md`
- `results/native_audit_report_consolidation.md`

**Boundary:**

```text
proof_status: not_a_proof
collatz_status: not_claimed_solved
global_closure_status: not_claimed
global_invariant_status: not_claimed
```
<!-- /V4.6_PUBLIC_README_SHORTFORM -->

A native structural reading of the Collatz dynamics.

This repository does not begin by trying to solve Collatz.

It begins by asking:

    What is Collatz before it becomes a conjecture?

## Core rule

    No solution before native language.

## Secondary rule

    No proof before native description.

## Primary position

Collatz is not treated first as a conjecture to solve, but as a native dynamical language whose grammar can be observed, mapped, and only later translated.

## What this repository is

This repository is a native-language research program for the Collatz dynamics.

It studies the structures generated by the rule itself:

    expansion
    discharge
    debt
    shadow
    regeneration
    compensation
    closure
    obstruction

It does not force the dynamics immediately into the human terminal question:

    Does every trajectory reach 1?

That question is treated as a later classical translation endpoint, not as the native starting point.

## What this repository is not

This repository is not:

    a proof of Collatz
    a claim that Collatz is solved
    a theorem claim
    a global closure claim
    a global invariant claim
    obstruction_impossibility_status: not_claimed

Current status:

    proof_status: not_a_proof
    theorem_status: no_theorems_introduced
    collatz_status: not_claimed_solved
    global_closure_status: not_claimed
    global_invariant_status: not_claimed

## Native route

The corrected native-language route is:

    v3.1  Native Language Inversion
    v3.2  Native Grammar Map
    v3.3  Native Sentence Extractor
    v3.4  Native Sentence Atlas
    v3.5  Native Grammar Recurrence Map
    v3.6  Native Grammar Mutation Atlas
    v3.7  Native Grammar Stability Map
    v3.8  Native Conservation Map
    v3.9  Native Invariant Candidate Map
    v4.0  Native Language Summary
    v4.1  Native Language README Consolidation

## What has been observed so far

Bounded native-language artifacts currently support these observations:

    Collatz can generate dangerous native sentence forms.
    Some dangerous native forms release.
    Some dangerous native forms remain stable in the bounded map.
    No obstruction-relevant invariant candidate was detected in the bounded artifacts.
    9780657630 repeatedly appears as a native grammar stress node.

These are native-language observations.

They are not proof statements.

## How to run the latest summary

    python examples/build_native_language_summary.py

Outputs:

    results/native_language_summary.json
    results/native_language_summary.md
    results/native_language_summary_certificate.json

## How to run the latest invariant candidate map

    python examples/build_native_invariant_candidate_map.py

Outputs:

    results/native_invariant_candidate_map.json
    results/native_invariant_candidate_map.md
    results/native_invariant_candidate_certificate.json

## Start here

Read:

    START_HERE.md
    CRC_CONJECTURE.md
    docs/NATIVE_LANGUAGE_SUMMARY.md
    docs/NATIVE_LANGUAGE_ROUTE.md
    docs/WHAT_COLLATZ_HAS_SAID.md
    docs/NATIVE_LANGUAGE_BOUNDARY.md
    docs/V40_PUBLIC_POSITIONING.md
    docs/README_CONSOLIDATION_V41.md
    docs/ENTRY_POINT_BOUNDARY.md
    docs/PUBLIC_REPO_POSITIONING.md

## Boundary

The repository is intentionally strict:

    bounded evidence != proof
    native grammar != theorem
    danger-release != proof of termination
    dangerous-stability != obstruction
    no obstruction-relevant invariant candidate detected != obstruction impossible

## Tests

    pytest -q

## Final position

Before asking whether Collatz terminates, this repository asks what Collatz says in its own generated structure.

The answer is not yet a proof.

It is a native language.

## v4.2 Native Language Index

The repository now includes a role-based native language index.

Run:

    python examples/build_native_language_index.py

Outputs:

    results/native_language_index.json
    results/native_language_index.md
    results/native_language_index_certificate.json

The index organizes the repo by native-language role:

    entry point
    grammar
    sentences
    recurrence
    mutation
    stability
    conservation
    invariant candidates
    summary
    results
    builders
    tests

Boundary:

    the index is not a theory layer
    the index is not a proof layer
    no solution before native language

## v4.3 Native Artifact Consistency Audit

The repository now includes a native artifact consistency audit.

Run:

    python examples/build_native_artifact_consistency_audit.py

Outputs:

    results/native_artifact_consistency_audit.json
    results/native_artifact_consistency_audit.md
    results/native_artifact_consistency_audit_certificate.json

The audit checks:

    indexed files exist
    entry files remain native-first
    certificates preserve not_a_proof
    builders exist
    README route is current

Boundary:

    audit_passed != proof
    audit_passed != theorem
    audit_passed != Collatz solved
    no solution before native language

## v4.4 Native Audit Report Consolidation

The repository now includes a consolidated native audit report.

Run:

    python examples/build_native_audit_report_consolidation.py

Outputs:

    results/native_audit_report_consolidation.json
    results/native_audit_report_consolidation.md
    results/native_audit_report_consolidation_certificate.json

The report consolidates:

    v4.3 audit
    v4.2 index
    v4.0 summary
    v3.9 invariant candidate map
    v3.8 conservation map
    v3.7 stability map
    v3.6 mutation atlas
    v3.5 recurrence map
    v3.4 sentence atlas
    v3.3 sentence extractor

Boundary:

    consolidated report != proof
    consolidated report != theorem
    consolidated report != Collatz solved
    no solution before native language

## v4.5 Native Public Research Brief

The repository now includes a public-facing research brief.

Run:

    python examples/build_native_public_research_brief.py

Outputs:

    results/native_public_research_brief.json
    results/native_public_research_brief.md
    results/native_public_research_brief_certificate.json

Purpose:

    explain what the project is
    explain what the project is not
    explain native language
    explain bounded artifacts
    preserve the non-proof boundary

Boundary:

    public brief != proof
    public brief != theorem
    public brief != Collatz solved
    no solution before native language

## v4.7 Public Entry Consistency Audit

The repository now includes a public entry consistency audit.

Run:

    python examples/build_public_entry_consistency_audit.py

Outputs:

    results/public_entry_consistency_audit.json
    results/public_entry_consistency_audit.md
    results/public_entry_consistency_audit_certificate.json

The audit checks:

    README shortform exists
    central question exists
    core rule exists
    public brief link exists
    consolidated report link exists
    non-proof boundary exists
    START_HERE is aligned
    CRC_CONJECTURE is aligned
    no forbidden public claim appears as a standalone assertion

Boundary:

    public_entry_audit_passed != proof
    public_entry_audit_passed != theorem
    public_entry_audit_passed != Collatz solved
    no solution before native language

## v4.8 Compression Debt Machine V0

The repository now includes a bounded Compression Debt Machine.

Run:

    python examples/build_compression_debt_machine_v0.py

Outputs:

    results/compression_debt_machine_v0.json
    results/compression_debt_machine_v0.md
    results/compression_debt_machine_v0_certificate.json

Purpose:

    make compression debt, release, and cheap regeneration computable
    measure bounded low-compression regeneration patterns
    preserve the non-proof boundary

Boundary:

    compression_debt_measurement != proof
    cheap_regeneration_detected != divergence
    release_detected != termination proof
    obstruction_candidate != obstruction theorem
    bounded evidence != global closure

## v4.9 Distributed Release Pressure V0

The repository now includes a bounded Distributed Release Pressure machine.

Run:

    python examples/build_distributed_release_pressure_v0.py

Outputs:

    results/distributed_release_pressure_v0.json
    results/distributed_release_pressure_v0.md
    results/distributed_release_pressure_v0_certificate.json

Purpose:

    measure response delay after debt peak
    measure post-peak release count
    measure post-peak strong release count
    measure post-peak release mass
    test whether debt creates distributed release pressure

Boundary:

    distributed_release_pressure != proof
    short_response_delay != termination theorem
    post_peak_release_mass != global invariant
    bounded pressure signal != global closure

## v5.0 Scale Stability Audit V0

The repository now includes a bounded Scale Stability Audit.

Run:

    python examples/build_scale_stability_audit_v0.py

Outputs:

    results/scale_stability_audit_v0.json
    results/scale_stability_audit_v0.md
    results/scale_stability_audit_v0_certificate.json

Purpose:

    test whether the distributed release pressure signal survives scale changes
    vary max_odd_seed, odd_steps, and post_peak_horizon
    audit the primary signal debt_peak_vs_post_peak_release_mass_h_pearson

Boundary:

    scale_stability_audit != proof
    stable_signal != theorem
    correlation != causation
    bounded reproducibility != global closure

## v5.1 Signal Decay Audit V0

The repository now includes a bounded Signal Decay Audit.

Run:

    python examples/build_signal_decay_audit_v0.py

Outputs:

    results/signal_decay_audit_v0.json
    results/signal_decay_audit_v0.md
    results/signal_decay_audit_v0_certificate.json

Purpose:

    test whether the primary distributed release pressure signal decays toward zero
    estimate a bounded positive floor candidate
    measure scale_vs_primary_signal_correlation
    measure signal_decay_slope
    compare early-window and late-window signal means

Boundary:

    signal_decay_audit != proof
    positive_floor_candidate != theorem
    bounded floor != global invariant
    no zero crossing in tested range != universal closure

## v5.2 Residual Decay Audit V0

The repository now includes a bounded Residual Decay Audit.

Run:

    python examples/build_residual_decay_audit_v0.py

Outputs:

    results/residual_decay_audit_v0.json
    results/residual_decay_audit_v0.md
    results/residual_decay_audit_v0_certificate.json

Purpose:

    separate apparent signal decay by measurement axis
    vary max_odd_seed while holding odd_steps and post_peak_horizon fixed
    vary odd_steps while holding max_odd_seed and post_peak_horizon fixed
    vary post_peak_horizon while holding max_odd_seed and odd_steps fixed

Boundary:

    residual_decay_audit != proof
    axis attribution != theorem
    correlation != causation
    bounded axis signal != global invariant

## v5.3 Seed-Scale Stratification Audit V0

The repository now includes a bounded Seed-Scale Stratification Audit.

Run:

    python examples/build_seed_scale_stratification_audit_v0.py

Outputs:

    results/seed_scale_stratification_audit_v0.json
    results/seed_scale_stratification_audit_v0.md
    results/seed_scale_stratification_audit_v0_certificate.json

Purpose:

    separate cumulative seed-scale decay from local block-level signal
    compare cumulative ranges against non-overlapping seed blocks
    test whether seed-scale weakening is local or caused by cumulative mixing

Boundary:

    seed_scale_stratification != proof
    block_signal != theorem
    cumulative_decay != global law
    positive block signal != invariant

## v5.4 Band Stabilization Audit V0

The repository now includes a bounded Band Stabilization Audit.

Run:

    python examples/build_band_stabilization_audit_v0.py

Outputs:

    results/band_stabilization_audit_v0.json
    results/band_stabilization_audit_v0.md
    results/band_stabilization_audit_v0_certificate.json

Purpose:

    test whether local block signals stabilize after initial seed-scale decay
    measure block_signal_values
    measure rolling_mean_3, rolling_min_3, and rolling_max_3
    estimate post_initial_floor, post_initial_ceiling, and post_initial_mean
    detect post_initial zero crossings

Boundary:

    band_stabilization_audit != proof
    positive_band != theorem
    band_floor != global invariant
    no zero crossing in tested blocks != universal closure

## v5.5 Extended Band Audit V0

The repository now includes a bounded Extended Band Audit.

Run:

    python examples/build_extended_band_audit_v0.py

Outputs:

    results/extended_band_audit_v0.json
    results/extended_band_audit_v0.md
    results/extended_band_audit_v0_certificate.json

Purpose:

    extend the local block band audit to 99999
    measure rolling_mean_5, rolling_min_5, and rolling_max_5
    measure last_5_mean, last_5_min, last_10_mean, and last_10_min
    detect extended zero crossings
    measure last_half_slope

Boundary:

    extended_band_audit != proof
    positive_extended_band != theorem
    last_5_positive != invariant
    no zero crossing in tested blocks != universal closure

## v5.6 Response-Time Invariance Audit V0

The repository now includes a bounded Response-Time Invariance Audit.

Run:

    python examples/build_response_time_invariance_audit_v0.py

Outputs:

    results/response_time_invariance_audit_v0.json
    results/response_time_invariance_audit_v0.md
    results/response_time_invariance_audit_v0_certificate.json

Purpose:

    test whether response timing remains stable when release-mass correlation weakens
    measure median_response_delay across seed blocks
    measure p_delay_1, p_delay_le_2, and p_delay_le_3
    measure no_response_rate
    compare timing stability against mass-correlation decay

Boundary:

    response_time_invariance != proof
    median_delay_1 != termination theorem
    immediate_response_rate != global invariant
    bounded response timing != Collatz solved

## v5.7 Post-Response Debt Survival Audit V0

The repository now includes a bounded Post-Response Debt Survival Audit.

Run:

    python examples/build_post_response_debt_survival_audit_v0.py

Outputs:

    results/post_response_debt_survival_audit_v0.json
    results/post_response_debt_survival_audit_v0.md
    results/post_response_debt_survival_audit_v0_certificate.json

Purpose:

    test whether the first rapid post-peak response actually reduces debt
    measure debt_after_first_release
    measure debt_drop_after_first_release
    measure survival_ratio
    measure p_reduced_below_peak
    measure p_new_peak_after_release

Boundary:

    post_response_debt_survival != proof
    debt_drop != termination theorem
    survival_ratio != global invariant
    bounded response effectiveness != Collatz solved

## v5.8 Post-Response Horizon Extension Audit V0

The repository now includes a bounded Post-Response Horizon Extension Audit.

Run:

    python examples/build_post_response_horizon_extension_audit_v0.py

Outputs:

    results/post_response_horizon_extension_audit_v0.json
    results/post_response_horizon_extension_audit_v0.md
    results/post_response_horizon_extension_audit_v0_certificate.json

Purpose:

    test whether post-response new peaks appear only under longer odd-step horizons
    vary odd_steps across 160, 240, 320, 480, 640, and 960
    measure p_new_peak_after_release
    measure p_reduced_below_peak
    measure max_post_response_regeneration_ratio

Boundary:

    horizon_extension_audit != proof
    no new peak within tested horizon != no new peak ever
    bounded horizon stability != global closure
    response effectiveness != termination theorem

## v5.9 Near-Breach Audit V0

The repository now includes a bounded Near-Breach Audit.

Run:

    python examples/build_near_breach_audit_v0.py

Outputs:

    results/near_breach_audit_v0.json
    results/near_breach_audit_v0.md
    results/near_breach_audit_v0_certificate.json

Purpose:

    identify trajectories closest to post-response new-peak breach
    measure regeneration_ratio
    measure gap_to_breach = 1 - regeneration_ratio
    rank top near-breach candidates
    test whether near-breach severity grows with seed scale

Boundary:

    near_breach_audit != proof
    no breach observed != no breach possible
    near-breach candidate != counterexample
    bounded gap != global invariant

## v6.0 Near-Breach Anatomy V0

The repository now includes a bounded Near-Breach Anatomy Audit.

Run:

    python examples/build_near_breach_anatomy_v0.py

Outputs:

    results/near_breach_anatomy_v0.json
    results/near_breach_anatomy_v0.md
    results/near_breach_anatomy_v0_certificate.json

Purpose:

    extract near-breach internal trajectory anatomy
    record a_i, delta_i, and prefix_debt sequences
    extract pre-peak, peak-to-response, and response-to-post-max windows
    compare top near-breach seeds against deterministic controls

Boundary:

    near_breach_anatomy != proof
    repeated pattern != theorem
    near-breach grammar != counterexample
    bounded anatomy != global invariant

## v6.1 Near-Breach Grammar Recurrence Audit V0

The repository now includes a bounded Near-Breach Grammar Recurrence Audit.

Run:

    python examples/build_near_breach_grammar_recurrence_audit_v0.py

Outputs:

    results/near_breach_grammar_recurrence_audit_v0.json
    results/near_breach_grammar_recurrence_audit_v0.md
    results/near_breach_grammar_recurrence_audit_v0_certificate.json

Purpose:

    search exact recurrence of near-breach Pattern A and Pattern B
    measure pattern_A_count and pattern_B_count
    measure pattern_after_pattern and recurrence distances
    test whether near-breach grammars are isolated or chainable

Boundary:

    grammar_recurrence != proof
    pattern recurrence != counterexample
    no recurrence observed != no recurrence possible
    bounded recurrence search != global invariant

## v6.2 Fuzzy Near-Breach Grammar Audit V0

The repository now includes a bounded Fuzzy Near-Breach Grammar Audit.

Run:

    python examples/build_fuzzy_near_breach_grammar_audit_v0.py

Outputs:

    results/fuzzy_near_breach_grammar_audit_v0.json
    results/fuzzy_near_breach_grammar_audit_v0.md
    results/fuzzy_near_breach_grammar_audit_v0_certificate.json

Purpose:

    search approximate recurrence of near-breach Pattern A and Pattern B
    measure hamming distance and normalized similarity
    measure fuzzy_A_count and fuzzy_B_count
    measure fuzzy_pattern_after_pattern
    test whether fuzzy near-breach grammars are isolated, chainable, or growth-producing

Boundary:

    fuzzy_grammar_audit != proof
    fuzzy recurrence != counterexample
    no fuzzy recurrence observed != no fuzzy recurrence possible
    bounded fuzzy grammar != global invariant

## v6.3 Fuzzy Rebound Anatomy V0

The repository now includes a bounded Fuzzy Rebound Anatomy Audit.

Run:

    python examples/build_fuzzy_rebound_anatomy_v0.py

Outputs:

    results/fuzzy_rebound_anatomy_v0.json
    results/fuzzy_rebound_anatomy_v0.md
    results/fuzzy_rebound_anatomy_v0_certificate.json

Purpose:

    isolate fuzzy near-breach grammar instances with post-pattern local growth
    measure whether rebound approaches the prior debt peak
    classify rebound as harmless, near-peak, second near-breach, or breach
    expose after-pattern a/delta/prefix sequences

Boundary:

    fuzzy_rebound_anatomy != proof
    local rebound != counterexample
    no second breach observed != no second breach possible
    bounded rebound anatomy != global invariant

## v6.4 Mature Rebound Guard V0

The repository now includes a bounded Mature Rebound Guard.

Run:

    python examples/build_mature_rebound_guard_v0.py

Outputs:

    results/mature_rebound_guard_v0.json
    results/mature_rebound_guard_v0.md
    results/mature_rebound_guard_v0_certificate.json

Purpose:

    correct raw fuzzy rebound breach classification
    separate weak-prefix rebound from mature-debt rebound
    require prior_debt_peak >= 4.0 before accepting a mature breach
    preserve raw v6.3 labels while adding guarded labels

Boundary:

    mature_rebound_guard != proof
    weak-prefix false breach != theorem
    no mature breach observed != no mature breach possible
    bounded guard != global closure

## v6.5 Finding Summary V0

The repository now includes a public bounded finding summary.

Read:

    docs/FINDING_SUMMARY_V0.md

Run:

    python examples/build_finding_summary_v0.py

Outputs:

    results/finding_summary_v0.json
    results/finding_summary_v0.md
    results/finding_summary_v0_certificate.json
    docs/FINDING_SUMMARY_V0.md

Current thesis:

    In bounded odd-step Collatz measurements, debt accumulation tends to trigger fast release,
    post-response debt generally falls below prior peaks, near-breach grammars exist but appear isolated,
    and apparent fuzzy breaches were reclassified as weak-prefix artifacts rather than mature regeneration chains.

Boundary:

    finding_summary != proof
    bounded evidence != global closure
    no mature second near-breach observed != no mature second near-breach possible
    Collatz remains unsolved

## v6.6 What Was Discovered

A public explanation of the current discovery state has been added.

Read:

    docs/WHAT_WAS_DISCOVERED.md

Purpose:

    explain what was measured
    explain what was discovered
    explain what was not discovered
    explain why it matters
    explain what would strengthen or weaken the interpretation

Current public thesis:

    In bounded odd-step Collatz measurements,
    debt accumulation tends to trigger fast release;
    post-response debt generally falls below prior peaks;
    near-breach grammars exist but appear isolated;
    apparent fuzzy breaches were weak-prefix artifacts;
    and no mature second near-breach chain was observed.

Boundary:

    not a proof
    not Collatz solved
    bounded measurement only
