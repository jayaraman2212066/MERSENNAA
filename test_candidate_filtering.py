#!/usr/bin/env python3
"""
Test script to verify candidate filtering is working correctly
"""

from enhanced_mersenne_discovery import EnhancedMersenneDiscovery

def test_candidate_filtering():
    """Test the candidate filtering logic"""
    print("🧪 Testing Candidate Filtering Logic")
    print("=" * 50)
    
    discovery = EnhancedMersenneDiscovery()
    
    # Test some invalid candidates (actually even numbers)
    invalid_candidates = [
        82589934,  # Even number
        82589936,  # Even number
        82589938,  # Even number
        82589940,  # Even number
        82589942,  # Even number
        82589944,  # Even number
        82589946,  # Even number
        82589948,  # Even number
        82589950,  # Even number
        82589952,  # Even number
        82589954,  # Even number
        82589956,  # Even number
        82589958,  # Even number
        82589960,  # Even number
        82589962,  # Even number
        82589964,  # Even number
        82589966,  # Even number
        82589968,  # Even number
        82589970,  # Even number
        82589972,  # Even number
        82589974,  # Even number
        82589976,  # Even number
        82589978,  # Even number
        82589980,  # Even number
        82589982,  # Even number
        82589984,  # Even number
        82589986,  # Even number
        82589988,  # Even number
        82589990,  # Even number
        82589992,  # Even number
        82589994,  # Even number
        82589996,  # Even number
        82589998,  # Even number
        82590000,  # Even number
        82590002,  # Even number
        82590004,  # Even number
        82590006,  # Even number
        82590008,  # Even number
        82590010,  # Even number
        82590012,  # Even number
        82590014,  # Even number
        82590016,  # Even number
        82590018,  # Even number
        82590020,  # Even number
    ]
    
    print("Testing invalid candidates (should all be False):")
    valid_count = 0
    for candidate in invalid_candidates:
        is_valid = discovery.is_valid_mersenne_exponent_candidate(candidate)
        if is_valid:
            valid_count += 1
            print(f"  ❌ {candidate:,} - INVALID (even number) but marked as valid!")
        else:
            print(f"  ✅ {candidate:,} - correctly rejected (even number)")
    
    print(f"\nInvalid candidates incorrectly accepted: {valid_count}")
    
    # Test some potentially valid candidates (odd numbers)
    print("\nTesting potentially valid candidates (odd numbers):")
    odd_candidates = [82589935, 82589937, 82589939, 82589941, 82589943, 82589945, 82589947, 82589949, 82589951, 82589953]
    
    valid_count = 0
    for candidate in odd_candidates:
        is_valid = discovery.is_valid_mersenne_exponent_candidate(candidate)
        if is_valid:
            valid_count += 1
            print(f"  ✅ {candidate:,} - valid candidate")
        else:
            print(f"  ❌ {candidate:,} - rejected (reason: not prime or other filter)")
    
    print(f"\nValid odd candidates found: {valid_count}")
    
    # Test candidate generation
    print("\nTesting candidate generation:")
    candidates = discovery.generate_candidates_after_52nd(82590000, 82600000, 10)
    print(f"Generated {len(candidates)} candidates:")
    for i, candidate in enumerate(candidates):
        print(f"  #{i+1}: {candidate:,} (odd: {candidate % 2 == 1}, prime: {discovery.is_prime(candidate)})")
    
    print("\n✅ Candidate filtering test complete!")

if __name__ == "__main__":
    test_candidate_filtering()
