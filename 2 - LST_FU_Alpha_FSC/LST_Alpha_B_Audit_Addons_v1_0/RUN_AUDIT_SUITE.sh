#!/usr/bin/env bash
set -euo pipefail

ALPHA_INV_OBS="137.035999084"
PRED_SCALE="240.739008512"
LEGACY_SCALE="240.463"

echo "=== Case A: Relational-recursion prediction, current primary ==="
python derive_scale_alpha_relational.py --alpha-inv-obs "$ALPHA_INV_OBS" --json relational_scale_prediction.json

echo
echo "=== Non-circularity guard for alpha-free modules ==="
python static_guard_all.py --paths lst_sigma_em0.py g_electron.py electron_density_certificate.py density_certificate_v2.py --json guard.json

echo
echo "=== Case B: Legacy supplied-scale bridge audit ==="
python scale_from_independent_inputs.py --from-json independent_scale.sample.json --json scale_manifest.json
python alpha_from_scale.py --scale "$LEGACY_SCALE" --json alpha_from_scale_legacy.json

echo
echo "=== Current predicted-scale bridge audit ==="
python alpha_from_scale.py --scale "$PRED_SCALE" --json alpha_from_scale_pred.json

echo
echo "=== Case C: Round-trip closure sanity check ==="
python scale_from_alpha.py --alpha-inv "$ALPHA_INV_OBS" --json scale_from_alpha.json

echo
echo "=== Case D: Alternative-hypothesis comparison ==="
python alt_hypothesis_sweep.py --alpha-inv-target "$ALPHA_INV_OBS" --scale "$PRED_SCALE" --json alt_pred.json
python alt_hypothesis_sweep.py --alpha-inv-target "$ALPHA_INV_OBS" --scale "$LEGACY_SCALE" --json alt_legacy.json

echo
echo "=== Case G: Robustness sweeps ==="
python robustness_sweep.py --scale "$PRED_SCALE" --rel-span 0.05 --points 9 --json sweep_pred.json
python robustness_sweep.py --scale "$LEGACY_SCALE" --rel-span 0.05 --points 9 --json sweep_legacy.json

echo
echo "=== Case F: Uncertainty budgets ==="
python uncertainty_budget.py --scale "$PRED_SCALE" --dscale 1e-3 --json ub_pred.json
python uncertainty_budget.py --scale "$LEGACY_SCALE" --dscale 1e-3 --json ub_legacy.json

echo
echo "=== Audit suite complete ==="
echo "Primary prediction: Scale_alpha,pred ≈ $PRED_SCALE, alpha_inv_pred ≈ 137.074274991"
echo "Round-trip target: Scale_alpha,target ≈ 240.705394812 from alpha_inv_obs = $ALPHA_INV_OBS"
echo "Legacy baseline: Scale_alpha,audit ≈ $LEGACY_SCALE"
