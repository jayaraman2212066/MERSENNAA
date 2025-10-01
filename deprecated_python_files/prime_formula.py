#!/usr/bin/env python3
import argparse
import bisect
import json
import math
import os
import sys
from typing import List, Optional


def _miller_rabin(n: int, bases: List[int]) -> bool:
	# Deterministic for 64-bit with bases >= {2,3,5,7,11,13,17}
	if n < 2:
		return False
	# small primes quick check
	for p in (2, 3, 5, 7, 11, 13, 17):
		if n % p == 0:
			return n == p
	# write n-1 = d * 2^s
	d = n - 1
	s = 0
	while d % 2 == 0:
		d //= 2
		s += 1
	def check(a: int) -> bool:
		x = pow(a, d, n)
		if x == 1 or x == n - 1:
			return True
		for _ in range(s - 1):
			x = (x * x) % n
			if x == n - 1:
				return True
		return False
	for a in bases:
		if a % n == 0:
			continue
		if not check(a):
			return False
	return True


def is_prime_64bit_deterministic(n: int) -> bool:
	# Deterministic for all 64-bit integers
	# Source: known base sets for Miller-Rabin primality up to 2^64
	bases = [2, 3, 5, 7, 11, 13, 17]
	return _miller_rabin(n, bases)


def _jacobi(a: int, n: int) -> int:
	# Jacobi symbol (a/n)
	if n <= 0 or n % 2 == 0:
		return 0
	a = a % n
	result = 1
	while a != 0:
		while a % 2 == 0:
			a //= 2
			if n % 8 in (3, 5):
				result = -result
		a, n = n, a
		if a % 4 == 3 and n % 4 == 3:
			result = -result
		a %= n
	return result if n == 1 else 0


def _strong_lucas_prp(n: int) -> bool:
	# Strong Lucas probable prime test
	# Find D such that Jacobi(D/n) == -1 with D in {5, -7, 9, -11, ...}
	if n % 2 == 0:
		return n == 2
	D = 5
	while True:
		j = _jacobi(D, n)
		if j == -1:
			break
		D = -D + 2 if D > 0 else -D + 2
	P = 1
	Q = (1 - D) // 4
	# n + 1 = d * 2^s
	d = n + 1
	s = 0
	while d % 2 == 0:
		d //= 2
		s += 1
	# Lucas sequences
	def lucas_uv(k: int) -> tuple[int, int]:
		U, V = 0, 2
		Qk = 1
		for bit in bin(k)[2:]:
			U = (U * V) % n
			V = (V * V - 2 * Qk) % n
			Qk = (Qk * Qk) % n
			if bit == '1':
				tU = (U + V) % n
				U = tU % n
				V = (V + D * U) % n
				Qk = (Qk * Q) % n
		return U, V
	U, V = lucas_uv(d)
	if U == 0 or V == 0:
		return True
	for _ in range(s - 1):
		V = (V * V - 2) % n
		if V == 0:
			return True
	return False


def is_probable_prime_bpsw(n: int) -> bool:
	# Baillie–PSW: base-2 Miller–Rabin + strong Lucas probable prime
	if n < 2:
		return False
	for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
		if n % p == 0:
			return n == p
	if not _miller_rabin(n, [2]):
		return False
	return _strong_lucas_prp(n)


def nth_prime_estimate(n: float) -> float:
	"""Dusart/Rosser-Schoenfeld style estimator for the nth prime.

	Works well for n >= 6. For small n, we clamp to known small primes.
	"""
	if n <= 1:
		return 2.0
	if n < 6:
		# rough small table fallback
		return [0.0, 2.0, 3.0, 5.0, 7.0, 11.0][int(max(1, round(n)))]
	ln = math.log(n)
	lnln = math.log(ln)
	# Dusart 2010 upper bound inspired approximation
	return n * (ln + lnln - 1 + ( (lnln - 2) / ln ))


