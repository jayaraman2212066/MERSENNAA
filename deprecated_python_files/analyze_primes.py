#!/usr/bin/env python3
import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from typing import Generator, Iterable, List, Optional, Tuple


PRIMELISTS_DIR = os.path.join(os.path.dirname(__file__), "primelists")


def iter_prime_files(base_dir: str) -> List[str]:
	"""Return list of prime list files in ascending numeric order.

	Includes small text lists and shards under `100000primes`.
	"""
	files: List[str] = []
	# Small lists
	for name in ("100primes.txt", "smallprimes.txt", "someprimes.txt"):
		path = os.path.join(base_dir, name)
		if os.path.isfile(path):
			files.append(path)
	# Sharded lists
	shard_dir = os.path.join(base_dir, "100000primes")
	if os.path.isdir(shard_dir):
		shards = []
		pattern = re.compile(r"^primes\.(\d{4})$")
		for entry in os.listdir(shard_dir):
			m = pattern.match(entry)
			if m:
				shards.append((int(m.group(1)), os.path.join(shard_dir, entry)))
			# ignore everything else (including .git)
		shards.sort(key=lambda x: x[0])
		files.extend([p for _, p in shards])
	return files


def iter_primes_from_file(path: str) -> Generator[int, None, None]:
	with open(path, "r", encoding="utf-8", errors="ignore") as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			# some files may have space separated primes per line; handle robustly
			for token in line.split():
				if token.isdigit():
					yield int(token)
				else:
					# defensive: remove stray characters (commas, etc.)
					clean = re.sub(r"[^0-9]", "", token)
					if clean:
						yield int(clean)


@dataclass
class GapStats:
	count: int = 0
	max_gap: int = 0
	max_gap_at: int = 0
	# bucket histogram for common gaps up to a cutoff; larger grouped into ">=cutoff"
	buckets: dict = None
	cutoff: int = 100

	def __post_init__(self):
		if self.buckets is None:
			self.buckets = Counter()

	def observe(self, prev_prime: Optional[int], current_prime: int) -> None:
		if prev_prime is None:
			return
		gap = current_prime - prev_prime
		self.count += 1
		if gap > self.max_gap:
			self.max_gap = gap
			self.max_gap_at = current_prime
		bucket_key = gap if gap < self.cutoff else f">={self.cutoff}"
		self.buckets[bucket_key] += 1


@dataclass
class ResidueStats:
	modulus: int = 30
	counts: dict = None

	def __post_init__(self):
		if self.counts is None:
			self.counts = Counter()

	def observe(self, prime_value: int) -> None:
		if prime_value <= 3:
			return
		self.counts[prime_value % self.modulus] += 1


@dataclass
class Milestone:
	n_value: int
	pi_n: int
	log_n: float
	approx_n_over_log_n: float
	approx_b_adjusted: float


@dataclass
class AnalysisResult:
	total_primes: int
	max_prime: int
	first_prime: int
	gap_stats: GapStats
	residue_stats: dict
	milestones: List[Milestone]
	c_estimated_cramer: float
	b_estimated_chebyshev: float


def analyze_stream(
	file_paths: List[str],
	max_files: Optional[int],
	max_primes: Optional[int],
	residue_mod: int,
	milestone_factor: float,
	gap_bucket_cutoff: int,
) -> AnalysisResult:
	prev_prime: Optional[int] = None
	first_prime: Optional[int] = None
	count = 0
	max_prime_seen = 0
	gap_stats = GapStats(cutoff=gap_bucket_cutoff)
	res_stats = ResidueStats(modulus=residue_mod)
	milestones: List[Milestone] = []
	# dynamic fitting for b in pi(n) ~ n / (log n - b)
	b_numerator = 0.0
	b_denominator = 0.0
	next_milestone_at = 0

	processed_files = 0
	start_time = time.time()
	last_report_count = 0
	last_report_time = start_time
	for path in file_paths:
		if max_files is not None and processed_files >= max_files:
			break
		for p in iter_primes_from_file(path):
			if first_prime is None:
				first_prime = p
			count += 1
			max_prime_seen = p
			gap_stats.observe(prev_prime, p)
			res_stats.observe(p)
			prev_prime = p
			# milestone sampling at geometric growth of n
			if p >= next_milestone_at:
				ln = math.log(p)
				if ln > 1.0:
					n_over_ln = p / ln
					# accumulate terms to estimate b in least squares sense
					# minimize sum (pi - n/(ln - b))^2 approx by linearizing around b small => use heuristic fit using one-parameter projection
					# Here, use relation: pi ~ n/(ln - b) => 1/pi ~ (ln - b)/n => b ~ ln - n/pi
					b_point = ln - (p / max(count, 1))
					# weighted by 1 to keep simple and robust
					b_numerator += b_point
					b_denominator += 1.0
					b_est = b_numerator / max(b_denominator, 1e-9)
					approx_b = p / max(ln - b_est, 1e-9)
					milestones.append(
						Milestone(
							n_value=p,
							pi_n=count,
							log_n=ln,
							approx_n_over_log_n=n_over_ln,
							approx_b_adjusted=approx_b,
						)
					)
					next_milestone_at = int(max(2, p * milestone_factor))
			# progress reporting
			if count % 100000 == 0:
				now = time.time()
				elapsed = now - start_time
				ince = count - last_report_count
				ince_time = now - last_report_time
				rate = (ince / ince_time) if ince_time > 0 else 0.0
				eta = (max_primes - count) / rate if (rate > 0 and max_primes and count < max_primes) else float('nan')
				print(f"progress primes={count} max={max_prime_seen} rate={rate:.0f}/s elapsed={elapsed:.0f}s eta={eta:.0f}s")
				last_report_count = count
				last_report_time = now
			if max_primes is not None and count >= max_primes:
				break
		if max_primes is not None and count >= max_primes:
			break
		processed_files += 1
		# file-level progress
		print(f"processed_files={processed_files} last_file={os.path.basename(path)} total_primes_so_far={count}")

	# Estimate Cramér model constant c from final max gap
	c_est = 0.0
	if max_prime_seen > 0:
		lnn2 = math.log(max_prime_seen) ** 2
		if lnn2 > 0:
			c_est = gap_stats.max_gap / lnn2

	# Estimate b using accumulated average
	b_est = (b_numerator / b_denominator) if b_denominator > 0 else 1.0

	return AnalysisResult(
		total_primes=count,
		max_prime=max_prime_seen,
		first_prime=first_prime or 0,
		gap_stats=gap_stats,
		residue_stats=dict(res_stats.counts),
		milestones=milestones,
		c_estimated_cramer=c_est,
		b_estimated_chebyshev=b_est,
	)


