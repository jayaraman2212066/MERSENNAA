#!/usr/bin/env python3
"""
Collect real benchmark data from the Flask /api/performance_test endpoint
and save it as JSON under proofs/.
"""

import json
import os
import sys
from typing import Any, Dict


def main(max_exponent: int = 127) -> None:
	# Ensure project root is on sys.path
	project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
	if project_root not in sys.path:
		sys.path.insert(0, project_root)

	from app import app
	os.makedirs('proofs', exist_ok=True)
	with app.test_client() as client:
		resp = client.post('/api/performance_test', json={'max_exponent': max_exponent})
		data: Dict[str, Any] = resp.get_json(force=True)
		with open('proofs/benchmark_results.json', 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2)
		print(f"Saved proofs/benchmark_results.json with {len(data.get('results', []))} entries")


if __name__ == '__main__':
	main()
