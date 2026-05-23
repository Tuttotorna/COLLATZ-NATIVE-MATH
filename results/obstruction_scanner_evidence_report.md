# Obstruction Scanner Evidence Report

Version: v2.7

This report interprets the v2.6 bounded obstruction scanner output.

It is not a proof.
It is not a theorem layer.
It is bounded native evidence.

## Summary

- tested_candidate_count: 439
- debt_window_count: 256578
- regeneration_count: 255331
- dangerous_regeneration_count: 50137
- obstruction_candidate_count: 0
- obstruction_detected: false
- native_interpretation: DANGEROUS_REGENERATION_FOUND_BUT_NO_OBSTRUCTION_CANDIDATE

## Boundary

No obstruction detected in a finite domain is not the same as no obstruction can exist.

Correct interpretation:

No obstruction candidate was detected in the v2.6 bounded domain.

Forbidden interpretation:

No obstruction can exist.

## Native conclusions

- The bounded domain contains many debt windows.
- The bounded domain contains many regeneration events.
- The bounded domain contains many dangerous-regeneration stress events.
- The bounded scanner detected no obstruction candidate.
- Dangerous regeneration is not obstruction by itself.
- No obstruction detected in a finite domain is not proof that obstruction cannot exist.

## Forbidden conclusions

- collatz_solved
- global_closure_proved
- obstruction_impossible
- finite_negative_result_is_proof
- dangerous_regeneration_equals_obstruction
- hardness_equals_obstruction

## Hardest by recovery

- n0=9780657630; odd_blocks=425; debt_windows=10399; regeneration=10397; dangerous_regeneration=4863; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=9780657631; odd_blocks=425; debt_windows=10383; regeneration=10381; dangerous_regeneration=4835; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=17592186044414; odd_blocks=210; debt_windows=2685; regeneration=2682; dangerous_regeneration=1178; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=127; hardest_score=15352831.108921394
- n0=63728127; odd_blocks=357; debt_windows=6727; regeneration=6725; dangerous_regeneration=1710; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=236; hardest_score=15179077.92751667
- n0=670617279; odd_blocks=370; debt_windows=7391; regeneration=7389; dangerous_regeneration=2294; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=231; hardest_score=15179077.92751667
- n0=989345275647; odd_blocks=506; debt_windows=10903; regeneration=10900; dangerous_regeneration=2672; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=173; hardest_score=5657363.860489567
- n0=626331; odd_blocks=189; debt_windows=2981; regeneration=2978; dangerous_regeneration=1087; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=110; hardest_score=4943146.874254355
- n0=2298025; odd_blocks=208; debt_windows=4761; regeneration=4758; dangerous_regeneration=1204; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0006230848644295239; max_post_recovery_blocks=110; hardest_score=4943146.874254355
- n0=9007199254740991; odd_blocks=309; debt_windows=4550; regeneration=4543; dangerous_regeneration=2385; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=132; hardest_score=4201028.748305032
- n0=3542887; odd_blocks=217; debt_windows=2946; regeneration=2941; dangerous_regeneration=695; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=112; hardest_score=4167566.030178391

## Tightest positive surplus

- n0=9780657630; odd_blocks=425; debt_windows=10399; regeneration=10397; dangerous_regeneration=4863; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=9780657631; odd_blocks=425; debt_windows=10383; regeneration=10381; dangerous_regeneration=4835; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=63728127; odd_blocks=357; debt_windows=6727; regeneration=6725; dangerous_regeneration=1710; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=236; hardest_score=15179077.92751667
- n0=670617279; odd_blocks=370; debt_windows=7391; regeneration=7389; dangerous_regeneration=2294; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=231; hardest_score=15179077.92751667
- n0=17592186044414; odd_blocks=210; debt_windows=2685; regeneration=2682; dangerous_regeneration=1178; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=127; hardest_score=15352831.108921394
- n0=4098; odd_blocks=56; debt_windows=642; regeneration=636; dangerous_regeneration=8; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=34; hardest_score=282630.8908032936
- n0=4099; odd_blocks=56; debt_windows=636; regeneration=630; dangerous_regeneration=8; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=34; hardest_score=282630.8908032936
- n0=77031; odd_blocks=129; debt_windows=1618; regeneration=1613; dangerous_regeneration=109; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=55; hardest_score=265293.091312249
- n0=77039; odd_blocks=112; debt_windows=1088; regeneration=1081; dangerous_regeneration=39; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=47; hardest_score=167149.38678719173
- n0=131071; odd_blocks=80; debt_windows=831; regeneration=829; dangerous_regeneration=213; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=62; hardest_score=1041271.7029595028

