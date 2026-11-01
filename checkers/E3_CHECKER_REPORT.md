# E3 Checker Report — Paper 11 Elevation, Cycle E3

## Independent audit of the forecastability-limit theorem package

**Checker role.** Independent checker for the E3 cycle; I did not write
`E3_PROOF.md`. **Materials audited:** `E3_PREREGISTRATION.md` (frozen
2026-11-01T17:46:07Z, SHA-256 `f5e38081…f7b03`), `E3_PROOF.md`,
`ELEVATION_LOG.md` (E3 freeze entry), `E4_RESULTS.md`, `E2_RESULTS.md`,
and the saved artifacts named in the pre-registration.
**Recomputation code (mine, written for this audit; imports nothing from
`src3/`):** `src3_checker/checker_recompute.py` (outputs
`src3_checker/checker_numbers.json`) and
`src3_checker/checker_mc_drift.py` (outputs
`src3_checker/checker_mc_drift.json`). All existing artifacts were
treated read-only.

**Headline verdict.** The numerical cycle is honest and reproducible —
every registered number in `E3_PROOF.md` is reproduced below to rounding
or better, with exactly one statement-level error found (a displayed
scalar formula in T2, §2/O2 note (iii), which the evaluation does not
use). The proof's central self-report — C1 at ladder step (iii) on both
family-1 arms — is correct, and the kill fires under pre-registration
§5 clause **(b)**. It **also** fires under clause **(a)**, via O1: the
L1 weakening (coverage/joint-lead at (T−1)δ instead of δ) is a failure
to close O1 at registered strength, **not a demotion** — no L1 demotion
rule was registered, and §5's demotion list does not contain it. The
consequences of that distinction are stated in §3 and not smoothed over.

---

## 1. Obligation-by-obligation table (O1–O8)

Categories are the pre-registration's own: **DISCHARGED** / **GAP** /
**ASSUMPTION-ADDED**. (No obligation required an assumption beyond the
registered Assumption AB, used exactly as registered; there is
therefore no ASSUMPTION-ADDED verdict. AB is flagged where it is load-
bearing.)

| Obl. | Verdict | One-line basis |
|---|---|---|
| O1 (L1 in full) | **GAP** | Per-step lemma and FAR clause discharge at δ; coverage/joint-lead clauses do **not** close at the frozen δ — only at (T−1)δ, in sketch. Frozen δ-strength for lead events is false in general (§1.1). |
| O2 (T2 reduction) | **DISCHARGED** (substance; two recorded defects) | Gaussianity, Pinsker+Jensen, and the scalar inequality (for x ≥ 1, as registered) are correct; the orthogonality identity is correct **as used** but mis-stated as written (sign/label slip, §1.2); the scalar inequality's eigenwise application to the covariance term is inapplicable as described — and is not used (exact KL is). |
| O3 (level closed forms) | **DISCHARGED** | V_pair and V_∞ verified four independent ways (§1.3). |
| O4 (drift channel) | **DISCHARGED** (exact route) | c_{φ,H} correct; fallback inequality proved; σ_μ² = 0 at the measured parameters is the registered boundary projection of an inconsistent moment system, not a hidden channel — but the direction of a nonzero-drift counterfactual is sign-dependent, not one-directional (§1.4). |
| O5 (C2) | **DISCHARGED** | Counting bound correct; both registered checks recomputed exactly (§2). |
| O6 (C3) | **DISCHARGED** | Determinism argument correct; R4 check recomputed exactly (§2). |
| O7 (P4) | **DISCHARGED** | Dependency inspection is sound: δ_G's inputs are enumerated and are all population-internal (§1.5). |
| O8 (regime computation) | **DISCHARGED** (as a computation) | Every registered estimator and check reproduced from the artifacts (§2), including both σ_n routes, the exact Kalman δ̂, and both lead-CDF arms. Two side-notes in §2.3 do not touch δ̂. |

### 1.1 O1 — Lemma L1: what closes, what does not

**The per-step lemma is correct, and I accept it in full.** With
a := P(A fires | ℱ_t) and b := P(X ∈ B | ℱ_t):

