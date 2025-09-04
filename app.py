from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import math
import time
import threading
from datetime import datetime
import os

app = Flask(__name__)

# Import your existing Mersenne analysis functions
try:
    from comprehensive_perfect_numbers_analysis import analyze_perfect_numbers
    from mersenne_prime_pattern_finder import find_mersenne_patterns
    from perfect_numbers_graph import generate_perfect_number_graph
except ImportError:
    # Fallback functions if imports fail
    def analyze_perfect_numbers():
        return {"status": "Analysis module not available"}
    
    def find_mersenne_patterns():
        return {"status": "Pattern finder not available"}
    
    def generate_perfect_number_graph():
        return {"status": "Graph generator not available"}

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
    
    def is_prime(self, n):
        """Simple primality test for small numbers"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def lucas_lehmer_test(self, p):
        """Lucas-Lehmer primality test for Mersenne numbers"""
        if p == 2:
            return True
        
        s = 4
        M = (1 << p) - 1  # 2^p - 1
        
        for _ in range(p - 2):
            s = (s * s - 2) % M
        
        return s == 0
    
    def test_mersenne_number(self, p):
        """Test if 2^p - 1 is prime"""
        start_time = time.time()
        
        if p <= 0:
            return {"valid": False, "error": "Exponent must be positive"}
        
        if p > 1000:  # Limit for demo purposes
            return {"valid": False, "error": "Exponent too large for demo (max 1000)"}
        
        try:
            M = (1 << p) - 1
            is_prime = self.lucas_lehmer_test(p)
            end_time = time.time()
            
            return {
                "valid": True,
                "exponent": p,
                "mersenne_number": str(M),
                "is_prime": is_prime,
                "computation_time": round(end_time - start_time, 4),
                "digits": len(str(M))
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def find_perfect_numbers(self, limit=10):
        """Find perfect numbers up to a limit"""
        perfect_numbers = []
        count = 0
        
        for p in range(2, 1000):  # Limit for demo
            if count >= limit:
                break
            
            if self.lucas_lehmer_test(p):
                perfect_number = (1 << (p - 1)) * ((1 << p) - 1)
                perfect_numbers.append({
                    "exponent": p,
                    "mersenne_prime": (1 << p) - 1,
                    "perfect_number": str(perfect_number),
                    "digits": len(str(perfect_number))
                })
                count += 1
        
        return perfect_numbers
    
    def analyze_patterns(self):
        """Analyze patterns in known Mersenne primes"""
        if len(self.known_mersenne_primes) < 2:
            return {"error": "Not enough data for analysis"}
        
        gaps = []
        for i in range(1, len(self.known_mersenne_primes)):
            gap = self.known_mersenne_primes[i] - self.known_mersenne_primes[i-1]
            gaps.append(gap)
        
        return {
            "total_known": len(self.known_mersenne_primes),
            "largest_known": max(self.known_mersenne_primes),
            "average_gap": sum(gaps) / len(gaps) if gaps else 0,
            "min_gap": min(gaps) if gaps else 0,
            "max_gap": max(gaps) if gaps else 0,
            "gaps": gaps[:10]  # First 10 gaps
        }

# Global calculator instance
calculator = MersenneCalculator()

@app.route('/')
def index():
    """Serve the main interactive webpage"""
    return render_template('index.html')

# --- Image gallery endpoints ---
KNOWN_IMAGE_DIRS = [
    ".",
    "all perfectno about",
    "finder_new_mersenne prim",
]

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def collect_images():
    images = []
    for base in KNOWN_IMAGE_DIRS:
        if not os.path.isdir(base):
            continue
        for root, _, files in os.walk(base):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in ALLOWED_EXT:
                    rel_root = os.path.relpath(root, start=os.getcwd())
                    images.append({
                        "name": f,
                        "path": os.path.join(rel_root, f).replace("\\", "/")
                    })
    return images

@app.route('/api/images')
def list_images():
    return jsonify({"images": collect_images()})

@app.route('/images/<path:filename>')
def serve_image(filename):
    # Securely serve from repo root only
    directory = os.getcwd()
    # Prevent path traversal
    safe_path = os.path.normpath(os.path.join(directory, filename))
    if not safe_path.startswith(directory):
        return jsonify({"error": "Invalid path"}), 400
    folder, file = os.path.split(safe_path)
    return send_from_directory(folder, file)

@app.route('/api/test_mersenne', methods=['POST'])
def test_mersenne():
    """API endpoint to test Mersenne numbers"""
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
    """API endpoint to find perfect numbers"""
    try:
        data = request.get_json()
        limit = int(data.get('limit', 5))
        
        if limit <= 0 or limit > 20:
            return jsonify({"error": "Limit must be between 1 and 20"})
        
        perfect_numbers = calculator.find_perfect_numbers(limit)
        return jsonify({
            "perfect_numbers": perfect_numbers,
            "count": len(perfect_numbers)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/analyze_patterns')
def analyze_patterns():
    """API endpoint to analyze Mersenne prime patterns"""
    try:
        patterns = calculator.analyze_patterns()
        return jsonify(patterns)
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/performance_test', methods=['POST'])
def performance_test():
    """API endpoint to test performance with different exponents"""
    try:
        data = request.get_json()
        max_exponent = int(data.get('max_exponent', 100))
        
        if max_exponent <= 0 or max_exponent > 500:
            return jsonify({"error": "Max exponent must be between 1 and 500"})
        
        results = []
        total_time = 0
        
        for p in range(2, min(max_exponent + 1, 100)):
            if p in calculator.known_mersenne_primes:
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
    """API endpoint to run comprehensive analysis"""
    try:
        # Run different types of analysis
        start_time = time.time()
        
        # Basic pattern analysis
        patterns = calculator.analyze_patterns()
        
        # Find some perfect numbers
        perfect_numbers = calculator.find_perfect_numbers(5)
        
        # Performance test
        performance_results = []
        for p in [2, 3, 5, 7, 13, 17, 19, 31]:
            start = time.time()
            is_prime = calculator.lucas_lehmer_test(p)
            end = time.time()
            performance_results.append({
                "exponent": p,
                "is_prime": is_prime,
                "time": round(end - start, 6)
            })
        
        end_time = time.time()
        
        return jsonify({
            "analysis_time": round(end_time - start_time, 4),
            "patterns": patterns,
            "perfect_numbers": perfect_numbers,
            "performance_test": performance_results,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/status')
def status():
    """API endpoint to check system status"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "calculator_ready": True,
        "known_mersenne_count": len(calculator.known_mersenne_primes)
    })

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    # For production (Render)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

