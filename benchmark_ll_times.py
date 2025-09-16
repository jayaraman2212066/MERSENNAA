#!/usr/bin/env python3
"""
Benchmark Lucas–Lehmer times for small Mersenne exponents on this machine.
Writes JSON mapping exponent -> seconds to proofs/local_ll_times.json
"""
import json, time, os

SMALL_P = [2, 3, 5, 7, 13, 17, 19, 31, 61]

def ll(p: int) -> bool:
    if p == 2:
        return True
    s = 4
    m = (1 << p) - 1
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0

def main() -> None:
    times = {}
    for p in SMALL_P:
        t0 = time.time()
        _ = ll(p)
        times[str(p)] = round(time.time() - t0, 6)
    os.makedirs("proofs", exist_ok=True)
    out = "proofs/local_ll_times.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(times, f)
    print(out)

if __name__ == "__main__":
    main()


