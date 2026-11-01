# E4 Results — Paper 11 Elevation, Cycle E4

## A scale-adapted test of the forecasting half

**Design:** `E4_PREREGISTRATION.md`, frozen 2026-11-01T16:16:40Z,
SHA-256 `766ac7510a53d3814b2ec8d4bd7af663c3e88d734992f1851c6aea29b3387f05`,
plus Amendment A-E4-1 (2026-11-01T16:51Z: confirmatory year 2023 →
2025 — the frozen endpoint serves only a rolling window and Jan–Aug
2023 are unobtainable from it; recorded before any confirmatory run)
and the §4 recording (2026-11-01T17:03Z: primary class and τ\* values,
recorded before the monitor/forecast stages). **Validation:**
`validate_e4.py` — **ALL PASS** (19 checks: population metrics
recomputed from the saved score parquets; τ\* quantiles and the
primary-class rule recomputed; monitor labels recomputed in full;
accounting recomputed from saved fold scores; all summary
medians/coverages and both arms' bootstrap CIs recomputed from the
saved per-pair lead rows; verdict labels re-derived). The full
forecast stage was executed twice; the two runs produced identical
headline files. Every number below is from these runs.

## The plain consequence

**VACUOUS AGAIN on the confirmatory arm — by a new mechanism — and,
on the secondary arm where the adapted design did produce a real
test, the forecasting claim failed it.** Details and scope:

- On family 2 (2025), scale adaptation could not manufacture a
  forecastable cell, because the *monitored statistic itself
  degenerates*: the primary class's deployed scores never reach the
  registered 0.5 decision cut, so its population gaps are identically
  zero in 84% of cells and the frozen quantile rule returns τ\* = 0.
  TRA-Q was not falsified on this arm — it was never testable on it.
- On family 1, the same adapted rule (τ\* = 0.0505, essentially the
  original design point) produced a genuinely non-vacuous cell, and
  TRA-Q **tied extrapolation** (Δ = 0.0) — the FALSIFIER-U pattern
  reproduced at adapted scale.
- So the cycle's question — *was TRA-Q's death a property of
  forecasting, or of the absolute-τ design?* — is answered where it
  can be answered: **not an artefact of absolute τ.** On the only arm
  where the adapted design could run, the advantage did not appear.
  Family 2 contributes no forecasting evidence either way; its two
  cycles instead map the design's boundary (E2: absolute thresholds
  make breaches vanish; E4: adapted thresholds cannot create a gap
  process where the deployed statistic is degenerate).

**E4 verdict: the conjunctive bar is NOT cleared (prongs 1–3 all
fail on the primary scope; prongs 2–3 are not evaluable there, which
the frozen bar counts as failure).**

---

## Confirmatory arm — family 2, calendar 2025

Corpus: 156/156 monthly files acquired from data.police.uk (one
legitimately empty month, humberside 2025-06); frozen §5 inclusion
rule → **8 forces** (avon-and-somerset, cheshire, cumbria,
devon-and-cornwall, hertfordshire, kent, northumbria, sussex);
**65,826 usable records**. Excluded mechanically: cleveland (SDE
share 0.712), humberside (min monthly usable 0), leicestershire
(min 65; SDE 0.743), south-wales (min 0), staffordshire (min 1).

Primary class (§5 rule): base-month holdout AUC LR 0.638995 vs GB
0.639791 — |Δ| = 0.0008 ≤ 0.005, tie → **LR primary**, GB secondary.

### The adapted thresholds (frozen Q₀.₇₀ rule, 96 cells per class)

| class | metric | τ\* (Q₀.₇₀) | gap = 0 share | max cell |
|---|---|---|---|---|
| LR (primary) | EO | **0.0** | 84.4% | 0.200 |
| LR | DP | **0.0** | 84.4% | — |
| GB (secondary) | EO | **0.003329** | 62.5% | 0.200 |
| GB | DP | **0.001934** | 62.5% | — |

