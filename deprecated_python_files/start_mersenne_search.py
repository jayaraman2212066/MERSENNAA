#!/usr/bin/env python3
"""
Quick Start Script for Advanced Mersenne Prime Search
Combines all strategies: Prime95 algorithms, pattern analysis, and optimization
"""

import json
import time
from advanced_mersenne_prime_finder import AdvancedMersennePrimeFinder

def load_config():
    """Load search configuration"""
    try:
        with open('mersenne_search_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Configuration file not found, using default settings")
        return {}

def main():
    """Main function to start the Mersenne prime search"""
    print("🚀 STARTING ADVANCED MERSENNE PRIME SEARCH 🚀")
    print("=" * 60)
    print("🔧 Features:")
    print("  • Prime95 advanced algorithms")
    print("  • Pattern analysis & prediction")
    print("  • Multi-threading optimization")
    print("  • Advanced Lucas-Lehmer test")
    print("  • Real-time progress monitoring")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Create the advanced finder
    finder = AdvancedMersennePrimeFinder()
    
    # Configure based on config file
    if config:
        num_predictions = config.get('search_configuration', {}).get('num_predictions', 3)
        print(f"📋 Using configuration: {num_predictions} predictions")
    else:
        num_predictions = 3
        print(f"📋 Using default: {num_predictions} predictions")
    
    # Start the search
    print(f"\n🎯 Starting search for Mersenne primes #{53} to #{52 + num_predictions}...")
    print("⏰ Estimated time: Varies by hardware and range size")
    print("💡 Tip: Use Ctrl+C to pause/resume the search")
    print("=" * 60)
    
    try:
        # Run the search
        start_time = time.time()
        results = finder.run_advanced_search(num_predictions=num_predictions)
        end_time = time.time()
        
        # Display results
        if results:
            print(f"\n🎉 SEARCH COMPLETE! 🎉")
            print(f"⏱️ Total time: {end_time - start_time:.1f} seconds")
            print(f"🔍 Found {len(results)} new Mersenne primes:")
            
            for i, result in enumerate(results, 1):
                print(f"  #{52 + i}: p = {result['exponent']:,} → 2^{result['exponent']} - 1")
                print(f"      Discovery time: {result['discovery_time']}")
            
            print(f"\n📁 Results saved to:")
            print(f"  • discovered_mersenne_primes.json")
            print(f"  • discovered_mersenne_primes.txt")
            
        else:
            print(f"\n🔍 Search completed. No new Mersenne primes found in this run.")
            print(f"💡 Try:")
            print(f"  • Increasing num_predictions in config")
            print(f"  • Expanding search ranges")
            print(f"  • Running longer searches")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Search paused by user")
        print(f"💾 Progress saved. Resume by running again.")
        print(f"📊 Current progress: {finder.candidates_tested:,} candidates tested")
        
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print(f"🔧 Check configuration and try again.")
        print(f"📋 Current status: {finder.candidates_tested:,} candidates tested")

if __name__ == "__main__":
    main()
