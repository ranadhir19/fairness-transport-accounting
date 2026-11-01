# Paper 11 — Elevation Cycle E3: RESULTS
## The forecastability-limit theorem, executed under its pre-registration

**Cycle:** E3 (commissioned by Ranadhir, 2026-11-01: *"Commission E3 as a limit theorem, then rebuild bound-only"*).
**Pre-registration:** `E3_PREREGISTRATION.md`, frozen 2026-11-01T17:46:07Z, SHA-256 `f5e38081ab14a5c343219755a50074a94142a8d53022c34c3eb95ac4bbdf7b03`.
**Proof text:** `E3_PROOF.md`. **Regime computation:** `src3/regime_e3.py`, `src3/regime_e3_followup.py` → `results3/regime_e3.json`, `results3/regime_e3_followup.json`.
**Independent checker:** `E3_CHECKER_REPORT.md` (477 lines) + `src3_checker/` (recompute + Monte Carlo; no `src3/` imports; all source artifacts read-only). $0 spent throughout.

---

## 1. Theorem status: KILLED at registered strength — both kill clauses fire

**Clause (b) — indisputable.** Corollary C1 (the commissioned explanation of the two family-1 falsifications) lands at demotion-ladder step **(iii) on BOTH family-1 arms**:
- Ladder (i) requires coverage gaps F(m) ≥ 1 + δ_marg − ½ ≈ **1.247 (K1) / 1.238 (K2)** — impossible, since δ_marg = 0.747 / 0.738 > ½ caps any coverage difference below 1.
- Ladder (ii), under its own both-arms convention, fails **both sides**: reference all-instances median = 1, F(1) = 0.5086 vs required ≥ 0.7891; F(0) = 0.4743 vs required ≤ 0.2109.
- C1 would have needed δ ≤ 0.0378 / 0.0426 (covered-only reading) or ≤ 0.00857 (all-instances). The evaluated bound is **δ̂ = 0.28912**. The uninflated joint gaps (≈0.098 / 0.109 and ≈0.152 / 0.141) are likewise far below δ̂. The bound *permits* the record; it does not explain it.

**Clause (a) — fires on the registered text (checker ruling, accepted).** Obligation O1 was registered as "L1 in full," including the pooled coverage/joint-lead passage at δ. That passage closes only at **(T−1)δ**, and §5's demotion category is exhaustively enumerated (C1 ladder (ii); O4 fallback) — an L1 weakening is not in it. The proof's appeal to a "demotion rule, pre-registration §3" cites a rule that does not exist there. The weakening is real, not an artefact: the checker exhibits the frozen δ-strength form as false in general (disjoint future sub-windows, each at per-step TV δ, give ℱ-rule coverage ≈ kδ/2 against ≲ δ for any FAR-matched 𝒢-rule, k ≤ 5 in family 1).

**Consequence.** No second E3 cycle exists without Ranadhir's new decision. The rebuild (Stage 3) proceeds **without a limit theorem**, using only the proved pieces at the exact strengths recorded in §3 below.

## 2. Obligation table (independent checker verdicts)

