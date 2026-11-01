# E2 Results — Second Benchmark Family for the Calibration-Transport Bound

**Paper 11 elevation, step E2** (audit §4 task P11-1). Pre-registration:
`E2_PREREGISTRATION.md`, frozen 2026-11-01T15:46:48Z, SHA-256
`f5020cbb3b27de84c9e7d28393c212186106a9d87742b7d339fab2cf64bde098`,
with Amendments A-E2-1 (instance definition) and A-E2-2 (τ-selection
outcome) appended under the paper's amendment discipline, each before the
run it affected. All numbers below are from the executed pipeline and were
reproduced by the independent validator (`validate_e2.py`: **ALL PASS** —
population-metric recompute, monitor completeness, label counts, and the
full accounting recomputed from saved fold scores).

---

## Verdict

**E2 DOES NOT CLEAR its pre-registered bar.** The bar (§8) is conjunctive,
and prong (1) — a non-vacuous headline cell under the frozen τ-selection
rule — **fails**: on the primary (LR) scope, no registered τ produces ≥ 3
forces crossing after the base month (2 at τ = 0.05; 1 at 0.10; 0 at 0.15
and 0.20). The headline cell (EO, τ\* = 0.05, H = 2) is therefore
**vacuity-limited** (failure mode **F3**), and per §10 the E3 theory step
is **not unlocked and was not started**.

**Simultaneously — and this is the cycle's substantive finding — the
ported T4 accounting criterion itself was MET on family 2, on both model
classes, with margins wider than family 1's:**

| Scope | Median fold TV50 | Folds within slack | Criterion (ported) | Family-1 comparison |
|---|---|---|---|---|
| LR (primary) | **0.4784** | **9/9** | **MET** | 0.3481, 50/50, MET |
| GB (secondary) | **0.2865** | **9/9** | **MET** | 0.1358, 50/51, NOT met |

The transport failure the bound has to price is large on this family
(CTRL fold FARs at the 0.10 target spread **0.551** (LR) / **0.263** (GB)
across forces, fold means 0.131 / 0.139), and on every fold of both classes
the achieved deviation sits inside TV50 + 0.02. This is **not** failure
mode F1: the bound *did* price family 2's transport. What failed is the
breach-process side of the design — at the registered absolute-τ grid, the
primary class's population EO gaps on UK stop-and-search data almost never
reach the threshold (2 of 108 force-month cells ≥ 0.05), so the
forecasting instance base the headline cell is built on rests on 2 of 9
forces. Both halves of that sentence are the result; neither may be
reported without the other.

## What was run

**Family 2:** UK Police stop-and-search records (data.police.uk),
territorial forces as deployment populations, months of 2024 as steps,
a frozen arrest-risk score monitored for equalised-odds gaps across
self-defined ethnicity (White vs non-White). Acquisition: 13 candidate
forces × 12 months via the API, 99,310 records in ~150 small cached files
(§3 budget rule stopped acquisition during the last candidate, sussex).

**Inclusion rule (§5) applied mechanically — 9 of 13 candidates included**
(71,347 usable records): avon-and-somerset, cheshire, cumbria,
devon-and-cornwall, hertfordshire, kent, leicestershire, northumbria,
south-wales. Excluded: cleveland (rule iv — SDE present for 79.4% of
involved-person records vs the 0.80 bar, a 0.6-point miss), humberside
(rule iii — the API returned an empty file for 2024-08), staffordshire
(rule iv — the force publishes SDE for 0.02% of involved-person records;
verified in the raw data, same schema), sussex (rule i — 9 of 12 months
cached when the budget stopped acquisition). Included forces' median
monthly usable populations run 393–1,113; arrest base rates 0.12–0.26;
non-White shares 0.09–0.50.

**Deployed models** (pooled Jan-2024, 70/30 split seed 0, 42 encoded
features, ethnicity never a feature): LR holdout AUC 0.619; GB 0.643.
**Monitor:** batches of 200, 25 seeds, 5,400 monitor rows; **accounting:**
LOSO CTRL exactly as family 1 (Platt-calibrated LR on the ported feature
set, 99-quantile candidate thresholds, closest-FAR pick rule).

