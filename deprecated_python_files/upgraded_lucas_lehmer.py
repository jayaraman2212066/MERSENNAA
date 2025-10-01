#!/usr/bin/env python3
"""
🚀 UPGRADED LUCAS-LEHMER TEST 🚀
Python implementation with gmpy2, multiprocessing, and advanced optimizations
"""

import gmpy2
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from typing import List, Tuple, Optional
import psutil

class UpgradedLucasLehmer:
    def __init__(self):
        # Set high precision for gmpy2
        gmpy2.get_context().precision = 1000000
        
    def upgraded_lucas_lehmer_test(self, p: int, progress_callback=None) -> bool:
        """
        Upgraded Lucas-Lehmer test with multiple optimizations
        """
        if p == 2:
            return True
        if p <= 1 or p % 2 == 0:
            return False
            
        print(f"🚀 Starting upgraded Lucas-Lehmer test for p={p}")
        start_time = time.time()
        
        # Use gmpy2 for arbitrary precision arithmetic
        s = gmpy2.mpz(4)
        M = gmpy2.mpz(2) ** p - 1
        
        # Optimized iteration with progress tracking
        iterations = p - 2
        checkpoint_interval = max(1, iterations // 100)  # 1% intervals
        
        for i in range(iterations):
            # Core Lucas-Lehmer iteration: s = (s² - 2) mod M
            s = (s * s - 2) % M
            
            # Progress reporting
            if progress_callback and i % checkpoint_interval == 0:
                progress = (i / iterations) * 100
                elapsed = time.time() - start_time
                eta = (elapsed / (i + 1)) * (iterations - i - 1) if i > 0 else 0
                progress_callback(progress, i, iterations, elapsed, eta)
            
            # Memory optimization: force garbage collection periodically
            if i % 10000 == 0 and i > 0:
                import gc
                gc.collect()
        
        result = (s == 0)
        total_time = time.time() - start_time
        
        print(f"✅ Lucas-Lehmer test completed in {total_time:.2f}s")
        print(f"🎯 Result: {'PRIME' if result else 'COMPOSITE'}")
        
        return result
    
    def batch_lucas_lehmer_test(self, candidates: List[int], max_workers: Optional[int] = None) -> List[Tuple[int, bool]]:
        """
        Parallel batch testing of multiple candidates
        """
        if max_workers is None:
            max_workers = min(len(candidates), psutil.cpu_count())
        
        print(f"🚀 Starting batch Lucas-Lehmer tests for {len(candidates)} candidates")
        print(f"🧵 Using {max_workers} parallel workers")
        
        results = []
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            future_to_candidate = {
                executor.submit(self._single_test_worker, p): p 
                for p in candidates
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_candidate):
                p = future_to_candidate[future]
                try:
                    result = future.result()
                    results.append((p, result))
                    completed += 1
                    
                    if result:
                        print(f"🎉 MERSENNE PRIME FOUND: 2^{p} - 1")
                    
                    progress = (completed / len(candidates)) * 100
                    elapsed = time.time() - start_time
                    print(f"📊 Progress: {progress:.1f}% ({completed}/{len(candidates)}) - {elapsed:.1f}s elapsed")
                    
                except Exception as e:
                    print(f"❌ Error testing p={p}: {e}")
                    results.append((p, False))
        
        total_time = time.time() - start_time
        primes_found = sum(1 for _, is_prime in results if is_prime)
        
        print(f"✅ Batch testing completed in {total_time:.2f}s")
        print(f"🏆 Found {primes_found} Mersenne primes out of {len(candidates)} candidates")
        
        return sorted(results)
    
    def _single_test_worker(self, p: int) -> bool:
        """Worker function for parallel processing"""
        return self.upgraded_lucas_lehmer_test(p)
    
    def optimized_small_test(self, p: int) -> bool:
        """Optimized test for small exponents (p <= 64)"""
        if p <= 64:
            s = 4
            M = (1 << p) - 1
            
            for _ in range(p - 2):
                s = ((s * s) - 2) % M
            
            return s == 0
        
        return self.upgraded_lucas_lehmer_test(p)

class AdvancedMersenneAnalyzer:
    def __init__(self):
        self.ll_test = UpgradedLucasLehmer()
        
    def smart_candidate_generation(self, start: int, end: int, max_candidates: int = 100) -> List[int]:
        """
        Generate smart candidates based on known patterns
        """
        print(f"🧠 Generating smart candidates in range [{start}, {end}]")
        
        candidates = []
        
        # Known Mersenne exponents for pattern analysis
        known_mersenne_exponents = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
            3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243,
            110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
            6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
            37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933
        ]
        
        # Pattern analysis
        for p in range(start, min(end + 1, start + max_candidates * 10)):
            if p % 2 == 0:  # Skip even numbers
                continue
                
            # Must be prime
            if not self._is_prime_fast(p):
                continue
            
            # Apply heuristic filters based on known patterns
            if self._passes_heuristic_filters(p, known_mersenne_exponents):
                candidates.append(p)
                
            if len(candidates) >= max_candidates:
                break
        
        print(f"📊 Generated {len(candidates)} smart candidates")
        return candidates
    
    def _is_prime_fast(self, n: int) -> bool:
        """Fast primality test using gmpy2"""
        return gmpy2.is_prime(n)
    
    def _passes_heuristic_filters(self, p: int, known_exponents: List[int]) -> bool:
        """Apply heuristic filters based on known Mersenne prime patterns"""
        
        # Filter 1: Modular patterns
        if p % 4 == 1:  # Slight preference for p ≡ 3 (mod 4)
            return True
        
        # Filter 2: Gap analysis - look for similar gaps to known primes
        if len(known_exponents) >= 2:
            recent_gaps = [known_exponents[i+1] - known_exponents[i] for i in range(-5, -1)]
            avg_gap = sum(recent_gaps) / len(recent_gaps)
            
            # Prefer candidates near expected gap size
            last_known = known_exponents[-1]
            expected_next = last_known + avg_gap
            
            if abs(p - expected_next) / expected_next < 0.5:  # Within 50% of expected
                return True
        
        # Filter 3: Digit sum patterns (weak heuristic)
        digit_sum = sum(int(d) for d in str(p))
        if digit_sum % 3 != 0:  # Avoid multiples of 3 in digit sum
            return True
        
        return False
    
    def comprehensive_search(self, start_range: int, end_range: int, batch_size: int = 50):
        """
        Comprehensive search with smart candidate generation and batch processing
        """
        print(f"🔍 Starting comprehensive Mersenne prime search")
        print(f"📍 Range: [{start_range}, {end_range}]")
        print(f"📦 Batch size: {batch_size}")
        
        all_results = []
        current_start = start_range
        
        while current_start <= end_range:
            current_end = min(current_start + batch_size * 100, end_range)
            
            # Generate smart candidates for this batch
            candidates = self.smart_candidate_generation(current_start, current_end, batch_size)
            
            if not candidates:
                current_start = current_end + 1
                continue
            
            # Test candidates in parallel
            batch_results = self.ll_test.batch_lucas_lehmer_test(candidates)
            all_results.extend(batch_results)
            
            # Report batch results
            primes_in_batch = [p for p, is_prime in batch_results if is_prime]
            if primes_in_batch:
                print(f"🎉 Batch [{current_start}, {current_end}] found primes: {primes_in_batch}")
            
            current_start = current_end + 1
        
        # Final summary
        all_primes = [p for p, is_prime in all_results if is_prime]
        print(f"\n🏆 SEARCH COMPLETE!")
        print(f"📊 Total candidates tested: {len(all_results)}")
        print(f"🎯 Mersenne primes found: {len(all_primes)}")
        
        if all_primes:
            print(f"🌟 Discovered primes: {all_primes}")
        
        return all_results

