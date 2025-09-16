#!/usr/bin/env python3
import json
import os
import sys


def main():
	weights_path = os.path.join(os.path.dirname(__file__), "nn_weights.json")
	out_path = os.path.join(os.path.dirname(__file__), "nn_classifier.tflite")
	if not os.path.isfile(weights_path):
		print(f"Weights not found: {weights_path}")
		return 2
	with open(weights_path, "r", encoding="utf-8") as f:
		obj = json.load(f)
	W1 = obj["W1"]; b1 = obj["b1"]; W2 = obj["W2"]; b2 = obj["b2"]

	try:
		import tensorflow as tf
	except Exception as e:
		print("TensorFlow not available. Install tensorflow to export TFLite.")
		return 3

	import numpy as np
	input_dim = len(W1)
	hid_dim = len(b1)
	# Build Keras model matching: input -> Dense(hid_dim, tanh) -> Dense(1, sigmoid)
	model = tf.keras.Sequential([
		tf.keras.layers.Input(shape=(input_dim,), dtype=tf.float32),
		tf.keras.layers.Dense(hid_dim, activation='tanh', use_bias=True),
		tf.keras.layers.Dense(1, activation='sigmoid', use_bias=True),
	])
	# Set weights
	W1_np = np.array(W1, dtype=np.float32)
	b1_np = np.array(b1, dtype=np.float32)
	W2_np = np.array(W2, dtype=np.float32)
	b2_np = np.array(b2, dtype=np.float32)
	model.layers[0].set_weights([W1_np, b1_np])
	model.layers[1].set_weights([W2_np, b2_np])

	# Convert to TFLite
	converter = tf.lite.TFLiteConverter.from_keras_model(model)
	tflite_model = converter.convert()
	with open(out_path, 'wb') as f:
		f.write(tflite_model)
	print(f"Wrote {out_path}")
	return 0


if __name__ == "__main__":
	sys.exit(main())


