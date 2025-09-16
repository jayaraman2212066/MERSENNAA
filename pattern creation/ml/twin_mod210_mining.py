#!/usr/bin/env python3
import argparse
import json
import os
import re
from collections import Counter


PRIMELISTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "primelists")


def iter_prime_files(base_dir: str):
	files = []
	for name in ("100primes.txt", "smallprimes.txt", "someprimes.txt"):
		p = os.path.join(base_dir, name)
		if os.path.isfile(p):
			files.append(p)
	shard_dir = os.path.join(base_dir, "100000primes")
	if os.path.isdir(shard_dir):
		pattern = re.compile(r"^primes\.(\d{4})$")
		shards = []
		for entry in os.listdir(shard_dir):
			m = pattern.match(entry)
			if m:
				shards.append((int(m.group(1)), os.path.join(shard_dir, entry)))
		shards.sort(key=lambda x: x[0])
		files.extend([p for _, p in shards])
	return files


def iter_primes_from_file(path: str):
	with open(path, "r", encoding="utf-8", errors="ignore") as f:
		for line in f:
			for token in line.strip().split():
				if token.isdigit():
					yield int(token)


def main():
	parser = argparse.ArgumentParser(description="Twin primes and residue mod 210 mining")
	parser.add_argument("--base", default=PRIMELISTS_DIR)
	parser.add_argument("--max-files", type=int, default=None)
	parser.add_argument("--out", default=os.path.join("analysis_full", "twin_mod210.json"))
	args = parser.parse_args()

	files = iter_prime_files(args.base)
	if args.max_files:
		files = files[: args.max_files]

	prev = None
	count = 0
	twin_count = 0
	mod210 = Counter()
	checkpoints = [10**k for k in range(2, 11)]  # up to 1e10
	checkpoint_idx = 0
	progress = []  # list of {n, pi, twin}

	for fp in files:
		for p in iter_primes_from_file(fp):
			count += 1
			if p > 3:
				mod210[p % 210] += 1
			if prev is not None and p - prev == 2:
				twin_count += 1
			prev = p
			# record progress at checkpoints of p
			while checkpoint_idx < len(checkpoints) and p >= checkpoints[checkpoint_idx]:
				progress.append({"n": checkpoints[checkpoint_idx], "pi": count, "twin": twin_count})
				checkpoint_idx += 1

	# write results
	os.makedirs(os.path.dirname(args.out), exist_ok=True)
	with open(args.out, "w", encoding="utf-8") as f:
		json.dump({
			"total_primes": count,
			"twin_primes": twin_count,
			"mod210": mod210,
			"progress": progress,
		}, f, indent=2)
	print(f"Wrote {args.out}")


if __name__ == "__main__":
	main()


