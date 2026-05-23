# Obstruction Scanner Evidence Report

Version: v2.7

This document defines the v2.7 evidence report layer.

The purpose is to interpret v2.6 bounded scanner output in native terms.

v2.7 does not enlarge the scan first.

v2.7 answers a different question:

What did the bounded scanner actually show?

## Source artifacts

v2.7 reads:

- results/bounded_obstruction_search_rows.jsonl
- results/bounded_obstruction_search_summary.json
- results/bounded_obstruction_search_certificate.json

## Output artifacts

v2.7 writes:

- results/obstruction_scanner_evidence_report.json
- results/obstruction_scanner_evidence_report.md
- results/obstruction_scanner_evidence_certificate.json

## Core interpretation

The v2.6 scanner found:

- many debt windows;
- many regeneration events;
- many dangerous-regeneration stress events;
- zero obstruction candidates.

This means:

No obstruction candidate was detected inside the bounded finite domain.

It does not mean:

No obstruction can exist.

## Status

v2.7 is an evidence interpretation layer.

It is not a proof layer.
