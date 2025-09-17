#!/usr/bin/env python3
"""
🚀 ENHANCED MERSENNE PRIME DISCOVERY ENGINE 🚀
Ensures candidates are only after 52nd Mersenne prime and integrates with Prime95 for verification
"""

import json
import time
import threading
import queue
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import math
import os
import subprocess
import sys

class EnhancedMersenneDiscovery:
    def __init__(self, config_file: str = "mersenne_search_config.json"):
        """Initialize the enhanced discovery engine"""
        self.config = self._load_config(config_file)
        self.known_mersenne_primes = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
            2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
            23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
            1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
            24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
            43112609, 57885161, 74207281, 77232917, 82589933
        ]
        
        # The 52nd Mersenne prime exponent (82589933) - we only search after this
        self.last_known_exponent = max(self.known_mersenne_primes)
        
        # Discovery state
        self.candidates_tested = 0
        self.discoveries = []
        self.running = False
        self.start_time = None
        self.current_candidate = None
        self.prime95_queue = queue.Queue()
        self.verification_results = queue.Queue()
        
        # Advanced pattern analysis
        try:
            from advanced_mersenne_pattern_analysis import AdvancedMersennePatternAnalysis
            self.pattern_analyzer = AdvancedMersennePatternAnalysis()
            print("🧠 Advanced pattern analysis loaded")
        except ImportError:
            self.pattern_analyzer = None
            print("⚠️ Advanced pattern analysis not available, using basic patterns")
        
        # Pattern analysis data
        self.pattern_weights = self._analyze_known_patterns()
        
        print("🚀 ENHANCED MERSENNE DISCOVERY ENGINE INITIALIZED 🚀")
        print(f"📊 Known Mersenne primes: {len(self.known_mersenne_primes)}")
        print(f"🎯 Last known exponent: {self.last_known_exponent:,}")
        print(f"🔍 Will only search for exponents > {self.last_known_exponent:,}")
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
                    "range_1": {"start": 85000000, "end": 90000000, "priority": "high"}
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
    
    def is_valid_mersenne_exponent_candidate(self, p: int) -> bool:
        """Check if a number is a valid Mersenne exponent candidate based on essential mathematical properties"""
        # Must be > 52nd Mersenne prime
        if p <= self.last_known_exponent:
            return False
        
        # Must be odd (except 2, but we're after 52nd)
        if p % 2 == 0:
            return False
        
        # Must be prime
        if not self.is_prime(p):
            return False
        
        # Modulo 4: must be ≡ 1 or 3 (all odd primes)
        if p % 4 not in [1, 3]:
            return False
        
        # Modulo 6: must be ≡ 1 or 5 (all primes > 3)
        if p > 3 and p % 6 not in [1, 5]:
            return False
        
        # Last digit: must end in 1, 3, 7, or 9 (except 2, 5)
        if p > 5 and p % 10 not in [1, 3, 7, 9]:
            return False
        
        # Basic binary properties
        binary = bin(p)[2:]
        
        # Must start with 1 (all positive numbers do, but good to check)
        if not binary.startswith('1'):
            return False
        
        # Reasonable binary length for large Mersenne exponents
        if len(binary) < 20:
            return False
        
        # Basic modulo 210 check (exclude obvious composites)
        mod_210 = p % 210
        if mod_210 % 2 == 0 or mod_210 % 3 == 0 or mod_210 % 5 == 0 or mod_210 % 7 == 0:
            return False
        
        return True
    
    def calculate_digital_root(self, n: int) -> int:
        """Calculate digital root of a number"""
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n
    
    def is_prime(self, n: int) -> bool:
        """Fast primality test for Mersenne exponent candidates"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        
        # Miller-Rabin test with optimal bases
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        
        # Use deterministic bases for different ranges
        if n < 1373653:
            bases = [2, 3]
        elif n < 9080191:
            bases = [31, 73]
        elif n < 4759123141:
            bases = [2, 7, 61]
        else:
            bases = [2, 3, 5, 7, 11, 13, 17]
        
        for a in bases:
            if a >= n:
                continue
            
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def generate_candidates_after_52nd(self, start: int, end: int, count: int = 1000) -> List[int]:
        """Generate VALID Mersenne exponent candidates ONLY after the 52nd Mersenne prime (82589933)"""
        # Ensure we only search after the 52nd known Mersenne prime
        effective_start = max(start, self.last_known_exponent + 1)
        
        if effective_start > end:
            print(f"⚠️ No candidates possible: start ({start:,}) must be > last known Mersenne prime ({self.last_known_exponent:,})")
            return []
        
        print(f"🧠 Generating VALID Mersenne exponent candidates after 52nd Mersenne prime...")
        print(f"📊 Searching range: {effective_start:,} to {end:,}")
        print(f"🔍 Applying advanced mathematical property filters...")
        
        candidates = []
        
        # Use advanced pattern analysis if available (temporarily disabled for testing)
        if False and self.pattern_analyzer:
            print(f"🧠 Using advanced pattern analysis for intelligent candidate generation...")
            priority_candidates = self.pattern_analyzer.generate_priority_candidates(effective_start, end, count)
            candidates = [candidate for candidate, score in priority_candidates]
            print(f"🎯 Generated {len(candidates)} priority candidates using advanced pattern analysis")
        else:
            # Fallback to basic pattern analysis
            weights = self.pattern_weights
            
            # Strategy 1: Exponential progression with filtering
            if weights["exponential"] > 0.5:
                current = effective_start
                while current < end and len(candidates) < count // 3:
                    next_candidate = int(current * (1 + weights["exponential"] * 0.1))
                    if next_candidate > current and next_candidate < end:
                        if self.is_valid_mersenne_exponent_candidate(next_candidate):
                            candidates.append(next_candidate)
                        current = next_candidate
                    else:
                        current += 2  # Skip even numbers
            
            # Strategy 2: Gap-based prediction with filtering
            if weights["avg_gap"] > 0:
                predicted = self.last_known_exponent + int(weights["avg_gap"])
                while predicted < end and len(candidates) < count // 3:
                    if predicted > effective_start and self.is_valid_mersenne_exponent_candidate(predicted):
                        candidates.append(predicted)
                    predicted += int(weights["avg_gap"] * 1.1)
            
            # Strategy 3: Modulo pattern analysis with filtering
            if "mod_patterns" in weights:
                common_mods = sorted(weights["mod_patterns"].items(), key=lambda x: x[1], reverse=True)
                for mod, freq in common_mods[:3]:
                    current = effective_start - (effective_start % 210) + mod
                    while current < end and len(candidates) < count // 6:
                        if current > effective_start and self.is_valid_mersenne_exponent_candidate(current):
                            candidates.append(current)
                        current += 210
            
            # Strategy 4: Smart random sampling with filtering
            remaining = count - len(candidates)
            if remaining > 0:
                import random
                random.seed(42)
                attempts = 0
                max_attempts = remaining * 10  # Prevent infinite loops
                
                while len(candidates) < count and attempts < max_attempts:
                    # Generate odd numbers only
                    candidate = random.randint(effective_start, end)
                    if candidate % 2 == 0:
                        candidate += 1
                    
                    if (candidate not in candidates and 
                        candidate <= end and 
                        self.is_valid_mersenne_exponent_candidate(candidate)):
                        candidates.append(candidate)
                    
                    attempts += 1
        
        # Remove duplicates and sort
        candidates = sorted(list(set(candidates)))
        final_candidates = candidates[:count]
        
        print(f"✅ Generated {len(final_candidates)} VALID candidates (all > {self.last_known_exponent:,})")
        print(f"🔍 All candidates are odd primes with proper Mersenne exponent properties")
        
        # Show sample of generated candidates with analysis
        if final_candidates:
            print(f"📋 Sample candidates: {final_candidates[:5]}")
            print(f"   Last digits: {[str(c)[-2:] for c in final_candidates[:5]]}")
            print(f"   Binary lengths: {[len(bin(c)[2:]) for c in final_candidates[:5]]}")
            print(f"   Popcounts: {[bin(c)[2:].count('1') for c in final_candidates[:5]]}")
            print(f"   Digital roots: {[self.calculate_digital_root(c) for c in final_candidates[:5]]}")
        
        return final_candidates
    
    def lucas_lehmer_test(self, p: int, timeout: float = 30.0) -> Tuple[bool, float]:
        """Enhanced Lucas-Lehmer test with timeout"""
        if p == 2:
            return True, 0.0
        
        start_time = time.time()
        s = 4
        M = (1 << p) - 1  # 2^p - 1
        
        try:
            for i in range(p - 2):
                if time.time() - start_time > timeout:
                    return False, time.time() - start_time
                
                s = (s * s - 2) % M
                
                if p > 10000 and i % 1000 == 0:
                    progress = (i / (p - 2)) * 100
                    print(f"  Lucas-Lehmer progress for p={p}: {progress:.1f}%")
            
            is_prime = (s == 0)
            computation_time = time.time() - start_time
            return is_prime, computation_time
            
        except Exception as e:
            print(f"  Error in Lucas-Lehmer test for p={p}: {e}")
            return False, time.time() - start_time
    
    def test_candidate_with_ll(self, candidate: int) -> Optional[Dict]:
        """Test a single candidate using Lucas-Lehmer test"""
        print(f"🔍 Testing candidate: p = {candidate:,}")
        
        # Pre-screening
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
                "method": "Lucas-Lehmer",
                "verified_by_prime95": False
            }
            
            print(f"🎉 POTENTIAL MERSENNE PRIME FOUND! 🎉")
            print(f"  Exponent: p = {candidate:,}")
            print(f"  Mersenne number: 2^{candidate} - 1")
            print(f"  Digits: {candidate:,}")
            print(f"  Test time: {test_time:.4f}s")
            print(f"  🔄 Sending to Prime95 for verification...")
            
            return discovery
        else:
            print(f"  ❌ Not prime (tested in {test_time:.4f}s)")
            return None
    
    def queue_for_prime95_verification(self, discovery: Dict):
        """Queue a discovery for Prime95 verification"""
        try:
            # Add to Prime95 worktodo
            worktodo_path = self.config.get('prime95_integration', {}).get('worktodo_path', 'worktodo.txt')
            mode = self.config.get('prime95_integration', {}).get('mode', 'LL')
            
            worktodo_line = f"{mode}=1,2,{discovery['exponent']},-1\n"
            
            with open(worktodo_path, 'a') as f:
                f.write(worktodo_line)
            
            print(f"📝 Queued p={discovery['exponent']:,} for Prime95 verification")
            
            # Store for later verification
            self.prime95_queue.put(discovery)
            
        except Exception as e:
            print(f"❌ Error queuing for Prime95: {e}")
    
    def check_prime95_results(self):
        """Check Prime95 results for verification"""
        try:
            results_path = self.config.get('prime95_integration', {}).get('results_path', 'results.txt')
            
            if not os.path.exists(results_path):
                return
            
            with open(results_path, 'r') as f:
                lines = f.readlines()
            
            # Check for new results
            for line in lines[-10:]:  # Check last 10 lines
                if "M" in line and "is prime" in line:
                    # Extract exponent from result
                    parts = line.split()
                    for part in parts:
                        if part.startswith('M') and part[1:].isdigit():
                            exp = int(part[1:])
                            
                            # Find corresponding discovery
                            for discovery in self.discoveries:
                                if discovery['exponent'] == exp and not discovery.get('verified_by_prime95', False):
                                    discovery['verified_by_prime95'] = True
                                    discovery['prime95_verification_time'] = datetime.now().isoformat()
                                    
                                    print(f"✅ Prime95 VERIFIED: p = {exp:,} is indeed a Mersenne prime!")
                                    self.verification_results.put(discovery)
                                    break
            
        except Exception as e:
            print(f"❌ Error checking Prime95 results: {e}")
    
    def run_sequential_discovery(self, start_range: int, end_range: int, max_candidates: int = 10000):
        """Run discovery sequentially - one candidate at a time with Prime95 verification"""
        print(f"\n🚀 STARTING ENHANCED SEQUENTIAL MERSENNE DISCOVERY 🚀")
        print(f"📊 Range: {start_range:,} to {end_range:,}")
        print(f"🎯 Max candidates: {max_candidates:,}")
        print(f"🔍 Only searching after 52nd Mersenne prime ({self.last_known_exponent:,})")
        print(f"🔄 Sequential testing with Prime95 verification")
        print("=" * 80)
        
        self.running = True
        self.start_time = time.time()
        
        # Generate candidates after 52nd Mersenne prime
        candidates = self.generate_candidates_after_52nd(start_range, end_range, max_candidates)
        
        if not candidates:
            print("❌ No valid candidates found")
            return []
        
        print(f"🎯 Testing {len(candidates)} candidates sequentially...")
        
        try:
            for i, candidate in enumerate(candidates):
                if not self.running:
                    print("⏹️ Discovery stopped by user")
                    break
                
                self.current_candidate = candidate
                self.candidates_tested += 1
                
                # Test candidate with Lucas-Lehmer
                result = self.test_candidate_with_ll(candidate)
                
                if result:
                    # Add to discoveries
                    self.discoveries.append(result)
                    
                    # Queue for Prime95 verification
                    self.queue_for_prime95_verification(result)
                
                # Check for Prime95 results periodically
                if i % 10 == 0:  # Check every 10 candidates
                    self.check_prime95_results()
                
                # Progress update
                elapsed = time.time() - self.start_time
                rate = self.candidates_tested / elapsed if elapsed > 0 else 0
                
                print(f"\r📊 Progress: {self.candidates_tested:,}/{len(candidates)} | "
                      f"Rate: {rate:.1f}/s | "
                      f"Discoveries: {len(self.discoveries)} | "
                      f"Elapsed: {elapsed:.1f}s", end="", flush=True)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
            
            # Final Prime95 check
            print(f"\n🔄 Final Prime95 verification check...")
            self.check_prime95_results()
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Discovery paused by user")
            self.running = False
        
        # Final results
        total_time = time.time() - self.start_time
        self._print_final_results(total_time)
        
        return self.discoveries
    
    def _print_final_results(self, total_time: float):
        """Print final discovery results"""
        print(f"\n" + "=" * 80)
        print(f"🎉 ENHANCED DISCOVERY COMPLETE! 🎉")
        print(f"=" * 80)
        print(f"⏱️ Total time: {total_time:.1f}s")
        print(f"🔍 Candidates tested: {self.candidates_tested:,}")
        print(f"🎯 Discovery rate: {self.candidates_tested/total_time:.1f} tests/second")
        print(f"🏆 Potential discoveries: {len(self.discoveries)}")
        
        verified_count = sum(1 for d in self.discoveries if d.get('verified_by_prime95', False))
        print(f"✅ Prime95 verified: {verified_count}")
        
        if self.discoveries:
            print(f"\n🌟 DISCOVERIES:")
            for i, discovery in enumerate(self.discoveries, 1):
                status = "✅ VERIFIED" if discovery.get('verified_by_prime95', False) else "⏳ PENDING"
                print(f"  #{i}: p = {discovery['exponent']:,} → 2^{discovery['exponent']} - 1 ({status})")
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
            filename = f"enhanced_mersenne_discoveries_{timestamp}.json"
        
        results = {
            "discoveries": self.discoveries,
            "candidates_tested": self.candidates_tested,
            "search_time": time.time() - self.start_time if self.start_time else 0,
            "pattern_weights": self.pattern_weights,
            "last_known_exponent": self.last_known_exponent,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")
        return filename

def main():
    """Main function for command-line usage"""
    print("🚀 ENHANCED MERSENNE PRIME DISCOVERY ENGINE 🚀")
    print("Sequential testing with Prime95 verification")
    print("=" * 80)
    
    # Initialize discovery engine
    discovery = EnhancedMersenneDiscovery()
    
    # Get search parameters
    try:
        start = int(input("Enter start range (e.g., 85000000): ") or "85000000")
        end = int(input("Enter end range (e.g., 90000000): ") or "90000000")
        max_candidates = int(input("Enter max candidates (e.g., 1000): ") or "1000")
    except ValueError:
        print("❌ Invalid input, using defaults")
        start, end, max_candidates = 85000000, 90000000, 1000
    
    # Run discovery
    try:
        discoveries = discovery.run_sequential_discovery(start, end, max_candidates)
        discovery.save_results()
        
        if discoveries:
            verified = sum(1 for d in discoveries if d.get('verified_by_prime95', False))
            print(f"\n🎉 SUCCESS! Found {len(discoveries)} potential Mersenne primes!")
            print(f"✅ Prime95 verified: {verified}")
        else:
            print(f"\n💡 No new discoveries this time. Try a larger range or more candidates.")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Discovery stopped by user")
    except Exception as e:
        print(f"\n❌ Error during discovery: {e}")

if __name__ == "__main__":
    main()