## Most debt windows

- n0=989345275647; odd_blocks=506; debt_windows=10903; regeneration=10900; dangerous_regeneration=2672; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=173; hardest_score=5657363.860489567
- n0=9780657630; odd_blocks=425; debt_windows=10399; regeneration=10397; dangerous_regeneration=4863; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=9780657631; odd_blocks=425; debt_windows=10383; regeneration=10381; dangerous_regeneration=4835; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=670617279; odd_blocks=370; debt_windows=7391; regeneration=7389; dangerous_regeneration=2294; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=231; hardest_score=15179077.92751667
- n0=63728127; odd_blocks=357; debt_windows=6727; regeneration=6725; dangerous_regeneration=1710; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=236; hardest_score=15179077.92751667
- n0=2298025; odd_blocks=208; debt_windows=4761; regeneration=4758; dangerous_regeneration=1204; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0006230848644295239; max_post_recovery_blocks=110; hardest_score=4943146.874254355
- n0=9007199254740991; odd_blocks=309; debt_windows=4550; regeneration=4543; dangerous_regeneration=2385; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=132; hardest_score=4201028.748305032
- n0=1117065; odd_blocks=196; debt_windows=3629; regeneration=3622; dangerous_regeneration=633; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=65; hardest_score=1041271.7029595028
- n0=837799; odd_blocks=195; debt_windows=3566; regeneration=3559; dangerous_regeneration=599; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=65; hardest_score=1041271.7029595028
- n0=281474976710652; odd_blocks=210; debt_windows=3020; regeneration=3017; dangerous_regeneration=1192; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0008960851374297807; max_post_recovery_blocks=103; hardest_score=2734115.205869027

## Most regeneration

- n0=989345275647; odd_blocks=506; debt_windows=10903; regeneration=10900; dangerous_regeneration=2672; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=173; hardest_score=5657363.860489567
- n0=9780657630; odd_blocks=425; debt_windows=10399; regeneration=10397; dangerous_regeneration=4863; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=9780657631; odd_blocks=425; debt_windows=10383; regeneration=10381; dangerous_regeneration=4835; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=670617279; odd_blocks=370; debt_windows=7391; regeneration=7389; dangerous_regeneration=2294; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=231; hardest_score=15179077.92751667
- n0=63728127; odd_blocks=357; debt_windows=6727; regeneration=6725; dangerous_regeneration=1710; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=236; hardest_score=15179077.92751667
- n0=2298025; odd_blocks=208; debt_windows=4761; regeneration=4758; dangerous_regeneration=1204; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0006230848644295239; max_post_recovery_blocks=110; hardest_score=4943146.874254355
- n0=9007199254740991; odd_blocks=309; debt_windows=4550; regeneration=4543; dangerous_regeneration=2385; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=132; hardest_score=4201028.748305032
- n0=1117065; odd_blocks=196; debt_windows=3629; regeneration=3622; dangerous_regeneration=633; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=65; hardest_score=1041271.7029595028
- n0=837799; odd_blocks=195; debt_windows=3566; regeneration=3559; dangerous_regeneration=599; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=65; hardest_score=1041271.7029595028
- n0=281474976710652; odd_blocks=210; debt_windows=3020; regeneration=3017; dangerous_regeneration=1192; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0008960851374297807; max_post_recovery_blocks=103; hardest_score=2734115.205869027