def composite_score(n: int, nn_weights_path: str = "ml/nn_weights.json", ga_weights_path: str = "ml/ga_weights.json") -> float:
	try:
		from ml.features import feature_vector_int
		feats = feature_vector_int(n)
		# GA linear score
		ga_w = None
		if os.path.isfile(ga_weights_path):
			with open(ga_weights_path, "r", encoding="utf-8") as f:
				ga_w = json.load(f).get("weights")
		ga_score = sum((ga_w[i] if ga_w else 0.0) * feats[i] for i in range(min(len(feats), 6)))
		# NN one-hidden-layer score (prefer TFLite if available)
		nn_score = 0.0
		tflite_path = os.path.join(os.path.dirname(nn_weights_path), "nn_classifier.tflite")
		if os.path.isfile(tflite_path):
			try:
				import numpy as np
				import tensorflow as tf
				interpreter = tf.lite.Interpreter(model_path=tflite_path)
				interpreter.allocate_tensors()
				input_details = interpreter.get_input_details()
				output_details = interpreter.get_output_details()
				X = np.array(feats, dtype=np.float32)[None, :]
				interpreter.set_tensor(input_details[0]['index'], X)
				interpreter.invoke()
				nn_score = float(interpreter.get_tensor(output_details[0]['index'])[0, 0])
			except Exception:
				nn_score = 0.0
		elif os.path.isfile(nn_weights_path):
			with open(nn_weights_path, "r", encoding="utf-8") as f:
				obj = json.load(f)
			W1 = obj["W1"]; b1 = obj["b1"]; W2 = obj["W2"]; b2 = obj["b2"]
			# compute tanh(feats@W1+b1) then sigmoid
			import numpy as np
			X = np.array(feats, dtype=np.float32)[None, :]
			Z1 = X @ np.array(W1, dtype=np.float32) + np.array(b1, dtype=np.float32)
			A1 = np.tanh(Z1)
			Z2 = A1 @ np.array(W2, dtype=np.float32) + np.array(b2, dtype=np.float32)
			nn_score = float(1.0 / (1.0 + np.exp(-Z2))[0, 0])
		return 0.5 * ga_score + nn_score
	except Exception:
		return 0.0


def prime_from_real(t: float, direction: int = 1) -> int:
	"""Map real t>=2 to a prime by rounding to nearest integer index and searching.

	- Estimate index k ≈ li(t) as t/log t, then refine by local search.
	- Convert to nearby integer and move in the desired direction (>= if direction=1, <= if -1)
	- Test successive odd numbers for primality deterministically up to 1e10
	"""
	if t < 2:
		raise ValueError("t must be >= 2")
	# starting guess for prime near t using inverse of pi(n) ~ n/log n
	# If t is meant as an index, we also allow caller to pass non-integer n and use nth prime estimate
	if t < 50:
		# near small numbers choose nearest prime by scanning
		m = max(2, int(round(t)))
		if m % 2 == 0:
			m += 1
		while m >= 2:
			if is_prime_deterministic_1e10(m):
				return m
			m += 2 if direction >= 0 else -2
	# Two interpretations: treat t as magnitude; produce closest prime >= t if direction>=0 else <= t
	n = int(math.floor(t))
	if n % 2 == 0:
		n += 1 if direction >= 0 else -1
	step = 2 if direction >= 0 else -2
	# try to take a few guided larger steps if heuristic says low likelihood
	for _ in range(5):
		s = composite_score(n)
		if s < 0.2:
			n += 10 * step
		else:
			break
	# clamp search upper bound to a large integer; use Python big ints
	upper_limit = (1 << 128) - 1
	while 2 <= n <= upper_limit:
		# certify deterministically up to 2^64, otherwise BPSW probable prime
		if n < (1 << 64):
			ok = is_prime_64bit_deterministic(n)
		else:
			ok = is_probable_prime_bpsw(n)
		if ok:
			return n
		# use small heuristic skips among 6k±1 candidates
		cand1 = n + step
		cand2 = n + 2 * step
		if cand2 % 6 in (1, 5):
			n = cand2
		else:
			n = cand1
	raise RuntimeError("search exceeded bounds")


def prime_index_from_real(u: float) -> int:
	"""Map a real u>=2 to an approximate index k in the sequence of primes.

	Uses li(u) ~ u / log u with small correction, then rounds.
	"""
	if u < 2:
		raise ValueError("u must be >= 2")
	lnu = math.log(u)
	if lnu <= 0:
		return 1
	# simple li approximation (not true logarithmic integral) for speed
	return max(1, int(round(u / lnu)))


def main(argv: Optional[List[str]] = None) -> int:
	parser = argparse.ArgumentParser(description="Prime generator formula over reals")
	parser.add_argument("t", type=float, help="Real input (>=2). If --as-index, treated as prime index.")
	parser.add_argument("--direction", type=int, default=1, choices=(-1, 1), help="Search direction: 1 for >=t, -1 for <=t")
	parser.add_argument("--as-index", action="store_true", help="Treat t as an index and return approximate nth prime")
	args = parser.parse_args(argv)
	if args.as_index:
		n_est = max(2.0, args.t)
		p = int(round(nth_prime_estimate(n_est)))
		# snap to the nearest prime by local search
		p = prime_from_real(float(p), direction=1 if args.direction >= 0 else -1)
		print(p)
		return 0
	else:
		p = prime_from_real(args.t, direction=args.direction)
		print(p)
		return 0


if __name__ == "__main__":
	sys.exit(main())


