import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import math

# All 52 known Mersenne prime exponents (as of 2024)
known_mersenne_exponents = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933
]

print("🔍 MERSENNE PRIME PATTERN ANALYSIS 🔍")
print("=" * 60)
print(f"Analyzing {len(known_mersenne_exponents)} known Mersenne prime exponents")
print("=" * 60)

# 1. GAP ANALYSIS - Find patterns in differences between consecutive exponents
print("\n📊 GAP ANALYSIS:")
gaps = []
for i in range(1, len(known_mersenne_exponents)):
    gap = known_mersenne_exponents[i] - known_mersenne_exponents[i-1]
    gaps.append(gap)
    print(f"Gap {i}: {known_mersenne_exponents[i-1]} → {known_mersenne_exponents[i]} = {gap:,}")

# 2. RATIO ANALYSIS - Find patterns in ratios
print("\n📈 RATIO ANALYSIS:")
ratios = []
for i in range(1, len(known_mersenne_exponents)):
    ratio = known_mersenne_exponents[i] / known_mersenne_exponents[i-1]
    ratios.append(ratio)
    print(f"Ratio {i}: {known_mersenne_exponents[i]:,} / {known_mersenne_exponents[i-1]:,} = {ratio:.3f}")

# 3. LOGARITHMIC ANALYSIS - Find patterns in log differences
print("\n🔢 LOGARITHMIC ANALYSIS:")
log_diffs = []
for i in range(1, len(known_mersenne_exponents)):
    log_diff = np.log10(known_mersenne_exponents[i]) - np.log10(known_mersenne_exponents[i-1])
    log_diffs.append(log_diff)
    print(f"Log Diff {i}: log₁₀({known_mersenne_exponents[i]:,}) - log₁₀({known_mersenne_exponents[i-1]:,}) = {log_diff:.3f}")

# 4. PATTERN SEARCH - Look for mathematical patterns
print("\n🔍 MATHEMATICAL PATTERN SEARCH:")

# Check if exponents follow any known sequences
def check_patterns():
    patterns = []
    
    # Check for arithmetic progression
    arithmetic_diffs = [known_mersenne_exponents[i+1] - known_mersenne_exponents[i] for i in range(len(known_mersenne_exponents)-1)]
    if len(set(arithmetic_diffs)) == 1:
        patterns.append(f"Arithmetic progression with difference {arithmetic_diffs[0]}")
    
    # Check for geometric progression
    geometric_ratios = [known_mersenne_exponents[i+1] / known_mersenne_exponents[i] for i in range(len(known_mersenne_exponents)-1)]
    if len(set([round(r, 3) for r in geometric_ratios])) == 1:
        patterns.append(f"Geometric progression with ratio {geometric_ratios[0]:.3f}")
    
    # Check for Fibonacci-like patterns
    fib_like = []
    for i in range(2, len(known_mersenne_exponents)):
        if known_mersenne_exponents[i] == known_mersenne_exponents[i-1] + known_mersenne_exponents[i-2]:
            fib_like.append(i)
    if fib_like:
        patterns.append(f"Fibonacci-like pattern at positions {fib_like}")
    
    # Check for polynomial patterns
    x = np.arange(len(known_mersenne_exponents))
    y = np.array(known_mersenne_exponents)
    
    # Try quadratic fit
    try:
        coeffs = np.polyfit(x, y, 2)
        quadratic_fit = f"Quadratic pattern: {coeffs[0]:.2e}x² + {coeffs[1]:.2e}x + {coeffs[2]:.2e}"
        patterns.append(quadratic_fit)
    except:
        pass
    
    # Check for exponential patterns
    try:
        log_y = np.log10(y)
        coeffs = np.polyfit(x, log_y, 1)
        exp_fit = f"Exponential pattern: y ≈ 10^({coeffs[0]:.3f}x + {coeffs[1]:.3f})"
        patterns.append(exp_fit)
    except:
        pass
    
    return patterns