def progress_callback(progress: float, current: int, total: int, elapsed: float, eta: float):
    """Progress callback for Lucas-Lehmer test"""
    print(f"\r📊 Progress: {progress:.1f}% ({current}/{total}) | "
          f"⏱️ Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s", end="", flush=True)

def main():
    print("🚀 UPGRADED LUCAS-LEHMER TEST SYSTEM 🚀")
    
    # Test known Mersenne primes for verification
    ll_test = UpgradedLucasLehmer()
    
    print("\n🧪 Testing known Mersenne primes:")
    known_primes = [3, 5, 7, 13, 17, 19, 31]
    
    for p in known_primes:
        result = ll_test.optimized_small_test(p)
        print(f"p={p}: {'✅ PRIME' if result else '❌ COMPOSITE'}")
    
    # Test batch processing
    print("\n🚀 Testing batch processing:")
    test_candidates = [61, 89, 107, 127]  # Known Mersenne primes
    batch_results = ll_test.batch_lucas_lehmer_test(test_candidates, max_workers=2)
    
    # Comprehensive search demo
    print("\n🔍 Comprehensive search demo:")
    analyzer = AdvancedMersenneAnalyzer()
    
    # Search in a small range for demonstration
    search_results = analyzer.comprehensive_search(1000, 2000, batch_size=10)
    
    print("\n✅ Upgraded Lucas-Lehmer test system ready!")

if __name__ == "__main__":
    main()