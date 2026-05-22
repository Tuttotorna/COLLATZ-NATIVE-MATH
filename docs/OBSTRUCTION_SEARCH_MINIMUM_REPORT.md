# Obstruction Search Minimum Report

Version: v2.5

This document defines the minimum report required for any obstruction search.

## Required fields

Every obstruction search report must include:

version
search_domain
candidate_generation_rule
tested_candidate_count
debt_window_count
regeneration_count
dangerous_regeneration_count
obstruction_candidate_count
closure_result_counts
proof_status
negative_result_boundary

## Required proof status

The proof status must be:

not_a_proof

unless a separate general proof layer is introduced.

## Required negative-result boundary

Every report must include:

No obstruction detected in the selected finite domain does not imply global closure.

## Required candidate boundary

Every report must include:

A hard case is not automatically an obstruction candidate.

## Required closure boundary

Every report must include:

Local recovery is not automatically native closure.

## Purpose

This prevents computational evidence from being overstated.
