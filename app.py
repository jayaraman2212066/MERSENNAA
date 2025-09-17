from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import math
import time
import threading
from datetime import datetime
import os
from prime95_integration import integrate_with_prime95

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

# Import revolutionary discovery system
try:
    from revolutionary_mersenne_discovery import RevolutionaryMersenneDiscovery
    from advanced_candidate_generator import AdvancedCandidateGenerator
    DISCOVERY_AVAILABLE = True
except ImportError:
    DISCOVERY_AVAILABLE = False
    print("⚠️ Revolutionary discovery system not available")

# Global discovery state for live demo
discovery_state = {
    "running": False,
    "engine": None,
    "start_time": None,
    "candidates_tested": 0,
    "discoveries": [],
    "current_candidate": None,
    "test_rate": 0.0,
    "threads_active": 0
}

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
    
    def lucas_lehmer_test(self, p: int, time_budget_seconds: float | None = None):
        """Lucas-Lehmer primality test for Mersenne numbers with optional time budget.
        Returns True/False, or raises TimeoutError if budget exceeded.
        """
        if p == 2:
            return True
        start = time.time()
        s = 4
        M = (1 << p) - 1  # 2^p - 1
        for _ in range(p - 2):
            s = (s * s - 2) % M
            if time_budget_seconds is not None and (time.time() - start) > time_budget_seconds:
                raise TimeoutError("Lucas-Lehmer timed out")
        return s == 0
    
    def test_mersenne_number(self, p, time_budget_seconds: float | None = 8.0):
        """Test if 2^p - 1 is prime"""
        start_time = time.time()
        
        if p <= 0:
            return {"valid": False, "error": "Exponent must be positive"}
        
        # No artificial upper bound on exponent for live demo
        
        try:
            M = (1 << p) - 1
            is_prime = self.lucas_lehmer_test(p, time_budget_seconds=time_budget_seconds)
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
            return {"valid": False, "error": "Computation timed out — try a smaller exponent"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def find_perfect_numbers(self, limit=10):
        """Find perfect numbers up to a limit"""
        perfect_numbers = []
        count = 0
        
        # Iterate over exponents without a low upper bound; stop when limit is reached
        for p in range(2, 100000):
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
    "all perfectno about",
    "finder_new_mersenne prim",
    ".",
]

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
SKIP_DIR_NAMES = {".git", "venv", ".venv", "node_modules", "__pycache__", "site-packages", "dist", "build"}


def collect_images():
    seen = set()
    images = []
    cwd = os.getcwd()
    for base in KNOWN_IMAGE_DIRS:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            # prune unwanted directories in-place
            dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in ALLOWED_EXT:
                    continue
                abs_path = os.path.normpath(os.path.join(root, f))
                rel_path = os.path.relpath(abs_path, start=cwd).replace("\\", "/")
                if rel_path in seen:
                    continue
                seen.add(rel_path)
                images.append({"name": f, "path": rel_path})
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
        
        if limit <= 0:
            return jsonify({"error": "Limit must be positive"})
        
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
        
        if max_exponent <= 0:
            return jsonify({"error": "Max exponent must be positive"})
        
        results = []
        total_time = 0
        
        for p in range(2, max_exponent + 1):
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

# --- Progress reporting for live demo ---
def _file_info(path: str):
    try:
        st = os.stat(path)
        return {
            "exists": True,
            "size": st.st_size,
            "modified": datetime.fromtimestamp(st.st_mtime).isoformat()
        }
    except Exception:
        return {"exists": False}

@app.route('/api/progress')
def progress():
    """Report current pipeline progress for UI (Prime95 + proofs)."""
    cfg = {}
    try:
        with open('mersenne_search_config.json','r',encoding='utf-8') as f:
            cfg = json.load(f)
    except Exception:
        pass
    p95 = (cfg.get('prime95_integration') or {})
    # If not explicitly enabled or running on a non-Windows environment like Render,
    # treat Prime95 as not configured and avoid probing Windows paths.
    is_configured = bool(p95.get('enabled')) and os.name == 'nt'
    results_path = p95.get('results_path') if is_configured else None
    worktodo_path = p95.get('worktodo_path') if is_configured else None

    proofs = {
        "demo": _file_info(os.path.join('proofs','mersenne_proof_demo.png')),
        "small": _file_info(os.path.join('proofs','mersenne_proof_small.png')),
        "upto61": _file_info(os.path.join('proofs','mersenne_proof_upto61.png')),
        "live": _file_info(os.path.join('proofs','mersenne_proof.png')),
    }
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "prime95": {
            "results": _file_info(results_path) if results_path else {"exists": False},
            "worktodo": _file_info(worktodo_path) if worktodo_path else {"exists": False},
            "configured": is_configured
        },
        "proofs": proofs
    })

