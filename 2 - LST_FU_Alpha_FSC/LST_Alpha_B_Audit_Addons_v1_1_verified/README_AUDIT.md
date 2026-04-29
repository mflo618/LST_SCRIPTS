# LST Alpha B Audit Add-Ons — Audit Workflow

This folder contains small, single-purpose scripts that let a reviewer check the electromagnetic-sector fine-structure constant closure one step at a time. Each script runs on its own, prints human-readable results, and optionally writes a JSON report you can save.

The current primary audit is the **relational-recursion prediction** of the Thomson-limit U(1) interface scale:

`Scale_alpha,pred(e) ≈ 240.739008512`

which gives:

`alpha_inv_pred ≈ 137.074274991`

The older supplied-scale audit using `Scale = 240.463` is retained as a **legacy bridge-architecture baseline**, not as the current primary prediction.

The closure equation used throughout is:

```text
alpha_inv = Scale_alpha(e)^2 / (7.5 * pi * phi^6)
```

The goal is to answer five practical questions:

1. **Is the pipeline non-circular?**  
   No hidden use of the measured fine-structure constant `alpha` in the steps that should be alpha-free.

2. **Is there a predictive step?**  
   Can the current relational-recursion path predict `Scale_alpha,pred`, and can the supplied-scale audit still map any alpha-free Scale deterministically to `alpha_inv`?

3. **Is the mapping consistent?**  
   If we invert the mapping, do we recover the Scale corresponding to a chosen `alpha_inv`?

4. **Are alternatives clearly worse?**  
   If we try another construction, does it visibly miss?

5. **Is the result stable?**  
   Do small changes in inputs produce appropriately small changes in outputs? Does `alpha_inv` scale as expected with Scale?

---

## What’s in this folder

- `derive_scale_alpha_relational.py`  
  Derives `Scale_alpha,pred(e)` from LST geometric constants using `phi^(4*phi)`, the U(1) cycle factor `2*pi*phi`, and the upstream `6/5` vacuum-stability ratio. This is the current primary prediction path.

- `scale_from_independent_inputs.py`  
  Locks a supplied **Scale** value from a small JSON file and records its provenance. This should be **alpha-free** for predictive or baseline audits.

- `alpha_from_scale.py`  
  Computes `alpha_inv` from a given Scale using the geometry/density closure relation.

- `scale_from_alpha.py`  
  Computes Scale from a given `alpha_inv`. Use this for **round-trip checks**, not for predictive audits.

- `alt_hypothesis_sweep.py`  
  Compares two constructions against a target `alpha_inv`:  
  1. an inverse-area construction, and  
  2. a Core×Scale construction used as a deliberate alternative.

- `static_guard_all.py`  
  Scans selected core modules and fails if any banned identifier appears at the **code** level where the path should be alpha-free. This is a **non-circularity** attest.

- `uncertainty_budget.py`  
  Propagates declared uncertainties in inputs such as Scale, `phi`, and `QC2` to a change in `alpha_inv`, with printed partial derivatives.

- `robustness_sweep.py`  
  Sweeps Scale in a small window and fits a log-log slope. Expect a slope near `2` because `alpha_inv ∝ Scale^2`.

Also included: minimal core modules these scripts import, such as `density_certificate_v2.py`, `g_electron.py`, `electron_density_certificate.py`, `lst_sigma_em0.py`, plus sample data files such as `independent_scale.sample.json`.

---

## Terms used

- **phi**: the golden ratio, `phi = (1 + sqrt(5)) / 2`.

- **Scale_alpha,pred**: the current relational-recursion prediction for the Thomson-limit U(1) interface scale, approximately `240.739008512`.

- **Scale_alpha,target**: the round-trip Scale inferred from measured `alpha_inv`, approximately `240.705394812`. This is an inversion reference, not a prediction.

- **Scale_alpha,audit**: the older supplied-scale baseline value, approximately `240.463`. It is retained for bridge-audit continuity and historical comparison.

- **Scale_mass(e)**: the fermion mass-formula structural scale for the electron, `Scale_mass(e) = phi^(4*phi) ≈ 22.5214537505`.

- **alpha_inv**: inverse fine-structure constant, e.g. `137.035999084`.

- **Provenance**: a short note describing where a number came from so others can reproduce it.

---

## Before you begin

- Python 3.8+ recommended.
- No extra packages required; everything uses the standard library.
- Run commands **inside this folder**.

---

## Case A — Relational-Recursion Prediction, Current Primary

**Purpose:** Derive the Thomson U(1) interface scale and predicted `alpha_inv` from LST geometric structure.

This case derives:

```text
Scale_alpha,pred(e) = phi^(4*phi) * 2*pi*phi * C_rel
```

