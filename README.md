# COLLATZ-NATIVE-MATH

A problem-born mathematical approach to Collatz via compression debt, 2-adic shadow, and cheap regeneration chains.

This repository does not claim to prove the Collatz conjecture.

It defines a local mathematical language born from the Collatz rule itself.

The guiding idea is:

    Collatz should not first be measured by an external mathematics.
    Collatz should be allowed to generate the mathematics needed to make its own behavior speak.

---

## Core claim

The classical Collatz rule is already known:

    if n is even: n -> n / 2
    if n is odd:  n -> 3n + 1

The unresolved part is not the local rule.

The unresolved part is the global destiny of the rule.

This repository explores the following local language:

    Collatz is not primarily a sequence of numbers.
    Collatz is a sequence of compression debts.

---

## Accelerated odd dynamics

Instead of watching every step, we watch only odd-to-odd transitions.

For every positive odd n_i:

    3 n_i + 1 = 2^(a_i) n_(i+1)

where:

    a_i >= 1
    n_i is odd
    n_(i+1) is odd

The value:

    a_i = v2(3 n_i + 1)

is called the compression debt.

---

## 2-adic shadow of -1

For every positive odd n_i, define:

    s_i = v2(n_i + 1)

This measures how closely n_i imitates -1 in the 2-adic sense.

If:

    s_i >= 2

then:

    a_i = 1

and the local step is an escape step.

During such an escape step:

    s_(i+1) = s_i - 1

So escape consumes the 2-adic shadow of -1.

---

## Cheap regeneration chain

Escape cannot continue forever unless the trajectory regenerates shadow.

A regeneration chain is a repeated pattern:

    regenerate shadow
    consume shadow through a = 1 escape steps
    regenerate shadow again
    consume again
    ...

A cheap regeneration chain is one where the trajectory regenerates enough shadow while keeping average compression debt too low.

The internal target of this repository is:

    No positive odd Collatz trajectory can sustain an infinite cheap regeneration chain.

Equivalently:

    no infinite cheap regeneration chain in positive odd Collatz dynamics

---

## Current status

This repository is exploratory.

It does not prove Collatz.

It defines:

    debt words
    compression debt
    2-adic shadow
    escape consumption
    regeneration
    cheap regeneration chains

and provides scripts to trace and test these quantities.

The goal is to determine whether this problem-born language can reduce the unresolved state of Collatz.

---

## Run the demo

    python examples/trace_collatz_native.py

Run tests:

    pytest -q

---

## Boundary

This repository does not claim:

    Collatz is solved
    a proof exists here
    this language is complete
    this replaces existing mathematics

It claims only:

    Collatz can be re-observed through a native language of debt, shadow, and regeneration.

Any result must be judged by one standard:

    does it reduce the unresolved state of the problem?

## v0.2: Regeneration epochs

v0.2 adds operational regeneration epochs.

The repository now measures:

    regenerated shadow
    compression cost
    cheapness ratio
    future escape capacity

Run:

    python examples/analyze_regeneration_epochs.py

The key clarification is:

    cheap regeneration exists locally.

Therefore the real target is not:

    no cheap regeneration exists

but:

    no infinite cheap regeneration chain exists in positive odd Collatz dynamics.

## v0.3: Cheap regeneration chain analysis

v0.3 adds finite chain diagnostics.

Run:

    python examples/analyze_cheap_regeneration_chains.py

This analyzes whether local cheap regeneration events can connect into chain-compatible segments before debt rises above:

    log2(3)

The current native target is:

    no infinite cheap regeneration chain in positive odd Collatz dynamics

v0.3 does not prove this.

It creates the first operational detector for finite chain-compatible regeneration.

## v0.4: Chain collapse analysis

v0.4 adds chain collapse and post-chain compensation analysis.

Run:

    python examples/analyze_chain_collapse.py

This analyzes finite chain-compatible runs and measures:

    chain length
    chain average debt
    collapse cause
    post-chain average debt
    compensation surplus

The v0.4 target is:

    finite cheap regeneration chains exist,
    but they should be followed by debt compensation.

This is still not a proof of Collatz.

It is a sharper operational form of the CRC target.

## v0.5: Collapse cause classification

v0.5 classifies why finite cheap regeneration chains collapse.

Run:

    python examples/analyze_collapse_causes.py

The classifier marks collapse mechanisms such as:

    debt_spike
    shadow_exhaustion
    failed_regeneration
    post_chain_overcompensation
    terminal_descent

This does not prove Collatz.

It sharpens the native target:

    every infinite cheap regeneration chain would need to avoid every known collapse mechanism forever.

## v0.6: Unclassified collapse analysis

v0.6 targets collapse episodes previously left unclassified.

