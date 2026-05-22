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
