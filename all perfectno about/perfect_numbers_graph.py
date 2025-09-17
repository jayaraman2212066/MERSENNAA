import matplotlib.pyplot as plt
import numpy as np

# All 52 known Mersenne prime exponents (as of 2025)
mersenne_exponents = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841
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

# Create dynamic visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))

# Left plot: Dynamic circular representation
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_aspect('equal')
ax1.set_title('Perfect Numbers: Circle of Infinity', fontsize=16, fontweight='bold', pad=20)

# Create circular points
angles = np.linspace(0, 2*np.pi, len(perfect_numbers), endpoint=False)

# Plot circles with dynamic sizing
for i, (angle, p, val) in enumerate(zip(angles, mersenne_exponents, perfect_numbers)):
    # Radius based on index (spiral outward)
    radius = 0.1 + (i * 0.8 / len(perfect_numbers))
    
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    
    # Dynamic circle size based on number magnitude
    if p <= 64:
        if isinstance(val, (int, float)) and val > 0:
            circle_size = min(0.05 + (np.log10(float(val)) / 50), 0.2)
        else:
            circle_size = 0.05
    else:
        circle_size = min(0.05 + (val / 200), 0.2)
    
    # Color based on magnitude
    color = plt.cm.viridis(i / len(perfect_numbers))
    
    circle = plt.Circle((x, y), circle_size, color=color, alpha=0.8, edgecolor='black', linewidth=1)
    ax1.add_patch(circle)
    
    # Add labels for key points
    if i % 5 == 0 or i == len(perfect_numbers) - 1:
        if p <= 64 and isinstance(val, (int, float)):
            label = f"#{i+1}\n{val:.1e}" if val > 1e6 else f"#{i+1}\n{int(val)}"
        else:
            label = f"#{i+1}\n10^{val:.0f}"
        
        ax1.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points',
                     fontsize=8, ha='center', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

# Add center point
center_circle = plt.Circle((0, 0), 0.03, color='red', alpha=0.9)
ax1.add_patch(center_circle)
ax1.annotate('START\n(6)', (0, 0), xytext=(0, -15), textcoords='offset points',
             ha='center', fontweight='bold', fontsize=10)

# Right plot: Dynamic bar chart with enhanced scaling
ax2.set_title('Perfect Numbers: Scale of Infinity', fontsize=16, fontweight='bold', pad=20)

# Create dynamic bars with gradient colors
bars = ax2.bar(range(len(perfect_numbers)), perfect_numbers, 
               color=[plt.cm.plasma(i/len(perfect_numbers)) for i in range(len(perfect_numbers))],
               alpha=0.8, edgecolor='black', linewidth=1)

# Enhanced x-axis labels
x_labels = []
for i in range(len(mersenne_exponents)):
    if i % 5 == 0 or i == len(mersenne_exponents) - 1:
        x_labels.append(f"#{i+1}\np={mersenne_exponents[i]:,}")
    else:
        x_labels.append("")
ax2.set_xticks(range(len(perfect_numbers)))
ax2.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)

# Set y-axis to log scale with enhanced formatting
ax2.set_yscale('log')
ax2.set_ylabel('Perfect Number Value (log scale)', fontsize=14, fontweight='bold')

# Add dynamic value labels with enhanced formatting
for i, (bar, val, p) in enumerate(zip(bars, perfect_numbers, mersenne_exponents)):
    if i % 5 == 0 or i == len(perfect_numbers) - 1:
        height = bar.get_height()
        if p <= 64 and isinstance(val, (int, float)):
            if val < 1000:
                label = str(int(val))
            elif val < 1000000:
                label = f"{val/1000:.1f}K"
            else:
                label = f"{val:.1e}"
        else:
            label = f"10^{val:.0f}"
        
        # Dynamic label positioning
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontweight='bold', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

# Add enhanced grid and styling
ax2.grid(True, alpha=0.3, which='both')
ax2.set_facecolor('#f8f9fa')

# Add comprehensive statistics box
max_val = max([v for v in perfect_numbers if isinstance(v, (int, float))])
min_val = min([v for v in perfect_numbers if isinstance(v, (int, float)) and v > 0])
stats_text = f"🌌 PERFECT NUMBERS UNIVERSE 🌌\n"
stats_text += f"Total Calculated: {len(perfect_numbers)}\n"
stats_text += f"Largest: 10^{max_val:.0f}\n"
stats_text += f"Smallest: {min_val}\n"
stats_text += f"Scale Range: {max_val/min_val:.1e}"

ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
         verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
         facecolor='gold', alpha=0.9, edgecolor='black', linewidth=2),
         fontsize=12, fontweight='bold')

# Add scale comparison
scale_text = "SCALE COMPARISON:\n"
scale_text += "• #1: 6 (human scale)\n"
scale_text += "• #10: 10²⁷ (galaxy scale)\n"
scale_text += "• #25: 10⁶⁵³² (universe scale)\n"
scale_text += "• #51: 10²⁴⁸⁵⁹⁵⁷⁰ (beyond imagination)"

ax2.text(0.98, 0.02, scale_text, transform=ax2.transAxes, 
         verticalalignment='bottom', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.9),
         fontsize=10, fontweight='bold')

plt.tight_layout()

# Save the dynamic graph
plt.savefig('perfect_numbers_dynamic_universe.png', dpi=300, bbox_inches='tight')
print("Dynamic graph saved as 'perfect_numbers_dynamic_universe.png'")

# Show the graph
plt.show()

# Print enhanced information
print("🌌 PERFECT NUMBERS: SCALE OF INFINITY 🌌")
print("=" * 60)
print(f"Total calculated: {len(perfect_numbers)}")
print(f"Scale range: {max_val/min_val:.1e}")
print("=" * 60)

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
