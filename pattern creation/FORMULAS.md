## Empirical formulas from prime dataset

- π(n) empirical fit: π(n) ≈ n / (log n - b)
  where b ≈ -369.42166808313215.

- Max gap growth: g_max(n) ≈ c · (log n)^2
  where c ≈ 188592.8868211282.

- Residue distribution mod m (default m=30): concentrated on reduced residue classes.

These parameters are estimated from the provided data using streaming statistics.

### Prime mapping over reals P(t)
For any real t ≥ 2, define P(t) to be the nearest prime in the chosen direction using:
- A composite likelihood score s(n) = 0.5 · (w_GA · f(n)) + NN(f(n)), with f(n) the feature vector on residues (mod 2,3,5,6,30) and fractional residues (mod 8,12,30), where:
  - w_GA are GA-evolved weights (saved in `ml/ga_weights.json`)
  - NN is a one-hidden-layer MLP (weights in `ml/nn_weights.json`)
- Guided search: step among 6k±1 candidates, prefer higher s(n), then
- Certify primality:
  - Deterministic Miller–Rabin (proven bases) for all 64-bit n
  - Baillie–PSW test beyond 64-bit

This yields a practical prime-generating function P(t) over the naturals/reals that maps any t ≥ 2 to a prime in the requested direction, and scales beyond the dataset.