Run:

    python examples/analyze_unclassified_collapses.py

The refined taxonomy adds:

    soft_debt_break
    weak_regeneration
    delayed_compensation
    end_of_chain_without_escape

The goal is to reduce unclassified collapse residue and sharpen the CRC obstruction language.

## v0.7: Compensation law search

v0.7 searches for quantitative compensation behavior.

Run:

    python examples/analyze_compensation_law.py

This measures:

    chain_deficit
    recovery_distance_blocks
    recovery_average_debt
    recovery_surplus
    recovery_to_chain_length_ratio

The v0.7 question is:

    after a low-debt cheap regeneration chain,
    how long before the trajectory average from that chain start crosses back above log2(3)?

This is not a proof.

It is a search for a compensation law.

## v0.8: Post-chain recovery analysis

v0.8 separates chain-start recovery from post-chain recovery.

Run:

    python examples/analyze_post_chain_recovery.py

v0.7 measured recovery from:

    chain_start_block

v0.8 also measures recovery from:

    chain_end_block + 1

This avoids a false impression of immediate compensation caused by including the initial regeneration block.

## v0.9: Hard recovery case analysis

v0.9 ranks the hardest recovered compensation cases.

Run:

    python examples/analyze_hard_recovery_cases.py

It ranks cases by:

    hardness_score
    post_chain_recovery_distance
    smallest post_chain_recovery_surplus
    chain_deficit_below_threshold
    recovery_distance_gap

The purpose is to identify the most dangerous recovered cases for later structural inspection.

## v1.0: Critical case dissection

v1.0 opens the hardest recovered case found by v0.9:

    n0 = 9780657630

Run:

    python examples/analyze_critical_case.py

The script writes:

    results/critical_case_dissection.json
    results/critical_case_blocks.jsonl
    results/critical_case_window.jsonl
    results/critical_case_summary.json

The purpose is to inspect the exact block structure behind the hardest known post-chain recovery case.

## v1.1: Critical frontier scan

v1.1 expands beyond the single v1.0 hard case.

Run:

    python examples/scan_critical_frontier.py

The script writes:

    results/critical_frontier_scan.jsonl
    results/critical_frontier_summary.json

The purpose is to test whether the v1.0 case is still the hardest observed recovered post-chain case inside a bounded frontier scan.

## v1.2 frontier stability certificate exact baseline

The critical frontier scanner now emits a stability certificate:

    python examples/scan_critical_frontier.py

Expected active frontier:

    current hardest: n0=9780657630
    hardness = 15.100955299032181
    comparison_status = SAME_AS_PREVIOUS
    frontier_stable = true
    harder_than_previous_critical = false

The certificate is written to:

    results/frontier_stability_certificate.json

Important: the baseline hardness must not be rounded below the comparison tolerance.

This is a finite computational certificate over the selected candidate frontier.
It is not a proof of the Collatz conjecture.

## v1.3 compensation law candidate

The repository now includes a finite scanner for the compensation-law candidate:

    python examples/analyze_compensation_law_candidate.py

The scanner detects maximal bad debt windows and checks whether each has a finite recovery window.

Generated outputs:

    results/compensation_law_candidate_rows.jsonl
    results/compensation_law_candidate_summary.json
    results/compensation_law_candidate_certificate.json

This is a falsifiable finite certificate. It is not a proof of the Collatz conjecture.

## v1.4 adversarial compensation scan

The v1.4 scan tries to break the compensation-law candidate.

Run:

    python examples/adversarial_compensation_scan.py

Generated artifacts:

    results/adversarial_compensation_rows.jsonl
    results/adversarial_compensation_summary.json
    results/adversarial_compensation_certificate.json

Meaning:

    no unrecovered bad window found = finite negative adversarial result

Limit:

    this is not a proof of the Collatz conjecture.

## v1.5 hardness metric report

The repository now separates different meanings of "hardest Collatz case".

Run:

`python examples/build_hardness_metric_report.py`

Outputs:

`results/hardness_metric_report.json`

`results/hardness_metric_report.md`

Key point:

`9780657630` can remain the hardest frontier-recovery case while `63728127` can be the hardest adversarial-compensation case.

This is not a contradiction. They are different measurement lenses.

## v1.5.1 hardness report correction

The hardness metric report now correctly records:

    tightest_positive_surplus:
      n0 = 63728127
      min_surplus = 1.7736432994075457e-05

This fixes a null extraction issue in v1.5.

## v1.6 Native Method Boundary

The repository now separates the native method from the classical translation layer.

The current computational scans remain valid evidence layers, but they are not the native theory itself.

Correct order:

native primitives
-> native dynamics
-> native obstruction question
-> native closure criterion
-> computational evidence
-> standard mathematical translation