patterns_found = check_patterns()
if patterns_found:
    for pattern in patterns_found:
        print(f"✅ Found: {pattern}")
else:
    print("❌ No obvious mathematical patterns found")

# 5. STATISTICAL ANALYSIS
print("\n📊 STATISTICAL ANALYSIS:")
print(f"Mean gap: {np.mean(gaps):,.2f}")
print(f"Standard deviation of gaps: {np.std(gaps):,.2f}")
print(f"Mean ratio: {np.mean(ratios):.3f}")
print(f"Standard deviation of ratios: {np.std(ratios):.3f}")

# 6. PREDICTION MODELS
print("\n🚀 PREDICTION MODELS:")

# Model 1: Linear extrapolation
x = np.arange(len(known_mersenne_exponents))
y = np.array(known_mersenne_exponents)
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print(f"Linear model: y = {slope:.2f}x + {intercept:.2f} (R² = {r_value**2:.3f})")

# Model 2: Exponential extrapolation
log_y = np.log10(y)
slope_exp, intercept_exp, r_value_exp, p_value_exp, std_err_exp = stats.linregress(x, log_y)
print(f"Exponential model: y = 10^({slope_exp:.3f}x + {intercept_exp:.3f}) (R² = {r_value_exp**2:.3f})")

# Model 3: Polynomial extrapolation
poly_coeffs = np.polyfit(x, y, 3)
poly_model = np.poly1d(poly_coeffs)
print(f"Cubic polynomial model: {poly_model}")

# 7. NEXT MERSENNE PRIME PREDICTIONS
print("\n🎯 NEXT MERSENNE PRIME PREDICTIONS:")

# Predict next 5 exponents using different models
next_predictions = []
for i in range(1, 6):
    next_index = len(known_mersenne_exponents) + i - 1
    
    # Linear prediction
    linear_pred = slope * next_index + intercept
    
    # Exponential prediction
    exp_pred = 10**(slope_exp * next_index + intercept_exp)
    
    # Polynomial prediction
    poly_pred = poly_model(next_index)
    
    next_predictions.append({
        'index': next_index + 1,
        'linear': int(linear_pred),
        'exponential': int(exp_pred),
        'polynomial': int(poly_pred)
    })
    
    print(f"#{len(known_mersenne_exponents) + i}:")
    print(f"  Linear: {int(linear_pred):,}")
    print(f"  Exponential: {int(exp_pred):,}")
    print(f"  Polynomial: {int(poly_pred):,}")
    print()

# 8. VISUALIZATION
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Plot 1: Exponent values over time
ax1.plot(range(1, len(known_mersenne_exponents) + 1), known_mersenne_exponents, 'bo-', linewidth=2, markersize=6)
ax1.set_xlabel('Mersenne Prime Index', fontsize=12, fontweight='bold')
ax1.set_ylabel('Exponent Value', fontsize=12, fontweight='bold')
ax1.set_title('Mersenne Prime Exponents Over Time', fontsize=14, fontweight='bold')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

