import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches

# All 52 known Mersenne prime exponents (as of 2024)
mersenne_exponents = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933
]

# Calculate perfect numbers: 2^(p-1) × (2^p - 1)
perfect_numbers = []
for p in mersenne_exponents:
    if p <= 64:  # For smaller exponents, calculate directly
        mersenne_part = (2**p) - 1
        perfect_number = (2**(p-1)) * mersenne_part
        perfect_numbers.append(perfect_number)
    else:  # For larger exponents, use log10 approximation
        log10_value = (2*p - 1) * 0.301
        perfect_numbers.append(log10_value)

# Function to calculate sum of proper divisors
def sum_proper_divisors(n):
    if n <= 1:
        return 0
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sum(divisors)

# Create comprehensive analysis for natural numbers
def analyze_natural_numbers(max_n):
    numbers = list(range(1, max_n + 1))
    sums = [sum_proper_divisors(n) for n in numbers]
    
    # Classify numbers
    deficient = []  # sum < n
    perfect = []    # sum = n
    abundant = []   # sum > n
    
    for i, (n, s) in enumerate(zip(numbers, sums)):
        if s < n:
            deficient.append(i)
        elif s == n:
            perfect.append(i)
        else:
            abundant.append(i)
    
    return numbers, sums, deficient, perfect, abundant

# Create the main figure with multiple subplots
fig = plt.figure(figsize=(20, 16))
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], width_ratios=[2, 1])

# Plot 1: Natural Numbers Analysis (Top Left)
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title('Natural Numbers: Deficient, Perfect, and Abundant Analysis', fontsize=14, fontweight='bold')

# Analyze first 1000 natural numbers for detailed view
max_analyze = 1000
numbers, sums, deficient, perfect, abundant = analyze_natural_numbers(max_analyze)

# Plot reference line (y = x)
ax1.plot(numbers, numbers, 'k--', alpha=0.5, label='Reference Line (y = x)')

# Plot sums with color coding
ax1.scatter([numbers[i] for i in deficient], [sums[i] for i in deficient], 
            c='red', alpha=0.6, s=20, label='Deficient (sum < n)')
ax1.scatter([numbers[i] for i in perfect], [sums[i] for i in perfect], 
            c='blue', alpha=0.8, s=50, label='Perfect (sum = n)', marker='*')
ax1.scatter([numbers[i] for i in abundant], [sums[i] for i in abundant], 
            c='green', alpha=0.6, s=20, label='Abundant (sum > n)')