Central native question:

Can a debt structure exist that never generates compensating discharge?

New documents:

docs/NATIVE_METHOD.md
docs/STANDARD_TRANSLATION_BOUNDARY.md
docs/NATIVE_OBJECTS.md
docs/NATIVE_RESEARCH_PROGRAM.md
docs/EVIDENCE_LAYER_STATUS.md

Boundary:

Standard mathematics re-enters only after the native structure has been exposed.

This is not a proof of the Collatz conjecture.

It is a methodological correction and a research boundary.

## v1.7 Native Obstruction Model

The repository now defines the native obstruction model.

A native obstruction is not merely:

    a long trajectory
    a high hardness score
    a tight positive surplus
    many bad windows

A native obstruction is:

    persistent unclosed debt

More precisely:

    debt is generated
    debt persists
    shadow is not erased
    regeneration occurs
    compensation is insufficient
    no closure event is forced
    the structure remains internally admissible

Central native question:

    Can debt regenerate forever without ever forcing compensating discharge?

New documents:

    docs/NATIVE_OBSTRUCTION_MODEL.md
    docs/NATIVE_FAILURE_CONDITION.md
    docs/NATIVE_REGENERATION.md
    docs/NATIVE_CLOSURE_OPPOSITE.md
    docs/NATIVE_HARDNESS_VS_OBSTRUCTION.md

This is not a proof of the Collatz conjecture. It defines the native obstruction target before standard mathematical translation.

## v1.8 Native Closure Conditions

The repository now defines native closure.

Native closure is not reaching 1.

Native closure is:

    obstruction potential erased

Closure sequence:

    debt generated
    -> debt shadow carried
    -> compensation appears
    -> compensation sufficiency holds
    -> shadow erasure holds
    -> regeneration does not preserve obstruction
    -> closure declared

Core distinction:

    local recovery != native closure
    reaching 1 != native closure
    positive surplus != full closure

New documents:

    docs/NATIVE_CLOSURE_CONDITIONS.md
    docs/NATIVE_CLOSURE_TEST.md
    docs/NATIVE_DEBT_ERASURE.md
    docs/NATIVE_SHADOW_ERASURE.md
    docs/NATIVE_COMPENSATION_SUFFICIENCY.md

This is not a proof of the Collatz conjecture. It defines the native closure target before standard mathematical translation.

## v1.9 Native Evidence Mapping

The repository now maps existing computational evidence into native objects.

This step does not add a bigger scan.

It maps:

    frontier_stability_certificate
    compensation_law_candidate_certificate
    adversarial_compensation_certificate
    hardness_metric_report

into:

    debt
    shadow
    compensation
    regeneration
    closure
    obstruction

Run:

    python examples/build_native_evidence_map.py

Outputs:

    results/native_evidence_map.json
    results/native_evidence_map.md

Core rule:

    Evidence is not proof.
    Hardness is not obstruction.
    Local recovery is not full native closure.
    Standard mathematics remains deferred.

Next:

    v2.0 Native-to-Standard Translation Boundary

## v2.1 Standard Definition Candidates

The repository now introduces candidate standard definitions.

Core rule:

    native object -> standard definition candidate -> native meaning retained

Stable candidate definitions:

    odd block
    discharge exponent
    expansion pressure
    local debt
    cumulative debt
    bad window
    compensation
    surplus

Open candidate definitions:

    shadow
    regeneration
    obstruction candidate
    closure candidate

This is not a proof layer.

It is a controlled definition layer before lemma candidates.

## v2.2 Local Debt Lemma Candidates

The repository now introduces lemma candidates.

Core rule:

native object -> standard definition -> lemma candidate -> native meaning retained

Stable lemma candidates include:

- odd block decomposition
- discharge exponent uniqueness
- local debt formation
- cumulative debt over an interval
- bad window equivalence
- compensation recovery
- positive surplus

Boundary lemma candidates include:

- local recovery is not native closure
- hardness is not obstruction
- tight surplus is not obstruction

This is not a theorem layer.
This is not a proof layer.

## v2.3 Shadow and Regeneration Definition Refinement

The repository now refines the previously open shadow/regeneration definitions.

Core distinctions:

- regeneration is renewed debt after compensation;
- benign regeneration is renewed debt that is compensated;
- dangerous regeneration is renewed debt with persistent shadow or weakening compensation;
- obstruction-preserving regeneration is renewed debt that keeps obstruction potential alive;
- shadow erasure means prior debt loses obstruction-carrying power.

Important boundary:

regeneration alone is not obstruction.

Obstruction requires:

persistent debt + non-erased shadow + dangerous regeneration + insufficient compensation + no closure event + internal admissibility

