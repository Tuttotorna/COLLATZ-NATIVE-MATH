# Near-Breach Audit V0 Results

## Status

This is a bounded near-breach audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`near_breach_below_one_percent_gap`

## Summary

- records_measured: `50000`
- analyzable_records: `35788`
- breach_count: `0`
- breach_rate: `0.000000000000`
- max_regeneration_ratio: `0.994339595811`
- min_gap_to_breach: `0.005660404189`
- mean_gap_to_breach: `3.506143061028`
- median_gap_to_breach: `1.564245406904`
- mean_regeneration_ratio: `-2.506143061028`
- median_regeneration_ratio: `-0.564245406904`
- gap_vs_log_seed_correlation: `-0.009002052657`
- gap_vs_log_seed_slope: `-0.243892102973`
- regeneration_ratio_vs_log_seed_correlation: `0.009002052657`
- regeneration_ratio_vs_log_seed_slope: `0.243892102973`
- first_half_best_gap: `0.005660404189`
- last_half_best_gap: `0.006951467865`
- top10_mean_seed: `28994.200000000001`
- top10_min_gap: `0.005660404189`
- top10_max_regeneration_ratio: `0.994339595811`
- near_breach_band_histogram:
  - 010001..019999: `4`
  - 030001..039999: `7`
  - 020001..029999: `5`
  - 040001..049999: `5`
  - 050001..059999: `6`
  - 060001..069999: `7`
  - 070001..079999: `6`
  - 080001..089999: `5`
  - 090001..099999: `5`
- band_best_candidates:
  - 000001..000999: `{'seed': 927, 'gap_to_breach': 0.029438879694982822, 'regeneration_ratio': 0.9705611203050172, 'debt_peak': 2.5112622276445142, 'response_delay': 1, 'survival_ratio': 0.03835350904445302, 'time_to_post_response_max': 4}`
  - 000001..009999: `{'seed': 2067, 'gap_to_breach': 0.019154435105108725, 'regeneration_ratio': 0.9808455648948913, 'debt_peak': 0.5851951371871749, 'response_delay': 1, 'survival_ratio': -1.417795943999537, 'time_to_post_response_max': 45}`
  - 010001..019999: `{'seed': 10087, 'gap_to_breach': 0.00566040418949143, 'regeneration_ratio': 0.9943395958105086, 'debt_peak': 6.359593029596537, 'response_delay': 2, 'survival_ratio': 0.7122341578538308, 'time_to_post_response_max': 27}`
  - 020001..029999: `{'seed': 20175, 'gap_to_breach': 0.006716619553084002, 'regeneration_ratio': 0.993283380446916, 'debt_peak': 5.359521518776384, 'response_delay': 2, 'survival_ratio': 0.6585378680806988, 'time_to_post_response_max': 27}`
  - 030001..039999: `{'seed': 35655, 'gap_to_breach': 0.006477970081142481, 'regeneration_ratio': 0.9935220299188575, 'debt_peak': 8.58809043019753, 'response_delay': 1, 'survival_ratio': 0.48591162376365943, 'time_to_post_response_max': 16}`
  - 040001..049999: `{'seed': 45127, 'gap_to_breach': 0.006744909936873156, 'regeneration_ratio': 0.9932550900631268, 'debt_peak': 8.248203961453708, 'response_delay': 1, 'survival_ratio': 0.4647274140086887, 'time_to_post_response_max': 16}`
  - 050001..059999: `{'seed': 53483, 'gap_to_breach': 0.0069514678646889205, 'regeneration_ratio': 0.9930485321353111, 'debt_peak': 8.003114441996383, 'response_delay': 1, 'survival_ratio': 0.44833508301928393, 'time_to_post_response_max': 16}`
  - 060001..069999: `{'seed': 60169, 'gap_to_breach': 0.007102279310044257, 'regeneration_ratio': 0.9928977206899557, 'debt_peak': 7.8331744546130775, 'response_delay': 1, 'survival_ratio': 0.4363667642266003, 'time_to_post_response_max': 16}`
  - 070001..079999: `{'seed': 71311, 'gap_to_breach': 0.007331691906081295, 'regeneration_ratio': 0.9926683080939187, 'debt_peak': 7.588070199024829, 'response_delay': 1, 'survival_ratio': 0.41816069851350385, 'time_to_post_response_max': 16}`
  - 080001..089999: `{'seed': 80225, 'gap_to_breach': 0.007499638823120436, 'regeneration_ratio': 0.9925003611768796, 'debt_peak': 7.418142949691951, 'response_delay': 1, 'survival_ratio': 0.4048325174949015, 'time_to_post_response_max': 16}`
  - 090001..099999: `{'seed': 90255, 'gap_to_breach': 0.007675489796860724, 'regeneration_ratio': 0.9923245102031393, 'debt_peak': 7.24818797671011, 'response_delay': 1, 'survival_ratio': 0.39087707459885007, 'time_to_post_response_max': 16}`

## Top near-breach candidates

