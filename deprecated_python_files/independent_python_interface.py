#!/usr/bin/env python3
"""
🚀 INDEPENDENT PYTHON INTERFACE 🚀
Python wrapper for the independent C++ Mersenne engine
"""

import subprocess
import json
import time
import threading
from datetime import datetime
from typing import List, Dict, Optional
import os

class IndependentMersenneInterface:
    def __init__(self):
        self.engine_path = "independent_mersenne_engine.exe"
        self.is_running = False
        self.current_process = None
        
    def compile_engine(self) -> bool:
        """Compile the independent C++ engine"""
        try:
            print("🔨 Compiling independent Mersenne engine...")
            result = subprocess.run(
                ["compile_independent_engine.bat"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                print("✅ Engine compiled successfully!")
                return True
            else:
                print(f"❌ Compilation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False
    
    def test_single_exponent(self, p: int, timeout: float = 300.0) -> Dict:
        """Test a single exponent using the independent engine"""
        if not os.path.exists(self.engine_path):
            if not self.compile_engine():
                return {"error": "Failed to compile engine"}
        
        try:
            # Create temporary input file
            with open("temp_input.txt", "w") as f:
                f.write(f"{p}\n1\n1\n")  # exponent, start, end, count
            
            start_time = time.time()
            
            # Run the engine
            process = subprocess.Popen(
                [self.engine_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send input
            stdout, stderr = process.communicate(
                input=f"{p}\n{p}\n1\n",
                timeout=timeout
            )
            
            end_time = time.time()
            
            # Parse results
            is_prime = "MERSENNE PRIME FOUND" in stdout
            computation_time = end_time - start_time
            
            # Clean up
            if os.path.exists("temp_input.txt"):
                os.remove("temp_input.txt")
            
            return {
                "exponent": p,
                "is_prime": is_prime,
                "computation_time": computation_time,
                "engine": "Independent C++",
                "stdout": stdout,
                "stderr": stderr
            }
            
        except subprocess.TimeoutExpired:
            if process:
                process.kill()
            return {
                "exponent": p,
                "error": "Timeout exceeded",
                "computation_time": timeout
            }
        except Exception as e:
            return {
                "exponent": p,
                "error": str(e),
                "computation_time": 0
            }
    
    def run_discovery_range(self, start: int, end: int, max_candidates: int = 1000) -> Dict:
        """Run discovery on a range using the independent engine"""
        if not os.path.exists(self.engine_path):
            if not self.compile_engine():
                return {"error": "Failed to compile engine"}
        
        try:
            print(f"🚀 Starting independent discovery: {start:,} to {end:,}")
            
            start_time = time.time()
            self.is_running = True
            
            # Run the engine with parameters
            self.current_process = subprocess.Popen(
                [self.engine_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Send parameters
            input_data = f"{start}\n{end}\n{max_candidates}\n"
            
            discoveries = []
            candidates_tested = 0
            
            # Read output in real-time
            for line in iter(self.current_process.stdout.readline, ''):
                print(line.strip())
                
                # Parse discoveries
                if "MERSENNE PRIME FOUND" in line:
                    # Extract exponent from output
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "p" and i + 2 < len(parts):
                            try:
                                exponent = int(parts[i + 2])
                                discoveries.append({
                                    "exponent": exponent,
                                    "discovery_time": datetime.now().isoformat(),
                                    "engine": "Independent C++"
                                })
                            except ValueError:
                                pass
                
                # Parse progress
                if "Progress:" in line:
                    try:
                        # Extract candidates tested
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part.endswith("%") and i + 1 < len(parts):
                                progress_part = parts[i + 1]
                                if "(" in progress_part and "/" in progress_part:
                                    tested = int(progress_part.split("(")[1].split("/")[0])
                                    candidates_tested = tested
                    except:
                        pass
                
                if not self.is_running:
                    break
            
            self.current_process.wait()
            end_time = time.time()
            
            return {
                "discoveries": discoveries,
                "candidates_tested": candidates_tested,
                "total_time": end_time - start_time,
                "engine": "Independent C++",
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "engine": "Independent C++",
                "status": "failed"
            }
        finally:
            self.is_running = False
            self.current_process = None
    
    def stop_discovery(self):
        """Stop the running discovery process"""
        self.is_running = False
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None
    
    def benchmark_performance(self, test_exponents: List[int]) -> Dict:
        """Benchmark the independent engine performance"""
        results = []
        total_time = 0
        
        print("🧪 Benchmarking independent engine performance...")
        
        for p in test_exponents:
            print(f"Testing p={p}...")
            result = self.test_single_exponent(p, timeout=60.0)
            
            if "error" not in result:
                results.append({
                    "exponent": p,
                    "computation_time": result["computation_time"],
                    "is_prime": result["is_prime"]
                })
                total_time += result["computation_time"]
            else:
                print(f"❌ Error testing p={p}: {result['error']}")
        
        if results:
            avg_time = total_time / len(results)
            return {
                "results": results,
                "total_time": total_time,
                "average_time": avg_time,
                "tests_per_second": len(results) / total_time if total_time > 0 else 0,
                "engine": "Independent C++"
            }
        else:
            return {"error": "No successful tests completed"}

def main():
    """Main function for testing the independent interface"""
    print("🚀 INDEPENDENT MERSENNE ENGINE INTERFACE 🚀")
    print("=" * 50)
    
    interface = IndependentMersenneInterface()
    
    # Test small known Mersenne primes
    test_exponents = [3, 5, 7, 13, 17, 19, 31]
    
    print("🧪 Testing known Mersenne primes:")
    for p in test_exponents:
        result = interface.test_single_exponent(p, timeout=30.0)
        
        if "error" not in result:
            status = "✅ PRIME" if result["is_prime"] else "❌ COMPOSITE"
            print(f"p={p}: {status} (time: {result['computation_time']:.4f}s)")
        else:
            print(f"p={p}: ❌ ERROR - {result['error']}")
    
    # Benchmark performance
    print("\n📊 Performance benchmark:")
    benchmark = interface.benchmark_performance([3, 5, 7, 13, 17])
    
    if "error" not in benchmark:
        print(f"Average time per test: {benchmark['average_time']:.4f}s")
        print(f"Tests per second: {benchmark['tests_per_second']:.2f}")
    else:
        print(f"❌ Benchmark failed: {benchmark['error']}")
    
    # Test discovery range (small range for demo)
    print("\n🔍 Testing discovery range:")
    discovery = interface.run_discovery_range(85000000, 85000100, 10)
    
    if "error" not in discovery:
        print(f"✅ Discovery completed in {discovery['total_time']:.2f}s")
        print(f"Candidates tested: {discovery['candidates_tested']}")
        print(f"Discoveries: {len(discovery['discoveries'])}")
    else:
        print(f"❌ Discovery failed: {discovery['error']}")

if __name__ == "__main__":
    main()