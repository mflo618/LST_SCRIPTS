# LST Computational Tools

This repository contains computational tools, reference implementations, and audit packs for the Light-Space Theory (LST) framework.

The repo is organized so that skeptical readers can either follow the theory in paper order or jump directly into the most compact numerical audit.

---

## Start Here

There are two recommended ways to verify the computational artifacts.

### A) Theory-first path

Run the folders in this order:

```text
1 → 2 → 3
```

1. **GRC / Phi-Gram**  
   Reproduce the geometric/dynamic selector and the SU(3) vs SU(4) separation.

2. **Alpha/FSC**  
   Audit the fine-structure constant closure, including the current relational-recursion prediction for the Thomson U(1) interface scale.

3. **FU ProofPack v3**  
   Run the bridge/β checks and Mass→CKM flavor checkpoint.

---

### B) Quick trust bootstrap

Start with:

```text
2 - LST_FU_Alpha_FSC/LST_Alpha_B_Audit_Addons_v1_1_verified/
```

This is the current verified Alpha/FSC audit pack. It contains the most compact calculator-safe test of the electromagnetic-sector claim.

Expected headline output:

```text
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

Observed Thomson-limit comparison:

```text
alpha_obs^-1 ≈ 137.035999084
```

Relative deviation:

```text
≈ +0.0279%
```

---

## Repo Layout

```text
/1 - LST_GRC_Phi_Gram/
    README.md
    phi_gram_ref.py
    mapping_demo.py
    ...

/2 - LST_FU_Alpha_FSC/
    LST_Alpha_A_ProofPack_v1_4_0/
        Researcher/developer proof pack for core alpha derivations.

    LST_Alpha_B_Audit_Addons_v1_1_verified/
        Current verified auditor pack.
        Use this folder first for the Alpha/FSC audit.

    LST_Alpha_B_Audit_Addons_v1_0/
        Legacy audit pack.
        Preserved for timestamp/history and comparison.

    README_AUDIT.md
    HOW_TO_VERIFY.md
    RUN_AUDIT_SUITE.sh
    MANIFEST.json
    CHECKSUMS.txt

/3 - LST_FU_ProofPack_A_v3/
    README.md
    run_doc_style.sh
    evolve.py
    mass_engine.py
    toggles.yaml
    ...

/README.md
/LICENSE
```

---

# 1 — LST_GRC_Phi_Gram

## What this checks

This folder reproduces the geometric resonance filter and dynamic stability selector.

Representative outcome:

```text
SU(2) / (4,5): Pass
SU(3) / (5,6): Pass
SU(4) / (6,7): static deep but dynamic fail
```

The important distinction is that SU(4) may show a deep static alignment, but it fails the dynamic stability criterion. This separates “a coherent-looking static state exists” from “the state is dynamically accessible/stable.”

## Example commands

```bash
# SU(2): harmonics (4,5) → Pass
python phi_gram_ref.py --harmonics 4,5 --group su3 --cesaro-start-T --check-dynamics

# SU(3): harmonics (5,6) → Pass
python phi_gram_ref.py --harmonics 5,6 --group su3 --cesaro-start-T --check-dynamics

# SU(4): harmonics (6,7) → dynamic Fail
python phi_gram_ref.py --harmonics 6,7 --group su3 --cesaro-start-T --check-dynamics
```

## Representative signatures

```text
SU(2), (4,5):
rel_min ≈ 1.09e-02
convergence_rate ≈ 8.69e-11
Result: Coherent / Pass

SU(3), (5,6):
rel_min ≈ 2.09e-02
convergence_rate ≈ 1.56e-10
Result: Coherent / Pass

SU(4), (6,7):
rel_min ≈ 7.08e-05
convergence_rate ≈ 4.75e-10
Result: Static deep, dynamic Fail
```

## Why this matters

This is the geometric/dynamic selector that supports the SU(3) over SU(4) separation used elsewhere in the LST framework.

---

# 2 — LST_FU_Alpha_FSC

## Current verified audit pack

Use:

```text
2 - LST_FU_Alpha_FSC/LST_Alpha_B_Audit_Addons_v1_1_verified/
```

This is the current verified Alpha/FSC auditor pack.

It supersedes the older `LST_Alpha_B_Audit_Addons_v1_0` workflow as the primary place to start, while preserving the older pack as historical baseline material.

---

## What this checks

The Alpha/FSC audit checks the electromagnetic-sector closure for the fine-structure constant at the Thomson limit.

The closure equation is:

```text
alpha_inv = Scale_alpha(e)^2 / (7.5 * pi * phi^6)
```

The current primary derivation predicts the Thomson U(1) relational-interface scale:

```text
Scale_alpha,pred(e)
  = phi^(4*phi) * 2*pi*phi * [2 - sqrt(6/5)]^(-1/2)
```

Expected output:

```text
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

Observed comparison:

```text
alpha_obs^-1 ≈ 137.035999084
```

