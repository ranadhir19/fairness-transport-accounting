# fairness-transport-accounting

Deposit accompanying the manuscript:

**Ranadhir Ghosh, "Transport Bounds for Fairness Statistics: An Accounting Audit Across Two Monitoring Programmes and the Documented Failure of Threshold-Crossing Forecasting"** (sole author).

The manuscript (`manuscript/Paper_11_Rebuilt3.tex`) is prepared for *Data Mining and Knowledge Discovery* (DMKD). It has **not** been submitted anywhere in this form. An earlier, differently framed version was rejected by *AI & Society* in 2026; this deposit is the record of the rebuilt paper and of the elevation cycles that produced it.

## What the paper establishes (and what it does not)

- **Proved:** transport bounds for the equalised-odds (EO) and demographic-parity (DP) gap statistics themselves — the DP transport is at most the sum of the two group-conditional score-law total variations; the EO transport is at most the maximum of the label-stratified transport sums, in the max-form the pipelines compute. The forms are tight in the stratum variations; a prevalence decomposition reduces the DP bound to FAR-type quantities plus named terms. Proofs are in the manuscript and in `proofs/CLOSURE_PROOF.md`, independently checked (`checkers/CLOSURE_CHECKER_REPORT.md`, obligations PO1–PO7 all discharged).
- **Audit:** the field's FAR accounting protocol, transported to the gap functionals and run on two monitoring programmes (US ACS classifiers across six states; UK police stop-and-search risk scores across nine forces). Three recorded FAR verdicts reproduce under the gap bound on their own surviving folds; the family-1 gap criterion is met on the folds that survive there. On family 2 the gap accounting is correct but loose; the FAR accounting remains the binding evidence there.
- **Negative record, at full strength:** the programme's fairness-breach forecasting claim failed its pre-registered falsifier twice on family 1 (the second time under a scale-adapted design), and family 2 twice produced no testable cell, for two reasons proved as theorems about the monitoring design (crossing rarity; cut degeneracy). A fitted-model history-value bound (δ̂ = 0.289) *permits* the failure record; it does not explain it. The commissioned limit theorem was killed at its registered strength (`results/E3_RESULTS.md`).

## Layout

- `manuscript/` — the paper (LaTeX source).
- `preregistrations/` — the frozen pre-registrations of every cycle (upgrade, E2, E3, E4, closure), with freeze hashes recorded in the documents.
- `proofs/` — the closure proof record (gap bounds) and the E3 proof record (history-value bound, at its weakened proved strength).
- `results/` — cycle result reports, plus the surviving fold-detail tables of both accountings (`closure/`), the E4 adapted-cycle artifacts (`e4/`, including a per-cell score summary for the 2025 LR degeneracy analysis), and the E2 family-2 artifacts (`e2/`).
- `checkers/` — the two independent checker reports and the programme's own per-cycle validators (deposited as records; they reference the original workspace layout). The self-contained deposit validator is `validate.py` at the root.

## Validate

```
python3 validate.py
```

Recomputes, from the deposited fold tables and population tables alone (standard library only): the gap-accounting medians, pass fractions and minimum margins for every cell of the manuscript's Table 2; the FAR-accounting medians of the E2 and E4 cycles; the 2025 cut-degeneracy counts (81 of 96 cells with no above-cut record; 21 above-cut records of 65,826); the crossing-rarity arithmetic; and the presence of the headline numbers in the manuscript source.

## Known gap in this deposit (disclosed, not repaired)

The family-1 expanded design's original run files (a 51-jurisdiction fold design) were lost in an archive migration before this deposit was assembled. Its two recorded FAR verdicts (LR: met; GB: **not met**) therefore rest on the programme's cycle reports and an independent tester's recomputation, and are represented here by those reports only — there are no fold artifacts for them, and the manuscript attributes them to the FAR accounting only. Nothing in this deposit silently re-adjudicates them under the gap bound.

## Data

No raw records are deposited. Family 2's source is the UK police open data (data.police.uk, stop-and-search extracts, 2024–2025); family 1's source is the US Census Bureau's American Community Survey (2014–2019, folktables construction). The deposit carries per-cell population summaries and fold tables derived from those sources.
