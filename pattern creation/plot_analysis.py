#!/usr/bin/env python3
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
	parser = argparse.ArgumentParser(description="Plot charts from analysis summary.json")
	parser.add_argument("--summary", default=os.path.join("analysis_full", "summary.json"))
	parser.add_argument("--outdir", default=os.path.join("analysis_full", "charts"))
	args = parser.parse_args()

	with open(args.summary, "r", encoding="utf-8") as f:
		data = json.load(f)
	os.makedirs(args.outdir, exist_ok=True)

	# 1) Gap histogram (bucketed)
	buckets = data["gap_stats"]["buckets"]
	labels = []
	values = []
	for k, v in buckets.items():
		labels.append(str(k))
		values.append(v)
	plt.figure(figsize=(12, 4))
	plt.bar(range(len(values)), values)
	plt.xticks(range(len(labels)), labels, rotation=90)
	plt.title("Prime gap histogram (bucketed)")
	plt.tight_layout()
	plt.savefig(os.path.join(args.outdir, "gaps_hist.png"))
	plt.close()

	# 2) Residue distribution mod m
	res_mod = data.get("residue_stats_mod", [])
	if res_mod:
		res_labels = [str(k) for k, _ in res_mod]
		res_vals = [v for _, v in res_mod]
		plt.figure(figsize=(10, 4))
		plt.bar(range(len(res_vals)), res_vals)
		plt.xticks(range(len(res_vals)), res_labels, rotation=90)
		plt.title("Residue counts (mod m)")
		plt.tight_layout()
		plt.savefig(os.path.join(args.outdir, "residues_mod.png"))
		plt.close()

		# Pie chart of top residues
		pairs = list(zip(res_labels, res_vals))
		pairs.sort(key=lambda t: t[1], reverse=True)
		top = pairs[:10]
		labels_pie = [p[0] for p in top]
		vals_pie = [p[1] for p in top]
		plt.figure(figsize=(6, 6))
		plt.pie(vals_pie, labels=labels_pie, autopct='%1.1f%%', startangle=90)
		plt.axis('equal')
		plt.title("Top residues (mod m)")
		plt.savefig(os.path.join(args.outdir, "residues_pie.png"))
		plt.close()

	# 3) Milestones: pi(n) vs n/log n and adjusted fit
	milestones = data.get("milestones", [])
	if milestones:
		ns = [m["n_value"] for m in milestones]
		pi_ns = [m["pi_n"] for m in milestones]
		n_over_log = [m["approx_n_over_log_n"] for m in milestones]
		adj = [m["approx_b_adjusted"] for m in milestones]
		plt.figure(figsize=(10, 5))
		plt.plot(ns, pi_ns, label="pi(n)")
		plt.plot(ns, n_over_log, label="n/log n")
		plt.plot(ns, adj, label="n/(log n - b)")
		plt.xscale("log")
		plt.yscale("log")
		plt.legend()
		plt.title("Milestones: counts vs approximations")
		plt.tight_layout()
		plt.savefig(os.path.join(args.outdir, "milestones.png"))
		plt.close()

		# Estimated b trend over milestones: b(n) = log n - n/pi(n)
		import math
		b_trend_x = []
		b_trend_y = []
		for m in milestones:
			if m["pi_n"] > 0 and m["n_value"] > 1:
				b_trend_x.append(m["n_value"])
				b_trend_y.append(math.log(m["n_value"]) - (m["n_value"] / m["pi_n"]))
		plt.figure(figsize=(10, 4))
		plt.plot(b_trend_x, b_trend_y)
		plt.xscale("log")
		plt.title("Estimated b(n) = log n - n/pi(n)")
		plt.xlabel("n")
		plt.ylabel("b(n)")
		plt.tight_layout()
		plt.savefig(os.path.join(args.outdir, "b_trend.png"))
		plt.close()

	# 4) Text summary figure
	fig = plt.figure(figsize=(8, 4))
	fig.text(0.01, 0.8, f"total_primes: {data['total_primes']}")
	fig.text(0.01, 0.65, f"max_prime: {data['max_prime']}")
	fig.text(0.01, 0.5, f"max_gap: {data['gap_stats']['max_gap']}")
	fig.text(0.01, 0.35, f"c_est cramer: {data['c_estimated_cramer']:.6f}")
	fig.text(0.01, 0.2, f"b_est chebyshev: {data['b_estimated_chebyshev']:.6f}")
	plt.axis('off')
	plt.savefig(os.path.join(args.outdir, "summary_text.png"))
	plt.close()

	# 5) Gap histogram with log-scale y
	plt.figure(figsize=(12, 4))
	plt.bar(range(len(values)), values)
	plt.xticks(range(len(labels)), labels, rotation=90)
	plt.yscale('log')
	plt.title("Prime gap histogram (log y)")
	plt.tight_layout()
	plt.savefig(os.path.join(args.outdir, "gaps_hist_log.png"))
	plt.close()

	# 6) Max gap overlay vs (log n)^2 (approx using milestones)
	import math
	if milestones:
		xs = [m["n_value"] for m in milestones]
		log2 = [math.log(x) ** 2 for x in xs]
		# scale (log n)^2 by fitted c
		c = data.get("c_estimated_cramer", 1.0)
		overlay = [c * v for v in log2]
		plt.figure(figsize=(10, 4))
		plt.plot(xs, overlay, label="c (log n)^2")
		plt.xscale('log')
		plt.yscale('log')
		plt.title("Overlay: c (log n)^2 (reference scale)")
		plt.legend()
		plt.tight_layout()
		plt.savefig(os.path.join(args.outdir, "gap_overlay_log2.png"))
		plt.close()

	print(f"Charts written to {args.outdir}")


if __name__ == "__main__":
	main()


