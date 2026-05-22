# Hard Recovery Cases

v0.9 isolates the hardest compensation cases found by the current native metrics.

Earlier versions showed:

    cheap regeneration exists
    chain-compatible segments exist
    finite chains exist
    chain collapses can be classified
    post-chain recovery exists in the sampled set

v0.8 showed that every detected chain in the sample had post-chain recovery.

v0.9 asks:

    which recovered chains are closest to failing recovery?

---

## Hardness criteria

A hard recovery case can be hard in several different ways.

### Long recovery distance

The post-chain window needs many future odd blocks before crossing above log2(3).

### Minimal recovery surplus

The recovery average crosses the threshold by a very small margin.

### Large chain deficit

The original chain average lies far below log2(3).

### Large recovery gap

The difference between chain-start recovery and post-chain recovery is large.

### High combined hardness

A composite score ranks cases that combine several risk factors.

---

## Why this matters

If a counterexample-like structure exists, it will not appear in easy cases.

It would likely resemble:

    long post-chain recovery distance
    very small recovery surplus
    large chain deficit
    repeated cheap regeneration
    low average debt close to log2(3)

Hard recovery cases are therefore the correct next target.

---

## v0.9 target

v0.9 does not prove Collatz.

It identifies the most structurally dangerous recovered cases.

Those cases become the next objects to inspect.
