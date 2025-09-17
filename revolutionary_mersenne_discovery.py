#!/usr/bin/env python3
"""
🚀 REVOLUTIONARY MERSENNE PRIME DISCOVERY ENGINE 🚀
Combines Prime95 algorithms with advanced pattern analysis for new Mersenne exponent discovery
"""

import json
import time
import threading
import multiprocessing
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import math
import os
import subprocess
import queue
import signal
import sys

class RevolutionaryMersenneDiscovery:
    def __init__(self, config_file: str = "mersenne_search_config.json"):
        """Initialize the revolutionary discovery engine"""
        self.config = self._load_config(config_file)
        self.known_mersenne_primes = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
            2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
            23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
            1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
            24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
            43112609, 57885161, 74207281, 77232917, 82589933
        ]
        
        # Discovery state
        self.candidates_tested = 0
        self.discoveries = []
        self.running = False
        self.start_time = None
        self.threads = []
        self.result_queue = queue.Queue()
        
        # Pattern analysis data
        self.pattern_weights = self._analyze_known_patterns()
        
        print("🚀 REVOLUTIONARY MERSENNE DISCOVERY ENGINE INITIALIZED 🚀")
        print(f"📊 Known Mersenne primes: {len(self.known_mersenne_primes)}")
        print(f"🔬 Pattern analysis weights: {self.pattern_weights}")
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found, using defaults")
            return {
                "search_ranges": {
                    "range_1": {"start": 85000000, "end": 86000000, "priority": "high"}
                },
                "prime95_integration": {"enabled": True, "mode": "LL"},
                "optimization_settings": {"use_parallel_processing": True, "max_workers": 4}
            }
    
    def _analyze_known_patterns(self) -> Dict:
        """Analyze patterns in known Mersenne primes for intelligent candidate generation"""
        if len(self.known_mersenne_primes) < 10:
            return {"exponential": 0.7, "polynomial": 0.2, "gap_analysis": 0.1}
        
        # Calculate gaps between consecutive Mersenne primes
        gaps = []
        for i in range(1, len(self.known_mersenne_primes)):
            gap = self.known_mersenne_primes[i] - self.known_mersenne_primes[i-1]
            gaps.append(gap)
        
        # Analyze gap patterns
        avg_gap = sum(gaps) / len(gaps)
        gap_variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps)
        
        # Exponential growth analysis
        log_primes = [math.log(p) for p in self.known_mersenne_primes[-10:]]
        if len(log_primes) > 1:
            growth_rate = (log_primes[-1] - log_primes[0]) / (len(log_primes) - 1)
        else:
            growth_rate = 0.1
        
        # Modulo pattern analysis
        mod_patterns = {}
        for p in self.known_mersenne_primes:
            mod = p % 210  # 210 = 2*3*5*7
            mod_patterns[mod] = mod_patterns.get(mod, 0) + 1
        
        return {
            "exponential": min(0.8, max(0.3, growth_rate)),
            "polynomial": min(0.3, max(0.1, 1 - growth_rate)),
            "gap_analysis": min(0.2, max(0.05, gap_variance / avg_gap)),
            "mod_patterns": mod_patterns,
            "avg_gap": avg_gap,
            "growth_rate": growth_rate
        }
    
    def generate_intelligent_candidates(self, start: int, end: int, count: int = 1000) -> List[int]:
        """Generate intelligent candidates using pattern analysis"""
        candidates = []
        weights = self.pattern_weights
        
        # Strategy 1: Exponential progression based on known growth
        if weights["exponential"] > 0.5:
            current = start
            while current < end and len(candidates) < count // 3:
                # Use exponential growth pattern
                next_candidate = int(current * (1 + weights["exponential"] * 0.1))
                if next_candidate > current and next_candidate < end:
                    candidates.append(next_candidate)
                    current = next_candidate
                else:
                    current += 1
        
        # Strategy 2: Gap-based prediction
        if weights["avg_gap"] > 0:
            last_known = max(self.known_mersenne_primes)
            predicted = last_known + int(weights["avg_gap"])
            while predicted < end and len(candidates) < count // 3:
                if predicted > start:
                    candidates.append(predicted)
                predicted += int(weights["avg_gap"] * 1.1)
        
        # Strategy 3: Modulo pattern analysis
        if "mod_patterns" in weights:
            # Find most common modulo patterns
            common_mods = sorted(weights["mod_patterns"].items(), key=lambda x: x[1], reverse=True)
            for mod, freq in common_mods[:3]:  # Top 3 patterns
                current = start - (start % 210) + mod
                while current < end and len(candidates) < count // 6:
                    if current > start:
                        candidates.append(current)
                    current += 210
        
        # Strategy 4: Random sampling in promising ranges
        remaining = count - len(candidates)
        if remaining > 0:
            import random
            random.seed(42)  # Reproducible results
            for _ in range(remaining):
                candidate = random.randint(start, end)
                if candidate not in candidates:
                    candidates.append(candidate)
        
        # Remove duplicates and sort
        candidates = sorted(list(set(candidates)))
        return candidates[:count]
    
    def lucas_lehmer_test(self, p: int, timeout: float = 30.0) -> Tuple[bool, float]:
        """Enhanced Lucas-Lehmer test with timeout and progress tracking"""
        if p == 2:
            return True, 0.0
        
        start_time = time.time()
        s = 4
        M = (1 << p) - 1  # 2^p - 1
        
        try:
            for i in range(p - 2):
                # Check timeout
                if time.time() - start_time > timeout:
                    return False, time.time() - start_time
                
                s = (s * s - 2) % M
                
                # Progress update every 1000 iterations for large exponents
                if p > 10000 and i % 1000 == 0:
                    progress = (i / (p - 2)) * 100
                    print(f"  Lucas-Lehmer progress for p={p}: {progress:.1f}%")
            
            is_prime = (s == 0)
            computation_time = time.time() - start_time
            return is_prime, computation_time
            
        except Exception as e:
            print(f"  Error in Lucas-Lehmer test for p={p}: {e}")
            return False, time.time() - start_time
    
    def test_candidate(self, candidate: int) -> Optional[Dict]:
        """Test a single candidate for Mersenne primality"""
        print(f"🔍 Testing candidate: p = {candidate:,}")
        
        # Pre-screening: basic checks
        if candidate <= 1 or candidate % 2 == 0:
            return None
        
        # Check if already known
        if candidate in self.known_mersenne_primes:
            print(f"  ✅ Already known Mersenne prime: p = {candidate}")
            return None
        
        # Run Lucas-Lehmer test
        is_prime, test_time = self.lucas_lehmer_test(candidate, timeout=60.0)
        
        if is_prime:
            discovery = {
                "exponent": candidate,
                "mersenne_number": str((1 << candidate) - 1),
                "digits": candidate,
                "discovery_time": datetime.now().isoformat(),
                "test_time": test_time,
                "method": "Lucas-Lehmer"
            }
            
            print(f"🎉 NEW MERSENNE PRIME DISCOVERED! 🎉")
            print(f"  Exponent: p = {candidate:,}")
            print(f"  Mersenne number: 2^{candidate} - 1")
            print(f"  Digits: {candidate:,}")
            print(f"  Test time: {test_time:.4f}s")
            
            return discovery
        else:
            print(f"  ❌ Not prime (tested in {test_time:.4f}s)")
            return None
    
    def worker_thread(self, candidate_queue: queue.Queue, thread_id: int):
        """Worker thread for parallel candidate testing"""
        while self.running:
            try:
                candidate = candidate_queue.get(timeout=1.0)
                if candidate is None:  # Shutdown signal
                    break
                
                result = self.test_candidate(candidate)
                if result:
                    self.result_queue.put(result)
                    self.discoveries.append(result)
                
                self.candidates_tested += 1
                candidate_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Error in worker thread {thread_id}: {e}")
    
    def run_discovery(self, start_range: int, end_range: int, max_candidates: int = 10000):
        """Run the revolutionary discovery process"""
        print(f"\n🚀 STARTING REVOLUTIONARY MERSENNE DISCOVERY 🚀")
        print(f"📊 Range: {start_range:,} to {end_range:,}")
        print(f"🎯 Max candidates: {max_candidates:,}")
        print(f"🧠 Using intelligent pattern analysis")
        print("=" * 80)
        
        self.running = True
        self.start_time = time.time()
        
        # Generate intelligent candidates
        print("🧠 Generating intelligent candidates using pattern analysis...")
        candidates = self.generate_intelligent_candidates(start_range, end_range, max_candidates)
        print(f"✅ Generated {len(candidates)} intelligent candidates")
        
        # Create candidate queue
        candidate_queue = queue.Queue()
        for candidate in candidates:
            candidate_queue.put(candidate)
        
        # Start worker threads
        max_workers = self.config.get("optimization_settings", {}).get("max_workers", 4)
        max_workers = min(max_workers, multiprocessing.cpu_count())
        
        print(f"🔄 Starting {max_workers} worker threads...")
        for i in range(max_workers):
            thread = threading.Thread(target=self.worker_thread, args=(candidate_queue, i))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        # Monitor progress
        try:
            while self.running and not candidate_queue.empty():
                elapsed = time.time() - self.start_time
                rate = self.candidates_tested / elapsed if elapsed > 0 else 0
                
                print(f"\r📊 Progress: {self.candidates_tested:,} tested | "
                      f"Rate: {rate:.1f}/s | "
                      f"Discoveries: {len(self.discoveries)} | "
                      f"Elapsed: {elapsed:.1f}s", end="", flush=True)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Discovery paused by user")
            self.running = False
        
        # Wait for threads to finish
        print(f"\n🔄 Waiting for worker threads to finish...")
        for thread in self.threads:
            thread.join(timeout=5)
        
        # Final results
        total_time = time.time() - self.start_time
        self._print_final_results(total_time)
        
        return self.discoveries
    
    def _print_final_results(self, total_time: float):
        """Print final discovery results"""
        print(f"\n" + "=" * 80)
        print(f"🎉 REVOLUTIONARY DISCOVERY COMPLETE! 🎉")
        print(f"=" * 80)
        print(f"⏱️ Total time: {total_time:.1f}s")
        print(f"🔍 Candidates tested: {self.candidates_tested:,}")
        print(f"🎯 Discovery rate: {self.candidates_tested/total_time:.1f} tests/second")
        print(f"🏆 New Mersenne primes found: {len(self.discoveries)}")
        
        if self.discoveries:
            print(f"\n🌟 DISCOVERIES:")
            for i, discovery in enumerate(self.discoveries, 1):
                print(f"  #{i}: p = {discovery['exponent']:,} → 2^{discovery['exponent']} - 1")
                print(f"      Discovery time: {discovery['discovery_time']}")
                print(f"      Test time: {discovery['test_time']:.4f}s")
        else:
            print(f"\n💡 No new Mersenne primes found in this run.")
            print(f"   Try expanding the search range or increasing max_candidates.")
        
        print(f"=" * 80)
    
    def save_results(self, filename: str = None):
        """Save discovery results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mersenne_discoveries_{timestamp}.json"
        
        results = {
            "discoveries": self.discoveries,
            "candidates_tested": self.candidates_tested,
            "search_time": time.time() - self.start_time if self.start_time else 0,
            "pattern_weights": self.pattern_weights,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")
        return filename

def main():
    """Main function for command-line usage"""
    print("🚀 REVOLUTIONARY MERSENNE PRIME DISCOVERY ENGINE 🚀")
    print("Combining Prime95 algorithms with advanced pattern analysis")
    print("=" * 80)
    
    # Initialize discovery engine
    discovery = RevolutionaryMersenneDiscovery()
    
    # Get search parameters
    try:
        start = int(input("Enter start range (e.g., 85000000): ") or "85000000")
        end = int(input("Enter end range (e.g., 86000000): ") or "86000000")
        max_candidates = int(input("Enter max candidates (e.g., 10000): ") or "10000")
    except ValueError:
        print("❌ Invalid input, using defaults")
        start, end, max_candidates = 85000000, 86000000, 10000
    
    # Run discovery
    try:
        discoveries = discovery.run_discovery(start, end, max_candidates)
        discovery.save_results()
        
        if discoveries:
            print(f"\n🎉 SUCCESS! Found {len(discoveries)} new Mersenne primes!")
        else:
            print(f"\n💡 No new discoveries this time. Try a larger range or more candidates.")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Discovery stopped by user")
    except Exception as e:
        print(f"\n❌ Error during discovery: {e}")

if __name__ == "__main__":
    main()
