# CRC Conjecture

CRC means Cheap Regeneration Chain.

## Informal statement

No positive odd Collatz trajectory can sustain an infinite cheap regeneration chain.

## Native formulation

A positive odd trajectory can escape only if it repeatedly does the following:

    regenerate 2-adic shadow of -1
    consume that shadow through a = 1 escape steps
    regenerate it again
    consume it again
    ...

while keeping the average compression debt at or below the escape threshold:

    average(a_i) <= log2(3)

The CRC conjecture says:

    this cannot happen in positive odd Collatz dynamics.

## Relation to Collatz

If every positive odd trajectory fails to sustain an infinite cheap regeneration chain, then every escaping trajectory is excluded.

This would reduce Collatz to the impossibility of infinite cheap regeneration.

## Current status

This is not proved.

This repository only formalizes and tests the language.

## v0.3 operational CRC form

v0.3 turns CRC into a finite diagnostic.

A locally cheap regeneration event is not enough.

The dangerous case is:

    locally cheap regeneration
    followed by another regeneration
    while the segment average debt remains <= log2(3)

Such an event is marked:

    chain_compatible = true

The long-term target becomes:

    no infinite sequence of chain_compatible regeneration events exists in N+.

## v0.4 collapse form

v0.4 adds the collapse form of CRC.

A chain-compatible segment is dangerous locally.

A finite chain-compatible run becomes less dangerous if followed by compensation:

    post_chain_average_debt > log2(3)

The long-term target becomes:

    every positive cheap regeneration chain is finite
    and every finite chain is eventually compensated by debt.

## v0.5 classified collapse form

v0.5 adds collapse cause classification.

A chain can collapse through:

    debt_spike
    shadow_exhaustion
    failed_regeneration
    post_chain_overcompensation
    terminal_descent

The CRC target becomes sharper:

    no infinite chain can avoid all collapse mechanisms forever.

## v0.6 refined collapse form

v0.6 refines the CRC obstruction vocabulary.

A chain can now collapse through:

    terminal_descent
    post_chain_overcompensation
    delayed_compensation
    debt_spike
    soft_debt_break
    failed_regeneration
    weak_regeneration
    shadow_exhaustion
    end_of_chain_without_escape

The refined CRC target is:

    no infinite chain can avoid the full collapse taxonomy forever.

## v0.7 compensation form

v0.7 turns CRC into a compensation-window search.

A dangerous chain has:

    chain_average_debt <= log2(3)

The compensating event is the first future window from the chain start with:

    recovery_average_debt > log2(3)

The refined CRC target becomes:

    no infinite chain can avoid finite recovery above log2(3).

## v0.8 post-chain recovery form

v0.8 refines the compensation form.

The earlier recovery window started at:

    chain_start_block

The stricter window starts at:

    chain_end_block + 1

The CRC target becomes:

    no finite cheap regeneration chain can be extended into an unrecovered post-chain escape window indefinitely.

## v0.9 hard recovery form

v0.9 adds hard recovery ranking.

The refined CRC target becomes:

    if every finite cheap chain recovers,
    the hardest recovered chains should reveal the limiting obstruction.

Hard cases are ranked by:

    long recovery distance
    small recovery surplus
    large chain deficit
    large recovery gap
    high combined hardness score

## v1.0 critical case form

v1.0 focuses the CRC target onto one critical recovered case.

The refined question becomes:

    can the critical recovery pattern be generalized or bounded?

If the pattern can be made arbitrarily long without recovery, the CRC direction fails.

If the pattern cannot be extended indefinitely, it may become a lemma candidate.

## v1.1 frontier form

v1.1 reframes the CRC search as a frontier problem.

Instead of asking only:

    does one hard case recover?

it asks:

    how does hardness move across nearby and structured candidates?

The relevant obstruction is no longer a single recovery event.

The relevant obstruction is whether recovery hardness can grow without bound.

## Frontier stability certificate exact baseline

The v1.2 scan does not claim proof.
It certifies that, within the selected finite frontier, the known critical case remains the active hardest case:

    n0 = 9780657630
    hardness = 15.100955299032181
    post-chain recovery distance = 114
    minimum surplus = 0.00275679752445801

