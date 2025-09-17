#!/usr/bin/env python3
"""
🧠 ADVANCED MERSENNE PATTERN ANALYSIS 🧠
Comprehensive analysis of Mersenne exponent patterns based on all 52 known exponents
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Set
from collections import Counter
import json

class AdvancedMersennePatternAnalysis:
    def __init__(self):
        """Initialize with all 52 known Mersenne prime exponents"""
        self.known_exponents = [
            2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
            2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
            23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
            1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
            24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
            43112609, 57885161, 74207281, 77232917, 82589933, 136279841
        ]
        
        # Analyze all patterns
        self.patterns = self._analyze_all_patterns()
        print(f"🧠 Advanced Mersenne Pattern Analysis initialized")
        print(f"📊 Analyzed {len(self.known_exponents)} known Mersenne exponents")
    
    def _analyze_all_patterns(self) -> Dict:
        """Comprehensive pattern analysis of all known Mersenne exponents"""
        patterns = {}
        
        # 1. Basic Properties
        patterns["basic"] = self._analyze_basic_properties()
        
        # 2. Binary Analysis
        patterns["binary"] = self._analyze_binary_properties()
        
        # 3. Digit Analysis
        patterns["digits"] = self._analyze_digit_properties()
        
        # 4. Modulo Analysis
        patterns["modulo"] = self._analyze_modulo_properties()
        
        # 5. Gap Analysis
        patterns["gaps"] = self._analyze_gap_properties()
        
        # 6. Suffix Analysis
        patterns["suffixes"] = self._analyze_suffix_patterns()
        
        # 7. Special Prime Properties
        patterns["special_primes"] = self._analyze_special_prime_properties()
        
        # 8. Hex Patterns
        patterns["hex"] = self._analyze_hex_patterns()
        
        # 9. Statistical Properties
        patterns["statistics"] = self._analyze_statistical_properties()
        
        return patterns
    
    def _analyze_basic_properties(self) -> Dict:
        """Analyze basic mathematical properties"""
        return {
            "all_prime": all(self._is_prime(p) for p in self.known_exponents),
            "all_odd_except_2": all(p % 2 == 1 or p == 2 for p in self.known_exponents),
            "last_digits": [p % 10 for p in self.known_exponents],
            "first_digits": [int(str(p)[0]) for p in self.known_exponents],
            "lengths": [len(str(p)) for p in self.known_exponents]
        }
    
    def _analyze_binary_properties(self) -> Dict:
        """Analyze binary representation properties"""
        binary_data = []
        for p in self.known_exponents:
            binary = bin(p)[2:]
            binary_data.append({
                "exponent": p,
                "binary": binary,
                "length": len(binary),
                "popcount": binary.count('1'),
                "starts_with_1": binary.startswith('1'),
                "ends_with_1": binary.endswith('1'),
                "has_pattern_111": '111' in binary,
                "has_pattern_000": '000' in binary
            })
        
        return {
            "data": binary_data,
            "length_stats": {
                "min": min(d["length"] for d in binary_data),
                "max": max(d["length"] for d in binary_data),
                "mean": np.mean([d["length"] for d in binary_data]),
                "median": np.median([d["length"] for d in binary_data])
            },
            "popcount_stats": {
                "min": min(d["popcount"] for d in binary_data),
                "max": max(d["popcount"] for d in binary_data),
                "mean": np.mean([d["popcount"] for d in binary_data]),
                "median": np.median([d["popcount"] for d in binary_data])
            },
            "all_start_with_1": all(d["starts_with_1"] for d in binary_data),
            "all_end_with_1": all(d["ends_with_1"] for d in binary_data)
        }
    
    def _analyze_digit_properties(self) -> Dict:
        """Analyze digit patterns and properties"""
        digit_sums = [sum(int(d) for d in str(p)) for p in self.known_exponents]
        digital_roots = [self._calculate_digital_root(p) for p in self.known_exponents]
        
        return {
            "digit_sums": digit_sums,
            "digital_roots": digital_roots,
            "digit_sum_stats": {
                "min": min(digit_sums),
                "max": max(digit_sums),
                "mean": np.mean(digit_sums),
                "median": np.median(digit_sums)
            },
            "digital_root_distribution": Counter(digital_roots),
            "last_digit_distribution": Counter([p % 10 for p in self.known_exponents]),
            "first_digit_distribution": Counter([int(str(p)[0]) for p in self.known_exponents])
        }
    
    def _analyze_modulo_properties(self) -> Dict:
        """Analyze modular arithmetic properties"""
        mod_2 = [p % 2 for p in self.known_exponents]
        mod_3 = [p % 3 for p in self.known_exponents]
        mod_4 = [p % 4 for p in self.known_exponents]
        mod_6 = [p % 6 for p in self.known_exponents]
        mod_10 = [p % 10 for p in self.known_exponents]
        mod_210 = [p % 210 for p in self.known_exponents]
        
        return {
            "mod_2": {"values": mod_2, "distribution": Counter(mod_2)},
            "mod_3": {"values": mod_3, "distribution": Counter(mod_3)},
            "mod_4": {"values": mod_4, "distribution": Counter(mod_4)},
            "mod_6": {"values": mod_6, "distribution": Counter(mod_6)},
            "mod_10": {"values": mod_10, "distribution": Counter(mod_10)},
            "mod_210": {"values": mod_210, "distribution": Counter(mod_210)},
            "preferred_mod_210": sorted(set(mod_210))
        }
    
    def _analyze_gap_properties(self) -> Dict:
        """Analyze gaps between consecutive exponents"""
        gaps = []
        for i in range(1, len(self.known_exponents)):
            gap = self.known_exponents[i] - self.known_exponents[i-1]
            gaps.append(gap)
        
        return {
            "gaps": gaps,
            "min_gap": min(gaps),
            "max_gap": max(gaps),
            "mean_gap": np.mean(gaps),
            "median_gap": np.median(gaps),
            "std_gap": np.std(gaps),
            "gap_distribution": Counter(gaps)
        }
    
    def _analyze_suffix_patterns(self) -> Dict:
        """Analyze suffix patterns (last 2-3 digits)"""
        last_two = [str(p)[-2:] for p in self.known_exponents if len(str(p)) >= 2]
        last_three = [str(p)[-3:] for p in self.known_exponents if len(str(p)) >= 3]
        
        return {
            "last_two": {
                "values": last_two,
                "distribution": Counter(last_two),
                "most_common": Counter(last_two).most_common(10)
            },
            "last_three": {
                "values": last_three,
                "distribution": Counter(last_three),
                "most_common": Counter(last_three).most_common(10)
            },
            "repeated_suffixes": [suffix for suffix, count in Counter(last_two).items() if count > 1]
        }
    
    def _analyze_special_prime_properties(self) -> Dict:
        """Analyze special prime properties (Sophie Germain, Safe primes)"""
        sophie_germain = []
        safe_primes = []
        
        for p in self.known_exponents:
            if self._is_prime(2 * p + 1):
                sophie_germain.append(p)
            if p > 2 and self._is_prime((p - 1) // 2):
                safe_primes.append(p)
        
        return {
            "sophie_germain": sophie_germain,
            "safe_primes": safe_primes,
            "sophie_germain_count": len(sophie_germain),
            "safe_prime_count": len(safe_primes)
        }
    
    def _analyze_hex_patterns(self) -> Dict:
        """Analyze hexadecimal patterns"""
        hex_data = []
        for p in self.known_exponents:
            hex_str = hex(p)[2:].upper()
            hex_data.append({
                "exponent": p,
                "hex": hex_str,
                "length": len(hex_str),
                "has_FF": 'FF' in hex_str,
                "ends_with_F": hex_str.endswith('F'),
                "has_ABCDEF": any(c in hex_str for c in 'ABCDEF')
            })
        
        return {
            "data": hex_data,
            "length_stats": {
                "min": min(d["length"] for d in hex_data),
                "max": max(d["length"] for d in hex_data),
                "mean": np.mean([d["length"] for d in hex_data])
            },
            "special_patterns": {
                "has_FF_count": sum(1 for d in hex_data if d["has_FF"]),
                "ends_with_F_count": sum(1 for d in hex_data if d["ends_with_F"]),
                "has_ABCDEF_count": sum(1 for d in hex_data if d["has_ABCDEF"])
            }
        }
    
    def _analyze_statistical_properties(self) -> Dict:
        """Analyze statistical properties"""
        lengths = [len(str(p)) for p in self.known_exponents]
        binary_lengths = [len(bin(p)[2:]) for p in self.known_exponents]
        popcounts = [bin(p)[2:].count('1') for p in self.known_exponents]
        digit_sums = [sum(int(d) for d in str(p)) for p in self.known_exponents]
        
        return {
            "exponent_count": len(self.known_exponents),
            "length_stats": {
                "mean": np.mean(lengths),
                "median": np.median(lengths),
                "std": np.std(lengths)
            },
            "binary_length_stats": {
                "mean": np.mean(binary_lengths),
                "median": np.median(binary_lengths),
                "std": np.std(binary_lengths)
            },
            "popcount_stats": {
                "mean": np.mean(popcounts),
                "median": np.median(popcounts),
                "std": np.std(popcounts)
            },
            "digit_sum_stats": {
                "mean": np.mean(digit_sums),
                "median": np.median(digit_sums),
                "std": np.std(digit_sums)
            }
        }
    
    def _is_prime(self, n: int) -> bool:
        """Fast primality test"""
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
        
        # Miller-Rabin test
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        
        bases = [2, 3, 5, 7, 11, 13, 17] if n > 4759123141 else [2, 3]
        
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
    
    def _calculate_digital_root(self, n: int) -> int:
        """Calculate digital root"""
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n
    
    def generate_priority_candidates(self, start: int, end: int, count: int = 1000) -> List[Tuple[int, float]]:
        """Generate candidates with priority scores based on pattern analysis"""
        candidates = []
        
        # Get preferred patterns
        preferred_mod_210 = self.patterns["modulo"]["preferred_mod_210"]
        common_suffixes = [suffix for suffix, _ in self.patterns["suffixes"]["last_two"]["most_common"][:10]]
        binary_length_range = (
            int(self.patterns["binary"]["length_stats"]["mean"] - 2),
            int(self.patterns["binary"]["length_stats"]["mean"] + 2)
        )
        popcount_range = (
            int(self.patterns["binary"]["popcount_stats"]["mean"] - 2),
            int(self.patterns["binary"]["popcount_stats"]["mean"] + 2)
        )
        
        for p in range(start, end, 2):  # Only odd numbers
            if not self._is_prime(p):
                continue
            
            score = 0.0
            
            # Basic requirements
            if p % 4 not in [1, 3] or p % 6 not in [1, 5]:
                continue
            
            if p > 5 and p % 10 not in [1, 3, 7, 9]:
                continue
            
            # Modulo 210 bonus
            if p % 210 in preferred_mod_210:
                score += 2.0
            
            # Suffix bonus
            p_str = str(p)
            if len(p_str) >= 2:
                last_two = p_str[-2:]
                if last_two in common_suffixes:
                    score += 3.0
            
            # Binary properties bonus
            binary = bin(p)[2:]
            if binary.startswith('1') and binary.endswith('1'):
                score += 1.0
            
            binary_length = len(binary)
            if binary_length_range[0] <= binary_length <= binary_length_range[1]:
                score += 2.0
            
            popcount = binary.count('1')
            if popcount_range[0] <= popcount <= popcount_range[1]:
                score += 2.0
            
            # Special prime properties bonus
            if self._is_prime(2 * p + 1):  # Sophie Germain
                score += 5.0
            
            if p > 2 and self._is_prime((p - 1) // 2):  # Safe prime
                score += 5.0
            
            # Hex pattern bonus
            hex_str = hex(p)[2:].upper()
            if 'FF' in hex_str or hex_str.endswith('F'):
                score += 1.0
            
            # Digital root bonus (prefer certain values)
            digital_root = self._calculate_digital_root(p)
            if digital_root in [1, 3, 7, 9]:
                score += 1.0
            
            if score > 0:
                candidates.append((p, score))
        
        # Sort by score (highest first) and return top candidates
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:count]
    
    def get_pattern_summary(self) -> str:
        """Get a comprehensive summary of all patterns"""
        summary = []
        summary.append("🧠 ADVANCED MERSENNE PATTERN ANALYSIS SUMMARY")
        summary.append("=" * 60)
        
        # Basic properties
        basic = self.patterns["basic"]
        summary.append(f"📊 Basic Properties:")
        summary.append(f"  • All prime: {basic['all_prime']}")
        summary.append(f"  • All odd except 2: {basic['all_odd_except_2']}")
        summary.append(f"  • Most common last digit: {Counter(basic['last_digits']).most_common(1)[0]}")
        summary.append(f"  • Most common first digit: {Counter(basic['first_digits']).most_common(1)[0]}")
        
        # Binary properties
        binary = self.patterns["binary"]
        summary.append(f"\n🔢 Binary Properties:")
        summary.append(f"  • All start with 1: {binary['all_start_with_1']}")
        summary.append(f"  • All end with 1: {binary['all_end_with_1']}")
        summary.append(f"  • Binary length: {binary['length_stats']['mean']:.1f} ± {np.std([d['length'] for d in binary['data']]):.1f}")
        summary.append(f"  • Popcount: {binary['popcount_stats']['mean']:.1f} ± {np.std([d['popcount'] for d in binary['data']]):.1f}")
        
        # Suffix patterns
        suffixes = self.patterns["suffixes"]
        summary.append(f"\n🔤 Suffix Patterns:")
        summary.append(f"  • Most common last-2: {suffixes['last_two']['most_common'][:5]}")
        summary.append(f"  • Repeated suffixes: {suffixes['repeated_suffixes']}")
        
        # Special primes
        special = self.patterns["special_primes"]
        summary.append(f"\n⭐ Special Prime Properties:")
        summary.append(f"  • Sophie Germain: {special['sophie_germain_count']} ({special['sophie_germain']})")
        summary.append(f"  • Safe primes: {special['safe_prime_count']} ({special['safe_primes']})")
        
        # Gap analysis
        gaps = self.patterns["gaps"]
        summary.append(f"\n📏 Gap Analysis:")
        summary.append(f"  • Min gap: {gaps['min_gap']:,}")
        summary.append(f"  • Max gap: {gaps['max_gap']:,}")
        summary.append(f"  • Mean gap: {gaps['mean_gap']:,.0f}")
        
        return "\n".join(summary)

def main():
    """Test the advanced pattern analysis"""
    analyzer = AdvancedMersennePatternAnalysis()
    
    print(analyzer.get_pattern_summary())
    
    # Test candidate generation
    print(f"\n🎯 Testing Priority Candidate Generation:")
    candidates = analyzer.generate_priority_candidates(82590000, 82600000, 10)
    
    print(f"Generated {len(candidates)} priority candidates:")
    for i, (candidate, score) in enumerate(candidates, 1):
        print(f"  #{i}: {candidate:,} (score: {score:.1f})")

if __name__ == "__main__":
    main()