This is still not a proof layer.
It prepares v2.4 Native Closure Lemma Candidates.

## v2.5 Obstruction Search Protocol

The repository now defines how to search for obstruction-preserving regeneration.

Search target:

obstruction-preserving regeneration

Required obstruction signature:

persistent debt
non-erased shadow
dangerous regeneration
insufficient compensation
no closure event
internal admissibility

Core boundary:

No obstruction detected in a finite domain is not the same as no obstruction can exist.

This is a protocol layer, not a proof layer.

## v2.6 Bounded Obstruction Search Scanner

The repository now includes a bounded scanner for native obstruction search.

The scanner searches for obstruction-preserving regeneration.

It does not merely search for:

    long trajectory
    high hardness score
    tight positive surplus
    many bad windows

Run:

    python examples/bounded_obstruction_search_scanner.py

Outputs:

    results/bounded_obstruction_search_rows.jsonl
    results/bounded_obstruction_search_summary.json
    results/bounded_obstruction_search_certificate.json

Boundary:

    No obstruction detected in a finite domain is not the same as no obstruction can exist.

This is not a proof layer.

## v2.7 Obstruction Scanner Evidence Report

The repository now includes an evidence report layer for the v2.6 bounded scanner.

Run:

    python examples/build_obstruction_scanner_evidence_report.py

Outputs:

    results/obstruction_scanner_evidence_report.json
    results/obstruction_scanner_evidence_report.md
    results/obstruction_scanner_evidence_certificate.json

The report identifies:

    hardest_by_recovery
    tightest_positive_surplus
    most_debt_windows
    most_regeneration
    most_dangerous_regeneration
    near_obstruction_cases

Boundary:

    No obstruction detected in a finite domain is not the same as no obstruction can exist.

This is not a proof layer.

## v2.8 Expanded Bounded Obstruction Search

The repository now includes targeted expanded bounded search.

This is not blind brute force.

The scanner expands around prior near-obstruction evidence and searches for:

obstruction-preserving regeneration

Run:

python examples/expanded_bounded_obstruction_search.py

Outputs:

results/expanded_bounded_obstruction_search_rows.jsonl
results/expanded_bounded_obstruction_search_summary.json
results/expanded_bounded_obstruction_search_certificate.json

Boundary:

No obstruction detected in a finite expanded bounded domain is not the same as no obstruction can exist.

This is not a proof layer.

## v2.9 Shadow Persistence Instrumentation

The repository now instruments shadow persistence over the v2.8 expanded bounded search.

The question is no longer simply:

more candidates

The question is:

does dangerous regeneration carry prior debt shadow?

Run:

python examples/build_shadow_persistence_instrumentation.py

Outputs:

results/shadow_persistence_report.json
results/shadow_persistence_report.md
results/shadow_persistence_certificate.json

Core boundary:

shadow signal != obstruction
persistent shadow signal != proof
finite negative result != impossibility

This prepares v3.0 Formal Native-to-Standard Lemma Draft.

## v3.1 Native Language Inversion

This project does not begin by trying to solve Collatz.

It begins by learning the native language generated by the Collatz transformation itself.

Core rule:

No solution before native language.

Secondary rule:

No proof before native description.

Collatz is treated first as a native dynamical language, not as a terminal human problem.

The native language currently includes:

expansion
discharge
debt
shadow
regeneration
compensation
closure
obstruction

The classical question, "does it reach 1?", is treated as a later translation-layer endpoint.

The native question is earlier:

What is Collatz before it becomes a conjecture?

The deeper native question is:

What kind of debt can survive its own discharge?

v3.1 reclassifies previous scans, evidence reports, and lemma drafts as tools for learning the native grammar, not as a proof claim.

## v3.2 Native Grammar Map

The repository now maps the native grammar generated by Collatz.

Core rule:

No solution before native language.

No proof before native description.

Collatz is treated first as a native dynamical grammar, not as a conjecture to solve.

Native grammar objects:

expansion
discharge
debt
shadow
regeneration
compensation
closure
obstruction

The prior scanners are now classified as grammar probes.

They do not prove Collatz.

They help observe what Collatz generates.

Next step:

v3.3 Native Sentence Extractor

## v3.4 Native Sentence Atlas

The repository now includes a Native Sentence Atlas.

The atlas does not ask first whether Collatz is solved.

It asks:

What sentence forms does Collatz produce before it is translated into a terminal conjecture?

Run:

    python examples/build_native_sentence_atlas.py

Outputs:

    results/native_sentence_atlas.json
    results/native_sentence_atlas.md
    results/native_sentence_atlas_certificate.json

Core rule:

    No solution before native language.

This is not a proof layer.