- The covariance identity
  E[ab] − E[E[a|𝒢_t]·E[b|𝒢_t]] = E[(a − E[a|𝒢_t])(b − E[b|𝒢_t])]
  is **correct**: expanding the right side, the two cross terms each
  equal E[E[a|𝒢_t]E[b|𝒢_t]] by the tower property (E[b|𝒢_t] is
  𝒢_t-measurable), leaving E[ab] − E[E[a|𝒢_t]E[b|𝒢_t]]. ∎
- P(A fires, X∈B) = E[ab] is correct given the proof's stated
  condition (the rule's external randomisation is independent of X
  given ℱ_t — alarms do not affect the process, pre-registration §2).
  P(A′ fires, X∈B) = E[q·E[b|𝒢_t]] with q = E[a|𝒢_t] is correct for
  the randomised 𝒢_t-rule, whose measurability is as required
  (q is 𝒢_t-measurable; one independent uniform realises it).
- The bound chain is correct: |a − E[a|𝒢_t]| ≤ 1 since a ∈ [0,1], and
  |b − E[b|𝒢_t]| ≤ TV(Law(X|ℱ_t), Law(X|𝒢_t)) pointwise (TV in the
  sup-over-B convention the statement uses), preserved by E[·].

**FAR — discharged at δ, with one qualification the proof glosses.**
With B = the whole space the per-step statement gives *exact equality*
of unconditional firing probabilities (P(A′) = E[q] = E[a] = P(A)), so
the FAR clause is in fact stronger than claimed **if** δ_t is read
under the falsifier's negative-instance distribution. Read
unconditionally, FAR is a conditional rate over negative steps, the
negative event is X-measurable, and the joint bound yields
|FAR(A) − FAR(A′)| ≤ δ/P(negative step), not δ. The proof's pooled
passage ("average of per-step firing indicators over negative
instances") does not flag this conditioning. No verdict in the cycle
turns on it — C1 is adjudicated from the lead clauses and its own
registered coverage inflation — but the rebuild should state the FAR
clause with the conditioning made explicit.

**Coverage and joint lead at δ — NOT discharged; the weakening is
real, and the frozen δ-strength is unprovable as stated.** Coverage
and {lead ≥ ℓ ∧ covered} are unions over the ≤ T−1 pre-breach alarm
opportunities of an instance. A per-step bound of δ cannot control a
union at δ: the first-alarm slices are disjoint, so per-step shifts
*add*. Sketch of a tight obstruction: k pre-breach steps with disjoint
future sub-windows; at step t, ℱ_t (but not 𝒢_t) reveals an
independent binary window-event B_t with P = p, so the per-step TV is
2p(1−p) =: δ. The rule that fires exactly when its window-event is
revealed has FAR 0 (it never fires on a negative step) and coverage
1−(1−p)^k ≈ kp. Any 𝒢_t-rule matching its FAR to δ can fire with
total probability ≲ δ across steps (its firing is independent of the
B_t), so its coverage is ≲ δ, while the ℱ-rule's coverage is ≈ kδ/2
— exceeding the δ clause for k ≥ 3 (family 1 has k ≤ 5). Hence no
proof of the frozen statement exists; (T−1)δ is the correct order,
not a failure of effort. **The proof's self-report of the weakening is
accurate in substance**: it states plainly that the frozen statement
asserted δ, that the executed proof carries (T−1)δ, that
(T−1)δ̂ = 5 × 0.289 = 1.45 is vacuous, and that the weakened clauses
are used nowhere (C1 fails already at δ — verified in §2: the joint
gaps are 0.098/0.152 and 0.109/0.141, all < δ̂).

Two qualifications on the weakened form itself: (i) as written, the
pooled passage invokes "the union bound" over events of *two different
rules*; the rigorous route is a hybrid/first-alarm argument (replace
one step's rule at a time, conditioning on the common past), which the
proof does not write out — the (T−1)δ clauses are therefore
**proved-in-sketch**, correct in order and, I judge, true, but not
fully written; (ii) the same breaching-instance conditioning gloss as
for FAR applies to "coverage" as a conditional rate (the joint-lead
form, which is what C1 actually consumes, is unconditional and
unaffected). Neither qualification changes any adjudication: the kill
does not need the weakened clauses to fail — it needs them to not be
at δ, and they are not.

**Why this is a GAP under clause (a), not a demotion.** Pre-
registration §4 defines O1 as "L1 in full: the covariance-identity
step, **the passage from per-step to pooled FAR/coverage/joint-lead
statistics**, and the randomised reference rule's measurability."
The pooled coverage/joint-lead passage at the frozen strength is part
of O1 and it did not close. §5's demotion category is explicitly
enumerated — "Ladder step (ii) for one or both arms, or O4's fallback
route" — and L1 weakening is not in it. `E3_PROOF.md` describes the
weakening as recorded "(demotion rule, pre-registration §3)"; §3
contains no demotion rule for L1 (its only demotion language concerns
a stronger-than-registered AB and the C1 ladder). The proof's
*transparency* is exemplary; its *classification* is wrong under the
registered text. See §3 for the adjudication consequence.

### 1.2 O2 — T2 reduction: discharged in substance, two defects recorded

**Gaussianity.** Both predictive laws are Gaussian: linear-Gaussian
state-space, Gaussian (diffuse-limit) posteriors, X_t a linear map of
state plus Gaussian innovations. ✓

**Orthogonality identity — correct as used, mis-stated as written.**
The computation uses E[(m_ℱ − m_𝒢)(m_ℱ − m_𝒢)ᵀ] through the mean term
tr(Σ_𝒢⁻¹ A (P_𝒢 − P_ℱ) Aᵀ), with P_𝒢, P_ℱ the *posterior covariances*.
That is correct: E[m_ℱ|𝒢_t] = m_𝒢 (tower property, common law,
𝒢_t ⊆ ℱ_t) gives E[(m_ℱ−m_𝒢)(m_ℱ−m_𝒢)ᵀ] = E Var(x|𝒢_t) − E Var(x|ℱ_t)
= P_𝒢 − P_ℱ ⪰ 0. **But** the identity as literally printed —
"= P̃_𝒢 − P̃_ℱ, the difference of the *posterior-mean* covariance
matrices" — is sign-reversed: if P̃ := Cov(m), then
P̃_𝒢 − P̃_ℱ = −(P_𝒢 − P_ℱ) ⪯ 0, which cannot equal a covariance of a
difference. (Numerically: P̃_𝒢 − P̃_ℱ would be −2.799e-4 in the level
coordinate; the true E[(m_ℱ−m_𝒢)²] is +2.799e-4 — confirmed by my
Monte Carlo filters: sample E[(m_ℱ−m_𝒢)²] = 2.797e-4 vs
V_pair − V_∞ = 2.799e-4.) This is a notation/label defect in the
statement line, not an error in the quantity evaluated; the rebuild
must print the identity with P̃ read as posterior covariances.
*Common-prior / diffuse-limit caveat*: the tower step needs both
filters to be the same Bayesian rule under one law — true in Model G
for ℱ = full batch history and 𝒢 = its last-two-batches sub-σ-field.
The diffuse level prior is a limit of proper priors; the identity
holds at each proper prior and both sides have finite limits
(P_𝒢 − P_ℱ is prior-independent in the limit, as the O3 closed forms
confirm). Applying the identity to the *record's* forecasters (which
use auxiliary batch statistics beyond {Y_s}) is exactly registered
Assumption AB — named, as registered, not added by the proof.

**Pinsker + Jensen.** Direction correct: TV ≤ √(KL/2) pointwise
(Pinsker), then E√(·) ≤ √(E·) since √ is concave. ✓

**Scalar inequality.** ½[x − 1 − ln x] ≤ (x−1)²/2 for x ≥ 1 is **true**
and the proof's derivative argument is correct in its final form:
with g(x) = (x−1)² − (x − 1 − ln x), g(1) = 0 and
g′(x) = 2(x−1) − (1 − 1/x) = (2x² − 3x + 1)/x = (2x−1)(x−1)/x ≥ 0 for
x ≥ 1. (The proof's first derivative line contains a garbled
intermediate expression before the "directly:" restart; the
factorisation it lands on is right. I also verified the inequality
numerically at x ∈ {1, 1.5, 2, 5}.) **However**, the registered
description "applied eigenwise" to the covariance term does not work
as described: since Σ_ℱ ⪯ Σ_𝒢 (more information, smaller predictive
covariance), the eigenvalues of Σ_𝒢⁻¹Σ_ℱ lie in (0, 1] — in the
evaluated case they are {0.716, 1.000} — where the x ≥ 1 inequality
is not guaranteed (it fails at λ = 0.1: ½[λ−1−ln λ] = 0.701 >
(λ−1)²/2 = 0.405; it happens to hold at λ = 0.716). This defect is
**inert**: the proof bounds nothing with the inequality in the
evaluation — KL̄ is computed exactly — so δ̂ is unaffected. It should
not be cited in the rebuild as a valid eigenwise bound without a
two-sided restatement.

**(iii) A related statement-level error (T2 text, not O3).** The
pre-registration's displayed level mean-term,
(V_pair − V_∞)/(Hσ_η² + V_pair), repeated in `E3_PROOF.md`'s level-
channel paragraph, is **not** the joint H = 2 mean term. The exact
trace is (V_pair − V_∞)/(V_pair + σ_η²) = 0.28421 (the 1ᵀΣ_𝒢⁻¹1
factor collapses to 1/(V_pair + σ_η²)); the displayed formula gives
0.22892, which is the *H-th marginal's* scalar ratio. The cycle's own
`results3/regime_e3.json` "level_channel_closed_form" inherits the
wrong value (mean_term 0.22892, delta_level_only 0.33832). The
headline evaluation never uses it — δ̂ comes from the exact Kalman
KL — so no adjudicated number moves; but the formula as printed in
both the pre-registration and the proof is wrong for the joint
statement and must be corrected in any rebuild.

### 1.3 O3 — level closed forms: discharged

Verified four independent ways at the measured parameters
(σ_η² = 2.378467e-4, σ_n² = 1.384565e-3):

- **Algebra**: V_pair from precisions 1/σ_n² + 1/(σ_η² + σ_n²);
  V_∞ as the non-negative root of V² + Vσ_η² − σ_η²σ_n² = 0
  (polynomial residual at my root: 0.0).
- **Brute-force Gaussian conditioning** (my own Schur complement on
  the explicit joint covariance of (Δ_t, Y_{t−1}, Y_t) with level
  prior variance L): L = 1e4 → 7.470412e-4; L = 1e6 → 7.470412e-4;
  closed form V_pair = 7.470412e-4. (L = 1e8 degrades to 7.470548e-4
  by floating-point cancellation in the Schur complement — expected,
  not a discrepancy.) Monte Carlo OLS conditioning at L = 25:
  residual variance 7.462e-4 vs Schur-at-L=25 7.470e-4 (within MC
  error ≈ 1.4e-6…1e-5 scale of the estimate).
- **Riccati iteration** (my own scalar recursion to fixed point):
  V_∞ = 4.671288e-4 = closed form to all digits shown.
- **Own 2-state Kalman** steady state / pair conditioning (§2):
  P_ℱ[0,0] = 4.671288e-4, P_𝒢[0,0] = 7.470413e-4 — matching the
  proof's claimed agreement with V_∞ and V_pair.

### 1.4 O4 — drift channel: discharged; vanishing is legitimate; direction is sign-dependent

**The coefficient and the fallback are proved correctly.**
c_{φ,h} = Σ_{j=0}^{h−1} φ^j is the right propagated coefficient
(Δ_{t+h} = Δ_t + Σ_j μ_{t+j} + Ση, E[μ_{t+j}|x_t] = φ^j μ_t), and the
fallback chain E‖μ̂_ℱ − μ̂_𝒢‖² = E Var(μ_t|𝒢_t) − E Var(μ_t|ℱ_t) ≤
E Var(μ_t|𝒢_t) ≤ σ_μ² is the same orthogonality identity, correctly
applied. The exact route (a) — both covariances from the Kalman
recursions — is what the evaluation uses; my independent Kalman
implementation, including a from-primitives innovation covariance
validated by Monte Carlo (conditional form: MC
[[1.782e-4, 1.778e-4],[1.778e-4, 4.005e-4]] vs formula
[[1.784e-4, 1.784e-4],[1.784e-4, 4.014e-4]]; combined
A·diag(0,σ_μ²)·Aᵀ + Σ_inn form likewise), reproduces it, and my
step-by-step Monte Carlo filters at a nonzero drift parameterisation
(φ = 0.5, σ_μ² = 0.25γ₀) give KL̄_MC = 0.12249 ± 0.00034 (block SE)
against the analytic 0.12211.

**The vanishing at the measured parameters is legitimate — as a
registered-estimator outcome.** The moment system is not merely
γ₁ < 0: Model G forces γ₂ = φ²σ_μ² ≥ 0, but the measured
γ₂ = −3.02e-5 < 0, and γ₁ < 0 with σ_μ² > 0 would force φ < 0, which
forces γ₂ > 0 — a contradiction. The implied values are φ = γ₂/γ₁ =
+3.135 (outside (−1, 1)) and σ_μ² = γ₁²/γ₂ = −3.08e-6 (negative).
**No** parameterisation of Model G reproduces the three measured
moments, so the registered boundary projection (φ = 0, σ_μ² = 0,
σ_η² = γ₀) is exactly the pre-registered handling, openly reported.
It is not a nonzero channel hidden by the projection in the sense of
a consistent alternative the map suppressed: there is no consistent
alternative *within the model at these moments*. Two honest caveats:
(1) the projection is an estimator outcome, not evidence that the
population drift is truly zero — δ̂ = 0.289 is a [C] certificate
*within the projected model*; (2) the proof's φ-sensitivity grid is
vacuous in the drift dimension (σ_μ² = 0 at every grid point, so δ is
constant by construction — my grid: identical to 10 digits; the
cycle's ~1e-10 wiggle is its 1e-12 prior floor, immaterial).

**Direction of a nonzero-but-unidentified drift channel — the
answer is sign-dependent, and I computed it rather than asserted it.**
Holding the measured γ₀ fixed and reallocating variance to the drift
channel (my Kalman, MC-validated as above): persistent drift
*lowers* δ̂ (φ = 0.5: 0.247 at 25% share, 0.219 at 50%, 0.201 at
75%; φ = 0.8: 0.231; φ = 0.9: 0.256) — a persistent drift makes the
last increment, which the pair filter sees, informative about the
future, shrinking the full-history advantage; φ = 0 allocation leaves
δ̂ exactly unchanged (0.2891214640 — white-noise drift is innovation
noise to both filters, an internal consistency check); anti-
persistent drift *raises* δ̂ (φ = −0.4: 0.308 at 25%, 0.331 at 50%) —
the branch matching γ₁'s sign, though it contradicts γ₂ ≥ 0. Adding
drift on top at fixed σ_η² (φ = 0.5) also lowers δ̂ (0.224 / 0.183).
So the boundary projection is **not** uniformly conservative for
δ̂'s value. What makes the cycle's conclusion safe is magnitude, not
direction: across the entire probed range δ ∈ [0.183, 0.331], while
C1 would need δ ≤ 0.0378 (K1) / 0.0426 (K2) for the covered-only
ladder step (i) and δ ≤ 0.00857 for the all-instances step (ii)
(§2). No drift reallocation comes within a factor of 4 of rescuing
C1. The kill is robust to the identification failure in every
direction; the exact value 0.289 is not.

### 1.5 O7 / P4 — dependency inspection: sound

δ_G's definition enumerates its inputs completely: (σ_η, σ_μ, φ,
σ_n, H) — one population's gap-process parameters and its batch
design — plus, through L1, that same population's instance
distribution at the falsifier's matched-FAR construction. I inspected
the T2/KL construction and the regime computation: no cross-
population quantity enters; in particular the null-score TV of the
transport bound (upgrade T1–T3) is neither an input, an output, nor
a relaxation of δ_G, and the σ_n and moment inputs are estimated from
family 1's own monitor/population artifacts (the falsifier's pooled
instance population — pooling across family 1's own trajectories is
the estimand's definition, not a transport quantity). Hence setting
the achieved-FAR transport error to zero changes δ_G by exactly
zero, as claimed, and R1 (transport repaired on both criteria in
both classes ∧ FALSIFIER-U fired in both classes) is the predicted
configuration. The proposition is an inspection claim, registered as
such, and the inspection holds. **DISCHARGED.**

---

## 2. Independent recomputation (O8 and the registered checks)

Method: my own estimators and my own Kalman/conditioning code
(`src3_checker/`), from the saved artifacts only. "Proof" = the value
in `E3_PROOF.md` / `results3/regime_e3.json` (+ followup). Flag rule:
discrepancy beyond rounding = relative difference > 0.1% on a quantity
the adjudication uses, or any difference in a count/verdict.

### 2.1 Family-1 regime quantities (from `results/population_metrics.csv`, `results/monitor_steps.csv`)

| Quantity | Proof | Checker | Flag |
|---|---|---|---|
| trajectories / cells / increments | 18 / 108 / 90 | 18 / 108 / 90 | — |
| mean increment | +0.00272 | +0.0027175 | — |
| γ₀ (ddof=1) | 2.3785e-4 | 2.378467e-4 | — |
| γ₁ (72 pairs) | −9.64e-6 | −9.6444e-6 | — |
| γ₂ (54 pairs) | −3.02e-5 | −3.0239e-5 | — |
| lag-1 / lag-2 autocorr | −0.041 / −0.127 | −0.04055 / −0.12714 | — |
| moment map | identification failure → boundary (φ=0, σ_μ²=0, σ_η²=γ₀) | same; implied φ = +3.135, implied σ_μ² = −3.08e-6, γ₂<0 impossible in Model G | — |
| σ_n: monitor SE mean | 0.03721 | 0.03720975 | — |
| σ_n: replicate-SD mean / median | 0.02889 / 0.02846 | 0.02888857 / 0.02845940 | — |
| σ_n used (registered larger) | 0.03721 | 0.03720975 | — |
| σ_n/σ_η | ≈ 2.41 | 2.413 | — |
| V_pair / V_∞ | 7.4704e-4 / 4.6713e-4 | 7.470412e-4 / 4.671288e-4 | — |
| Kalman P_ℱ[0,0] / P_𝒢[0,0] | 4.6713e-4 / 7.4704e-4 | 4.671288e-4 / 7.470413e-4 | — |
| mean-term trace | 0.28421 | 0.28420745 | — |
| covariance part of KL̄ | 0.02510 | 0.02507872 (= 0.0251 at 4 d.p.) | — |
| **KL̄** | **0.16718** | **0.16718244** (Δ = 5e-8, iteration tolerance) | — |
| **δ̂ = √(KL̄/2)** | **0.28912** | **0.28912146** | — |
| δ̂, Monte Carlo filters (independent) | — | KL̄_MC = 0.16706 ± 0.00031 (block SE, 398k steps) → δ ≈ 0.2890 | confirms |
| δ̂ at replicate σ_n = 0.02889 | 0.22257 | 0.22257154 | — |
| φ grid {0, 0.2, 0.4, 0.6} at σ_μ²=0 | 0.28912 throughout | 0.2891214640 throughout (exactly constant) | — |
| V_pair − V_∞ ; Hσ_η² | 2.799e-4 ; 4.757e-4 | 2.799124e-4 ; 4.756934e-4 | — |

### 2.2 Lead-CDF checks (C1) and corollaries C2/C3

**K1** — `results/leadtime_distributions.csv`, metric eo, τ = 0.05,
H = 2, LOSO, far_target 0.10 (175 instances per method):

| Quantity | Proof | Checker | Flag |
|---|---|---|---|
| coverage proposed / extrap | 0.59429 / 0.52571 | 0.594286 / 0.525714 | — |
| median lead proposed / extrap / last-value | 3.0 / 3.0 / 2.0 | 3.0 / 3.0 / 2.0 | — |
| extrap covered CDF F(3) / F(2) | 0.59783 / 0.34783 | 0.597826 / 0.347826 | — |
| joint gaps F(3)−½ ; ½−F(2) | 0.098 ; 0.152 | 0.09783 ; 0.15217 (both < δ̂) | — |
| δ_marg (covered-only, factor 2.5849) | 0.747 | 0.74734 | — |
| ladder (i) requirement F(3) ≥ 1.247, F(2) ≤ −0.247 | impossible | impossible → **FAIL** | — |
| ladder (ii) own convention: all-inst median / F(1) / F(0) | 1 / 0.5086 / 0.4743 | 1.0 / 0.508571 / 0.474286 | — |
| ladder (ii) requirement ≥ 0.78912 / ≤ 0.21088 | FAIL both sides | FAIL both sides | — |
| ladder (ii) at covered median (side check): F_all(3) / F_all(2) | 0.78857 / 0.65714 | 0.788571 / 0.657143 → FAIL (upper side by 0.0005) | — |
| joint sup-diff proposed vs extrap, ℓ=1..5 | 0.103 | 0.102857 | — |

**K2** — `elevation/results4/f1_arm_leads.parquet`, far_target 0.10,
H = 2 (175 instances per method):

| Quantity | Proof | Checker | Flag |
|---|---|---|---|
| coverage traq / extrap | 0.60571 / 0.52571 | 0.605714 / 0.525714 | — |
| median lead traq / extrap | 3.0 / 3.0 | 3.0 / 3.0 | — |
| extrap covered CDF F(3) / F(2) | 0.60870 / 0.35870 | 0.608696 / 0.358696 | — |
| joint gaps F(3)−½ ; ½−F(2) | 0.109 ; 0.141 | 0.10870 ; 0.14130 (both < δ̂) | — |
| δ_marg (factor 2.5531) | 0.738 | 0.73816 | — |
| ladder (i) requirement F(3) ≥ 1.238, F(2) ≤ −0.238 | impossible | impossible → **FAIL** | — |
| ladder (ii) own convention: median / F(1) / F(0) | 1 / 0.5086 / 0.4743 | 1.0 / 0.508571 / 0.474286 → FAIL both sides | — |
| ladder (ii) at covered median: F_all(3) / F_all(2) | 0.79429 / 0.66286 | 0.794286 / 0.662857 → FAIL (lower side) | — |
| joint sup-diff traq vs extrap | 0.154 | 0.154286 | — |

(The two arms' all-instances extrap distributions are numerically
identical — same 175 instances, same deterministic reference rule —
so the identical ladder-(ii) numbers are expected, not a copy error.
C1 rescue ceilings, for the record: ladder (i) needs δ ≤ 0.0378 (K1)
/ 0.0426 (K2); ladder (ii) needs δ ≤ 0.00857 (both arms, binding side
F(1) − ½). δ̂ = 0.289 exceeds these by 7.6× / 34×.)

**C2** — family 2 from `elevation/results/population_metrics.csv`;
family 1 from `results/population_metrics.csv`:

| Quantity | Proof | Checker | Flag |
|---|---|---|---|
| family-2 LR p̂ at τ=0.05 | 2/108 = 0.01852 | 2/108 = 0.018519 | — |
| bound N(T−1)p̂ = 99·p̂ | 1.833 < 3 | 1.833333 < 3 | — |
| crossings after base (forces) | 2 | 2 | — |
| family-1 share ≥ 0.05 | 0.3056 (33/108) | 0.305556 (33/108) | — |
| family-1 bound 18·5·share | 27.5 ≫ 3 | 27.500 ≫ 3 | — |

**C3** — family 2 2025 LR from `elevation/results4/population_metrics.csv`:

| Quantity | Proof | Checker | Flag |
|---|---|---|---|
| cells | 96 | 96 | — |
| EO = 0 / DP = 0 / both = 0 | 81/96 = 84.4% each | 81 / 81 / 81 = 0.84375 each | — |
| τ\* = 0 at q ∈ {0.60, 0.70, 0.80} | per `tau_star.json` | confirmed in `tau_star.json` (LR EO/DP all 0.0) | — |
| spike maximum (max EO) | 0.20 | 0.200 | — |

**Remark R-τ\* inputs** (descriptive, not adjudicated): family-2
batch σ_n from `elevation/results/monitor.parquet` — replicate SD
mean 0.019644 (proof 0.01964), SE mean 0.021724 (proof 0.02172);
τ\*_GB = 0.003329 (proof 0.003329); ratios 5.90× / 6.53× — the
proof's "≈ 6× below batch noise" is accurate.

### 2.3 Discrepancies found (complete list)

1. **T2's displayed level mean-term formula is wrong for the joint
   statement** (pre-registration §3, repeated in `E3_PROOF.md`):
   (V_pair − V_∞)/(Hσ_η² + V_pair) = 0.22892 ≠ the exact joint trace
   (V_pair − V_∞)/(V_pair + σ_η²) = 0.28421. The cycle's
   `regime_e3.json` side-check ("level_channel_closed_form",
   delta_level_only 0.33832) inherits the wrong formula. **Not used
   in δ̂; no adjudicated number affected.** This is the only
   substantive discrepancy.
2. Everything else agrees to rounding or better. The largest
   differences: KL̄ (5e-8, Kalman iteration tolerance), covariance
   part printed as 0.02510 vs recomputed 0.025079 (identical at the
   printed 4 d.p.), φ-grid wiggle ~1e-10 in the cycle's output vs
   exactly constant in mine (the cycle's 1e-12 prior floor). None is
   beyond rounding; no count, coverage, CDF value, or verdict
   differs.

---

## 3. Kill adjudication (pre-registration §5)

§5 has two kill clauses. **Clause (b) fires, indisputably:** the
proof closes (L1's per-step core, T2, C2, C3, P4 as detailed above),
and C1 lands at ladder step (iii) for **both** family-1 arms — ladder
(i) requires a CDF value ≥ 1.247 (K1) / 1.238 (K2), which is
impossible, and ladder (ii) under its own convention fails on both
sides in both arms (F(1) = 0.5086 vs ≥ 0.7891; F(0) = 0.4743 vs
≤ 0.2109). The theory is true but too weak to explain the record it
was commissioned to explain — exactly the failure mode clause (b)
exists to catch. K1 is **NOT COVERED**, K2 is **NOT COVERED**; K3 and
K4 are covered by C2 and C3 respectively.

**Clause (a) also fires, on the registered text.** O1 — defined in
§4 as L1 *in full*, including the pooled passage for
coverage/joint-lead — did not close at the frozen strength: those
clauses stand only at (T−1)δ, in sketch (§1.1), and the frozen
δ-strength is false in general, not merely unproved. §5's demotion
category is exhaustive as written (C1 ladder (ii); O4's fallback) and
does not include an L1 weakening; the proof's citation of a "demotion
rule, pre-registration §3" for it does not correspond to any
registered rule. I therefore record the weakening as an **O1 failure
under clause (a)**, in addition to clause (b) — not as a demotion.
This does not change the headline outcome (the package is killed at
registered strength under either clause, and C1's failure is
independent of the weakening, since C1 fails already when granted
the frozen δ), but it changes what may be claimed to stand:

**Correct registered reading of the outcome.** "E3 killed at
registered strength; C1 NOT COVERED on both arms" — **correct**.
"L1/T2/C2/C3/P4 stand as proved results" — **correct only with L1
qualified**: what stands is L1's per-step statement and FAR clause at
δ (FAR with the conditioning qualification of §1.1), and the
coverage/joint-lead clauses at (T−1)δ in proved-sketch form; the
frozen L1, verbatim, does **not** stand, and per §5 ("whatever this
cycle produces is what the bound-only rebuild may use, verbatim in
strength") the rebuild may use L1 only at the weakened strength.
T2 stands as proved for the reduction and closed forms, with the
P̃-notation corrected to posterior covariances, the level mean-term
formula corrected to (V_pair − V_∞)/(V_pair + σ_η²) for the joint
statement, the eigenwise scalar bound not cited as registered, and
δ̂ = 0.289 standing as a [C] evaluation *within the projected
Model G* (robust for C1's purpose across the full probed drift
range δ ∈ [0.183, 0.331], §1.4). C2, C3, and P4 stand as proved,
with their registered checks recomputed exactly. Remark R-τ\*
remains a remark, as the proof leaves it. No second E3 cycle is
authorised by this report; per §5 that requires Ranadhir's new
decision.

**Checker sign-off.** Obligation verdicts: O1 GAP; O2 DISCHARGED
(substance, two recorded defects); O3 DISCHARGED; O4 DISCHARGED;
O5 DISCHARGED; O6 DISCHARGED; O7 DISCHARGED; O8 DISCHARGED.
Numerical audit: one substantive discrepancy (the unused T2 scalar
formula, §2.3.1); no adjudicated number differs beyond rounding.
Kill: §5 clauses (a) **and** (b) both fire; E3 is killed at
registered strength; C1 NOT COVERED on both family-1 arms.