## Most dangerous regeneration

- n0=9780657630; odd_blocks=425; debt_windows=10399; regeneration=10397; dangerous_regeneration=4863; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=9780657631; odd_blocks=425; debt_windows=10383; regeneration=10381; dangerous_regeneration=4835; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963
- n0=989345275647; odd_blocks=506; debt_windows=10903; regeneration=10900; dangerous_regeneration=2672; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=173; hardest_score=5657363.860489567
- n0=9007199254740991; odd_blocks=309; debt_windows=4550; regeneration=4543; dangerous_regeneration=2385; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=132; hardest_score=4201028.748305032
- n0=670617279; odd_blocks=370; debt_windows=7391; regeneration=7389; dangerous_regeneration=2294; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=231; hardest_score=15179077.92751667
- n0=63728127; odd_blocks=357; debt_windows=6727; regeneration=6725; dangerous_regeneration=1710; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=236; hardest_score=15179077.92751667
- n0=2298025; odd_blocks=208; debt_windows=4761; regeneration=4758; dangerous_regeneration=1204; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0006230848644295239; max_post_recovery_blocks=110; hardest_score=4943146.874254355
- n0=281474976710652; odd_blocks=210; debt_windows=3020; regeneration=3017; dangerous_regeneration=1192; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0008960851374297807; max_post_recovery_blocks=103; hardest_score=2734115.205869027
- n0=281474976710653; odd_blocks=210; debt_windows=3017; regeneration=3014; dangerous_regeneration=1183; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0008960851374297807; max_post_recovery_blocks=98; hardest_score=2734115.205869027
- n0=17592186044414; odd_blocks=210; debt_windows=2685; regeneration=2682; dangerous_regeneration=1178; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=127; hardest_score=15352831.108921394

## Near obstruction cases