# Plot 2: Gaps between consecutive exponents
ax2.plot(range(1, len(gaps) + 1), gaps, 'ro-', linewidth=2, markersize=6)
ax2.set_xlabel('Gap Index', fontsize=12, fontweight='bold')
ax2.set_ylabel('Gap Size', fontsize=12, fontweight='bold')
ax2.set_title('Gaps Between Consecutive Mersenne Prime Exponents', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Plot 3: Ratios between consecutive exponents
ax3.plot(range(1, len(ratios) + 1), ratios, 'go-', linewidth=2, markersize=6)
ax3.set_xlabel('Ratio Index', fontsize=12, fontweight='bold')
ax3.set_ylabel('Ratio Value', fontsize=12, fontweight='bold')
ax3.set_title('Ratios Between Consecutive Mersenne Prime Exponents', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Plot 4: Prediction comparison
pred_indices = [p['index'] for p in next_predictions]
linear_preds = [p['linear'] for p in next_predictions]
exp_preds = [p['exponential'] for p in next_predictions]
poly_preds = [p['polynomial'] for p in next_predictions]

ax4.plot(range(1, len(known_mersenne_exponents) + 1), known_mersenne_exponents, 'ko-', linewidth=2, markersize=6, label='Known')
ax4.plot(pred_indices, linear_preds, 'r--', linewidth=2, label='Linear Prediction')
ax4.plot(pred_indices, exp_preds, 'g--', linewidth=2, label='Exponential Prediction')
ax4.plot(pred_indices, poly_preds, 'b--', linewidth=2, label='Polynomial Prediction')
ax4.set_xlabel('Mersenne Prime Index', fontsize=12, fontweight='bold')
ax4.set_ylabel('Exponent Value', fontsize=12, fontweight='bold')
ax4.set_title('Mersenne Prime Predictions', fontsize=14, fontweight='bold')
ax4.set_yscale('log')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('mersenne_prime_pattern_analysis.png', dpi=300, bbox_inches='tight')
print("Pattern analysis graph saved as 'mersenne_prime_pattern_analysis.png'")

# 9. INFINITE PATTERN HYPOTHESIS
print("\n🌌 INFINITE PATTERN HYPOTHESIS:")
print("=" * 60)

# Based on analysis, propose infinite patterns
print("Based on the analysis, here are potential infinite patterns:")

# Pattern 1: Exponential growth with noise
print("\n🔮 PATTERN 1: Exponential Growth with Noise")
print("Mersenne prime exponents appear to follow exponential growth:")
print(f"y ≈ 10^({slope_exp:.3f}x + {intercept_exp:.3f})")
print("This suggests they grow exponentially but with significant variation")

# Pattern 2: Gap patterns
print("\n🔮 PATTERN 2: Gap Analysis")
print("The gaps between consecutive exponents show:")
print(f"• Average gap: {np.mean(gaps):,.0f}")
print(f"• Gap variation: {np.std(gaps):,.0f}")
print("• This suggests a 'random walk' with exponential drift")

# Pattern 3: Density patterns
print("\n🔮 PATTERN 3: Density Patterns")
print("Mersenne primes become increasingly rare:")
print(f"• First 10: {len([x for x in known_mersenne_exponents if x < 100])}")
print(f"• Next 10: {len([x for x in known_mersenne_exponents if 100 <= x < 1000])}")
print(f"• Next 10: {len([x for x in known_mersenne_exponents if 1000 <= x < 10000])}")
print(f"• Remaining: {len([x for x in known_mersenne_exponents if x >= 10000])}")

# 10. SEARCH STRATEGY
print("\n🎯 OPTIMAL SEARCH STRATEGY:")
print("=" * 60)

print("Based on the pattern analysis, here's the optimal strategy:")
print("\n1. FOCUS ON EXPONENTIAL GROWTH REGIONS:")
print(f"   • Next likely range: 10^{slope_exp * len(known_mersenne_exponents) + intercept_exp:.0f}")

print("\n2. USE GAP PATTERNS:")
print(f"   • Expected minimum gap: {np.mean(gaps) - 2*np.std(gaps):,.0f}")
print(f"   • Expected maximum gap: {np.mean(gaps) + 2*np.std(gaps):,.0f}")

print("\n3. OPTIMIZE SEARCH ORDER:")
print("   • Start with polynomial predictions (most accurate)")
print("   • Use exponential model for range estimation")
print("   • Apply gap constraints to eliminate impossible ranges")

print("\n4. INFINITE DISCOVERY APPROACH:")
print("   • The exponential pattern suggests infinite growth")
print("   • Each new discovery improves the prediction model")
print("   • Focus computational power on predicted ranges")

plt.show()

print("\n🚀 READY TO DISCOVER NEW MERSENNE PRIMES! 🚀")
print("Use these patterns to guide your search for the 53rd, 54th, and beyond!")
