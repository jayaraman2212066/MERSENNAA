#!/usr/bin/env python3
"""
Plot benchmark results from proofs/benchmark_results.json as a PNG chart.
"""

import json
import os
from typing import List, Dict, Any
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main() -> None:
	os.makedirs('proofs', exist_ok=True)
	with open('proofs/benchmark_results.json', 'r', encoding='utf-8') as f:
		data: Dict[str, Any] = json.load(f)
	results: List[Dict[str, Any]] = data.get('results', [])
	if not results:
		print('No results to plot')
		return
	
	exponents = [r['exponent'] for r in results]
	times = [r['computation_time'] for r in results]
	
	plt.figure(figsize=(10, 6), dpi=140)
	plt.plot(exponents, times, marker='o', linestyle='-', color='#4CAF50', label='Time per exponent (s)')
	plt.title('Lucas-Lehmer Benchmark: Time per Known Mersenne Exponent Test')
	plt.xlabel('Exponent p')
	plt.ylabel('Computation time (seconds)')
	plt.grid(True, alpha=0.3)
	plt.legend()
	out = 'proofs/benchmark_chart.png'
	plt.tight_layout()
	plt.savefig(out)
	print(f'Saved {out}')


if __name__ == '__main__':
	main()
