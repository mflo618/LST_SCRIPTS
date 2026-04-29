# How to Verify (Traceability)

These scripts are real computations, not mocks. They make no network calls and use deterministic Decimal arithmetic where precision matters.

Run commands **inside this folder**:

`2 - LST_FU_Alpha_FSC/LST_Alpha_B_Audit_Addons_v1_0/`

---

## Current primary verification path

### 1. Relational-recursion prediction

Run:

```bash
python derive_scale_alpha_relational.py --json relational_scale_prediction.json
```

Expected key outputs:

```text
scale_mass       ≈ 22.5214537505
C_rel            ≈ 1.0514352631
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

This is the current primary prediction path. It derives the Thomson U(1) relational-interface scale from LST geometric structure:

```text
Scale_alpha,pred = phi^(4*phi) * 2*pi*phi * [2 - sqrt(6/5)]^(-1/2)
```

The script compares the prediction to the observed Thomson-limit value only after the prediction has been computed.

---

### 2. Non-circularity guard for alpha-free modules

Run:

```bash
python static_guard_all.py --paths lst_sigma_em0.py g_electron.py electron_density_certificate.py density_certificate_v2.py --json guard.json
```

Expected:

```text
No AST-level banned identifier hits.
```

This checks the alpha-free construction modules. The relational prediction script may contain `alpha_inv_obs` only for post-prediction comparison; the core prediction is computed first.

---

### 3. Legacy supplied-scale bridge audit

Run:

```bash
python scale_from_independent_inputs.py --from-json independent_scale.sample.json --json scale_manifest.json
python alpha_from_scale.py --scale 240.463 --json alpha_from_scale_legacy.json
```

Expected:

```text
alpha_inv ≈ 136.760142
```

This is the historical supplied-scale baseline. It verifies the bridge architecture but is no longer the primary prediction.

---

### 4. Current predicted-scale bridge audit

Run:

```bash
python alpha_from_scale.py --scale 240.739008512 --json alpha_from_scale_pred.json
```

Expected:

```text
alpha_inv ≈ 137.074274991
```

This verifies that the closure formula reproduces the relational-recursion prediction when the predicted Scale is supplied directly.

---

### 5. Round-trip closure sanity check

Run:

```bash
python scale_from_alpha.py --alpha-inv 137.035999084 --json scale_from_alpha.json
```

Expected:

```text
Scale_alpha,target ≈ 240.705394812
```

This is not a prediction. It is the Scale implied by the measured fine-structure constant under the closure equation.

---

### 6. Alternative-hypothesis comparison

Run both the current-prediction and legacy-baseline comparisons:

```bash
python alt_hypothesis_sweep.py --alpha-inv-target 137.035999084 --scale 240.739008512 --json alt_pred.json
python alt_hypothesis_sweep.py --alpha-inv-target 137.035999084 --scale 240.463 --json alt_legacy.json
```

Expected:

- The inverse-area / relational-capacity construction lands near the target.
- The Core×Scale construction misses by many orders of magnitude.

---

### 7. Robustness sweep

Run:

```bash
python robustness_sweep.py --scale 240.739008512 --rel-span 0.05 --points 9 --json sweep_pred.json
python robustness_sweep.py --scale 240.463 --rel-span 0.05 --points 9 --json sweep_legacy.json
```

Expected:

```text
log-log slope ≈ 2
```

because:

```text
alpha_inv ∝ Scale^2
```

---

### 8. Uncertainty budget

Run:

```bash
python uncertainty_budget.py --scale 240.739008512 --dscale 1e-3 --json ub_pred.json
python uncertainty_budget.py --scale 240.463 --dscale 1e-3 --json ub_legacy.json
```

Expected:

- A nominal `alpha_inv`.
- Partial derivatives such as `da_dscale`.
- Absolute and relative propagated uncertainty.

---

## Three Scale values to keep distinct

| Symbol | Value | Role |
|---|---:|---|
| `Scale_alpha,pred` | `≈ 240.739008512` | Current relational-recursion prediction |
| `Scale_alpha,target` | `≈ 240.705394812` | Round-trip from measured alpha, not a prediction |
| `Scale_alpha,audit` | `≈ 240.463` | Historical supplied-scale audit baseline |

---

## Traceability notes

- `derive_scale_alpha_relational.py` is the current primary prediction script.
- `alpha_from_scale.py --scale 240.463` is retained as a legacy bridge-architecture baseline.
- `scale_from_alpha.py --alpha-inv 137.035999084` is a round-trip inversion check, not a prediction.
- `static_guard_all.py` checks the alpha-free modules for code-level circularity.
- `alt_hypothesis_sweep.py` checks that the Core×Scale alternative fails decisively.

---

## Checksums and manifest

If `CHECKSUMS.txt` and `MANIFEST.json` have been regenerated after these edits, check them for file hashes and sizes.

If they have **not** been regenerated, do not treat old checksum entries as authoritative for newly edited files.