## Compensation law candidate

The v1.3 direction is not to claim a proof.

The target candidate law is:

    every structurally dangerous low-debt window must be followed by finite compensation.

In v1.3 this is tested only over a finite frontier. A proof would require showing that compensation is forced by the arithmetic structure of 3n + 1 and v2(3n + 1).

## Adversarial compensation scan

The v1.4 scan searches for bad compensation windows that fail to recover.

A failure is recorded as a counterexample candidate, not as a proof-level contradiction.

Current intended reading:

    finite scan domain
    adversarially generated candidate set
    bad windows searched
    unrecovered windows counted
    no proof claim

## Hardness metric boundary

The current repository does not use a single universal meaning of hardness.

It separates:

- frontier recovery hardness
- compensation-window hardness
- adversarial compensation hardness
- tightest positive surplus
- known long-trajectory anchors

Different hardest cases are expected when the metric changes.

## v1.5.1 metric hygiene

The hardness report separates finite stress metrics. The tightest positive surplus metric now records the actual finite margin instead of a null placeholder.

## Native method boundary

The current project should not be read as a standard proof attempt first.

The native method studies:

expansion
discharge
debt
shadow
regeneration
compensation
obstruction
closure

The central native obstruction question is:

Can a debt structure exist that never generates compensating discharge?

The standard Collatz framing should re-enter only after the native closure mechanism is explicit.

## Native obstruction model

The native counterexample target is not just a trajectory that is long or hard.

The native obstruction target is:

    a self-preserving debt structure
    that regenerates
    without forced compensating discharge

Therefore, the project must distinguish:

    hardness != obstruction
    local recovery != closure
    long trajectory != native failure
    tight surplus != counterexample

The next step is native closure: showing whether such obstruction can or cannot exist.

## Native closure conditions

Native closure is not the same as reaching 1.

The native closure target is:

    debt can no longer preserve itself as obstruction

Therefore:

    local recovery != closure
    positive surplus != closure
    terminality != closure
    closure = obstruction potential erased

The next step is to map existing evidence artifacts into this native closure structure.

## Native evidence mapping

The existing computational artifacts are now mapped into native objects.

The purpose is to avoid jumping back to standard mathematics too early.

Mapped native objects:

    debt
    shadow
    compensation
    regeneration
    closure
    obstruction

Current interpretation:

    frontier stability = selected frontier evidence
    compensation recovery = local recovery evidence
    adversarial scan = finite obstruction-search evidence
    hardness report = stress classification, not obstruction

This does not prove the Collatz conjecture.

It prepares the next phase:

    native-to-standard translation boundary

## Native-to-standard translation boundary

The project now enters controlled translation.

The native source layer is preserved.

The standard layer may express native objects, but must not replace them.

Core distinction:

text:
native closure != reaching 1
hardness != obstruction
local recovery != closure
finite evidence != proof

The next phase is v2.1 Standard Definition Candidates.

## Standard definition candidates

v2.1 begins the controlled return to standard mathematics.

The standard layer may now define objects, but only under this rule:

    native object -> standard definition candidate -> native meaning retained

This prevents premature collapse into classical framing.

Current status:

    definitions only
    no theorem
    no proof claim
    no global closure claim

The next step is v2.2 Local Debt Lemma Candidates.

## Local debt lemma candidates

v2.2 introduces candidate lemmas.

Current status:

definitions -> lemma candidates

Not yet:

lemma candidates -> theorems
lemma candidates -> proof
finite evidence -> global closure

Key boundaries:

local debt != obstruction
bad window != obstruction
local recovery != native closure
positive surplus != full closure
hardness != obstruction

The next step is v2.3 Shadow and Regeneration Definition Refinement.

## Shadow and regeneration refinement

v2.3 refines the open native definitions needed before closure lemmas.

The project now separates:

regeneration
benign regeneration
dangerous regeneration
obstruction-preserving regeneration
shadow erasure

Critical boundary:

regeneration alone is not obstruction.

A native obstruction requires obstruction-preserving regeneration, not merely renewed debt.

No proof claim is made.
The next step is v2.4 Native Closure Lemma Candidates.
