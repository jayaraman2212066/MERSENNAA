#!/usr/bin/env python3
import argparse
import json
import math
import random
from dataclasses import dataclass
from typing import List, Tuple


def feature_vector(n: int) -> List[float]:
	# Same basic features as NN, but numeric only
	return [
		1.0 if (n % 2) else 0.0,
		1.0 if (n % 3) else 0.0,
		(n % 6) / 5.0,
		(n % 30) / 29.0,
		1.0 if (n % 6 in (1, 5)) else 0.0,
		1.0 if (n % 30 in (1, 7, 11, 13, 17, 19, 23, 29)) else 0.0,
	]


def is_prime_fast(n: int) -> bool:
	if n < 2:
		return False
	if n % 2 == 0:
		return n == 2
	limit = int(math.isqrt(n))
	for d in range(3, limit + 1, 2):
		if n % d == 0:
			return False
	return True


def score_candidate(weights: List[float], n: int) -> float:
	feats = feature_vector(n)
	return sum(w * x for w, x in zip(weights, feats))


def fitness(weights: List[float], sample_size: int, start: int, end: int) -> float:
	# Rank correlation between score and primality in a random sample
	nums = [random.randint(start, end) for _ in range(sample_size)]
	labels = [1.0 if is_prime_fast(k) else 0.0 for k in nums]
	scores = [score_candidate(weights, k) for k in nums]
	# simple AUC proxy by comparing ordered pairs
	pairs = 0
	correct = 0
	for i in range(len(nums)):
		for j in range(i + 1, len(nums)):
			if labels[i] != labels[j]:
				pairs += 1
				if (scores[i] - scores[j]) * (labels[i] - labels[j]) > 0:
					correct += 1
	return correct / pairs if pairs else 0.5


def evolve(pop: List[List[float]], generations: int, sample_size: int, start: int, end: int) -> Tuple[List[float], float]:
	for _ in range(generations):
		scored = [(ind, fitness(ind, sample_size, start, end)) for ind in pop]
		scored.sort(key=lambda t: t[1], reverse=True)
		elite = [w for w, _ in scored[: max(2, len(pop) // 5)]]
		new_pop = elite[:]
		while len(new_pop) < len(pop):
			pa, pb = random.sample(elite, 2)
			child = [(a + b) / 2 for a, b in zip(pa, pb)]
			# mutate
			for i in range(len(child)):
				if random.random() < 0.2:
					child[i] += random.gauss(0, 0.1)
			new_pop.append(child)
		pop = new_pop
	best = max(pop, key=lambda w: fitness(w, sample_size, start, end))
	best_fit = fitness(best, sample_size * 2, start, end)
	return best, best_fit


def main():
	parser = argparse.ArgumentParser(description="Genetic algorithm to evolve prime scoring heuristic")
	parser.add_argument("--population", type=int, default=40)
	parser.add_argument("--generations", type=int, default=30)
	parser.add_argument("--sample-size", type=int, default=200)
	parser.add_argument("--start", type=int, default=100)
	parser.add_argument("--end", type=int, default=500000)
	parser.add_argument("--save", type=str, default="ml/ga_weights.json")
	args = parser.parse_args()

	random.seed(42)
	pop = [[random.gauss(0, 1) for _ in range(6)] for _ in range(args.population)]
	best, fit = evolve(pop, args.generations, args.sample_size, args.start, args.end)
	print("best_weights:", ", ".join(f"{w:.3f}" for w in best))
	print(f"fitness≈{fit:.4f}")
	with open(args.save, "w", encoding="utf-8") as f:
		json.dump({"weights": best, "fitness": fit}, f)
	print(f"saved_weights={args.save}")


if __name__ == "__main__":
	main()


