#!/usr/bin/env python3
import argparse
import os
import re
from collections import Counter
from typing import List


PRIMELISTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "primelists")


def iter_prime_files(base_dir: str) -> List[str]:
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
	parser = argparse.ArgumentParser(description="Pattern mining on prime lists")
	parser.add_argument("--base", default=PRIMELISTS_DIR)
	parser.add_argument("--max-files", type=int, default=5)
	parser.add_argument("--residue-mod", type=int, default=30)
	args = parser.parse_args()

	files = iter_prime_files(args.base)
	files = files[: args.max_files] if args.max_files else files
	resid = Counter()
	gaps = Counter()
	prev = None
	for fp in files:
		for p in iter_primes_from_file(fp):
			if p > 3:
				resid[p % args.residue_mod] += 1
			if prev is not None:
				g = p - prev
				gaps[g if g < 100 else ">=100"] += 1
			prev = p
	print("top residues:", resid.most_common(10))
	print("top gaps:", gaps.most_common(10))


if __name__ == "__main__":
	main()