## Population audit — why the τ rule failed

- LR population EO gaps are small and mostly far below the registered
  grid: max cell 0.100; **2/108 cells ≥ 0.05** (northumbria 2024-04,
  0.057; devon-and-cornwall 2024-12, 0.100). DP gaps never reach 0.05 for
  either class (maxima 0.034 LR / 0.042 GB), so every DP cell and every
  EO cell at τ ≥ 0.10 has its positives confined to at most one force and
  the LOSO fits fail single-class on that force's fold (recorded in
  `cell_spreads.csv`) — the vacuity is broad, not knife-edge.
- GB gaps are larger (14/108 cells ≥ 0.05; 6 forces crossing after base at
  τ = 0.05, which *would* have qualified) — but the headline scope is LR
  by the frozen design, and the cell is not reassigned post hoc.
- Sensitivity (officer-defined ethnicity, audit-only per §4): crossings
  after base at τ = 0.05 number 2 (LR) / 7 (GB) — the LR vacuity is not an
  artefact of the self-defined grouping.
- Disclosure: the largest non-White SDE category in the analysis set is
  "Other ethnic group — Not stated" (9,705 records, 13.6% of usable;
  White-British is 67.8%). Under the frozen grouping these records sit in
  A = 0, pulling that group's alarm rates toward the pooled mean — a
  plausible contributor to the small population gaps, recorded here
  because it bounds what "small gaps" means on this family.

## Accounting detail (headline cell, FAR target 0.10)

**LR folds** (θ ≈ 0.088–0.131 except northumbria 0.025): five folds
achieve FAR_fold = 0.000 at a θ calibrated to ≈ 0.10 on the pooled train
(avon-and-somerset, hertfordshire, kent, leicestershire, south-wales);
the two breaching forces' folds alarm heavily (devon-and-cornwall
FAR_fold 0.551, deviation 0.450 vs TV50 0.712, margin +0.282;
northumbria 0.326, deviation 0.225 vs TV50 0.246, margin **+0.041** — the
tightest LR fold). All 9 folds pass at both histogram conventions
(median TV20 0.336, 9/9).

**GB folds:** all 9 pass at the 50-bin convention (deviations 0.046–0.161
against TV50 0.181–0.519). At the 20-bin sensitivity, 8/9 pass: cumbria's
TV20 collapses to 0.015 against a deviation of 0.161 (its TV50 is 0.199)
— the same finer/coarser-convention fragility that decided family 1's GB
scope, here in the sensitivity rather than the headline convention.

**Instance anatomy:** LR headline cell — 2,225 instances, **75 positives
(3.4%), all from 2 forces** (devon-and-cornwall 25, northumbria 50),
2,150 nulls. GB — 1,925 instances, 275 positives (14.3%) from 6 forces.
The accounting is a statement about null-score distributions and is
well-supported by the null counts (175–250 test nulls per fold); the
*breach* side of the cell is the thin part, exactly as the τ rule said.

## Bar adjudication (§8, prong by prong)

1. **Non-vacuous headline cell (τ rule, conditions (a)+(b)): FAIL.**
   Condition (b) holds everywhere (share below τ at base = 1.000);
   condition (a) fails at every grid point on the LR scope. → F3.
2. **H-E2-1 accounting criterion on LR (median TV50 ≥ 0.05 and pass
   fraction ≥ 0.99): PASS** — 0.4784 and 9/9 = 1.000.
3. **H-E2-2 caveat (phenomenon absent + TVs trivial): does not trigger** —
   the FAR spread is 0.551, the largest single number in this report.

**Overall: E2 does not clear.** Prongs 2–3 passing does not rescue
prong 1; the bar was written conjunctively precisely so that a strong
accounting on a vacuity-limited cell could not be promoted into a
replication claim after the fact.

## What this does to Paper 11's standing (audit §4 terms)

The audit made Level 1 **WORTH conditional on the calibration-transport
bound** and Level 2 **ADEQUATE only with E2+E3**. After this cycle:

- **The bound's empirical core is strengthened, and is now two-family.**
  The upgrade tester's first-named cap — "still one benchmark family" —
  is lifted *for the T4 accounting claim*: the same protocol, ported
  without alteration, again found null-score TV pricing the observed FAR
  transport, on a different continent, instrument, and attribute
  structure, for both model classes (family 1's GB scope missed; family
  2's meets it at the headline convention). If a future version of the
  paper is built around the bound + accounting protocol, this is now its
  strongest evidence.
- **The paper's forecasting frame gets no second-family support — and
  positive evidence of scale-boundedness.** At the absolute τ grid the
  paper inherited from its ACS design, a second family's primary-class
  gaps sit an order of magnitude below the threshold in 106/108 cells.
  The breach-forecasting construction is not wrong on family 2; it is
  *inapplicable* at its registered scale. Any future design that wants a
  second family for the forecasting half needs a scale-adapted τ
  (e.g., τ set relative to each family's gap distribution) — which is a
  **new pre-registration decision for Ranadhir**, not a repair available
  to this cycle.
- **The formal elevation gate is not passed.** E2 was the gating
  substance for E3; E3 (forecastability-limit theory) is therefore **not
  started**, per the brief's conditional and §10. Level 2's "ADEQUATE
  only with E2+E3" condition is unmet as a package: the E2 evidence is
  split (accounting travels, breach design vacuous), and no theory cycle
  has run.
- **Level-1 verdict: SURVIVES, NARROWED.** It survives for exactly the
  component it was conditioned on — the transport bound with its
  accounting protocol — which leaves this cycle *stronger* than it
  entered (two families, both classes). It does not survive as a verdict
  on the paper as submitted (forecasting-led, single-τ framing): that
  paper's second-family test failed on vacuity grounds. The park
  condition in the audit ("if the bound's accounting does not travel,
  the route becomes park") is **not** triggered — the accounting did
  travel. The honest one-line standing: **a bound-centred paper now has
  two-family evidence; the submitted forecasting paper does not; and the
  elevation programme's own bar records this cycle as NOT CLEARED, with
  E3 unrun.** Venue choice remains deferred until Ranadhir decides what
  the next cycle is.

## Limitations of this E2 (recorded, not buried)

- Batch 200 against monthly populations of 330–1,490 is a 13–60% sampling
  fraction (family 1 sampled ~2–4%): batch features are less noisy
  relative to their populations, and null-score TVs include batch-resampling
  variation across seeds. The margins are wide enough that the accounting
  conclusion is not knife-edge (tightest LR margin +0.041), but the two
  families' TV magnitudes are not directly comparable as effect sizes.
- Plug-in TV50 at 175–250 test nulls per fold is biased upward; family 1's
  folds had ~10× the nulls. The bias direction favours "pass"; the GB
  cumbria TV20 reversal shows the sensitivity is real at the margins.
- Nine folds (vs 51): the ≥ 0.99 prong is all-or-nothing at this count.
- One calendar year (2024): a single seasonal cycle; arrest is an
  officer-decision label (label bias is intrinsic to this family, as
  family 1's ACS labels are survey constructs); the "Not stated" SDE mass
  (13.6%) dilutes the non-White group under the frozen grouping.
- Family 2's GB estimator (sklearn GradientBoostingClassifier, §6) is a
  disclosed substitute for family 1's unavailable implementation; the
  class, not the estimator, was mirrored.

## Artifacts

`E2_PREREGISTRATION.md` (frozen + Amendments A-E2-1/A-E2-2) ·
`src/` (acquire, build_populations, select_analysis_set, train_score,
tau_rule, monitor2, accounting2, audit_sensitivity, common2) ·
`results/` (audit_counts.json, analysis_set.json, deployed_diag.json,
population_metrics.csv, population_metrics_ode.csv, audit_sensitivity.json,
tau_rule.json, monitor.parquet, fold_detail.csv, cell_spreads.csv,
accounting.json, fold_scores.npz) · `validate_e2.py` (ALL PASS) ·
`logs/` (acquisition and run logs) · `data/raw/` (cached API responses).
No manuscript file was edited; no venue was chosen; nothing was submitted;
spend $0.
