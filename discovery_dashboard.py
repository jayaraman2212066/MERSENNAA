#!/usr/bin/env python3
"""
📊 MERSENNE DISCOVERY DASHBOARD 📊
Real-time monitoring and visualization for Mersenne prime discovery
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
import sys

class DiscoveryDashboard:
    def __init__(self, discovery_engine=None):
        """Initialize the discovery dashboard"""
        self.discovery_engine = discovery_engine
        self.stats = {
            "start_time": None,
            "candidates_tested": 0,
            "discoveries": [],
            "current_candidate": None,
            "test_rate": 0.0,
            "estimated_completion": None,
            "threads_active": 0,
            "memory_usage": 0.0
        }
        self.running = False
        self.update_interval = 1.0  # seconds
        
    def start_monitoring(self):
        """Start real-time monitoring"""
        self.running = True
        self.stats["start_time"] = time.time()
        
        print("📊 Discovery Dashboard started")
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)
        
        try:
            while self.running:
                self._update_stats()
                self._display_dashboard()
                time.sleep(self.update_interval)
        except KeyboardInterrupt:
            print("\n⏹️ Dashboard monitoring stopped")
            self.running = False
    
    def _update_stats(self):
        """Update statistics from discovery engine"""
        if not self.discovery_engine:
            return
        
        # Update basic stats
        self.stats["candidates_tested"] = getattr(self.discovery_engine, 'candidates_tested', 0)
        self.stats["discoveries"] = getattr(self.discovery_engine, 'discoveries', [])
        self.stats["threads_active"] = len(getattr(self.discovery_engine, 'threads', []))
        
        # Calculate test rate
        if self.stats["start_time"]:
            elapsed = time.time() - self.stats["start_time"]
            if elapsed > 0:
                self.stats["test_rate"] = self.stats["candidates_tested"] / elapsed
        
        # Estimate completion (if we have a target)
        if hasattr(self.discovery_engine, 'target_candidates') and self.discovery_engine.target_candidates:
            remaining = self.discovery_engine.target_candidates - self.stats["candidates_tested"]
            if self.stats["test_rate"] > 0:
                eta_seconds = remaining / self.stats["test_rate"]
                self.stats["estimated_completion"] = datetime.now() + timedelta(seconds=eta_seconds)
        
        # Memory usage (simplified)
        try:
            import psutil
            process = psutil.Process()
            self.stats["memory_usage"] = process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            self.stats["memory_usage"] = 0.0
    
    def _display_dashboard(self):
        """Display the real-time dashboard"""
        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🚀 REVOLUTIONARY MERSENNE DISCOVERY DASHBOARD 🚀")
        print("=" * 80)
        
        # Time and status
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed = time.time() - self.stats["start_time"] if self.stats["start_time"] else 0
        
        print(f"🕐 Current Time: {current_time}")
        print(f"⏱️  Elapsed Time: {self._format_duration(elapsed)}")
        print(f"🔄 Status: {'RUNNING' if self.running else 'STOPPED'}")
        print()
        
        # Discovery statistics
        print("📊 DISCOVERY STATISTICS")
        print("-" * 40)
        print(f"🔍 Candidates Tested: {self.stats['candidates_tested']:,}")
        print(f"🏆 Discoveries Found: {len(self.stats['discoveries'])}")
        print(f"📈 Test Rate: {self.stats['test_rate']:.2f} tests/second")
        print(f"🧵 Active Threads: {self.stats['threads_active']}")
        print(f"💾 Memory Usage: {self.stats['memory_usage']:.1f} MB")
        print()
        
        # Recent discoveries
        if self.stats["discoveries"]:
            print("🌟 RECENT DISCOVERIES")
            print("-" * 40)
            recent = self.stats["discoveries"][-3:]  # Last 3 discoveries
            for i, discovery in enumerate(recent, 1):
                exp = discovery.get('exponent', 'Unknown')
                test_time = discovery.get('test_time', 0)
                disc_time = discovery.get('discovery_time', 'Unknown')
                print(f"  #{len(self.stats['discoveries'])-len(recent)+i}: p = {exp:,} (tested in {test_time:.4f}s)")
            print()
        
        # Progress estimation
        if self.stats["estimated_completion"]:
            eta = self.stats["estimated_completion"]
            print("⏰ ESTIMATED COMPLETION")
            print("-" * 40)
            print(f"🎯 ETA: {eta.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏳ Time Remaining: {self._format_duration((eta - datetime.now()).total_seconds())}")
            print()
        
        # Performance metrics
        print("⚡ PERFORMANCE METRICS")
        print("-" * 40)
        if self.stats["candidates_tested"] > 0:
            efficiency = len(self.stats["discoveries"]) / self.stats["candidates_tested"] * 100
            print(f"🎯 Discovery Efficiency: {efficiency:.4f}%")
        
        if self.stats["test_rate"] > 0:
            print(f"🚀 Tests per Hour: {self.stats['test_rate'] * 3600:.0f}")
            print(f"📊 Tests per Day: {self.stats['test_rate'] * 86400:.0f}")
        print()
        
        # System info
        print("💻 SYSTEM INFORMATION")
        print("-" * 40)
        print(f"🐍 Python Version: {sys.version.split()[0]}")
        print(f"🖥️  Platform: {sys.platform}")
        print(f"📁 Working Directory: {os.getcwd()}")
        print()
        
        print("Press Ctrl+C to stop monitoring...")
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def add_discovery(self, discovery: Dict):
        """Add a new discovery to the dashboard"""
        self.stats["discoveries"].append(discovery)
        print(f"\n🎉 NEW DISCOVERY! p = {discovery.get('exponent', 'Unknown'):,}")
    
    def save_report(self, filename: str = None):
        """Save discovery report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"discovery_report_{timestamp}.json"
        
        report = {
            "session_info": {
                "start_time": self.stats["start_time"],
                "end_time": time.time(),
                "duration": time.time() - self.stats["start_time"] if self.stats["start_time"] else 0
            },
            "statistics": self.stats,
            "discoveries": self.stats["discoveries"],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Discovery report saved to: {filename}")
        return filename

def main():
    """Main function for testing the dashboard"""
    print("📊 MERSENNE DISCOVERY DASHBOARD TEST 📊")
    print("=" * 50)
    
    # Create a mock discovery engine for testing
    class MockDiscoveryEngine:
        def __init__(self):
            self.candidates_tested = 0
            self.discoveries = []
            self.threads = []
            self.target_candidates = 1000
        
        def simulate_progress(self):
            """Simulate discovery progress"""
            import random
            import time
            
            for i in range(100):
                self.candidates_tested += 1
                
                # Simulate discovery (1% chance)
                if random.random() < 0.01:
                    discovery = {
                        "exponent": 85000000 + i,
                        "test_time": random.uniform(0.1, 2.0),
                        "discovery_time": datetime.now().isoformat()
                    }
                    self.discoveries.append(discovery)
                    print(f"🎉 Mock discovery: p = {discovery['exponent']:,}")
                
                time.sleep(0.1)  # Simulate work
    
    # Test the dashboard
    mock_engine = MockDiscoveryEngine()
    dashboard = DiscoveryDashboard(mock_engine)
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=dashboard.start_monitoring)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Simulate discovery progress
    try:
        mock_engine.simulate_progress()
    except KeyboardInterrupt:
        print("\n⏹️ Test stopped by user")
    
    # Save final report
    dashboard.save_report()
    print("✅ Dashboard test complete!")

if __name__ == "__main__":
    main()
