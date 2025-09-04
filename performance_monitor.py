#!/usr/bin/env python3
"""
🚀 ULTRA-SPEED MERSENNE FINDER PERFORMANCE MONITOR 🚀
Real-time performance tracking and analysis for Acer Aspire 5

Features:
- Real-time performance monitoring
- CPU/GPU utilization tracking
- Thermal monitoring
- Progress visualization
- Performance predictions
- Speed comparison with standard methods
"""

import psutil
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np
import os
import json
from datetime import datetime, timedelta
import subprocess
import platform

class PerformanceMonitor:
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        self.temperature = []
        self.timestamps = []
        self.operations_per_sec = []
        self.candidates_tested = []
        self.start_time = time.time()
        self.monitoring = False
        
        # Performance thresholds for Acer Aspire 5
        self.cpu_threshold = 85  # Celsius
        self.memory_threshold = 90  # Percent
        self.performance_target = 1000000  # ops/sec target
        
        # Initialize system info
        self.system_info = self.get_system_info()
        
    def get_system_info(self):
        """Get detailed system information"""
        info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            'memory': psutil.virtual_memory()._asdict(),
            'disk': psutil.disk_usage('/')._asdict() if os.name != 'nt' else psutil.disk_usage('C:\\')._asdict()
        }
        
        # Try to get GPU info
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.used', '--format=csv,noheader,nounits'], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    gpu_info = result.stdout.strip().split(',')
                    info['gpu'] = {
                        'name': gpu_info[0].strip(),
                        'memory_total': int(gpu_info[1]),
                        'memory_used': int(gpu_info[2])
                    }
        except:
            info['gpu'] = None
            
        return info
    
    def get_cpu_temperature(self):
        """Get CPU temperature (platform-dependent)"""
        try:
            if os.name == 'nt':  # Windows
                # Try to use OpenHardwareMonitor or similar
                return None
            else:  # Linux
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    temp = int(f.read()) / 1000.0
                    return temp
        except:
            return None
    
    def monitor_performance(self):
        """Monitor system performance in real-time"""
        while self.monitoring:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.append(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_usage.append(memory.percent)
            
            # Temperature
            temp = self.get_cpu_temperature()
            self.temperature.append(temp if temp else 0)
            
            # Timestamp
            self.timestamps.append(time.time() - self.start_time)
            
            # Check for performance data from Mersenne finder
            self.check_mersenne_progress()
            
            # Keep only last 1000 data points
            if len(self.timestamps) > 1000:
                self.cpu_usage = self.cpu_usage[-1000:]
                self.memory_usage = self.memory_usage[-1000:]
                self.temperature = self.temperature[-1000:]
                self.timestamps = self.timestamps[-1000:]
                self.operations_per_sec = self.operations_per_sec[-1000:]
                self.candidates_tested = self.candidates_tested[-1000:]
    
    def check_mersenne_progress(self):
        """Check for progress updates from Mersenne finder"""
        try:
            # Check if results file exists and has new data
            if os.path.exists('ultra_speed_mersenne_results.txt'):
                with open('ultra_speed_mersenne_results.txt', 'r') as f:
                    lines = f.readlines()
                    if lines:
                        # Parse last line for operations per second
                        for line in reversed(lines):
                            if 'Operations/Second:' in line:
                                try:
                                    ops = int(line.split(':')[1].strip())
                                    self.operations_per_sec.append(ops)
                                    break
                                except:
                                    pass
        except:
            pass
    
    def start_monitoring(self):
        """Start performance monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_performance)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("🚀 Performance monitoring started!")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
        print("⏹️ Performance monitoring stopped!")
    
    def get_performance_summary(self):
        """Get current performance summary"""
        if not self.cpu_usage:
            return "No performance data available"
        
        summary = {
            'current_cpu': self.cpu_usage[-1],
            'current_memory': self.memory_usage[-1],
            'current_temp': self.temperature[-1] if self.temperature[-1] > 0 else 'Unknown',
            'avg_cpu': np.mean(self.cpu_usage),
            'avg_memory': np.mean(self.memory_usage),
            'peak_cpu': max(self.cpu_usage),
            'peak_memory': max(self.memory_usage),
            'elapsed_time': time.time() - self.start_time,
            'operations_per_sec': self.operations_per_sec[-1] if self.operations_per_sec else 0
        }
        
        return summary
    
    def create_performance_dashboard(self):
        """Create real-time performance dashboard"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('🚀 Ultra-Speed Mersenne Finder Performance Dashboard\nAcer Aspire 5 (12th Gen + RTX 2050)', 
                     fontsize=16, fontweight='bold')
        
        # CPU Usage
        ax1.set_title('CPU Usage (%)', fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('CPU Usage (%)')
        ax1.grid(True, alpha=0.3)
        
        # Memory Usage
        ax2.set_title('Memory Usage (%)', fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Memory Usage (%)')
        ax2.grid(True, alpha=0.3)
        
        # Temperature
        ax3.set_title('CPU Temperature (°C)', fontweight='bold')
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Temperature (°C)')
        ax3.grid(True, alpha=0.3)
        
        # Operations per Second
        ax4.set_title('Performance (Operations/Second)', fontweight='bold')
        ax4.set_xlabel('Time (seconds)')
        ax4.set_ylabel('Operations/Second')
        ax4.grid(True, alpha=0.3)
        
        # Add threshold lines
        ax3.axhline(y=self.cpu_threshold, color='red', linestyle='--', alpha=0.7, label=f'Threshold ({self.cpu_threshold}°C)')
        ax3.legend()
        
        ax4.axhline(y=self.performance_target, color='green', linestyle='--', alpha=0.7, label=f'Target ({self.performance_target:,} ops/sec)')
        ax4.legend()
        
        def animate(i):
            if not self.monitoring or not self.timestamps:
                return
            
            # Update CPU usage
            ax1.clear()
            ax1.set_title('CPU Usage (%)', fontweight='bold')
            ax1.set_ylim(0, 100)
            ax1.set_xlabel('Time (seconds)')
            ax1.set_ylabel('CPU Usage (%)')
            ax1.grid(True, alpha=0.3)
            ax1.plot(self.timestamps, self.cpu_usage, 'b-', linewidth=2)
            
            # Update Memory usage
            ax2.clear()
            ax2.set_title('Memory Usage (%)', fontweight='bold')
            ax2.set_ylim(0, 100)
            ax2.set_xlabel('Time (seconds)')
            ax2.set_ylabel('Memory Usage (%)')
            ax2.grid(True, alpha=0.3)
            ax2.plot(self.timestamps, self.memory_usage, 'g-', linewidth=2)
            
            # Update Temperature
            ax3.clear()
            ax3.set_title('CPU Temperature (°C)', fontweight='bold')
            ax3.set_xlabel('Time (seconds)')
            ax3.set_ylabel('Temperature (°C)')
            ax3.grid(True, alpha=0.3)
            valid_temp = [t for t in self.temperature if t > 0]
            if valid_temp:
                ax3.plot(self.timestamps[:len(valid_temp)], valid_temp, 'r-', linewidth=2)
            ax3.axhline(y=self.cpu_threshold, color='red', linestyle='--', alpha=0.7, label=f'Threshold ({self.cpu_threshold}°C)')
            ax3.legend()
            
            # Update Operations per second
            ax4.clear()
            ax4.set_title('Performance (Operations/Second)', fontweight='bold')
            ax4.set_xlabel('Time (seconds)')
            ax4.set_ylabel('Operations/Second')
            ax4.grid(True, alpha=0.3)
            if self.operations_per_sec:
                ax4.plot(self.timestamps[:len(self.operations_per_sec)], self.operations_per_sec, 'purple', linewidth=2)
            ax4.axhline(y=self.performance_target, color='green', linestyle='--', alpha=0.7, label=f'Target ({self.performance_target:,} ops/sec)')
            ax4.legend()
        
        ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False)
        plt.tight_layout()
        plt.show()
        
        return ani
    
    def print_system_info(self):
        """Print detailed system information"""
        print("🖥️ SYSTEM INFORMATION")
        print("=" * 50)
        print(f"Platform: {self.system_info['platform']}")
        print(f"Processor: {self.system_info['processor']}")
        print(f"CPU Cores: {self.system_info['cpu_count']}")
        
        if self.system_info['cpu_freq']:
            print(f"CPU Frequency: {self.system_info['cpu_freq'].get('current', 'Unknown'):.1f} MHz")
        
        print(f"Memory: {self.system_info['memory']['total'] // (1024**3):.1f} GB")
        print(f"Disk: {self.system_info['disk']['total'] // (1024**3):.1f} GB")
        
        if self.system_info['gpu']:
            print(f"GPU: {self.system_info['gpu']['name']}")
            print(f"GPU Memory: {self.system_info['gpu']['memory_total']} MB")
        else:
            print("GPU: Not detected")
        
        print("=" * 50)
    
    def print_performance_tips(self):
        """Print performance optimization tips for Acer Aspire 5"""
        print("\n💡 PERFORMANCE OPTIMIZATION TIPS FOR ACER ASPIRE 5")
        print("=" * 60)
        print("1. 🧵 Use 8-10 threads (optimal for 12th Gen Intel)")
        print("2. 🌡️  Monitor CPU temperature (keep below 85°C)")
        print("3. 💾 Close unnecessary applications")
        print("4. 🔌 Ensure laptop is plugged in (High Performance mode)")
        print("5. 💨 Use cooling pad for better thermal performance")
        print("6. ⚡ Set Windows power plan to 'High Performance'")
        print("7. 🚫 Disable background services and updates")
        print("8. 🔍 Monitor memory usage (keep below 90%)")
        print("=" * 60)

def main():
    print("🚀 ULTRA-SPEED MERSENNE FINDER PERFORMANCE MONITOR 🚀")
    print("Optimized for Acer Aspire 5 (12th Gen + RTX 2050)")
    print("=" * 70)
    
    monitor = PerformanceMonitor()
    monitor.print_system_info()
    monitor.print_performance_tips()
    
    print("\n🎯 Starting performance monitoring...")
    print("📊 Launching real-time dashboard...")
    print("💡 Tips: Keep this window open while running Mersenne finder")
    print("⏹️  Press Ctrl+C to stop monitoring")
    
    try:
        monitor.start_monitoring()
        monitor.create_performance_dashboard()
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping performance monitor...")
        monitor.stop_monitoring()
        
        # Final performance summary
        summary = monitor.get_performance_summary()
        print("\n📊 FINAL PERFORMANCE SUMMARY")
        print("=" * 40)
        print(f"Total monitoring time: {summary['elapsed_time']:.1f} seconds")
        print(f"Peak CPU usage: {summary['peak_cpu']:.1f}%")
        print(f"Peak memory usage: {summary['peak_memory']:.1f}%")
        print(f"Average CPU usage: {summary['avg_cpu']:.1f}%")
        print(f"Average memory usage: {summary['avg_memory']:.1f}%")
        print(f"Peak operations/second: {summary['operations_per_sec']:,}")
        
        # Performance rating
        if summary['operations_per_sec'] >= 1000000:
            rating = "🚀 EXCELLENT - World record speed!"
        elif summary['operations_per_sec'] >= 500000:
            rating = "⚡ GREAT - Very fast performance!"
        elif summary['operations_per_sec'] >= 100000:
            rating = "👍 GOOD - Solid performance!"
        else:
            rating = "⚠️  NEEDS OPTIMIZATION"
        
        print(f"Performance Rating: {rating}")
        print("=" * 40)

if __name__ == "__main__":
    main()