- seed `10087`: regeneration_ratio=`0.994339595811`, gap_to_breach=`0.005660404189`, debt_peak=`6.359593029597`, response_delay=`2`, survival_ratio=`0.712234157854`, time_to_post_response_max=`27`
- seed `13449`: regeneration_ratio=`0.993944433639`, gap_to_breach=`0.006055566361`, debt_peak=`5.944591287057`, response_delay=`2`, survival_ratio=`0.692144748815`, time_to_post_response_max=`27`
- seed `15131`: regeneration_ratio=`0.993766152823`, gap_to_breach=`0.006233847177`, debt_peak=`5.774582854601`, response_delay=`2`, survival_ratio=`0.683081238949`, time_to_post_response_max=`27`
- seed `17023`: regeneration_ratio=`0.993577091021`, gap_to_breach=`0.006422908979`, debt_peak=`5.604604883591`, response_delay=`2`, survival_ratio=`0.673469641147`, time_to_post_response_max=`27`
- seed `35655`: regeneration_ratio=`0.993522029919`, gap_to_breach=`0.006477970081`, debt_peak=`8.588090430198`, response_delay=`1`, survival_ratio=`0.485911623764`, time_to_post_response_max=`16`
- seed `20175`: regeneration_ratio=`0.993283380447`, gap_to_breach=`0.006716619553`, debt_peak=`5.359521518776`, response_delay=`2`, survival_ratio=`0.658537868081`, time_to_post_response_max=`27`
- seed `45127`: regeneration_ratio=`0.993255090063`, gap_to_breach=`0.006744909937`, debt_peak=`8.248203961454`, response_delay=`1`, survival_ratio=`0.464727414009`, time_to_post_response_max=`16`
- seed `22697`: regeneration_ratio=`0.993063444909`, gap_to_breach=`0.006936555091`, debt_peak=`5.189588571906`, response_delay=`2`, survival_ratio=`0.647356699185`, time_to_post_response_max=`27`
- seed `53483`: regeneration_ratio=`0.993048532135`, gap_to_breach=`0.006951467865`, debt_peak=`8.003114441996`, response_delay=`1`, survival_ratio=`0.448335083019`, time_to_post_response_max=`16`
- seed `57115`: regeneration_ratio=`0.992965211745`, gap_to_breach=`0.007034788255`, debt_peak=`7.908325146690`, response_delay=`1`, survival_ratio=`0.441722819644`, time_to_post_response_max=`16`
- seed `60169`: regeneration_ratio=`0.992897720690`, gap_to_breach=`0.007102279310`, debt_peak=`7.833174454613`, response_delay=`1`, survival_ratio=`0.436366764227`, time_to_post_response_max=`16`
- seed `63387`: regeneration_ratio=`0.992828907372`, gap_to_breach=`0.007171092628`, debt_peak=`7.758007844917`, response_delay=`1`, survival_ratio=`0.430905774718`, time_to_post_response_max=`16`
- seed `25535`: regeneration_ratio=`0.992828558915`, gap_to_breach=`0.007171441085`, debt_peak=`5.019614133229`, response_delay=`2`, survival_ratio=`0.635415473123`, time_to_post_response_max=`27`
- seed `64255`: regeneration_ratio=`0.992810724090`, gap_to_breach=`0.007189275910`, debt_peak=`7.738386112273`, response_delay=`1`, survival_ratio=`0.429462758749`, time_to_post_response_max=`16`
- seed `67691`: regeneration_ratio=`0.992740216981`, gap_to_breach=`0.007259783019`, debt_peak=`7.663230804217`, response_delay=`1`, survival_ratio=`0.423867350857`, time_to_post_response_max=`16`
- seed `26899`: regeneration_ratio=`0.992719669753`, gap_to_breach=`0.007280330247`, debt_peak=`4.944537652280`, response_delay=`2`, survival_ratio=`0.629879723330`, time_to_post_response_max=`27`
- seed `71311`: regeneration_ratio=`0.992668308094`, gap_to_breach=`0.007331691906`, debt_peak=`7.588070199025`, response_delay=`1`, survival_ratio=`0.418160698514`, time_to_post_response_max=`16`
- seed `76153`: regeneration_ratio=`0.992575575823`, gap_to_breach=`0.007424424177`, debt_peak=`7.493293962294`, response_delay=`1`, survival_ratio=`0.410801513133`, time_to_post_response_max=`16`
- seed `80225`: regeneration_ratio=`0.992500361177`, gap_to_breach=`0.007499638823`, debt_peak=`7.418142949692`, response_delay=`1`, survival_ratio=`0.404832517495`, time_to_post_response_max=`16`
- seed `30263`: regeneration_ratio=`0.992460445749`, gap_to_breach=`0.007539554251`, debt_peak=`4.774535181903`, response_delay=`2`, survival_ratio=`0.616701192023`, time_to_post_response_max=`27`

## Native interpretation

The audit does not search for average behavior.

It searches for the hardest bounded cases: trajectories closest to regenerating a new post-response peak.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