@app.route('/api/queue_mersenne', methods=['POST'])
def queue_mersenne():
    """Append one or more exponents to Prime95 WorkToDo (no upper limit)."""
    try:
        data = request.get_json(force=True)
        exps = data.get('exponents')
        mode = (data.get('mode') or 'LL').upper()
        if isinstance(exps, int):
            exponents = [int(exps)]
        elif isinstance(exps, list):
            exponents = [int(x) for x in exps if int(x) > 1]
        else:
            return jsonify({"error": "Provide 'exponents' as int or list of ints"}), 400

        # Load config and integrate
        cfg = {}
        try:
            with open('mersenne_search_config.json','r',encoding='utf-8') as f:
                cfg = json.load(f)
        except Exception:
            pass
        # force mode if provided
        if 'prime95_integration' in cfg:
            cfg['prime95_integration']['mode'] = mode

        result = integrate_with_prime95(exponents, cfg)
        return jsonify({
            "queued": len(exponents),
            "mode": mode,
            "worktodo": result.get('worktodo_path'),
            "lines_written": result.get('lines_written'),
            "launched": result.get('launched', False)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/start_discovery', methods=['POST'])
def start_discovery():
    """Start revolutionary Mersenne prime discovery (unlimited range)"""
    if not DISCOVERY_AVAILABLE:
        return jsonify({"error": "Revolutionary discovery system not available"}), 500
    
    try:
        data = request.get_json()
        start_range = int(data.get('start_range', 85000000))
        end_range = int(data.get('end_range', 86000000))
        max_candidates = int(data.get('max_candidates', 10000))
        workers = int(data.get('workers', 4))
        
        if discovery_state["running"]:
            return jsonify({"error": "Discovery already running"}), 400
        
        # Validate parameters
        if start_range < 2 or end_range <= start_range:
            return jsonify({"error": "Invalid range parameters"}), 400
        
        if max_candidates < 1 or max_candidates > 1000000:
            return jsonify({"error": "Max candidates must be between 1 and 1,000,000"}), 400
        
        if workers < 1 or workers > 16:
            return jsonify({"error": "Workers must be between 1 and 16"}), 400
        
        # Initialize discovery engine
        discovery_state["engine"] = RevolutionaryMersenneDiscovery()
        discovery_state["engine"].config["optimization_settings"]["max_workers"] = workers
        discovery_state["start_time"] = time.time()
        discovery_state["running"] = True
        discovery_state["candidates_tested"] = 0
        discovery_state["discoveries"] = []
        discovery_state["current_candidate"] = None
        discovery_state["test_rate"] = 0.0
        discovery_state["threads_active"] = 0
        
        # Start discovery in background thread
        def run_discovery():
            try:
                discoveries = discovery_state["engine"].run_discovery(start_range, end_range, max_candidates)
                discovery_state["discoveries"] = discoveries
            except Exception as e:
                print(f"Discovery error: {e}")
            finally:
                discovery_state["running"] = False
        
        discovery_thread = threading.Thread(target=run_discovery)
        discovery_thread.daemon = True
        discovery_thread.start()
        
        return jsonify({
            "status": "started",
            "start_range": start_range,
            "end_range": end_range,
            "max_candidates": max_candidates,
            "workers": workers,
            "start_time": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/discovery_status')
def discovery_status():
    """Get current discovery status and progress"""
    if not DISCOVERY_AVAILABLE:
        return jsonify({"error": "Revolutionary discovery system not available"}), 500
    
    try:
        # Update stats from engine if available
        if discovery_state["engine"]:
            discovery_state["candidates_tested"] = getattr(discovery_state["engine"], 'candidates_tested', 0)
            discovery_state["discoveries"] = getattr(discovery_state["engine"], 'discoveries', [])
            discovery_state["threads_active"] = len(getattr(discovery_state["engine"], 'threads', []))
            
            # Calculate test rate
            if discovery_state["start_time"]:
                elapsed = time.time() - discovery_state["start_time"]
                if elapsed > 0:
                    discovery_state["test_rate"] = discovery_state["candidates_tested"] / elapsed
        
        return jsonify({
            "running": discovery_state["running"],
            "candidates_tested": discovery_state["candidates_tested"],
            "discoveries": discovery_state["discoveries"],
            "current_candidate": discovery_state["current_candidate"],
            "test_rate": round(discovery_state["test_rate"], 2),
            "threads_active": discovery_state["threads_active"],
            "start_time": discovery_state["start_time"],
            "elapsed_time": time.time() - discovery_state["start_time"] if discovery_state["start_time"] else 0,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stop_discovery', methods=['POST'])
def stop_discovery():
    """Stop the running discovery process"""
    if not DISCOVERY_AVAILABLE:
        return jsonify({"error": "Revolutionary discovery system not available"}), 500
    
    try:
        if not discovery_state["running"]:
            return jsonify({"error": "No discovery running"}), 400
        
        discovery_state["running"] = False
        if discovery_state["engine"]:
            discovery_state["engine"].running = False
        
        return jsonify({
            "status": "stopped",
            "candidates_tested": discovery_state["candidates_tested"],
            "discoveries": discovery_state["discoveries"],
            "stop_time": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate_candidates', methods=['POST'])
def generate_candidates():
    """Generate intelligent candidates using pattern analysis"""
    if not DISCOVERY_AVAILABLE:
        return jsonify({"error": "Revolutionary discovery system not available"}), 500
    
    try:
        data = request.get_json()
        start_range = int(data.get('start_range', 85000000))
        end_range = int(data.get('end_range', 86000000))
        count = int(data.get('count', 1000))
        
        if count < 1 or count > 10000:
            return jsonify({"error": "Count must be between 1 and 10,000"}), 400
        
        generator = AdvancedCandidateGenerator()
        candidates = generator.generate_intelligent_candidates(start_range, end_range, count)
        analysis = generator.analyze_candidate_quality(candidates)
        
        return jsonify({
            "candidates": candidates,
            "analysis": analysis,
            "count": len(candidates),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    # For production (Render)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

