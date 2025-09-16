import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button
    import matplotlib.patches as patches
except Exception:
    plt = None

# All 52 known Mersenne prime exponents (as of 2024)
mersenne_exponents = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933
]

def _compute_perfect_numbers_values():
    values = []
    for p in mersenne_exponents:
        if p <= 64:
            mersenne_part = (2**p) - 1
            perfect_number = (2**(p-1)) * mersenne_part
            values.append(perfect_number)
        else:
            log10_value = (2*p - 1) * 0.301
            values.append(log10_value)
    return values

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

def analyze_natural_numbers(max_n):
    numbers = list(range(1, max_n + 1))
    sums = [sum_proper_divisors(n) for n in numbers]
    deficient = []
    perfect = []
    abundant = []
    for i, (n, s) in enumerate(zip(numbers, sums)):
        if s < n:
            deficient.append(i)
        elif s == n:
            perfect.append(i)
        else:
            abundant.append(i)
    return numbers, sums, deficient, perfect, abundant

def analyze_perfect_numbers():
    values = _compute_perfect_numbers_values()
    max_analyze = 1000
    numbers, sums, deficient, perfect, abundant = analyze_natural_numbers(max_analyze)
    # Return a lightweight summary suitable for API responses
    return {
        "status": "ok",
        "mersenne_count": len(mersenne_exponents),
        "natural_numbers_analyzed": max_analyze,
        "deficient_count": len(deficient),
        "perfect_count": len(perfect),
        "abundant_count": len(abundant),
        "first_values_preview": values[:10]
    }

def generate_comprehensive_plot(output_path: str = 'comprehensive_perfect_numbers_analysis.png'):
    if plt is None:
        raise RuntimeError('matplotlib is not available in this environment')

    perfect_numbers = _compute_perfect_numbers_values()
    fig = plt.figure(figsize=(20, 16))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], width_ratios=[2, 1])

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title('Natural Numbers: Deficient, Perfect, and Abundant Analysis', fontsize=14, fontweight='bold')
    max_analyze = 1000
    numbers, sums, deficient, perfect, abundant = analyze_natural_numbers(max_analyze)
    ax1.plot(numbers, numbers, 'k--', alpha=0.5, label='Reference Line (y = x)')
    ax1.scatter([numbers[i] for i in deficient], [sums[i] for i in deficient], c='red', alpha=0.6, s=20, label='Deficient (sum < n)')
    ax1.scatter([numbers[i] for i in perfect], [sums[i] for i in perfect], c='blue', alpha=0.8, s=50, label='Perfect (sum = n)', marker='*')
    ax1.scatter([numbers[i] for i in abundant], [sums[i] for i in abundant], c='green', alpha=0.6, s=20, label='Abundant (sum > n)')
    ax1.set_xlabel('Natural Number (n)', fontsize=12)
    ax1.set_ylabel('Sum of Proper Divisors', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title('All 52 Perfect Numbers Scale', fontsize=14, fontweight='bold')
    bars = ax2.bar(range(len(perfect_numbers)), perfect_numbers,
                   color=plt.cm.plasma(np.linspace(0, 1, len(perfect_numbers))),
                   alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_xlabel('Perfect Number Index', fontsize=12)
    ax2.set_ylabel('Perfect Number Value (log scale)', fontsize=12)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)
    for i, (bar, val, p) in enumerate(zip(bars, perfect_numbers, mersenne_exponents)):
        if i % 5 == 0 or i == len(perfect_numbers) - 1:
            if p <= 64 and isinstance(val, (int, float)):
                label = f"#{i+1}\n{val:.1e}" if val > 1e6 else f"#{i+1}\n{int(val)}"
            else:
                label = f"#{i+1}\n10^{val:.0f}"
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                     label, ha='center', va='bottom', fontsize=8, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_title('Interactive Perfect Numbers Universe - Use Mouse Wheel to Zoom', fontsize=16, fontweight='bold')
    angles = np.linspace(0, 4*np.pi, len(perfect_numbers))
    radii = np.linspace(0.1, 1.0, len(perfect_numbers))
    for i, (angle, radius, p, val) in enumerate(zip(angles, radii, mersenne_exponents, perfect_numbers)):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        if p <= 64:
            if isinstance(val, (int, float)) and val > 0:
                circle_size = min(0.05 + (np.log10(float(val)) / 100), 0.15)
            else:
                circle_size = 0.05
        else:
            circle_size = min(0.05 + (val / 300), 0.15)
        circle = plt.Circle((x, y), circle_size, color=plt.cm.viridis(i/len(perfect_numbers)),
                            alpha=0.8, edgecolor='black', linewidth=1)
        ax3.add_patch(circle)
        if i % 5 == 0 or i == len(perfect_numbers) - 1:
            if p <= 64 and isinstance(val, (int, float)):
                label = f"#{i+1}\n{val:.1e}" if val > 1e6 else f"#{i+1}\n{int(val)}"
            else:
                label = f"#{i+1}\n10^{val:.0f}"
            ax3.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points',
                         fontsize=9, ha='center', fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))
    center_circle = plt.Circle((0, 0), 0.02, color='red', alpha=0.9)
    ax3.add_patch(center_circle)
    ax3.annotate('START\n(6)', (0, 0), xytext=(0, -10), textcoords='offset points',
                 ha='center', fontweight='bold', fontsize=10)
    ax3.set_xlim(-1.2, 1.2)
    ax3.set_ylim(-1.2, 1.2)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)

    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    stats_text = "COMPREHENSIVE PERFECT NUMBERS UNIVERSE — see console for details"
    ax4.text(0.5, 0.5, stats_text, transform=ax4.transAxes,
             ha='center', va='center', fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.9, edgecolor='black', linewidth=2))

    plt.tight_layout()
    plt.rcParams['toolbar'] = 'toolmanager'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    return output_path

if __name__ == '__main__':
    if plt is None:
        raise SystemExit('matplotlib is not available to render plots')
    out = generate_comprehensive_plot()
    print(f"Comprehensive analysis graph saved as '{out}'")
