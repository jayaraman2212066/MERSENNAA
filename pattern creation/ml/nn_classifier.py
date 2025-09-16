#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
from dataclasses import dataclass
from typing import Tuple

import numpy as np

from .features import feature_vector_int


def is_prime_simple(n: int) -> bool:
	if n < 2:
		return False
	if n % 2 == 0:
		return n == 2
	limit = int(math.isqrt(n))
	for d in range(3, limit + 1, 2):
		if n % d == 0:
			return False
	return True


def features(n: int) -> np.ndarray:
	return np.array(feature_vector_int(n), dtype=np.float32)


def make_dataset(count: int, start: int = 100, end: int = 500000) -> Tuple[np.ndarray, np.ndarray]:
	X = np.zeros((count, 9), dtype=np.float32)
	y = np.zeros((count, 1), dtype=np.float32)
	for i in range(count):
		n = random.randint(start, end)
		X[i] = features(n)
		y[i, 0] = 1.0 if is_prime_simple(n) else 0.0
	return X, y


@dataclass
class MLP:
	input_dim: int
	hidden_dim: int
	seed: int = 42

	def __post_init__(self):
		rng = np.random.default_rng(self.seed)
		self.W1 = rng.normal(0, 0.2, (self.input_dim, self.hidden_dim)).astype(np.float32)
		self.b1 = np.zeros((self.hidden_dim,), dtype=np.float32)
		self.W2 = rng.normal(0, 0.2, (self.hidden_dim, 1)).astype(np.float32)
		self.b2 = np.zeros((1,), dtype=np.float32)

	def forward(self, X: np.ndarray) -> Tuple[np.ndarray, dict]:
		Z1 = X @ self.W1 + self.b1
		A1 = np.tanh(Z1)
		Z2 = A1 @ self.W2 + self.b2
		Y = 1.0 / (1.0 + np.exp(-Z2))
		cache = {"X": X, "Z1": Z1, "A1": A1, "Z2": Z2, "Y": Y}
		return Y, cache

	def backward(self, cache: dict, y_true: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
		m = y_true.shape[0]
		Y = cache["Y"]
		A1 = cache["A1"]
		X = cache["X"]
		dZ2 = (Y - y_true) / m
		dW2 = A1.T @ dZ2
		db2 = np.sum(dZ2, axis=0)
		dA1 = dZ2 @ self.W2.T
		dZ1 = dA1 * (1 - np.tanh(cache["Z1"]) ** 2)
		dW1 = X.T @ dZ1
		db1 = np.sum(dZ1, axis=0)
		return dW1, db1, dW2, db2

	def step(self, grads: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], lr: float) -> None:
		dW1, db1, dW2, db2 = grads
		self.W1 -= lr * dW1
		self.b1 -= lr * db1
		self.W2 -= lr * dW2
		self.b2 -= lr * db2

	def loss(self, Y: np.ndarray, y_true: np.ndarray) -> float:
		eps = 1e-9
		return float(np.mean(-(y_true * np.log(Y + eps) + (1 - y_true) * np.log(1 - Y + eps))))

	def save(self, path: str) -> None:
		obj = {
			"W1": self.W1.tolist(),
			"b1": self.b1.tolist(),
			"W2": self.W2.tolist(),
			"b2": self.b2.tolist(),
		}
		with open(path, "w", encoding="utf-8") as f:
			json.dump(obj, f)

	@classmethod
	def load(cls, path: str) -> "MLP":
		with open(path, "r", encoding="utf-8") as f:
			obj = json.load(f)
		model = cls(input_dim=len(obj["W1"]), hidden_dim=len(obj["b1"]))
		model.W1 = np.array(obj["W1"], dtype=np.float32)
		model.b1 = np.array(obj["b1"], dtype=np.float32)
		model.W2 = np.array(obj["W2"], dtype=np.float32)
		model.b2 = np.array(obj["b2"], dtype=np.float32)
		return model


def accuracy(Y: np.ndarray, y_true: np.ndarray) -> float:
	pred = (Y >= 0.5).astype(np.float32)
	return float(np.mean(pred == y_true))


def main():
	parser = argparse.ArgumentParser(description="Simple NumPy MLP for prime vs composite classification")
	parser.add_argument("--train", type=int, default=20000, help="Training samples")
	parser.add_argument("--val", type=int, default=5000, help="Validation samples")
	parser.add_argument("--epochs", type=int, default=5, help="Epochs")
	parser.add_argument("--hidden", type=int, default=32, help="Hidden size")
	parser.add_argument("--lr", type=float, default=0.05, help="Learning rate")
	parser.add_argument("--save", type=str, default="ml/nn_weights.json", help="Path to save weights")
	args = parser.parse_args()

	Xtr, ytr = make_dataset(args.train)
	Xva, yva = make_dataset(args.val)
	model = MLP(input_dim=Xtr.shape[1], hidden_dim=args.hidden)
	for epoch in range(1, args.epochs + 1):
		Ytr, cache = model.forward(Xtr)
		L = model.loss(Ytr, ytr)
		grads = model.backward(cache, ytr)
		model.step(grads, lr=args.lr)
		Yva, _ = model.forward(Xva)
		acc = accuracy(Yva, yva)
		print(f"epoch={epoch} loss={L:.4f} val_acc={acc:.4f}")
	model.save(args.save)
	print(f"saved_weights={args.save}")


if __name__ == "__main__":
	main()