| Obligation | Verdict | Substance |
|---|---|---|
| O1 (L1 proved at registered strength) | **GAP** | Covariance identity correct; per-step bound and FAR discharge at δ (unconditional firing probabilities are in fact exactly equal; the conditional-rate reading carries a δ/P(negative-step) qualification the proof's pooled passage does not flag). Coverage/joint-lead close only at (T−1)δ, and there only in sketch — the union bound needs a hybrid/first-alarm argument the proof does not write out. |
| O2 (T2 reduction) | **DISCHARGED** (substance; two defects recorded) | Gaussianity, Pinsker+Jensen direction, and the scalar inequality ½[x−1−ln x] ≤ (x−1)²/2 for x ≥ 1 (derivative g′(x) = (2x−1)(x−1)/x ≥ 0) all verified. Defect (i): the orthogonality identity as literally printed is sign-reversed (Cov(m_G) − Cov(m_F) = −(P_G − P_F)); the formula actually used, tr(Σ_G⁻¹A(P_G−P_F)Aᵀ), is correct, the diffuse-limit caveat is sound (tower property, 𝒢_t ⊆ ℱ_t; MC: E[(m_F−m_G)²] = 2.797e-4 ≈ V_pair−V_∞ = 2.799e-4), and Assumption AB is used exactly as registered — nothing added. Defect (ii): the "eigenwise" application of the scalar bound is inapplicable as described (eigenvalues {0.716, 1.000} ⊂ (0,1]) — inert, because KL̄ is computed exactly, never via the bound. |
| O3 (level closed forms) | **DISCHARGED** | V_pair = 7.470412e-4, V_∞ = 4.671288e-4 verified four independent ways (closed-form algebra, Riccati polynomial residual 0.0; brute-force Schur conditioning at diffuse L = 1e6; Monte Carlo OLS conditioning; checker's own Riccati iteration and Kalman read-off). |
| O4 (drift channel) | **DISCHARGED** | c_{φ,H} = Σφ^j correct; the proved fallback E‖μ̂_ℱ−μ̂_𝒢‖² ≤ σ_μ² stands. The drift vanishing is legitimate: with γ₂ = −3.02e-5 < 0, **no** Model G parameterisation fits the moments (Model G requires γ₂ = φ²σ_μ² ≥ 0; implied φ = γ₂/γ₁ = +3.135, implied σ_μ² = γ₁²/γ₂ = −3.08e-6), so σ_μ² = 0 is the registered boundary projection of an inconsistent system, not a hidden channel. |
| O5 (C2) | **DISCHARGED** | Counting bound correct; both numerical checks exact (§4). |
| O6 (C3) | **DISCHARGED** | Determinism argument correct; degeneracy check exact (§4). |
| O7 (P4 separation) | **DISCHARGED** | Dependency inspection sound: δ_G's inputs are (σ_η, σ_μ, φ, σ_n, H) plus the same population's instance distribution at matched FAR; the transport bound's null-score TV enters nowhere. |
| O8 (regime computation) | **DISCHARGED** | All registered estimators and checks reproduced by the checker from the saved artifacts (§5). |

**No ASSUMPTION-ADDED verdicts anywhere.** Assumption AB was used exactly as registered.

## 3. What stands as proved (exact strengths the rebuild may use)

- **L1, weakened form only:** per-step alarm-probability bound at δ, and FAR at δ. Coverage/joint-lead statements at **(T−1)δ**, at union-bound-sketch level. The frozen L1 does **not** stand verbatim.
- **T2 [C]:** the Model G evaluation δ̂ = **0.28912** at the registered (boundary-projected) parameters, with two corrections on the record: the P̃ notation in the orthogonality identity (sign as printed) and the displayed level mean-term — the exact joint trace term is **0.28421**; the printed 0.22892 is the H-th marginal's ratio and is inherited by `regime_e3.json`'s side-check. It is never used in δ̂; no adjudicated number is affected.
- **C2** (crossing rarity) and **C3** (cut degeneracy) stand as proved, with their registered hypotheses.
- **P4** (transport/forecastability separation) stands.

## 4. Corollary coverage table (fixed in advance by the pre-registration)

| # | Record item | Verdict | Basis (checker-confirmed numbers) |
|---|---|---|---|
| K1 | FALSIFIER-U at absolute τ (family 1) | **NOT COVERED** | 175 instances; coverages proposed 0.5943 / extrap 0.5257; medians 3.0 / 3.0; F(3) = 0.5978, F(2) = 0.3478; δ_marg = 0.747; joint sup-difference 0.103 ≪ δ̂ = 0.289 |
| K2 | FALSIFIER-U at adapted τ* (family 1, E4 secondary arm) | **NOT COVERED** | 175 instances; coverages 0.6057 / 0.5257; F(3) = 0.6087, F(2) = 0.3587; δ_marg = 0.738; sup-difference 0.154 ≪ δ̂ |
| K3 | E2 scale-boundedness vacuity (family 2, 2024) | **COVERED by C2** | p̂(0.05) = 2/108 = 0.01852; bound 9 × 11 × p̂ = **1.833 < 3** (registered scoreability floor); observed crossings after base = **2** ✓. Family-1 consistency check: share ≥ 0.05 = 33/108 = 0.3056, bound 27.5 ✓ |
| K4 | E4 statistic-degeneracy vacuity (family 2, 2025 LR) | **COVERED by C3** | EO = 0 and DP = 0 in **81/96 cells (84.4%)**; τ* = 0 at q ∈ {0.60, 0.70, 0.80}; quantised spike max EO 0.20 ✓ |

## 5. The measured regime (checker-recomputed from saved artifacts; agreement exact at printed precision)

- Population EO increments (90): mean +0.00272; **γ₀ = 2.3785e-4 (σ_inc = 0.01542); γ₁ = −9.64e-6 (autocorr −0.041); γ₂ = −3.02e-5 (autocorr −0.127)** → moment-map identification failure (γ₁ ≤ 0, γ₂ < 0) → registered boundary projection (φ = 0, σ_μ² = 0, σ_η² = γ₀). The drift channel is exactly zero at every permitted parameterisation.
- **σ_n = 0.03721** (monitor saved-SE mean; the registered larger measure; replicate-SD mean 0.02889, median 0.02846). σ_n/σ_η ≈ 2.41 — batch noise dominates per-step movement; this is why the level channel carries the whole bound and why full history genuinely informs the current level.
- **δ̂ = 0.28912 (KL̄ = 0.16718)**; checker Monte Carlo independently confirms KL̄ = 0.16706 ± 0.00031. At replicate σ_n: 0.22257. Across φ ∈ {0, 0.2, 0.4, 0.6} (σ_μ² = 0): exactly flat at 0.28912.
- Robustness probes (checker, MC-validated): forcing a drift component at φ = 0.5 *lowers* δ̂ (0.247 at 25% γ₀ share; 0.219 at 50%); anti-persistent φ = −0.4 raises it (0.308). **No probed value in [0.183, 0.331] rescues C1** — the kill conclusion does not hinge on the boundary projection.

## 6. What the E3 outcome does and does not license the paper to say

**Licensed:** the falsification record and the accounting evidence carry the paper; C2 and C3 at proved strength (the two vacuity mechanisms are theorems, usable as pre-flight checks); P4's separation; L1/T2 reported as a *boundary result* — the natural information bound evaluated at the measured regime (δ̂ = 0.289) is an order of magnitude too weak to explain the falsifications, because at n = 2,000 batch noise is ≈2.4× the process's per-step movement; a theorem that does explain the record would need per-instance structure, and that is stated as the open problem.

**Not licensed:** any claim that the forecasting failures were information-theoretically necessary; any use of L1 at its frozen δ-strength for coverage/joint-lead statements; any citation of the E4 confirmatory arm as a forecasting falsification (per E4's closing assessment — the falsifications are the upgrade's FALSIFIER-U and the E4 family-1 secondary arm).

## 7. Discrepancy record

One substantive discrepancy (T2's displayed mean-term formula, §3 above — no adjudicated number affected); O2's two recorded defects (one notational, one inert); the checker's γ₀ at ddof1 (2.378467e-4) vs the proof's value agree at printed precision. All other checker-vs-proof differences are at or below rounding. The Stage-2 self-assessment had provisionally treated the (T−1)δ weakening as a demotion; the checker's clause-(a) ruling (§1) supersedes that reading and is the one recorded here.
