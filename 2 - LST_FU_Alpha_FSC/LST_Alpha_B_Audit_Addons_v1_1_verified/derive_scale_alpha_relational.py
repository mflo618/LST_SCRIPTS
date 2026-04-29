#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# derive_scale_alpha_relational.py
#
# Relational-recursion derivation of the Thomson U(1) interface scale and
# the predicted fine-structure constant.
#
# Computes Scale_alpha,pred(e) from LST geometric structure via:
# phi^(4*phi), the U(1) cycle factor 2*pi*phi, and the upstream 6/5
# stability ratio (which fixes q = sqrt(6/5) via Theorem H.1 / Corollary H.3).
#
#   Scale_alpha,pred = phi^(4*phi) * 2*pi*phi * C_rel
#
# where C_rel is the absolute-deficit recursion correction:
#
#   q       = phi^(3 - D_eff) = sqrt(6/5)
#   epsilon = q - 1
#   C_rel   = 1 / sqrt(1 - epsilon) = [2 - sqrt(6/5)]^(-1/2)
#
# Closure formula:
#
#   alpha_inv_pred = Scale_alpha,pred^2 / (7.5 * pi * phi^6)
#
# Also emits the relative-deficit branch for comparison:
#
#   epsilon_relative = (q - 1) / q
#   C_relative       = (6/5)^(1/4)
#
# Non-circular prediction path: alpha_inv_obs is used only for comparison
# after scale_alpha_pred and alpha_inv_pred are computed. The prediction
# itself does not consume alpha or g as input.
# ---------------------------------------------------------------------------

from decimal import Decimal, getcontext
import json
import argparse
import math

getcontext().prec = 80

DECIMAL_PI = Decimal(
    "3.14159265358979323846264338327950288419716939937510"
)


def d(x):
    return Decimal(x)


def phi_dec():
    """Golden ratio at 80-digit precision."""
    return (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)