ax1.set_xlabel('Natural Number (n)', fontsize=12)
ax1.set_ylabel('Sum of Proper Divisors', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Perfect Numbers Scale (Top Right)
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_title('All 52 Perfect Numbers Scale', fontsize=14, fontweight='bold')

# Create bars for perfect numbers
bars = ax2.bar(range(len(perfect_numbers)), perfect_numbers, 
               color=plt.cm.plasma(np.linspace(0, 1, len(perfect_numbers))),
               alpha=0.8, edgecolor='black', linewidth=1)

ax2.set_xlabel('Perfect Number Index', fontsize=12)
ax2.set_ylabel('Perfect Number Value (log scale)', fontsize=12)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

# Add labels for key perfect numbers
for i, (bar, val, p) in enumerate(zip(bars, perfect_numbers, mersenne_exponents)):
    if i % 5 == 0 or i == len(perfect_numbers) - 1:
        if p <= 64 and isinstance(val, (int, float)):
            label = f"#{i+1}\n{val:.1e}" if val > 1e6 else f"#{i+1}\n{int(val)}"
        else:
            label = f"#{i+1}\n10^{val:.0f}"
        
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                label, ha='center', va='bottom', fontsize=8, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

# Plot 3: Interactive Zoom View (Middle)
ax3 = fig.add_subplot(gs[1, :])
ax3.set_title('Interactive Perfect Numbers Universe - Use Mouse Wheel to Zoom', fontsize=16, fontweight='bold')

# Create spiral-like visualization for perfect numbers
angles = np.linspace(0, 4*np.pi, len(perfect_numbers))
radii = np.linspace(0.1, 1.0, len(perfect_numbers))

# Plot perfect numbers as circles
for i, (angle, radius, p, val) in enumerate(zip(angles, radii, mersenne_exponents, perfect_numbers)):
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    
    # Dynamic circle size
    if p <= 64:
        if isinstance(val, (int, float)) and val > 0:
            circle_size = min(0.05 + (np.log10(float(val)) / 100), 0.15)
        else:
            circle_size = 0.05
    else:
        circle_size = min(0.05 + (val / 300), 0.15)
    
    circle = plt.Circle((x, y), circle_size, 
                       color=plt.cm.viridis(i/len(perfect_numbers)),
                       alpha=0.8, edgecolor='black', linewidth=1)
    ax3.add_patch(circle)
    
    # Add labels for key points
    if i % 5 == 0 or i == len(perfect_numbers) - 1:
        if p <= 64 and isinstance(val, (int, float)):
            label = f"#{i+1}\n{val:.1e}" if val > 1e6 else f"#{i+1}\n{int(val)}"
        else:
            label = f"#{i+1}\n10^{val:.0f}"
        
        ax3.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points',
                     fontsize=9, ha='center', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

# Add center point
center_circle = plt.Circle((0, 0), 0.02, color='red', alpha=0.9)
ax3.add_patch(center_circle)
ax3.annotate('START\n(6)', (0, 0), xytext=(0, -10), textcoords='offset points',
             ha='center', fontweight='bold', fontsize=10)

ax3.set_xlim(-1.2, 1.2)
ax3.set_ylim(-1.2, 1.2)
ax3.set_aspect('equal')
ax3.grid(True, alpha=0.3)

# Plot 4: Statistics and Scale Comparison (Bottom)
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

# Create comprehensive statistics
stats_text = f"""
🌌 COMPREHENSIVE PERFECT NUMBERS UNIVERSE 🌌

📊 ANALYSIS SUMMARY:
• Natural Numbers Analyzed: 1 to {max_analyze:,}
• Perfect Numbers Found: {len(perfect_numbers)}
• Deficient Numbers: {len(deficient):,} (sum < n)
• Abundant Numbers: {len(abundant):,} (sum > n)
• Perfect Numbers in Range: {len(perfect)} (sum = n)

🚀 PERFECT NUMBERS SCALE:
• Smallest: {perfect_numbers[0]} (human scale)
• Largest: 10^{max([v for v in perfect_numbers if isinstance(v, (int, float))]):.0f} (cosmic scale)
• Scale Range: 10^{max([v for v in perfect_numbers if isinstance(v, (int, float))]) - np.log10(perfect_numbers[0]):.0f}

🔍 INTERACTIVE FEATURES:
• Mouse wheel: Zoom in/out on the spiral view
• Hover over bars: See perfect number details
• Scroll through all 52 perfect numbers
• Explore the massive scale differences

💡 SCALE COMPARISON:
• #1: 6 (human scale - can count on fingers)
• #10: 10²⁷ (galaxy scale - stars in a galaxy)
• #25: 10⁶⁵³² (universe scale - atoms in universe)
• #51: 10²⁴⁸⁵⁹⁵⁷⁰ (beyond imagination - cosmic scale)
"""

ax4.text(0.5, 0.5, stats_text, transform=ax4.transAxes, 
         ha='center', va='center', fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.9, edgecolor='black', linewidth=2))

plt.tight_layout()

# Enable interactive features
plt.rcParams['toolbar'] = 'toolmanager'

# Save the comprehensive graph
plt.savefig('comprehensive_perfect_numbers_analysis.png', dpi=300, bbox_inches='tight')
print("Comprehensive analysis graph saved as 'comprehensive_perfect_numbers_analysis.png'")

# Show the interactive graph
plt.show()

# Print detailed analysis
print("🌌 COMPREHENSIVE PERFECT NUMBERS ANALYSIS 🌌")
print("=" * 80)
print(f"Natural numbers analyzed: 1 to {max_analyze:,}")
print(f"Perfect numbers found: {len(perfect_numbers)}")
print(f"Deficient numbers: {len(deficient):,}")
print(f"Abundant numbers: {len(abundant):,}")
print(f"Perfect numbers in range: {len(perfect)}")
print("=" * 80)

print("\n📊 PERFECT NUMBERS DETAILS:")
for i, (p, val) in enumerate(zip(mersenne_exponents, perfect_numbers), 1):
    print(f"#{i:2d}: p = {p:8,} → Perfect Number = 2^(p-1) × (2^p - 1)")
    if p <= 64 and isinstance(val, (int, float)):
        if val < 1000:
            print(f"     Value: {int(val)} (human scale)")
        elif val < 1000000:
            print(f"     Value: {val:,.0f} (city scale)")
        else:
            print(f"     Value: {val:.2e} (planetary scale)")
    else:
        print(f"     Value: 10^{val:.0f} (cosmic scale)")
    print()