The LR degeneracy is a property of the deployed statistic at the
registered cut: in the sampled populations the LR's maximum score is
0.46–0.496 (alarm share exactly 0.0), against 2024's 0.56 max / 0.7%
alarm share. The 2025 arrest base rates are lower and the LR's
probability mass sits entirely below 0.5, so the 0.5-cut EO/DP gaps
are zero almost everywhere (the nonzero cells are small-subgroup
flips reaching 0.20). No repair was applied: §3 of the pre-reg
bars post-audit design changes on the confirmatory arm, and the §4
recording stated this consequence before the pipeline ran.

### Prong 1 — non-vacuity at adapted scale (primary): **FAIL**

Crossings strictly after the base month: **0** of 8 (≥ 3 required).
Share of forces below τ\* at base: **0.0** (≥ 0.40 required). Forces
with label-1 instances: **0** (≥ 3 required). Defined headline
instances on the primary scope: **0** (a label requires pop gap < τ;
at τ = 0 none exists). This is failure mode F3 in a new sub-form —
*statistic degeneracy*, not E2's scale-boundedness: there is no gap
process to forecast, at any threshold the frozen rule can name.

### Prong 2 — forecasting advantage (primary): **NOT EVALUABLE → FAIL**

With zero labelled instances in the gating cell, no lead time,
coverage, or bootstrap quantity is defined for any method. The
record states this as a non-evaluable prong, explicitly **not** a
falsification of TRA-Q on this arm. The §10 sensitivity quantiles
(Q₀.₆₀, Q₀.₈₀) are also 0.0 for LR — the degeneracy is not a
knife-edge of the 0.70 constant.

### Prong 3 — accounting, ported T4 (primary): **NOT EVALUABLE → FAIL**

No instances → no folds → the criterion cannot be computed on the
primary class. Neither F1 (the bound fails to price transport) nor
F2 (no transport to price) is asserted for the primary scope: the
accounting is simply untestable where the statistic degenerates.

### Secondary class GB — reported in full, non-gating

GB's gap process is a spike train (62.5% zeros, spikes to 0.20);
τ\*_GB = 0.003329 sits just above the zero mass. Its prong-1-style
quantities also fail: **1** force crosses strictly after base
(≥ 3 required), 37.5% of forces below τ\* at base. On that single
breaching force (25 seed-pairs; 1,375 defined instances, 50
positives, cell-wide), at FAR 0.10, H = 2:

| method | coverage | median lead (months) |
|---|---|---|
| **TRA-Q** | **0.00** | — (no covered pair) |
| CTRL | 0.00 | — |
| CUSUM | 0.00 | — |
| last-value | 0.36 | 1.0 |
| extrapolation | 0.40 | 1.0 |
| FairCanary point (reference) | — | lead ≤ 0 by construction |

Descriptively, the claimant caught none of the breaches the trivial
forecasters caught ~40% of — but with one breaching force this
carries no adjudicative weight and is not a verdict. GB's
**accounting criterion is MET** (7 of 8 folds evaluable; median fold
TV50 **0.3475**, pass fraction **1.0**) — the bound's accounting
travels on the GB scope of family 2's 2025 corpus as it did on both
classes in 2024. GB headline-cell Brier: CTRL 0.00310 vs climatology
0.00183 (CTRL's probabilities are worse than the base-rate constant
on this sparse cell; descriptive only).

---

## Secondary arm — family 1 re-test at adapted scale (§9)

τ\*_F1(EO) = **0.050533** (Q₀.₇₀ of the frozen 108-cell table; the
original τ = 0.05 sits at its 69.4th percentile — the adapted rule
lands essentially on the original design point, as the anchor
intended). Original 18 trajectories, LR, corrected U1–U3 semantics.

- **Prong 1: PASS.** 7/18 trajectories cross strictly after base;
  77.8% below τ\* at base; 7 trajectories with label-1 instances.