def write_outputs(result: AnalysisResult, output_dir: str, write_formulas: bool) -> None:
	os.makedirs(output_dir, exist_ok=True)
	# JSON summary
	summary_path = os.path.join(output_dir, "summary.json")
	with open(summary_path, "w", encoding="utf-8") as f:
		json.dump(
			{
				"total_primes": result.total_primes,
				"max_prime": result.max_prime,
				"first_prime": result.first_prime,
				"gap_stats": {
					"count": result.gap_stats.count,
					"max_gap": result.gap_stats.max_gap,
					"max_gap_at": result.gap_stats.max_gap_at,
					"cutoff": result.gap_stats.cutoff,
					"buckets": result.gap_stats.buckets,
				},
				"residue_stats_mod": list(result.residue_stats.items()),
				"milestones": [asdict(m) for m in result.milestones],
				"c_estimated_cramer": result.c_estimated_cramer,
				"b_estimated_chebyshev": result.b_estimated_chebyshev,
			},
			f,
			indent=2,
		)

	# Formulas as markdown
	if write_formulas:
		formulas_path = os.path.join(os.path.dirname(__file__), "FORMULAS.md")
		with open(formulas_path, "w", encoding="utf-8") as f:
			f.write("## Empirical formulas from prime dataset\n\n")
			f.write("- π(n) empirical fit: π(n) ≈ n / (log n - b)\n")
			f.write(f"  where b ≈ {result.b_estimated_chebyshev:.6f}.\n\n")
			f.write("- Max gap growth: g_max(n) ≈ c · (log n)^2\n")
			f.write(f"  where c ≈ {result.c_estimated_cramer:.6f}.\n\n")
			f.write("- Residue distribution mod m (default m=30): concentrated on reduced residue classes.\n\n")
			f.write("These parameters are estimated from the provided data using streaming statistics.\n")
		print(f"Wrote formulas to {formulas_path}")
	print(f"Wrote summary to {summary_path}")


def build_arg_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description=(
			"Stream and analyze large prime lists to estimate empirical formulas and statistics."
		)
	)
	parser.add_argument(
		"--base",
		dest="base_dir",
		default=PRIMELISTS_DIR,
		help="Base directory containing prime lists (default: primelists)",
	)
	parser.add_argument(
		"--max-files",
		type=int,
		default=None,
		help="Limit number of files processed (for quick runs)",
	)
	parser.add_argument(
		"--max-primes",
		type=int,
		default=None,
		help="Limit number of primes processed (for sampling)",
	)
	parser.add_argument(
		"--residue-mod",
		type=int,
		default=30,
		help="Modulus for residue class distribution (default: 30)",
	)
	parser.add_argument(
		"--milestone-factor",
		type=float,
		default=1.05,
		help="Geometric factor for milestone sampling (default: 1.05)",
	)
	parser.add_argument(
		"--gap-bucket-cutoff",
		type=int,
		default=100,
		help="Gap histogram buckets up to this value; larger grouped together",
	)
	parser.add_argument(
		"--output-dir",
		default=os.path.join(os.path.dirname(__file__), "analysis"),
		help="Directory to write outputs (summary.json)",
	)
	parser.add_argument(
		"--write-formulas",
		action="store_true",
		help="Also write/update FORMULAS.md at project root",
	)
	return parser


def main(argv: Optional[List[str]] = None) -> int:
	args = build_arg_parser().parse_args(argv)
	base_dir = os.path.abspath(args.base_dir)
	if not os.path.isdir(base_dir):
		print(f"Base directory not found: {base_dir}", file=sys.stderr)
		return 2
	files = iter_prime_files(base_dir)
	if not files:
		print(f"No prime files found under {base_dir}", file=sys.stderr)
		return 3
	result = analyze_stream(
		file_paths=files,
		max_files=args.max_files,
		max_primes=args.max_primes,
		residue_mod=args.residue_mod,
		milestone_factor=args.milestone_factor,
		gap_bucket_cutoff=args.gap_bucket_cutoff,
	)
	write_outputs(result, args.output_dir, args.write_formulas)
	# Print brief console summary
	print(
		f"total={result.total_primes} max={result.max_prime} max_gap={result.gap_stats.max_gap} c~{result.c_estimated_cramer:.4f} b~{result.b_estimated_chebyshev:.4f}"
	)
	return 0


if __name__ == "__main__":
	sys.exit(main())


