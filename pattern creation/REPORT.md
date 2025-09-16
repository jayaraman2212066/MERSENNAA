## Prime Analysis Report (Full dataset < 1e10)

- Total primes: 460,815,295
- Max prime: 9,999,999,967
- Max observed gap: 99,990,027 (at 1e8)
- Fitted constants:
  - b in π(n) ≈ n / (log n − b): -369.42166808313215
  - c in g_max(n) ≈ c · (log n)^2: 188592.8868211282

### Charts (full data)
- Gaps histogram: analysis_full/charts/gaps_hist.png
- Gaps histogram (log y): analysis_full/charts/gaps_hist_log.png
- Residue distribution (mod 30): analysis_full/charts/residues_mod.png
- Residues top-10 share: analysis_full/charts/residues_pie.png
- Milestones: analysis_full/charts/milestones.png
- b(n) trend: analysis_full/charts/b_trend.png
- (log n)^2 overlay: analysis_full/charts/gap_overlay_log2.png
- Summary text: analysis_full/charts/summary_text.png

### Interpreting results
- Density: π(n) tracks n/log n with a fitted shift b; the adjusted n/(log n − b) aligns better across scales.
- Gaps: Bulk of gaps are small even at high n; the observed extreme gap is consistent with c (log n)^2 scaling.
- Residues: As expected, primes concentrate on reduced residue classes mod 30.

### Usage
- Composite generator (guided search + certification):
  - python prime_formula.py 1000000000 --direction 1
- Re-generate charts:
  - python plot_analysis.py --summary "analysis_full/summary.json" --outdir "analysis_full/charts"
