#!/usr/bin/env python3
"""
Generate a proof PNG from Prime95 (GIMPS) results.txt confirmations.

- Parses lines like: "M( 82589933 ) is prime!"
- Captures nearby context (timestamp lines and residue/hash lines if present)
- Renders a clean PNG summary suitable as a shareable proof artifact

Usage:
  python generate_proof_png.py --results C:/Prime95/results.txt --out proofs/mersenne_proof.png
"""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import json


CONFIRM_RE = re.compile(r"M\(\s*(\d+)\s*\)\s+is\s+prime", re.IGNORECASE)


def parse_confirmations(results_path: str, context_lines: int = 2) -> List[Tuple[int, List[str]]]:
    """
    Return a list of tuples: (exponent, context) for each confirmation found.
    Context contains up to `context_lines` lines before and after the match.
    """
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"results.txt not found at: {results_path}")

    with open(results_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [ln.rstrip("\n") for ln in f]

    confirmations: List[Tuple[int, List[str]]] = []
    for idx, line in enumerate(lines):
        m = CONFIRM_RE.search(line)
        if not m:
            continue
        p = int(m.group(1))
        start = max(0, idx - context_lines)
        end = min(len(lines), idx + context_lines + 1)
        ctx = lines[start:end]
        confirmations.append((p, ctx))
    return confirmations


def _format_int_with_commas(n: int) -> str:
    return f"{n:,}"


def render_proof_png(confirmations: List[Tuple[int, List[str]]], out_path: str, times: dict | None = None) -> str:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    title = "GIMPS / Prime95 Confirmations"
    subtitle = datetime.now().strftime("Generated on %Y-%m-%d %H:%M:%S")

    # Conservative spacing to avoid overlap across renderers
    per_item_height = 0.9  # inches per confirmation
    fig_height = max(4.0, 2.2 + per_item_height * max(1, len(confirmations)))
    fig = plt.figure(figsize=(14, fig_height))
    fig.patch.set_facecolor("#0f0f23")
    ax = plt.gca()
    ax.axis("off")

    y = 0.96
    plt.text(0.02, y, title, transform=ax.transAxes, fontsize=22, fontweight="bold", color="#00d4ff")
    y -= 0.06
    plt.text(0.02, y, subtitle, transform=ax.transAxes, fontsize=12, color="#b8c6db")
    y -= 0.04

    if not confirmations:
        plt.text(0.02, y, "No confirmations found in results.txt", transform=ax.transAxes, fontsize=14, color="#ff6b6b")
    else:
        for i, (p, _ctx) in enumerate(confirmations, 1):
            y -= 0.07
            plt.text(0.02, y, f"#{i}  M({p:,}) is prime!", transform=ax.transAxes, fontsize=18, fontweight="bold", color="#00ff88", family="DejaVu Sans Mono")
            # For moderately small exponents, include explicit value 2^p - 1
            if p <= 128:
                value = (1 << p) - 1
                y -= 0.045
                detail = f"2^{p} - 1 = {_format_int_with_commas(value)}"
                # If benchmark times provided, include them
                if times:
                    t = times.get(str(p)) or times.get(p)
                    if t is not None:
                        # present as ms if < 1s
                        if t < 1.0:
                            t_str = f"{t*1000:.1f} ms"
                        else:
                            t_str = f"{t:.3f} s"
                        detail += f"   |   LL time (your Acer A5): {t_str}"
                plt.text(0.045, y, detail, transform=ax.transAxes, fontsize=12, color="#b8c6db", family="DejaVu Sans Mono")
            y -= 0.01

    plt.tight_layout(rect=(0, 0, 1, 1))
    plt.savefig(out_path, dpi=160, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a proof PNG from Prime95 results.txt")
    parser.add_argument("--results", default="C:/Prime95/results.txt", help="Path to Prime95 results.txt")
    parser.add_argument("--out", default="proofs/mersenne_proof.png", help="Output PNG path")
    parser.add_argument("--times", default=None, help="Optional JSON mapping of exponent->seconds for displaying local LL timings")
    args = parser.parse_args()

    confirmations = parse_confirmations(args.results)
    times = None
    if args.times and os.path.exists(args.times):
        try:
            with open(args.times, "r", encoding="utf-8") as f:
                times = json.load(f)
        except Exception:
            times = None
    out_file = render_proof_png(confirmations, args.out, times=times)
    print(f"✅ Proof PNG written to: {out_file}")
    if confirmations:
        print(f"   Included {len(confirmations)} confirmation(s)")
    else:
        print("   Note: No confirmations were found — is Prime95 finished?")


if __name__ == "__main__":
    main()