where:

```text
q       = phi^(3 - D_eff) = sqrt(6/5)
epsilon = q - 1
C_rel   = 1 / sqrt(1 - epsilon)
        = [2 - sqrt(6/5)]^(-1/2)
```

Run:

```bash
python derive_scale_alpha_relational.py --json relational_scale_prediction.json
```

Expected output:

```text
scale_mass       = phi^(4*phi)                 ≈ 22.5214537505
q                = sqrt(6/5)                   ≈ 1.0954451150
epsilon          = q - 1                       ≈ 0.0954451150
C_rel            = [2 - sqrt(6/5)]^(-1/2)      ≈ 1.0514352631
Scale_alpha,pred = scale_mass * 2*pi*phi*C_rel ≈ 240.739008512
alpha_inv_pred   = Scale_alpha,pred^2 / (7.5*pi*phi^6)
                                                 ≈ 137.074274991
```

Comparison with measurement:

```text
alpha_inv_obs        ≈ 137.035999084
Scale_alpha,target   ≈ 240.705394812
rel_error_alpha_inv  ≈ +0.0279 %
rel_error_scale      ≈ +0.0140 %
```

The script also evaluates the alternative **relative-deficit** recursion reading, in which the missing capacity is measured against the completed target rather than the existing layer:

```text
epsilon_relative   = (q - 1) / q
C_relative         = (6/5)^(1/4) ≈ 1.046635
alpha_inv_relative ≈ 135.826
rel_error_relative ≈ -0.883 %
```

The temporally natural absolute-deficit branch is observationally favored over the relative-deficit alternative by approximately `31x` in relative error.

**What this tells us:** this is the framework’s strongest current electromagnetic-sector claim. The Thomson U(1) interface scale is predicted from the relational-recursion lift, not supplied.

---

## Case B — Supplied-Scale Audit, Legacy Baseline

**Purpose:** Verify the bridge architecture: given any alpha-free supplied Scale value, the closure formula maps it deterministically to `alpha_inv`.

This was the original predictive workflow using `Scale = 240.463` from the earlier density-certificate baseline. It is retained as a non-circularity and bridge-architecture audit, but it is no longer the current primary prediction.

Run:

```bash
python alpha_from_scale.py --scale 240.463 --json alpha_from_scale.json
```

Expected output:

```text
alpha_inv = (240.463)^2 / (7.5*pi*phi^6) ≈ 136.760142
```

**What this tells us:** there is a clear deterministic map from an alpha-free supplied Scale to `alpha_inv`. No fitting to alpha occurs in this path. The result is less precise than Case A and is now treated as a historical baseline.

You can also run the supplied-scale audit using the current predicted scale:

```bash
python alpha_from_scale.py --scale 240.739008512 --json alpha_from_scale_pred.json
```

Expected:

```text
alpha_inv ≈ 137.074274991
```

---

## Case C — Round-Trip Closure, Sanity Check

**Purpose:** Show the mapping is internally consistent.

Compute the Scale that would reproduce CODATA `alpha_inv`:

```bash
python scale_from_alpha.py --alpha-inv 137.035999084
```

Expected:

```text
Scale_alpha,target ≈ 240.705394812
```

Then plug that Scale back in:

```bash
python alpha_from_scale.py --scale 240.7053948116
```

Expected:

```text
alpha_inv ≈ 137.035999084
```

**What this tells us:** the formulas invert each other correctly. This is a **sanity check**, not a prediction, because it starts from measured alpha.

---

## Case D — Alternative Hypothesis Comparison

**Purpose:** Show that the chosen inverse-area construction outperforms a clear alternative.

Legacy baseline comparison:

```bash
python alt_hypothesis_sweep.py --alpha-inv-target 137.035999084 --scale 240.463 --json alt_legacy.json
```

Current prediction comparison:

```bash
python alt_hypothesis_sweep.py --alpha-inv-target 137.035999084 --scale 240.739008512 --json alt_pred.json
```

Expected behavior:

- **Inverse-area construction:** lands near the target.
- **Core×Scale construction:** misses by many orders of magnitude, showing it is not competitive.

**What this tells us:** the inverse-area relational-capacity construction is strongly preferred over the deliberate Core×Scale alternative.

---

## Case E — Non-Circularity Guard

**Purpose:** Ensure the alpha-free pathway is actually alpha-free in code.

Run:

```bash
python static_guard_all.py --paths lst_sigma_em0.py g_electron.py electron_density_certificate.py density_certificate_v2.py --json guard.json
```

Expected:

```text
No AST-level hits for banned identifiers.
```

Token hits in comments or docstrings may be allowed depending on the script settings; AST hits indicate real code references that need removal.

