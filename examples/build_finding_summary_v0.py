#!/usr/bin/env python3
"""
Finding Summary V0.

This script consolidates the v4.8-v6.4 measurement line into one public
bounded finding summary.

It does not prove Collatz.
It does not claim Collatz is solved.
It summarizes bounded measurement evidence only.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"

SOURCE_FILES = {
    "v4.8_compression_debt": RESULTS / "compression_debt_machine_v0.json",
    "v4.9_distributed_release_pressure": RESULTS / "distributed_release_pressure_v0.json",
    "v5.0_scale_stability": RESULTS / "scale_stability_audit_v0.json",
    "v5.1_signal_decay": RESULTS / "signal_decay_audit_v0.json",
    "v5.2_residual_decay": RESULTS / "residual_decay_audit_v0.json",
    "v5.3_seed_scale_stratification": RESULTS / "seed_scale_stratification_audit_v0.json",
    "v5.4_band_stabilization": RESULTS / "band_stabilization_audit_v0.json",
    "v5.5_extended_band": RESULTS / "extended_band_audit_v0.json",
    "v5.6_response_time_invariance": RESULTS / "response_time_invariance_audit_v0.json",
    "v5.7_post_response_debt_survival": RESULTS / "post_response_debt_survival_audit_v0.json",
    "v5.8_post_response_horizon_extension": RESULTS / "post_response_horizon_extension_audit_v0.json",
    "v5.9_near_breach": RESULTS / "near_breach_audit_v0.json",
    "v6.0_near_breach_anatomy": RESULTS / "near_breach_anatomy_v0.json",
    "v6.1_near_breach_grammar_recurrence": RESULTS / "near_breach_grammar_recurrence_audit_v0.json",
    "v6.2_fuzzy_near_breach_grammar": RESULTS / "fuzzy_near_breach_grammar_audit_v0.json",
    "v6.3_fuzzy_rebound_anatomy": RESULTS / "fuzzy_rebound_anatomy_v0.json",
    "v6.4_mature_rebound_guard": RESULTS / "mature_rebound_guard_v0.json",
}


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def get_nested(obj: dict | None, path: list[str], default=None):
    if obj is None:
        return default

    cur = obj

    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]

    return cur


def fmt(value):
    if value is None:
        return "None"
    if isinstance(value, float):
        return f"{value:.12f}"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build() -> dict:
    sources = {name: load_json(path) for name, path in SOURCE_FILES.items()}
    missing_sources = [
        name for name, data in sources.items()
        if data is None
    ]

    v48 = sources["v4.8_compression_debt"]
    v49 = sources["v4.9_distributed_release_pressure"]
    v50 = sources["v5.0_scale_stability"]
    v51 = sources["v5.1_signal_decay"]
    v52 = sources["v5.2_residual_decay"]
    v53 = sources["v5.3_seed_scale_stratification"]
    v54 = sources["v5.4_band_stabilization"]
    v55 = sources["v5.5_extended_band"]
    v56 = sources["v5.6_response_time_invariance"]
    v57 = sources["v5.7_post_response_debt_survival"]
    v58 = sources["v5.8_post_response_horizon_extension"]
    v59 = sources["v5.9_near_breach"]
    v60 = sources["v6.0_near_breach_anatomy"]
    v61 = sources["v6.1_near_breach_grammar_recurrence"]
    v62 = sources["v6.2_fuzzy_near_breach_grammar"]
    v63 = sources["v6.3_fuzzy_rebound_anatomy"]
    v64 = sources["v6.4_mature_rebound_guard"]

    findings = [
        {
            "id": "F1",
            "name": "Debt creates measurable release pressure",
            "status": "bounded_positive_signal",
            "evidence": {
                "v4.8_debt_peak_vs_release_count": get_nested(v48, ["aggregate", "debt_peak_vs_release_count_pearson"]),
                "v4.8_debt_peak_vs_strong_release_count": get_nested(v48, ["aggregate", "debt_peak_vs_strong_release_count_pearson"]),
                "v4.9_debt_peak_vs_post_peak_release_mass": get_nested(v49, ["aggregate", "debt_peak_vs_post_peak_release_mass_h_pearson"]),
                "v4.9_debt_peak_vs_post_peak_strong_release_count": get_nested(v49, ["aggregate", "debt_peak_vs_post_peak_strong_release_count_h_pearson"]),
            },
            "interpretation": "Higher bounded debt peaks tend to be followed by stronger or more massive release behavior.",
            "boundary": "Correlation is not proof and does not imply global closure.",
        },
        {
            "id": "F2",
            "name": "The pressure signal is scale-positive but decays with seed scale",
            "status": "positive_signal_with_decay",
            "evidence": {
                "v5.1_first_signal": get_nested(v51, ["decay", "first_signal"]),
                "v5.1_last_signal": get_nested(v51, ["decay", "last_signal"]),
                "v5.1_relative_drop": get_nested(v51, ["decay", "relative_drop"]),
                "v5.1_zero_crossing_observed": get_nested(v51, ["decay", "zero_crossing_observed"]),
                "v5.2_decay_axes": get_nested(v52, ["residual_attribution", "decay_axes"]),
                "v5.2_growth_axes": get_nested(v52, ["residual_attribution", "growth_axes"]),
            },
            "interpretation": "The debt-release correlation remains positive in the tested ranges, but the seed-scale axis weakens it.",
            "boundary": "A positive bounded floor is not a theorem and cannot be extrapolated as an invariant.",
        },
        {
            "id": "F3",
            "name": "After the initial drop, local seed blocks remain positive but weak",
            "status": "weak_positive_band",
            "evidence": {
                "v5.4_band_status": get_nested(v54, ["block_summary", "band_status"]),
                "v5.4_post_initial_floor": get_nested(v54, ["block_summary", "post_initial_floor"]),
                "v5.4_post_initial_mean": get_nested(v54, ["block_summary", "post_initial_mean"]),
                "v5.5_band_status": get_nested(v55, ["block_summary", "band_status"]),
                "v5.5_last_10_mean": get_nested(v55, ["block_summary", "last_10_mean"]),
                "v5.5_last_10_min": get_nested(v55, ["block_summary", "last_10_min"]),
            },
            "interpretation": "The signal does not vanish in the tested local bands, but it becomes weak and should not be overstated.",
            "boundary": "A weak positive band is descriptive only.",
        },
        {
            "id": "F4",
            "name": "Response time is highly stable",
            "status": "strong_response_time_invariance_candidate",
            "evidence": {
                "v5.6_timing_status": get_nested(v56, ["timing_summary", "timing_status"]),
                "v5.6_median_delay_all_1": get_nested(v56, ["timing_summary", "median_delay_all_1"]),
                "v5.6_p_delay_1_floor": get_nested(v56, ["timing_summary", "p_delay_1_floor"]),
                "v5.6_p_delay_le_2_floor": get_nested(v56, ["timing_summary", "p_delay_le_2_floor"]),
                "v5.6_no_response_rate_max": get_nested(v56, ["timing_summary", "no_response_rate_max"]),
            },
            "interpretation": "Across measured blocks, the first post-peak response usually appears immediately or very quickly.",
            "boundary": "Stable response timing is not a termination proof.",
        },
        {
            "id": "F5",
            "name": "Post-response debt usually collapses below the prior peak",
            "status": "strong_post_response_reduction_candidate",
            "evidence": {
                "v5.7_survival_status": get_nested(v57, ["survival_summary", "survival_status"]),
                "v5.7_p_reduced_floor": get_nested(v57, ["survival_summary", "p_reduced_floor"]),
                "v5.7_p_new_peak_ceiling": get_nested(v57, ["survival_summary", "p_new_peak_ceiling"]),
                "v5.7_last_10_p_reduced_mean": get_nested(v57, ["survival_summary", "last_10_p_reduced_mean"]),
                "v5.7_last_10_p_new_peak_mean": get_nested(v57, ["survival_summary", "last_10_p_new_peak_mean"]),
            },
            "interpretation": "Once response occurs, bounded debt typically reduces rather than forming a new peak.",
            "boundary": "Post-response reduction is bounded evidence only.",
        },
        {
            "id": "F6",
            "name": "Extended horizons did not produce new post-response peaks",
            "status": "extended_horizon_no_new_peak_observed",
            "evidence": {
                "v5.8_zero_new_peak_all_horizons": get_nested(v58, ["horizon_summary", "zero_new_peak_all_horizons"]),
                "v5.8_p_new_peak_after_release_max_values": get_nested(v58, ["horizon_summary", "p_new_peak_after_release_max_values"]),
                "v5.8_reduced_floor_all_horizons": get_nested(v58, ["horizon_summary", "reduced_floor_all_horizons"]),
                "v5.8_max_regen_ratio_all_horizons": get_nested(v58, ["horizon_summary", "max_regen_ratio_all_horizons"]),
            },
            "interpretation": "Increasing bounded horizon length did not create post-response new-peak behavior in the tested range.",
            "boundary": "No bounded new peak is not global impossibility.",
        },
        {
            "id": "F7",
            "name": "Near-breach candidates exist but remain below breach",
            "status": "near_breach_below_one_percent_gap",
            "evidence": {
                "v5.9_records_measured": get_nested(v59, ["summary", "records_measured"]),
                "v5.9_breach_count": get_nested(v59, ["summary", "breach_count"]),
                "v5.9_max_regeneration_ratio": get_nested(v59, ["summary", "max_regeneration_ratio"]),
                "v5.9_min_gap_to_breach": get_nested(v59, ["summary", "min_gap_to_breach"]),
                "v5.9_top10_min_gap": get_nested(v59, ["summary", "top10_min_gap"]),
            },
            "interpretation": "Some trajectories nearly rebuild prior debt, but no true breach was observed in the bounded set.",
            "boundary": "Near-breach is not divergence and not a proof boundary.",
        },
        {
            "id": "F8",
            "name": "Near-breach grammar is expansion-rich but isolated",
            "status": "isolated_near_breach_grammar",
            "evidence": {
                "v6.0_near_breach_response_delay_histogram": get_nested(v60, ["comparison", "near_breach_response_delay_histogram"]),
                "v6.0_near_breach_time_to_post_max_histogram": get_nested(v60, ["comparison", "near_breach_time_to_post_max_histogram"]),
                "v6.0_near_breach_a1_rate": get_nested(v60, ["comparison", "near_breach_mean_response_to_post_max_a1_rate"]),
                "v6.0_near_breach_a_ge_3_rate": get_nested(v60, ["comparison", "near_breach_mean_response_to_post_max_a_ge_3_rate"]),
                "v6.1_recurrence_seed_count": get_nested(v61, ["summary", "recurrence_seed_count"]),
                "v6.1_pattern_after_pattern_seed_count": get_nested(v61, ["summary", "pattern_after_pattern_seed_count"]),
            },
            "interpretation": "Near-breach windows are driven by expansion-rich grammar, but measured recurrences did not chain.",
            "boundary": "Grammar isolation is a bounded observation, not a global theorem.",
        },
        {
            "id": "F9",
            "name": "Fuzzy grammar increases hits but not dangerous chains",
            "status": "fuzzy_isolated_occurrences",
            "evidence": {
                "v6.2_fuzzy_hit_seed_count": get_nested(v62, ["summary", "fuzzy_hit_seed_count"]),
                "v6.2_fuzzy_hit_rate": get_nested(v62, ["summary", "fuzzy_hit_rate"]),
                "v6.2_fuzzy_recurrence_seed_count": get_nested(v62, ["summary", "fuzzy_recurrence_seed_count"]),
                "v6.2_dangerous_fuzzy_chain_seed_count": get_nested(v62, ["summary", "dangerous_fuzzy_chain_seed_count"]),
                "v6.2_post_fuzzy_pattern_new_local_peak_rate": get_nested(v62, ["summary", "post_fuzzy_pattern_new_local_peak_rate_per_instance"]),
            },
            "interpretation": "Relaxing exact grammar increases detected pattern hits, but did not generate recurring dangerous chains in the bounded test.",
            "boundary": "Fuzzy absence of chains is not a global exclusion.",
        },
        {
            "id": "F10",
            "name": "Apparent fuzzy breaches were weak-prefix artifacts",
            "status": "false_breach_corrected",
            "evidence": {
                "v6.3_breach_after_fuzzy_pattern_instance_count": get_nested(v63, ["summary", "breach_after_fuzzy_pattern_instance_count"]),
                "v6.4_raw_breach_count": get_nested(v64, ["summary", "raw_breach_after_fuzzy_pattern_count"]),
                "v6.4_weak_prefix_false_breach_count": get_nested(v64, ["summary", "weak_prefix_false_breach_count"]),
                "v6.4_mature_rebound_count": get_nested(v64, ["summary", "mature_rebound_count"]),
                "v6.4_mature_breach_count": get_nested(v64, ["summary", "mature_breach_count"]),
                "v6.4_mature_second_near_breach_count": get_nested(v64, ["summary", "mature_second_near_breach_count"]),
            },
            "interpretation": "The raw v6.3 breach signal was caused by low prior peaks, not by mature debt regeneration.",
            "boundary": "Correcting false positives strengthens measurement language but does not prove Collatz.",
        },
    ]

    concise_thesis = {
        "one_sentence": (
            "In bounded odd-step Collatz measurements, debt accumulation tends to trigger fast release, "
            "post-response debt generally falls below prior peaks, near-breach grammars exist but appear isolated, "
            "and apparent fuzzy breaches were reclassified as weak-prefix artifacts rather than mature regeneration chains."
        ),
        "negative_result": (
            "No mature second near-breach chain was observed in the measured artifacts."
        ),
        "non_claims": [
            "This is not a proof of Collatz.",
            "This does not solve Collatz.",
            "This does not establish a global invariant.",
            "This does not exclude all possible divergent behavior.",
            "This is bounded measurement evidence only.",
        ],
    }

    result = {
        "version": "v6.5",
        "machine": "Finding Summary V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": {
            name: {
                "path": str(path.relative_to(ROOT)),
                "present": sources[name] is not None,
                "version": get_nested(sources[name], ["version"]),
                "machine": get_nested(sources[name], ["machine"]),
                "bounded_assessment": get_nested(sources[name], ["bounded_assessment"]),
            }
            for name, path in SOURCE_FILES.items()
        },
        "missing_sources": missing_sources,
        "findings": findings,
        "concise_thesis": concise_thesis,
        "public_positioning": {
            "best_short_label": "bounded structural measurement of Collatz odd-step debt/release grammar",
            "what_is_new_inside_this_repo": [
                "A native debt/release vocabulary was made computable.",
                "Post-peak release pressure was measured across scale and horizon variations.",
                "Response timing and post-response debt survival were separated from raw correlation.",
                "Near-breach grammar was isolated and then guarded against fuzzy false positives.",
                "Weak-prefix rebound was separated from mature-debt rebound.",
            ],
            "strongest_current_claim": (
                "Within the measured bounded artifacts, no persistent mature low-compression regeneration chain was observed."
            ),
            "weakest_current_point": (
                "The work remains empirical and bounded; larger scale, independent replication, and formalization are needed."
            ),
        },
        "boundary": {
            "proof_status": "not_a_proof",
            "collatz_status": "not_claimed_solved",
            "theorem_status": "no_theorem_claimed",
            "global_closure_status": "not_claimed",
            "global_invariant_status": "not_claimed",
            "bounded_evidence_status": "measurement_only",
        },
    }

    return result


def write_markdown(result: dict) -> str:
    lines = []

    lines.append("# COLLATZ-NATIVE-MATH v6.x Finding Summary V0")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded finding summary.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("It is not a theorem layer.")
    lines.append("")
    lines.append("It summarizes the measurement line from v4.8 through v6.4.")
    lines.append("")
    lines.append("## One-sentence thesis")
    lines.append("")
    lines.append(result["concise_thesis"]["one_sentence"])
    lines.append("")
    lines.append("## Negative result")
    lines.append("")
    lines.append(result["concise_thesis"]["negative_result"])
    lines.append("")
    lines.append("## What this repository currently measures")
    lines.append("")
    lines.append("The repository measures bounded odd-step Collatz behavior through a native vocabulary:")
    lines.append("")
    lines.append("```text")
    lines.append("debt")
    lines.append("release")
    lines.append("response")
    lines.append("regeneration")
    lines.append("near-breach")
    lines.append("weak-prefix rebound")
    lines.append("mature-debt rebound")
    lines.append("```")
    lines.append("")
    lines.append("The central bounded question is:")
    lines.append("")
    lines.append("```text")
    lines.append("Can debt regenerate into a persistent mature low-compression chain?")
    lines.append("```")
    lines.append("")
    lines.append("In the current measured artifacts, the answer observed so far is:")
    lines.append("")
    lines.append("```text")
    lines.append("No persistent mature low-compression regeneration chain observed.")
    lines.append("```")
    lines.append("")
    lines.append("## Findings")
    lines.append("")

    for finding in result["findings"]:
        lines.append(f"### {finding['id']} — {finding['name']}")
        lines.append("")
        lines.append(f"- status: `{finding['status']}`")
        lines.append(f"- interpretation: {finding['interpretation']}")
        lines.append(f"- boundary: {finding['boundary']}")
        lines.append("")
        lines.append("Evidence:")
        lines.append("")
        for key, value in finding["evidence"].items():
            lines.append(f"- {key}: `{fmt(value)}`")
        lines.append("")

    lines.append("## What is new inside this repo")
    lines.append("")
    for item in result["public_positioning"]["what_is_new_inside_this_repo"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Strongest current claim")
    lines.append("")
    lines.append(result["public_positioning"]["strongest_current_claim"])
    lines.append("")

    lines.append("## Weakest current point")
    lines.append("")
    lines.append(result["public_positioning"]["weakest_current_point"])
    lines.append("")

    lines.append("## Non-claims")
    lines.append("")
    for item in result["concise_thesis"]["non_claims"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Source artifacts")
    lines.append("")
    for name, src in result["sources"].items():
        lines.append(
            f"- {name}: `{src['path']}` | present=`{src['present']}` | "
            f"version=`{fmt(src['version'])}` | machine=`{fmt(src['machine'])}` | "
            f"assessment=`{fmt(src['bounded_assessment'])}`"
        )
    lines.append("")

    lines.append("## Missing sources")
    lines.append("")
    if result["missing_sources"]:
        for name in result["missing_sources"]:
            lines.append(f"- `{name}`")
    else:
        lines.append("None.")
    lines.append("")

    lines.append("## Boundary")
    lines.append("")
    for key, value in result["boundary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    result = build()

    json_path = RESULTS / "finding_summary_v0.json"
    md_result_path = RESULTS / "finding_summary_v0.md"
    cert_path = RESULTS / "finding_summary_v0_certificate.json"
    public_doc_path = DOCS / "FINDING_SUMMARY_V0.md"

    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    markdown = write_markdown(result)
    md_result_path.write_text(markdown, encoding="utf-8")
    public_doc_path.write_text(markdown, encoding="utf-8")

    certificate = {
        "version": "v6.5",
        "artifact": "Finding Summary V0",
        "generated_at_utc": result["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_result_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
            str(public_doc_path.relative_to(ROOT)),
        ],
        "missing_sources": result["missing_sources"],
        "finding_count": len(result["findings"]),
        "strongest_current_claim": result["public_positioning"]["strongest_current_claim"],
        "boundary": result["boundary"],
    }

    cert_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"WROTE: {json_path}")
    print(f"WROTE: {md_result_path}")
    print(f"WROTE: {cert_path}")
    print(f"WROTE: {public_doc_path}")
    print("")
    print("BOUNDED SUMMARY:")
    print(f"  version: {result['version']}")
    print(f"  finding_count: {len(result['findings'])}")
    print(f"  missing_sources: {result['missing_sources']}")
    print("")
    print("THESIS:")
    print(f"  {result['concise_thesis']['one_sentence']}")
    print("")
    print("NEGATIVE RESULT:")
    print(f"  {result['concise_thesis']['negative_result']}")
    print("")
    print("STRONGEST CURRENT CLAIM:")
    print(f"  {result['public_positioning']['strongest_current_claim']}")
    print("")
    print("FINDINGS:")
    for finding in result["findings"]:
        print(f"  {finding['id']}: {finding['status']} | {finding['name']}")
    print("")
    print("BOUNDARY:")
    for key, value in result["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
