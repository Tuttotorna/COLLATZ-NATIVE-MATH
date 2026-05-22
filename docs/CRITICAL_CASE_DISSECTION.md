# Critical Case Dissection

v1.0 stops adding broad taxonomy and opens the hardest known case found by v0.9.

The critical case is:

    n0 = 9780657630

v0.9 ranked it as the hardest recovered post-chain compensation case:

    post_chain_recovery_distance = 114
    post_chain_recovery_surplus ~= 0.002757
    chain_deficit ~= 0.156391
    hardness_score ~= 15.100955

This means recovery exists, but only barely.

---

## Why this case matters

The case is not interesting because it is large.

It is interesting because it is close to the threshold:

    log2(3) ~= 1.584963

The recovery window average was only slightly above the threshold:

    recovery_average ~= 1.587719

So the observed recovery margin was tiny.

That makes this case a natural target for structural inspection.

---

## v1.0 question

The v1.0 question is:

    what exact block structure produces the 114-block recovery distance?

The dissection records:

    critical chain start
    critical chain end
    post-chain recovery start
    post-chain recovery end
    block-by-block debt word
    rolling recovery averages
    deficit accumulation
    compensation accumulation
    first crossing above log2(3)

---

## Boundary

v1.0 is still not a proof of Collatz.

It is a microscope.

It turns the hardest sampled recovered case into a concrete object that can be inspected.
