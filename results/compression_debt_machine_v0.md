# Compression Debt Machine V0 Results

## Status

This is a bounded measurement result.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

## Parameters

- max_odd_seed: `999`
- odd_steps: `80`
- epsilon: `0.0`
- log2_3: `1.584962500721`

## Counts

- odd_seeds_measured: `500`
- terminated_within_bound: `500`
- not_terminated_within_bound: `0`
- cheap_chain_epsilon_0_count: `1`
- regeneration_capable_count: `231`

## Aggregate measurements

- mean_delta_mean: `-0.751209666150`
- cumulative_debt_mean: `-8.524089003324`
- debt_peak_mean: `1.656567700596`
- max_debt_peak: `6.892124975745`
- max_a_seen: `10`
- debt_peak_vs_max_a_pearson: `0.014038722339`
- debt_peak_vs_release_count_pearson: `0.639086442305`
- debt_peak_vs_strong_release_count_pearson: `0.634836694059`

## Highest debt-peak samples

- seed `703`: debt_peak=`6.892124975745`, mean_delta=`-0.152538401275`, max_a=`6`, release_count=`12`, terminated=`True`
- seed `27`: debt_peak=`6.832421226170`, mean_delta=`-0.115972865906`, max_a=`5`, release_count=`7`, terminated=`True`
- seed `31`: debt_peak=`6.633112417947`, mean_delta=`-0.127030674625`, max_a=`5`, release_count=`7`, terminated=`True`
- seed `937`: debt_peak=`6.477600617158`, mean_delta=`-0.156696908534`, max_a=`6`, release_count=`12`, terminated=`True`
- seed `41`: debt_peak=`6.229756723715`, mean_delta=`-0.133938800115`, max_a=`5`, release_count=`7`, terminated=`True`
- seed `871`: debt_peak=`6.191683935998`, mean_delta=`-0.150254290902`, max_a=`5`, release_count=`13`, terminated=`True`
- seed `47`: debt_peak=`6.032719876656`, mean_delta=`-0.146173390834`, max_a=`5`, release_count=`7`, terminated=`True`
- seed `55`: debt_peak=`5.805949014809`, mean_delta=`-0.141008773501`, max_a=`5`, release_count=`8`, terminated=`True`
- seed `63`: debt_peak=`5.610028804834`, mean_delta=`-0.153263587782`, max_a=`5`, release_count=`8`, terminated=`True`
- seed `71`: debt_peak=`5.437561608829`, mean_delta=`-0.166209381608`, max_a=`5`, release_count=`7`, terminated=`True`

## Native interpretation

The machine makes the debt/release vocabulary computable.

A possible divergent Collatz behavior would require more than local growth.

It would require persistent low-compression regeneration.

The V0 machine measures bounded approximations of that requirement.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- obstruction_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
