"""
Lightweight heuristic number theory helpers used by the advanced search.

All functions are fast, dependency-free approximations sufficient for
ranking candidate exponents. They are NOT used for proof of primality.
"""

from __future__ import annotations

import math


def prime_number_theorem_pi_estimate(x: int | float) -> float:
    """
    Estimate of π(x) using the Prime Number Theorem: π(x) ~ x / log x.
    Returns 0.0 for x < 3 to avoid log-domain issues.
    """
    if x < 3:
        return 0.0
    return float(x) / max(1e-9, math.log(float(x)))


def li_estimate(x: int | float) -> float:
    """
    Logarithmic integral approximation li(x). For simplicity, use the
    offset series around log and a numerical fallback for small x.
    This is a crude approximation suitable only for ranking.
    """
    if x <= 0:
        return 0.0
    # Numerical quadrature with simple composite Simpson on [2, x]
    a = 2.0
    b = float(x)
    if b <= a:
        return 0.0
    n = 256  # fixed small number of panels
    h = (b - a) / n
    def f(t: float) -> float:
        return 1.0 / max(1e-12, math.log(t))
    s = f(a) + f(b)
    for i in range(1, n):
        t = a + i * h
        s += (4.0 if i % 2 == 1 else 2.0) * f(t)
    return 0.5 * h * s


def cramers_gap_estimate(x: int | float) -> float:
    """
    Cramér's conjecture heuristic for prime gaps near x: O((log x)^2).
    """
    if x < 3:
        return 1.0
    lx = math.log(float(x))
    return lx * lx


def hardy_littlewood_twin_constant() -> float:
    """Return the Hardy-Littlewood twin prime constant A2 ≈ 0.6601618."""
    return 0.66016181584686957392781211001455577843