For the relational-recursion script, note that `alpha_inv_obs` appears only in the post-prediction comparison block. The predicted values `Scale_alpha,pred` and `alpha_inv_pred` are computed before and independently of `alpha_inv_obs`.

**What this tells us:** the alpha-free construction path does not secretly reference measured alpha or the electromagnetic coupling where it should not.

---

## Case F — Uncertainty Budget

**Purpose:** Quantify how small input changes move `alpha_inv`.

Legacy baseline example:

```bash
python uncertainty_budget.py --scale 240.463 --dscale 1e-3 --json ub_legacy.json
```

Current prediction example:

```bash
python uncertainty_budget.py --scale 240.739008512 --dscale 1e-3 --json ub_pred.json
```

Expected:

- A printed `alpha_inv` for the nominal Scale.
- Partial derivatives such as `da_dscale`.
- Absolute and relative uncertainty estimates.

Because:

```text
alpha_inv ∝ Scale^2
```

a relative error `epsilon` in Scale produces approximately `2epsilon` in `alpha_inv`.

---

## Case G — Robustness Sweep

**Purpose:** Check the expected scaling and basic numerical stability.

Legacy baseline example:

```bash
python robustness_sweep.py --scale 240.463 --rel-span 0.05 --points 9 --json sweep_legacy.json
```

Current prediction example:

```bash
python robustness_sweep.py --scale 240.739008512 --rel-span 0.05 --points 9 --json sweep_pred.json
```

Expected:

- A log-log slope very close to `2.0`.
- A smooth table of `(Scale, alpha_inv)` pairs in the JSON.

**What this tells us:** the implementation behaves as expected and small changes in Scale do not cause erratic jumps.

---

## Three-Scale Distinction

To prevent confusion across audit outputs, the pack distinguishes:

| Symbol | Value | Role |
|---|---:|---|
| `Scale_alpha,pred` | `≈ 240.739008512` | Relational-recursion prediction, current primary |
| `Scale_alpha,target` | `≈ 240.705394812` | Round-trip from measured alpha, inversion reference, not prediction |
| `Scale_alpha,audit` | `≈ 240.463` | Earlier supplied-scale baseline, historical bridge audit |

Interpretation:

- `Scale_alpha,pred` is what the current derivation predicts.
- `Scale_alpha,target` is what the observed alpha would require under the closure formula.
- `Scale_alpha,audit` was the earlier alpha-free supplied-scale test value. It remains useful for testing the bridge architecture, but it is superseded by `Scale_alpha,pred` as the predictive output.

---

## Interpreting the numbers you may see

With the current relational-recursion prediction:

```text
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

This is approximately `+0.0279%` above the measured Thomson-limit value:

```text
alpha_inv_obs ≈ 137.035999084
```

With the round-trip inversion:

```text
Scale_alpha,target ≈ 240.705394812
```

This is the Scale required to reproduce measured alpha exactly through the closure formula. It is not a prediction.

With the historical supplied-scale audit:

```text
Scale_alpha,audit ≈ 240.463
alpha_inv         ≈ 136.760142
```

This is approximately `0.20%` below the measured value and is retained as a baseline bridge-audit result.

---

## Non-Circularity Guarantees

Across the audit cases:

1. **K is alpha-free.**  
   The interaction constant is:

   ```text
   K = 1 / (60*pi^2)
   ```

   It is constructed without using alpha or `g`.

2. **The closure formula is non-circular.**  
   `alpha_from_scale.py` computes `alpha_inv` from a supplied Scale.  
   `derive_scale_alpha_relational.py` computes `Scale_alpha,pred` and `alpha_inv_pred` before using `alpha_inv_obs` for comparison.

3. **The round-trip is labeled as a round-trip.**  
   `scale_from_alpha.py` starts from measured `alpha_inv`, so it is explicitly not a prediction.

4. **Alternative constructions are tested.**  
   `alt_hypothesis_sweep.py` verifies that the Core×Scale alternative fails by many orders of magnitude.

5. **Stability is tested.**  
   `robustness_sweep.py` and `uncertainty_budget.py` verify the expected `alpha_inv ∝ Scale^2` behavior.

---

## Conditional-Theorem Status of Case A

The relational-recursion derivation is presented as a **candidate lemma** in the main paper and appendix.

It is a conditional theorem once the residual-emergence rule is accepted:

Given that each next emergence layer is the residual generated from the actually existing layer under Φ_E closure through the stable-capacity operator:

```text
S_q(A) = q*A
```

the recursion follows:

```text
A_(n+1) = (q - 1)*A_n
```

and therefore:

```text
C_rel = [2 - sqrt(6/5)]^(-1/2)
```

The remaining audit target is to derive the residual-emergence rule itself from a formal Φ_E action on a precisely defined relational-interface capacity measure, rather than stating it as the temporal-emergence principle.

---

## Frequently Asked Questions

### Q: What does “alpha-free” mean in practice?

The process did not reference the measured alpha value anywhere in the predictive path: no fitting, no seeding with alpha, and no hidden dependency.

For Case A, the predicted Scale and `alpha_inv` are computed before the script uses `alpha_inv_obs` for comparison.

For Case B, the supplied Scale must come with provenance showing it was obtained without using measured alpha.

---

### Q: Why are there three different Scale values?

Because they play different roles:

- `240.739...` is the current prediction.
- `240.705...` is the measured-alpha round-trip target.
- `240.463` is the older supplied-scale audit baseline.

They should not be interchanged.

---

### Q: What if I want to demonstrate perfect agreement with CODATA alpha?

Use:

```bash
python scale_from_alpha.py --alpha-inv 137.035999084
```

then feed the resulting Scale into:

```bash
python alpha_from_scale.py --scale <returned_scale>
```

This is a closure test, not a predictive audit.

---

### Q: Why keep the old 240.463 audit at all?

Because it still tests the bridge architecture: given an alpha-free Scale, the closure formula deterministically maps it to `alpha_inv`, and the Core×Scale alternative fails. It is useful historically and diagnostically, but it is no longer the primary prediction.

---

### Q: What proves this is not circular?

Several things together:

1. The interaction constant `K` is alpha-free.
2. The prediction script computes `Scale_alpha,pred` and `alpha_inv_pred` before comparing to measured alpha.
3. The round-trip path is clearly labeled as non-predictive.
4. Static guard scripts check the alpha-free modules for forbidden code-level identifiers.

---

### Q: My numbers differ slightly from the examples. Is that a problem?

Tiny differences can happen due to platform precision or formatting. Large differences where a close match is expected should be investigated.

---

## Troubleshooting

### ModuleNotFoundError when running a script

Ensure you are running commands **inside this folder** so Python can import the included modules.

---

### Static guard failure

Read the generated `guard.json`.

If the hit is in a docstring or comment, it may be only a token hit depending on the guard settings. AST hits indicate real code references that need removal.

---

### Unexpected large errors in `alt_hypothesis_sweep.py`

Verify the `--scale` value and the `--alpha-inv-target` you intended to test. Typos of one or two digits can cause large relative errors.

---

### Case A output differs from the README

Run:

```bash
python derive_scale_alpha_relational.py --no-json
```

Check that the script prints approximately:

```text
scale_mass       ≈ 22.5214537505
C_rel            ≈ 1.0514352631
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

If not, confirm the script file was updated correctly.

---

## Appendix — Relations Used

Golden ratio:

```text
phi = (1 + sqrt(5)) / 2
```

Mass structural scale:

```text
Scale_mass(e) = phi^(4*phi)
```

Vacuum compression factor:

```text
q = phi^(3 - D_eff) = sqrt(6/5)
```

Absolute-deficit residual:

```text
epsilon = q - 1
```

Relational correction:

```text
C_rel = 1 / sqrt(1 - epsilon)
      = [2 - sqrt(6/5)]^(-1/2)
```

Relational-recursion prediction:

```text
Scale_alpha,pred(e) = phi^(4*phi) * 2*pi*phi * C_rel
```

Electromagnetic closure:

```text
alpha_inv = Scale_alpha(e)^2 / (7.5*pi*phi^6)
```

Equivalent closure using `G_e`:

```text
G_e = phi^6 / (2*Scale_alpha(e)^2)
alpha_inv = 1 / (15*pi*G_e)
```

Inverse relation:

```text
Scale_alpha = sqrt(alpha_inv * 7.5*pi*phi^6)
```

Expected scaling:

```text
alpha_inv ∝ Scale_alpha^2
```

So a relative change `epsilon` in Scale produces approximately `2epsilon` in `alpha_inv`.

---

## What each case ultimately tells us

- **Case A, relational-recursion prediction:** The framework predicts a Thomson U(1) interface scale and corresponding alpha value from LST geometric structure.
- **Case B, supplied-scale audit:** The closure maps any alpha-free supplied Scale deterministically to `alpha_inv`.
- **Case C, round-trip closure:** The mapping is internally consistent but not predictive.
- **Case D, alternative comparison:** The inverse-area construction wins decisively over the Core×Scale competitor.
- **Case E, non-circularity guard:** No hidden alpha usage contaminates the alpha-free path.
- **Case F, uncertainty budget:** Small input uncertainties translate to appropriately sized output uncertainties.
- **Case G, robustness sweep:** The expected `alpha_inv ∝ Scale^2` scaling holds numerically.