def phi_pow(phi, exponent):
    """phi^exponent for non-integer Decimal exponent.

    Decimal ln/exp can be extremely slow on some Python builds. The audit
    displays 10-12 significant digits, so we use the standard-library
    double-precision path for this single non-integer power and convert the
    result back to Decimal via repr for stable downstream arithmetic.
    """
    return Decimal(repr(math.exp(float(exponent) * math.log(float(phi)))))


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Relational-recursion derivation of Scale_alpha,pred(e) and "
            "alpha_inv_pred from LST geometric constants (phi, 2*pi, "
            "and the upstream 6/5 stability ratio)."
        )
    )
    parser.add_argument(
        "--alpha-inv-obs",
        type=str,
        default="137.035999084",
        help="Observed Thomson-limit alpha^-1 for comparison (default: CODATA value).",
    )
    parser.add_argument(
        "--json",
        type=str,
        default="relational_scale_prediction.json",
        help="Path to write JSON output (default: relational_scale_prediction.json).",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Skip JSON output.",
    )
    args = parser.parse_args()

    # ---- Core derived quantities (LST geometric constants) ----
    phi = phi_dec()
    four_phi = Decimal(4) * phi
    scale_mass = phi_pow(phi, four_phi)            # phi^(4*phi)
    six_fifths = Decimal(6) / Decimal(5)
    q = six_fifths.sqrt()                          # phi^(3 - D_eff) = sqrt(6/5)

    # ---- Absolute-deficit branch (primary prediction) ----
    epsilon_absolute = q - Decimal(1)
    one_minus_eps = Decimal(1) - epsilon_absolute  # = 2 - sqrt(6/5)
    C_absolute = Decimal(1) / one_minus_eps.sqrt()

    # ---- Relational lift ----
    two_pi_phi = Decimal(2) * DECIMAL_PI * phi
    scale_alpha_pred = scale_mass * two_pi_phi * C_absolute

    # ---- Closure formula ----
    phi6 = phi ** 6
    denom_closure = Decimal("7.5") * DECIMAL_PI * phi6
    alpha_inv_pred = (scale_alpha_pred * scale_alpha_pred) / denom_closure

    # ---- Round-trip target from observed alpha_inv ----
    alpha_inv_obs = d(args.alpha_inv_obs)
    scale_alpha_target = (denom_closure * alpha_inv_obs).sqrt()

    # ---- Errors (primary branch) ----
    rel_error_alpha_inv = (alpha_inv_pred - alpha_inv_obs) / alpha_inv_obs
    rel_error_scale = (scale_alpha_pred - scale_alpha_target) / scale_alpha_target

    # ---- Relative-deficit branch (alternative reading) ----
    epsilon_relative = (q - Decimal(1)) / q
    one_minus_eps_rel = Decimal(1) - epsilon_relative  # = 1/q = sqrt(5/6)
    C_relative = Decimal(1) / one_minus_eps_rel.sqrt()  # = q^(1/2) = (6/5)^(1/4)
    scale_alpha_relative = scale_mass * two_pi_phi * C_relative
    alpha_inv_relative = (scale_alpha_relative * scale_alpha_relative) / denom_closure
    relative_branch_error = (alpha_inv_relative - alpha_inv_obs) / alpha_inv_obs

    # Branch error ratio (how many times worse the relative branch is)
    if rel_error_alpha_inv != 0:
        branch_error_ratio = abs(relative_branch_error) / abs(rel_error_alpha_inv)
    else:
        branch_error_ratio = d("NaN")

    # ---- Display ----
    print("=== Relational-Recursion Derivation of Scale_alpha,pred(e) ===")
    print()
    print("Core quantities (phi, pi, and the upstream 6/5 stability ratio):")
    print(f"  phi                  = {phi}")
    print(f"  scale_mass = phi^(4*phi)")
    print(f"                       = {scale_mass}")
    print(f"  q = sqrt(6/5)        = {q}")
    print()
    print("Absolute-deficit branch (primary prediction):")
    print(f"  epsilon              = q - 1 = {epsilon_absolute}")
    print(f"  C_rel                = 1 / sqrt(1 - epsilon)")
    print(f"                       = {C_absolute}")
    print(f"  scale_alpha_pred     = scale_mass * 2*pi*phi * C_rel")
    print(f"                       = {scale_alpha_pred}")
    print(f"  alpha_inv_pred       = scale_alpha_pred^2 / (7.5*pi*phi^6)")
    print(f"                       = {alpha_inv_pred}")
    print()
    print("Comparison with measurement:")
    print(f"  alpha_inv_obs        = {alpha_inv_obs}")
    print(f"  scale_alpha_target   = sqrt(7.5*pi*phi^6 * alpha_inv_obs)")
    print(f"                       = {scale_alpha_target}")
    print(f"  rel_error_alpha_inv  = {rel_error_alpha_inv}  ({rel_error_alpha_inv * 100} %)")
    print(f"  rel_error_scale      = {rel_error_scale}  ({rel_error_scale * 100} %)")
    print()
    print("Relative-deficit branch (alternative reading):")
    print(f"  epsilon_relative     = (q-1)/q = {epsilon_relative}")
    print(f"  C_relative           = (6/5)^(1/4) = {C_relative}")
    print(f"  alpha_inv_relative   = {alpha_inv_relative}")
    print(f"  relative_branch_err  = {relative_branch_error}  ({relative_branch_error * 100} %)")
    print()
    print(f"Branch error ratio (|relative| / |absolute|) = {branch_error_ratio}")
    print()
    print("The temporally natural absolute-deficit branch is observationally")
    print("favored over the structurally available relative-deficit alternative")
    print(f"by approximately {branch_error_ratio:.3f}x in relative error.")
    print()

    # ---- JSON output ----
    if not args.no_json:
        payload = {
            "scale_mass": str(scale_mass),
            "q": str(q),
            "epsilon_absolute": str(epsilon_absolute),
            "C_absolute": str(C_absolute),
            "scale_alpha_pred": str(scale_alpha_pred),
            "alpha_inv_pred": str(alpha_inv_pred),
            "alpha_inv_obs": str(alpha_inv_obs),
            "rel_error_alpha_inv": str(rel_error_alpha_inv),
            "scale_alpha_target": str(scale_alpha_target),
            "rel_error_scale": str(rel_error_scale),
            "epsilon_relative": str(epsilon_relative),
            "C_relative": str(C_relative),
            "alpha_inv_relative": str(alpha_inv_relative),
            "relative_branch_error": str(relative_branch_error),
            "branch_error_ratio": str(branch_error_ratio),
        }
        with open(args.json, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote {args.json}")


if __name__ == "__main__":
    main()
