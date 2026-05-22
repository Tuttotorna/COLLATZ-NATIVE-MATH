# Adversarial Compensation Scan

Version: v1.4

This scan attempts to break the compensation-law candidate.

It starts from known hard cases and expands into local adversarial neighborhoods:
- nearby integers
- powers-of-two offsets
- bit-flip perturbations
- doubled and halved structural relatives

The scan searches for bad windows where the local average debt falls below log2(3).

A bad window is considered recovered when a following finite block raises the combined average back to at least log2(3).

The scanner writes:

results/adversarial_compensation_rows.jsonl
results/adversarial_compensation_summary.json
results/adversarial_compensation_certificate.json

The certificate is finite. It is not a proof of the Collatz conjecture.