- n0=9780657630; odd_blocks=425; debt_windows=10399; regeneration=10397; dangerous_regeneration=4863; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963; class=EXTREME_STRESS_BUT_COMPENSATED
- n0=9780657631; odd_blocks=425; debt_windows=10383; regeneration=10381; dangerous_regeneration=4835; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=7.15128842860846e-05; max_post_recovery_blocks=183; hardest_score=74280320.99431963; class=EXTREME_STRESS_BUT_COMPENSATED
- n0=989345275647; odd_blocks=506; debt_windows=10903; regeneration=10900; dangerous_regeneration=2672; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=173; hardest_score=5657363.860489567; class=DANGEROUS_REGENERATION_STRESS
- n0=9007199254740991; odd_blocks=309; debt_windows=4550; regeneration=4543; dangerous_regeneration=2385; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=132; hardest_score=4201028.748305032; class=DANGEROUS_REGENERATION_STRESS
- n0=670617279; odd_blocks=370; debt_windows=7391; regeneration=7389; dangerous_regeneration=2294; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=231; hardest_score=15179077.92751667; class=DANGEROUS_REGENERATION_STRESS
- n0=63728127; odd_blocks=357; debt_windows=6727; regeneration=6725; dangerous_regeneration=1710; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=236; hardest_score=15179077.92751667; class=DANGEROUS_REGENERATION_STRESS
- n0=2298025; odd_blocks=208; debt_windows=4761; regeneration=4758; dangerous_regeneration=1204; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0006230848644295239; max_post_recovery_blocks=110; hardest_score=4943146.874254355; class=DANGEROUS_REGENERATION_STRESS
- n0=281474976710652; odd_blocks=210; debt_windows=3020; regeneration=3017; dangerous_regeneration=1192; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0008960851374297807; max_post_recovery_blocks=103; hardest_score=2734115.205869027; class=DANGEROUS_REGENERATION_STRESS
- n0=281474976710653; odd_blocks=210; debt_windows=3017; regeneration=3014; dangerous_regeneration=1183; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0008960851374297807; max_post_recovery_blocks=98; hardest_score=2734115.205869027; class=DANGEROUS_REGENERATION_STRESS
- n0=17592186044414; odd_blocks=210; debt_windows=2685; regeneration=2682; dangerous_regeneration=1178; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0001438822575672294; max_post_recovery_blocks=127; hardest_score=15352831.108921394; class=DANGEROUS_REGENERATION_STRESS
- n0=281474976710655; odd_blocks=210; debt_windows=2892; regeneration=2889; dangerous_regeneration=1151; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=89; hardest_score=4167566.030178391; class=DANGEROUS_REGENERATION_STRESS
- n0=281474976710654; odd_blocks=210; debt_windows=2958; regeneration=2955; dangerous_regeneration=1150; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=89; hardest_score=825037.0239494141; class=DANGEROUS_REGENERATION_STRESS
- n0=626331; odd_blocks=189; debt_windows=2981; regeneration=2978; dangerous_regeneration=1087; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=110; hardest_score=4943146.874254355; class=DANGEROUS_REGENERATION_STRESS
- n0=17592186044415; odd_blocks=210; debt_windows=2619; regeneration=2616; dangerous_regeneration=1069; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.00040335293738058553; max_post_recovery_blocks=127; hardest_score=1715778.698497959; class=DANGEROUS_REGENERATION_STRESS
- n0=4503599627370492; odd_blocks=210; debt_windows=2753; regeneration=2750; dangerous_regeneration=927; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=89; hardest_score=551822.1840512156; class=DANGEROUS_REGENERATION_STRESS
- n0=9007199254740984; odd_blocks=210; debt_windows=2753; regeneration=2750; dangerous_regeneration=927; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=89; hardest_score=551822.1840512156; class=DANGEROUS_REGENERATION_STRESS
- n0=4503599627370493; odd_blocks=210; debt_windows=2750; regeneration=2747; dangerous_regeneration=921; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=88; hardest_score=551822.1840512156; class=DANGEROUS_REGENERATION_STRESS
- n0=9007199254740986; odd_blocks=210; debt_windows=2750; regeneration=2747; dangerous_regeneration=921; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=88; hardest_score=551822.1840512156; class=DANGEROUS_REGENERATION_STRESS
- n0=68719476734; odd_blocks=191; debt_windows=2625; regeneration=2623; dangerous_regeneration=895; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=86; hardest_score=1520416.537506571; class=DANGEROUS_REGENERATION_STRESS
- n0=68719476735; odd_blocks=191; debt_windows=2560; regeneration=2558; dangerous_regeneration=875; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0007517849931295562; max_post_recovery_blocks=86; hardest_score=1629455.2447775372; class=DANGEROUS_REGENERATION_STRESS
- n0=4503599627370494; odd_blocks=210; debt_windows=2755; regeneration=2752; dangerous_regeneration=875; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=86; hardest_score=1520416.537506571; class=DANGEROUS_REGENERATION_STRESS
- n0=9007199254740988; odd_blocks=210; debt_windows=2755; regeneration=2752; dangerous_regeneration=875; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=86; hardest_score=1520416.537506571; class=DANGEROUS_REGENERATION_STRESS
- n0=9007199254740989; odd_blocks=210; debt_windows=2752; regeneration=2749; dangerous_regeneration=872; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0012443958305681235; max_post_recovery_blocks=85; hardest_score=825037.0239494141; class=DANGEROUS_REGENERATION_STRESS
- n0=4503599627370495; odd_blocks=210; debt_windows=2709; regeneration=2706; dangerous_regeneration=857; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0007517849931295562; max_post_recovery_blocks=86; hardest_score=1629455.2447775372; class=DANGEROUS_REGENERATION_STRESS
- n0=9007199254740990; odd_blocks=210; debt_windows=2709; regeneration=2706; dangerous_regeneration=857; obstruction_candidates=0; closure_result=DANGEROUS_REGENERATION_DETECTED; min_surplus=0.0007517849931295562; max_post_recovery_blocks=86; hardest_score=1629455.2447775372; class=DANGEROUS_REGENERATION_STRESS

## Next

v2.8 Expanded Bounded Obstruction Search

