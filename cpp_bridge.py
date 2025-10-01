import subprocess
import json
import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

def run_cpp_executable(exe_name, args=[]):
    """Run C++ executable and return results"""
    try:
        if not os.path.exists(exe_name):
            return {"error": f"Executable {exe_name} not found"}
        
        cmd = [exe_name] + [str(arg) for arg in args]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "C++ computation timed out"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/cpp_mersenne_test', methods=['POST'])
def cpp_mersenne_test():
    """Test Mersenne number using C++ executable"""
    data = request.get_json()
    exponent = data.get('exponent', 0)
    
    if exponent < 2:
        return jsonify({"error": "Exponent must be >= 2"})
    
    # Try different C++ executables
    executables = ['mersenne_system.exe', 'mersenne_fixed.exe', 'optimal_mersenne_engine.exe']
    
    for exe in executables:
        if os.path.exists(exe):
            start_time = time.time()
            result = run_cpp_executable(exe, [exponent])
            end_time = time.time()
            
            if result.get("success"):
                return jsonify({
                    "exponent": exponent,
                    "computation_time": round(end_time - start_time, 4),
                    "cpp_output": result["stdout"],
                    "executable_used": exe,
                    "digits": len(str(2**exponent - 1))
                })
    
    return jsonify({"error": "No C++ executables found"})

@app.route('/api/cpp_performance_test', methods=['POST'])
def cpp_performance_test():
    """Run performance test using C++ executable"""
    data = request.get_json()
    max_exp = data.get('max_exponent', 50)
    
    results = []
    total_time = 0
    
    for exe in ['mersenne_system.exe', 'optimal_mersenne_engine.exe']:
        if os.path.exists(exe):
            for p in [2, 3, 5, 7, 13, 17, 19, 31]:
                if p <= max_exp:
                    start_time = time.time()
                    result = run_cpp_executable(exe, [p])
                    end_time = time.time()
                    
                    comp_time = end_time - start_time
                    total_time += comp_time
                    
                    results.append({
                        "exponent": p,
                        "computation_time": round(comp_time, 6),
                        "executable": exe,
                        "success": result.get("success", False)
                    })
            break
    
    if not results:
        return jsonify({"error": "No C++ executables available"})
    
    return jsonify({
        "results": results,
        "total_time": round(total_time, 4),
        "average_time": round(total_time / len(results), 4),
        "total_tested": len(results)
    })

@app.route('/api/cpp_discovery_test', methods=['POST'])
def cpp_discovery_test():
    """Test discovery candidates using C++ executable"""
    data = request.get_json()
    candidates = data.get('candidates', [31, 61, 89, 107, 127])
    
    results = []
    for exe in ['mersenne_system.exe', 'optimal_mersenne_engine.exe']:
        if os.path.exists(exe):
            for p in candidates[:5]:  # Test first 5 candidates
                start_time = time.time()
                result = run_cpp_executable(exe, [p])
                end_time = time.time()
                
                results.append({
                    "candidate": p,
                    "computation_time": round(end_time - start_time, 6),
                    "executable": exe,
                    "cpp_output": result.get("stdout", ""),
                    "success": result.get("success", False)
                })
            break
    
    if not results:
        return jsonify({"error": "No C++ executables available"})
    
    return jsonify({"results": results, "executable_used": results[0]["executable"] if results else None})

if __name__ == '__main__':
    print("Starting C++ Bridge Server...")
    print("Available executables:")
    executables = ['mersenne_system.exe', 'mersenne_fixed.exe', 'optimal_mersenne_engine.exe']
    for exe in executables:
        status = "Found" if os.path.exists(exe) else "Missing"
        print(f"  {exe}: {status}")
    print("\nServer running at http://127.0.0.1:5001")
    print("Use Ctrl+C to stop")
    app.run(host='127.0.0.1', port=5001)