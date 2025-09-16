#include <bits/stdc++.h>
using namespace std;

// Deterministic Miller-Rabin for 32-bit integers (n < 2^32)
// Bases {2, 3, 5, 7, 11} are sufficient for < 3,474,749,660,383 but our p <= ~1.2e8

static inline uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t mod){
    return (a * b) % mod;
}

static uint64_t pow_mod(uint64_t a, uint64_t d, uint64_t mod){
    uint64_t r = 1;
    a %= mod;
    while(d){
        if(d & 1) r = mul_mod(r, a, mod);
        a = mul_mod(a, a, mod);
        d >>= 1;
    }
    return r;
}

static bool miller_rabin(uint32_t n){
    if(n < 2) return false;
    static uint32_t small_primes[] = {2,3,5,7,11,13,17,19,23,29,31};
    for(uint32_t p: small_primes){ if(n == p) return true; if(n % p == 0 && n != p) return false; }
    uint32_t d = n - 1, r = 0; while((d & 1) == 0){ d >>= 1; r++; }
    uint32_t bases[] = {2, 3, 5, 7, 11};
    for(uint32_t a: bases){
        if(a >= n) continue;
        uint64_t x = pow_mod(a, d, n);
        if(x == 1 || x == n - 1) continue;
        bool ok = false;
        for(uint32_t i = 1; i < r; i++){
            x = mul_mod(x, x, n);
            if(x == n - 1){ ok = true; break; }
        }
        if(!ok) return false;
    }
    return true;
}

int main(int argc, char** argv){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    if(argc < 3){
        cerr << "Usage: candidate_generator <range_start> <range_end>\n";
        return 1;
    }
    long long start = atoll(argv[1]);
    long long end = atoll(argv[2]);
    if(start < 2) start = 2;
    if(end < start){
        return 0;
    }
    // Generate prime exponents (odd primes only)
    if(start % 2 == 0) start++;
    for(long long p = start; p <= end; p += 2){
        if(miller_rabin((uint32_t)p)){
            cout << p << '\n';
        }
    }
    return 0;
}


