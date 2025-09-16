## ML components for prime pattern discovery

- Neural Networks: small NumPy MLP to classify integers as prime/composite using handcrafted features; intended for small/medium ranges.
- Genetic Algorithms: evolve linear heuristic scorers over features to guide prime search.
- Pattern Mining: stream statistics from prime lists to extract frequent residues, gap motifs, and simple co-occurrence patterns.

### Quick start

Train NN classifier (small demo):

```
python ml/nn_classifier.py --train 20000 --val 5000 --epochs 5
```

Run GA to evolve a heuristic:

```
python ml/ga_heuristic.py --train 50000 --generations 30
```

Mine patterns from `primelists`:

```
python ml/pattern_mining.py --max-files 5 --residue-mod 30
```

All tools use only NumPy to keep dependencies minimal.


