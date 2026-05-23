# What Was Discovered

## Status

This document explains what the repository has discovered so far.

It does not prove Collatz.

It does not claim Collatz is solved.

It does not introduce a theorem.

It does not claim global closure.

It summarizes bounded structural measurements.

## Short version

The work did not discover a proof.

It discovered a measurable structural grammar inside odd-step Collatz behavior.

That grammar can be summarized as:

```text
debt -> release -> response -> reduction
```

The important negative result is:

```text
No persistent mature low-compression regeneration chain was observed
inside the measured bounded artifacts.
```

This matters because a divergent Collatz-like behavior would need more than local growth.

It would need the ability to regenerate growth after release again and again.

The current measurements show local near-regeneration events, but not a persistent mature chain.

## What was measured

The repository measures odd-step Collatz dynamics.

For an odd integer n_i:

```text
3*n_i + 1 = 2^a_i * n_(i+1)
```

where:

```text
a_i = v2(3*n_i + 1)
n_(i+1) = (3*n_i + 1) / 2^a_i
```

The value a_i is the local discharge.

The logarithmic odd-step drift is:

```text
delta_i = log2(n_(i+1) / n_i)
```

Interpretation:

```text
delta_i > 0  -> debt creation / expansion
delta_i < 0  -> discharge / compression
```

The native vocabulary is:

```text
debt
release
response
regeneration
near-breach
weak-prefix rebound
mature-debt rebound
```

## What was discovered

### 1. Debt creates measurable release pressure

The measurements show that higher debt peaks tend to be followed by stronger release behavior.

This does not mean Collatz is proved.

It means the native idea of debt creating pressure became measurable.

Earlier versions measured positive relationships between debt_peak, post_peak_release_count, post_peak_strong_release_count, and post_peak_release_mass.

This is bounded structural evidence, not a theorem.

### 2. The release response is usually fast

A major measured result is response-time stability.

After a debt peak, the first release response usually appears immediately or very quickly.

In the current measured artifacts:

```text
median response delay = 1
```

This suggests that Collatz does not merely allow debt to build freely inside the measured range.

It tends to answer debt quickly.

Boundary:

```text
fast response != proof
```

### 3. Post-response debt usually falls below the prior peak

The next question was more important:

```text
After response, does debt survive?
```

The measured result was strong reduction.

Post-response debt generally falls below the previous debt peak.

That means local expansion is not enough.

A dangerous trajectory would need to do something more specific:

```text
create debt
survive release
regenerate above the prior peak
repeat this pattern
```

The measured artifacts did not show that as a mature persistent chain.

### 4. Near-breach candidates exist

The repo did find near-breach candidates.

A near-breach is a trajectory that almost rebuilds prior debt after release.

These are the most interesting cases because they are the places where Collatz most closely resembles a regeneration structure.

But in the bounded measurement:

```text
breach_count = 0
```

and the best candidates stayed below breach.

So the repository found where the pressure is highest, but did not find mature escape.

### 5. Near-breach grammar is expansion-rich but isolated

Near-breach candidates share grammar.

They are not just arbitrary seeds.

Some of them contain repeated-looking a_i patterns.

The important observation is:

```text
near-breach windows are expansion-rich
```

They often contain many a = 1 steps, which are locally expansive.

But the next question was:

```text
Do these grammars recur?
```

The measured answer was:

```text
No dangerous recurrence chain observed.
```

So the repo separated:

```text
near-breach grammar
!=
persistent near-breach recurrence
```

### 6. Fuzzy matching increased hits but not dangerous chains

Exact pattern matching can be too strict.

So the repo also tested fuzzy grammar matching.

That increased the number of detected pattern hits.

But the important result was:

```text
more fuzzy hits did not become dangerous fuzzy chains
```

This prevents a common mistake:

```text
similar pattern found
therefore dangerous recurrence found
```

The repo measured the difference.

### 7. Apparent fuzzy breaches were false positives

At v6.3, two apparent fuzzy breaches appeared.

That looked important.

But v6.4 corrected the interpretation.

Those apparent breaches were caused by weak prior peaks.

In plain terms:

```text
If the starting peak is tiny,
a later rebound can look huge by ratio,
even if it is not mature debt regeneration.
```

So v6.4 introduced the mature rebound guard.

Result:

```text
raw fuzzy breaches: 2
weak-prefix false breaches: 2
mature breaches: 0
mature second near-breaches: 0
```

This is one of the most important results of the repo.

Not because it proves Collatz.

Because it shows the measurement language can correct itself.

It can separate a seductive false signal from a mature structural signal.

## What was not discovered

The repository did not discover a proof.

It did not discover a global invariant.

It did not discover a universal stopping rule.

It did not prove that divergence is impossible.

It did not prove that mature regeneration chains cannot exist.

It did not prove that the observed bounded behavior continues forever.

Any public claim stronger than this would be wrong.

## Why this matters

The value of the work is not that it solved Collatz.

The value is that it reframed Collatz as a measurable structural process.

Instead of asking only:

```text
Does every number reach 1?
```

the repo also asks:

```text
What would a non-terminating behavior need to preserve?
```

The measured answer is:

```text
It would need persistent mature low-compression regeneration.
```

Then the repo asks:

```text
Do we observe that structure?
```

Current bounded answer:

```text
No.
```

This is not a proof.

But it is a meaningful obstruction language.

It turns the vague idea of possible endless growth into a more precise structural requirement.

A divergent candidate would need to defeat the observed pattern:

```text
debt -> release -> response -> reduction
```

and replace it with:

```text
debt -> release -> mature regeneration -> new debt peak -> repeat
```

That second grammar was not observed as a persistent mature chain.

## What would strengthen this work

The work becomes stronger if future versions add:

```text
larger seed ranges
larger odd-step horizons
independent replication
faster implementation
formal definitions
comparison with known probabilistic Collatz heuristics
adversarial search for mature regeneration chains
public notebooks with reproducible plots
```

The most important next scientific test is not another small metric.

It is an adversarial search:

```text
Find seeds that maximize mature post-response regeneration.
```

If such seeds exist, they should be hunted directly.

If they do not appear under aggressive search, the obstruction language becomes more credible.

## What would weaken or falsify this work

The current interpretation would weaken if future tests find:

```text
mature_breach_count > 0
mature_second_near_breach_count > 0
recurring mature near-breach chains
post-response new peaks at meaningful frequency
response delay growing with scale
debt survival increasing with scale
fuzzy grammar recurrence becoming persistent
```

That would not disprove Collatz.

But it would weaken the current structural interpretation.

A good measurement framework must say what would count against it.

## Current public thesis

```text
In bounded odd-step Collatz measurements,
debt accumulation tends to trigger fast release;
post-response debt generally falls below prior peaks;
near-breach grammars exist but appear isolated;
apparent fuzzy breaches were weak-prefix artifacts;
and no mature second near-breach chain was observed.
```

## Honest conclusion

This repository does not solve Collatz.

But it does appear to have found a useful measurement language for Collatz.

The core discovery is not a final answer.

The core discovery is a sharper question:

```text
Can Collatz sustain persistent mature low-compression regeneration?
```

So far, in the measured bounded artifacts:

```text
No.
```

## Boundary

```text
measurement != proof
bounded evidence != global theorem
near-breach != divergence
rebound != mature breach
fuzzy similarity != structural recurrence
weak-prefix ratio spike != mature regeneration
no observed mature chain != impossible mature chain
Collatz remains unsolved
```