Relative deviation:

```text
≈ +0.0279%
```

---

## Main Alpha/FSC commands

Run commands inside:

```text
2 - LST_FU_Alpha_FSC/LST_Alpha_B_Audit_Addons_v1_1_verified/
```

### Case A — Current relational-recursion prediction

```bash
python derive_scale_alpha_relational.py --json relational_scale_prediction.json
```

Expected key values:

```text
scale_mass       ≈ 22.5214537505
C_rel            ≈ 1.0514352631
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

This is the current primary prediction path.

---

### Case B — Round-trip closure reference

```bash
python scale_from_alpha.py --alpha-inv 137.035999084
```

Expected:

```text
Scale_alpha,target ≈ 240.705394812
```

This is not a prediction. It is the scale value implied by the measured fine-structure constant under the closure equation.

---

### Case C — Legacy supplied-scale audit baseline

```bash
python alpha_from_scale.py --scale 240.463
```

Expected:

```text
alpha_inv ≈ 136.760142
```

This is the older supplied-scale bridge audit. It is retained for historical continuity and for testing the bridge architecture, but it is no longer the framework’s primary Alpha/FSC prediction.

---

### Case D — Non-circularity guard

```bash
python static_guard_all.py --paths lst_sigma_em0.py g_electron.py electron_density_certificate.py density_certificate_v2.py --json guard.json
```

Expected:

```text
No AST-level banned identifier hits.
```

This checks the alpha-free construction modules. In the relational prediction script, `alpha_inv_obs` appears only in the post-prediction comparison block.

---

## Three Alpha/FSC scale values

The audit distinguishes three scale values:

| Symbol | Value | Role |
|---|---:|---|
| `Scale_alpha,pred` | `≈ 240.739008512` | Current relational-recursion prediction |
| `Scale_alpha,target` | `≈ 240.705394812` | Round-trip from measured alpha; not a prediction |
| `Scale_alpha,audit` | `≈ 240.463` | Historical supplied-scale audit baseline |

This distinction prevents the older `240.463` supplied-scale workflow from being confused with the current relational-recursion prediction.

---

## What the verified Alpha/FSC pack establishes

The verified Alpha/FSC audit pack provides:

- calculator-safe arithmetic for the relational-recursion prediction,
- non-circular closure arithmetic,
- a clear distinction between prediction, round-trip target, and historical baseline,
- a branch comparison against the relative-deficit alternative,
- static checks for hidden alpha usage in alpha-free modules,
- robustness and uncertainty scripts for the closure formula.

The current primary claim is **not** that `240.463` is the final predicted Thomson scale. The current primary claim is:

```text
Scale_alpha,pred ≈ 240.739008512
alpha_inv_pred   ≈ 137.074274991
```

---

# 3 — LST_FU_ProofPack_A_v3

## What this checks

This folder contains broader framework checks, including:

- **Bridge / β runner**  
  Uses convergence rates from the GRC/Phi-Gram work to form a one-loop dynamic discriminant.

- **Mass → CKM runner**  
  Provides a one-run flavor checkpoint with documented band checks.

## Example commands

```bash
# Bridge / beta runner
python evolve.py --inputs inputs/alphas_MZ.json --scheme inputs/scheme.json --targets targets

# Flavor runner
python mass_engine.py --config toggles.yaml

# Batch runner
bash run_doc_style.sh
```

---

# Suggested Verification Order

For a skeptical reader:

1. Start with the current verified Alpha/FSC pack:

   ```text
   2 - LST_FU_Alpha_FSC/LST_Alpha_B_Audit_Addons_v1_1_verified/
   ```

   Run:

   ```bash
   python derive_scale_alpha_relational.py --json relational_scale_prediction.json
   ```

2. Then run the GRC/Phi-Gram selector:

   ```text
   1 - LST_GRC_Phi_Gram/
   ```

3. Then run the broader FU proof pack:

   ```text
   3 - LST_FU_ProofPack_A_v3/
   ```

This order gives a quick numerical trust bootstrap first, then the geometric selector, then the broader framework checks.

---

# About

These scripts are computational certificates and reference implementations for the Light-Space Theory framework. They are intended to make the numerical and algebraic claims inspectable, reproducible, and falsifiable.

For full theoretical context, paper drafts, and surrounding discussion, see the Light-Space Theory materials associated with mflo.life.

---

# Requirements

Most scripts use standard Python.

General baseline:

```text
Python 3.8+
```

Some folders may require:

```text
NumPy
```

Install if needed:

```bash
pip install numpy
```

Specific folders may include their own README or verification notes. Follow the folder-local instructions when they differ from this root overview.

---

# License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

You are free to run, study, share, and modify this software. If you distribute a modified version, you must also share your modifications under the same GPLv3 license.

The full text of the license is available in the `LICENSE` file.

---

# Contact

For more information on the theoretical framework, visit:

```text
https://mflo.life
```
