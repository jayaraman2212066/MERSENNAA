from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import math
import time
import os
from datetime import datetime

# Ensure Flask can find templates
app = Flask(__name__, template_folder='templates', static_folder='archived_png_files')

class MersenneCalculator:
    def __init__(self):
        self.known_mersenne_primes = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
            2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
            23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
            1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
            24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
            43112609, 57885161, 74207281, 77232917, 82589933
        ]
    
    def lucas_lehmer_test(self, p: int, time_budget_seconds=8.0):
        if p == 2:
            return True
        start = time.time()
        s = 4
        M = (1 << p) - 1
        for _ in range(p - 2):
            s = (s * s - 2) % M
            if time_budget_seconds and (time.time() - start) > time_budget_seconds:
                raise TimeoutError("Lucas-Lehmer timed out")
        return s == 0
    
    def test_mersenne_number(self, p, time_budget_seconds=8.0):
        start_time = time.time()
        if p <= 0:
            return {"valid": False, "error": "Exponent must be positive"}
        
        try:
            M = (1 << p) - 1
            is_prime = self.lucas_lehmer_test(p, time_budget_seconds)
            end_time = time.time()
            
            return {
                "valid": True,
                "exponent": p,
                "mersenne_number": str(M),
                "is_prime": is_prime,
                "computation_time": round(end_time - start_time, 4),
                "digits": len(str(M))
            }
        except TimeoutError:
            return {"valid": False, "error": "Computation timed out"}
        except Exception as e:
            return {"valid": False, "error": str(e)}

calculator = MersenneCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test_mersenne', methods=['POST'])
def test_mersenne():
    try:
        data = request.get_json()
        exponent = int(data.get('exponent', 0))
        if exponent <= 0:
            return jsonify({"error": "Exponent must be positive"})
        result = calculator.test_mersenne_number(exponent)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/find_perfect_numbers', methods=['POST'])
def find_perfect_numbers():
    try:
        data = request.get_json()
        limit = int(data.get('limit', 5))
        perfect_numbers = []
        
        for i, p in enumerate(calculator.known_mersenne_primes[:limit]):
            perfect_number = (1 << (p - 1)) * ((1 << p) - 1)
            perfect_numbers.append({
                "exponent": p,
                "mersenne_prime": (1 << p) - 1,
                "perfect_number": str(perfect_number),
                "digits": len(str(perfect_number))
            })
        
        return jsonify({"perfect_numbers": perfect_numbers, "count": len(perfect_numbers)})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/performance_test', methods=['POST'])
def performance_test():
    try:
        data = request.get_json()
        max_exponent = int(data.get('max_exponent', 100))
        results = []
        total_time = 0
        
        for p in calculator.known_mersenne_primes:
            if p > max_exponent:
                break
            start_time = time.time()
            is_prime = calculator.lucas_lehmer_test(p)
            end_time = time.time()
            
            computation_time = end_time - start_time
            total_time += computation_time
            
            results.append({
                "exponent": p,
                "is_prime": is_prime,
                "computation_time": round(computation_time, 4)
            })
        
        return jsonify({
            "results": results,
            "total_time": round(total_time, 4),
            "average_time": round(total_time / len(results), 4) if results else 0,
            "total_tested": len(results)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/run_analysis')
def run_analysis():
    try:
        start_time = time.time()
        
        # Basic analysis
        gaps = []
        for i in range(1, len(calculator.known_mersenne_primes)):
            gap = calculator.known_mersenne_primes[i] - calculator.known_mersenne_primes[i-1]
            gaps.append(gap)
        
        patterns = {
            "total_known": len(calculator.known_mersenne_primes),
            "largest_known": max(calculator.known_mersenne_primes),
            "average_gap": sum(gaps) / len(gaps) if gaps else 0
        }
        
        end_time = time.time()
        
        return jsonify({
            "analysis_time": round(end_time - start_time, 4),
            "patterns": patterns,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/research_analysis.pdf')
def research_analysis():
    try:
        return send_from_directory('.', 'research_analysis.pdf', as_attachment=False)
    except FileNotFoundError:
        return jsonify({"error": "Research analysis not found"}), 404

@app.route('/archived_png_files/<path:filename>')
def serve_archived_images(filename):
    try:
        return send_from_directory('archived_png_files', filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))