- **Prong 2: FAIL.** TRA-Q pooled median lead **3.0 yr**, coverage
  **0.606** (175 breaching pairs). Against the gating baselines at
  FAR 0.10, H = 2: last-value Δ = **+1.0**, 95% CI **[−1.0, 4.0]**
  (includes 0 — fails); extrapolation Δ = **0.0**, CI [−0.5, 2.0]
  (tie — fails); CUSUM Δ = **+1.0**, CI **[1.0, 3.0]** (met, but the
  prong requires all three). The advantage criterion is not met.
- **Prong 3: PASS.** Median fold TV50 **0.4053**, pass fraction
  **1.0** (6/6 folds within slack).

Reading: at the adapted scale, on the family where the claim was
born and first died, the cell is non-vacuous, the accounting
travels — and the forecasting advantage is still absent, by the same
signature as FALSIFIER-U (a tie with linear extrapolation). Scale
adaptation changed the threshold from 0.05 to 0.0505 and changed
nothing else. Whatever kills the advantage on family 1, it is not
the threshold's units.

---

## What this cycle establishes, and what it does not

1. The forecasting claim has now failed **every non-vacuous test**
   administered to it: the original falsifier (family 1, absolute
   τ), FALSIFIER-U at expanded scope (family 1, absolute τ), and the
   adapted-scale re-test (family 1, τ\*). No test has ever produced
   the registered advantage.
2. Family 2 has twice failed to produce a testable forecasting
   cell — at absolute thresholds because breaches are too rare
   (E2's F3), at adapted thresholds because the primary deployed
   statistic is degenerate at the registered cut (E4). Family 2
   therefore provides **no evidence about forecasting**, in either
   direction; its positive contribution remains the accounting
   result (bound travels: E2 both classes 2024; E4 GB 2025).
3. E4 does **not** show the forecasting claim is false in general —
   it shows it is false on family 1 under both threshold regimes,
   and untestable on family 2 under both. A third empirical cycle
   under yet another post-hoc scale, class, or cut is not licensed
   by anything in this record.

## E3 eligibility (closing statement, per the audit's condition)

The audit gated E3 — forecastability-limit theory — on the
forecasting question being settled by substance, with a one-cycle
kill criterion. **Assessment: E3 is eligible in exactly one form,
and not in another.**

- **Eligible:** a limit theorem that *explains the accumulated
  record* — the two family-1 falsifications (why, at batch
  resolution, the gap process's innovation noise swamps the drift
  signal any observable forecaster could exploit, so extrapolation
  is not beatable at matched FAR), together with the family-2
  boundary phenomena as corollaries about the monitored statistic
  (breach rarity at absolute levels; degeneracy of a cut-based gap
  when the deployed score distribution lives below the cut). Such a
  theorem converts four negative results into one positive
  statement about when breach forecasting is possible at all, and
  its natural quantities — innovation variance vs drift, priced
  against the null-score transport the bound already measures —
  are already in the programme's hands.
- **Not eligible:** any E3 that rescues or re-scopes the
  forecasting claim; any third empirical cycle dressed as theory;
  and any write-up that cites the E4 confirmatory arm as a
  forecasting *falsification* (it is a degeneracy — the falsification
  evidence is family 1's, now twice over).
- E3 is not started by this cycle. It requires its own
  pre-registration (statement of the limit claim, proof strategy,
  the audit's one-cycle kill criterion) and Ranadhir's decision.

## Artifacts

`results4/`: analysis_set.json, deployed_diag.json, tau_star.json,
population_metrics.csv, monitor.parquet, forecast_leads4.parquet,
forecast_summary4.csv, accounting_folds4.csv,
accounting_scores4.parquet, accounting4.json, calibration4.csv,
headline4.json, sensitivity4.csv (header-only: the primary class's
sensitivity cells are degenerate, as recorded), f1_arm.json,
f1_arm_leads.parquet, f1_arm_summary.csv, f1_accounting_folds.csv,
f1_accounting_scores.parquet. Code: `src4/` (engine4.py shared by
both arms), `validate_e4.py` (ALL PASS). The 2024 trees and the
submitted manuscript were not touched.
