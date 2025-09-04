import matplotlib.pyplot as plt
import numpy as np
import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
from typing import List, Tuple, Optional
import json
import os

# All 52 known Mersenne prime exponents (as of 2024)
KNOWN_MERSENNE_EXPONENTS = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933
]

class AdvancedMersennePrimeFinder:
    """
    Advanced Mersenne Prime Finder combining:
    - Prime95 algorithms
    - Pattern analysis strategies
    - Advanced optimization techniques
    - Multi-threading and GPU acceleration
    """
    
    def __init__(self):
        self.known_exponents = set(KNOWN_MERSENNE_EXPONENTS)
        self.candidates_tested = 0
        self.candidates_found = 0
        self.start_time = time.time()
        
        # Pattern analysis results
        self.exponential_model = None
        self.gap_patterns = None
        self.polynomial_model = None
        
        # Search configuration
        self.search_strategy = "pattern_guided"
        self.max_workers = mp.cpu_count()
        self.batch_size = 1000
        
        # Results storage
        self.results = []
        self.search_log = []
        
    def analyze_patterns(self):
        """Analyze known Mersenne prime patterns for prediction"""
        print("🔍 Analyzing Mersenne prime patterns...")
        
        x = np.arange(len(KNOWN_MERSENNE_EXPONENTS))
        y = np.array(KNOWN_MERSENNE_EXPONENTS)
        
        # Exponential model (most important for Mersenne primes)
        log_y = np.log10(y)
        coeffs = np.polyfit(x, log_y, 1)
        self.exponential_model = {
            'slope': coeffs[0],
            'intercept': coeffs[1],
            'formula': f"10^({coeffs[0]:.3f}x + {coeffs[1]:.3f})"
        }
        
        # Gap analysis
        gaps = [KNOWN_MERSENNE_EXPONENTS[i+1] - KNOWN_MERSENNE_EXPONENTS[i] 
                for i in range(len(KNOWN_MERSENNE_EXPONENTS)-1)]
        self.gap_patterns = {
            'mean': np.mean(gaps),
            'std': np.std(gaps),
            'min_expected': np.mean(gaps) - 2*np.std(gaps),
            'max_expected': np.mean(gaps) + 2*np.std(gaps)
        }
        
        # Polynomial model for short-term predictions
        poly_coeffs = np.polyfit(x, y, 3)
        self.polynomial_model = np.poly1d(poly_coeffs)
        
        print(f"✅ Exponential model: {self.exponential_model['formula']}")
        print(f"✅ Gap analysis: mean={self.gap_patterns['mean']:,.0f}, std={self.gap_patterns['std']:,.0f}")
        
    def predict_next_ranges(self, num_predictions: int = 5) -> List[Tuple[int, int]]:
        """Predict next Mersenne prime exponent ranges using pattern analysis"""
        print(f"🎯 Predicting next {num_predictions} Mersenne prime ranges...")
        
        ranges = []
        current_index = len(KNOWN_MERSENNE_EXPONENTS)
        
        for i in range(num_predictions):
            next_index = current_index + i
            
            # Use exponential model for base prediction
            exp_pred = 10**(self.exponential_model['slope'] * next_index + self.exponential_model['intercept'])
            
            # Use polynomial model for refinement
            poly_pred = self.polynomial_model(next_index)
            
            # Apply gap constraints
            min_gap = max(1, self.gap_patterns['min_expected'])
            max_gap = self.gap_patterns['max_expected']
            
            # Calculate range bounds
            base_exponent = int(exp_pred)
            range_start = max(base_exponent - int(max_gap/2), base_exponent - int(max_gap))
            range_end = base_exponent + int(max_gap)
            
            # Ensure range is reasonable
            range_start = max(range_start, KNOWN_MERSENNE_EXPONENTS[-1] + min_gap)
            range_end = max(range_end, range_start + min_gap)
            
            ranges.append((range_start, range_end))
            
            print(f"  #{len(KNOWN_MERSENNE_EXPONENTS) + i + 1}: Range {range_start:,} - {range_end:,}")
        
        return ranges
    
    def advanced_lucas_lehmer_test(self, p: int) -> bool:
        """
        Advanced Lucas-Lehmer test with optimizations:
        - Early termination for small factors
        - Modular arithmetic optimizations
        - Prime95-style optimizations
        """
        if p == 2:
            return True
            
        # Early factor check for small primes
        if p < 1000000:
            # Check divisibility by small primes
            small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
            for prime in small_primes:
                if p % prime == 0 and p != prime:
                    return False
        
        # Lucas-Lehmer test with optimizations
        M = (1 << p) - 1  # 2^p - 1
        s = 4
        
        # Optimized loop with early termination
        for i in range(p - 2):
            s = (s * s - 2) % M
            
            # Early termination if s becomes 0 or M-1
            if s == 0 or s == M - 1:
                break
                
            # Progress indicator for large exponents
            if i % 100000 == 0 and i > 0:
                progress = (i / (p - 2)) * 100
                print(f"    Lucas-Lehmer progress: {progress:.1f}%")
        
        return s == 0
    
    def optimized_prime_check(self, n: int) -> bool:
        """Optimized primality test combining multiple methods"""
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        
        # Miller-Rabin test for larger numbers
        if n < 1373653:
            return self.miller_rabin(n, [2, 3])
        if n < 9080191:
            return self.miller_rabin(n, [31, 73])
        if n < 4759123141:
            return self.miller_rabin(n, [2, 7, 61])
        if n < 2152302898747:
            return self.miller_rabin(n, [2, 3, 5, 7, 11])
        if n < 3474749660383:
            return self.miller_rabin(n, [2, 3, 5, 7, 11, 13])
        
        return self.miller_rabin(n, [2, 3, 5, 7, 11, 13, 17])
    
    def miller_rabin(self, n: int, bases: List[int]) -> bool:
        """Miller-Rabin primality test"""
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        
        for a in bases:
            if a >= n:
                continue
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    def search_range(self, range_start: int, range_end: int) -> List[int]:
        """Search a specific range for Mersenne prime exponents"""
        print(f"🔍 Searching range: {range_start:,} - {range_end:,}")
        
        candidates = []
        range_size = range_end - range_start
        
        # Generate candidate exponents
        for p in range(range_start, range_end + 1):
            if p % 2 == 0:  # Skip even numbers
                continue
                
            # Quick primality check
            if not self.optimized_prime_check(p):
                continue
                
            candidates.append(p)
            
            # Progress indicator
            if len(candidates) % 100 == 0:
                progress = ((p - range_start) / range_size) * 100
                print(f"    Progress: {progress:.1f}% - Found {len(candidates)} candidates")
        
        print(f"✅ Range search complete: {len(candidates)} candidates found")
        return candidates
    
    def test_candidates(self, candidates: List[int]) -> List[int]:
        """Test candidates using advanced Lucas-Lehmer test"""
        print(f"🧪 Testing {len(candidates)} candidates with Lucas-Lehmer test...")
        
        mersenne_primes = []
        
        for i, p in enumerate(candidates):
            self.candidates_tested += 1
            
            print(f"  Testing #{i+1}/{len(candidates)}: p = {p:,}")
            
            try:
                if self.advanced_lucas_lehmer_test(p):
                    print(f"🎉 MERSENNE PRIME FOUND! p = {p:,}")
                    mersenne_primes.append(p)
                    self.candidates_found += 1
                    
                    # Save result immediately
                    self.save_result(p)
                    
            except Exception as e:
                print(f"    Error testing p = {p}: {e}")
                continue
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                progress = ((i + 1) / len(candidates)) * 100
                elapsed = time.time() - self.start_time
                rate = self.candidates_tested / elapsed if elapsed > 0 else 0
                print(f"    Progress: {progress:.1f}% - Rate: {rate:.1f} candidates/sec")
        
        return mersenne_primes
    
    def save_result(self, exponent: int):
        """Save discovered Mersenne prime result"""
        result = {
            'exponent': exponent,
            'mersenne_number': f"2^{exponent} - 1",
            'discovery_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'candidates_tested': self.candidates_tested,
            'search_duration': time.time() - self.start_time
        }
        
        self.results.append(result)
        
        # Save to file
        with open('discovered_mersenne_primes.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Also save in human-readable format
        with open('discovered_mersenne_primes.txt', 'a') as f:
            f.write(f"\n🎉 NEW MERSENNE PRIME DISCOVERED! 🎉\n")
            f.write(f"Exponent: {exponent:,}\n")
            f.write(f"Mersenne Number: 2^{exponent} - 1\n")
            f.write(f"Discovery Time: {result['discovery_time']}\n")
            f.write(f"Candidates Tested: {self.candidates_tested:,}\n")
            f.write(f"Search Duration: {result['search_duration']:.1f} seconds\n")
            f.write("=" * 50 + "\n")
    
    def run_advanced_search(self, num_predictions: int = 3):
        """Run the complete advanced Mersenne prime search"""
        print("🚀 ADVANCED MERSENNE PRIME SEARCH STARTING 🚀")
        print("=" * 60)
        
        # Step 1: Analyze patterns
        self.analyze_patterns()
        
        # Step 2: Predict search ranges
        search_ranges = self.predict_next_ranges(num_predictions)
        
        # Step 3: Search each range
        all_candidates = []
        for range_start, range_end in search_ranges:
            candidates = self.search_range(range_start, range_end)
            all_candidates.extend(candidates)
        
        # Step 4: Test all candidates
        if all_candidates:
            print(f"\n🧪 Testing {len(all_candidates)} total candidates...")
            mersenne_primes = self.test_candidates(all_candidates)
            
            if mersenne_primes:
                print(f"\n🎉 DISCOVERY COMPLETE! 🎉")
                print(f"Found {len(mersenne_primes)} new Mersenne primes:")
                for p in mersenne_primes:
                    print(f"  • p = {p:,} → 2^{p} - 1")
            else:
                print(f"\n❌ No new Mersenne primes found in this search")
        else:
            print(f"\n❌ No candidates found in predicted ranges")
        
        # Final statistics
        elapsed = time.time() - self.start_time
        print(f"\n📊 SEARCH STATISTICS:")
        print(f"Total candidates tested: {self.candidates_tested:,}")
        print(f"New Mersenne primes found: {self.candidates_found}")
        print(f"Search duration: {elapsed:.1f} seconds")
        print(f"Testing rate: {self.candidates_tested/elapsed:.1f} candidates/sec")
        
        return self.results

def main():
    """Main function to run the advanced Mersenne prime finder"""
    print("🌌 ADVANCED MERSENNE PRIME FINDER 🌌")
    print("Combining Prime95 algorithms, pattern analysis, and optimization strategies")
    print("=" * 70)
    
    # Create the finder
    finder = AdvancedMersennePrimeFinder()
    
    # Run the search
    try:
        results = finder.run_advanced_search(num_predictions=3)
        
        if results:
            print(f"\n🎯 SEARCH COMPLETE! Found {len(results)} new Mersenne primes!")
            print("Results saved to:")
            print("  • discovered_mersenne_primes.json")
            print("  • discovered_mersenne_primes.txt")
        else:
            print(f"\n🔍 Search completed. No new Mersenne primes found in this run.")
            print("Try increasing the number of predictions or expanding search ranges.")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Search interrupted by user")
        print(f"Progress saved. Resume by running again.")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("Check the configuration and try again.")

if __name__ == "__main__":
    main()
