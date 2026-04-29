#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Traceability: records an alpha-free supplied Scale and its provenance.
# Real deterministic computation; no network I/O.
# -----------------------------------------------------------------------------
import argparse
import hashlib
import json
from decimal import Decimal, getcontext

getcontext().prec = 80


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(
        description="Record a supplied alpha-free Scale value and provenance."
    )
    ap.add_argument("--from-json", required=True, help="JSON file containing a 'scale' field.")
    ap.add_argument("--json", help="Optional output manifest path.")
    args = ap.parse_args()

    with open(args.from_json, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if "scale" not in payload:
        raise SystemExit("Input JSON must contain a 'scale' field.")

    scale = Decimal(str(payload["scale"]))
    report = {
        "input_file": args.from_json,
        "input_sha256": sha256_file(args.from_json),
        "scale": str(scale),
        "provenance": payload.get("provenance", ""),
        "alpha_free": payload.get("alpha_free", None),
        "status": payload.get("status", "supplied-scale audit input"),
    }

    print(json.dumps(report, indent=2))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
