#!/usr/bin/env python3
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
	parser = argparse.ArgumentParser(description="Plot twin prime density and mod210 residues")
	parser.add_argument("--input", default=os.path.join("analysis_full", "twin_mod210.json"))
	parser.add_argument("--outdir", default=os.path.join("analysis_full", "charts"))
	args = parser.parse_args()

	with open(args.input, "r", encoding="utf-8") as f:
		data = json.load(f)
	os.makedirs(args.outdir, exist_ok=True)

	# Twin density over checkpoints
	progress = data.get("progress", [])
	if progress:
		x = [p["n"] for p in progress]
		pi = [p["pi"] for p in progress]
		twins = [p["twin"] for p in progress]
		density = [twins[i] / pi[i] if pi[i] else 0 for i in range(len(pi))]
		plt.figure(figsize=(8, 4))
		plt.plot(x, density)
		plt.xscale('log')
		plt.title("Twin prime density (twins / π(n))")
		plt.xlabel("n")
		plt.ylabel("density")
		plt.tight_layout()
		plt.savefig(os.path.join(args.outdir, "twin_density.png"))
		plt.close()

	# Residues mod 210 (bar for reduced classes > 0)
	mod210 = data.get("mod210", {})
	if mod210:
		items = sorted(((int(k), v) for k, v in mod210.items()), key=lambda t: t[0])
		xs = [k for k, _ in items]
		vals = [v for _, v in items]
		plt.figure(figsize=(12, 4))
		plt.bar(range(len(xs)), vals)
		plt.xticks(range(len(xs)), [str(k) for k in xs], rotation=90)
		plt.title("Residue counts mod 210")
		plt.tight_layout()
		plt.savefig(os.path.join(args.outdir, "residues_mod210.png"))
		plt.close()

	print(f"Charts written to {args.outdir}")


if __name__ == "__main__":
	main()


