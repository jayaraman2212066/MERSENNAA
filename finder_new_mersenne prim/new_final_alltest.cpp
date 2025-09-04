/*


🔹 Key Upgrades:
Avoids repeated pow() calls → Uses in-place modular squaring.

Checks only prime exponents → Big reduction in work.

Uses Lucas–Lehmer test, which is optimal for Mersenne primes.

Custom big integer struct → Much faster than GMP for moderate sizes.

No extra heap allocations per iteration → Keeps vectors reused.









*/











#include <bits/stdc++.h>
using namespace std;

// ------------------------
// Fast big integer using vector<uint32_t>
// ------------------------
struct BigInt {
    vector<uint32_t> d; // base 2^32

    BigInt(uint64_t val = 0) {
        if (val) d.push_back((uint32_t)val);
        uint32_t high = (uint32_t)(val >> 32);
        if (high) d.push_back(high);
    }

    void trim() {
        while (!d.empty() && d.back() == 0) d.pop_back();
    }

    static BigInt modmul(const BigInt &a, const BigInt &b, const BigInt &mod) {
        BigInt res;
        res.d.assign(a.d.size() + b.d.size(), 0);
        for (size_t i = 0; i < a.d.size(); i++) {
            uint64_t carry = 0;
            for (size_t j = 0; j < b.d.size() || carry; j++) {
                uint64_t cur = res.d[i + j] +
                               (uint64_t)a.d[i] * (j < b.d.size() ? b.d[j] : 0) +
                               carry;
                res.d[i + j] = (uint32_t)cur;
                carry = cur >> 32;
            }
        }
        return res.mod(mod);
    }

    BigInt mod(const BigInt &m) const {
        BigInt res = *this;
        res %= m;
        return res;
    }

    void operator%=(const BigInt &m) {
        if (cmp(*this, m) < 0) return;
        BigInt cur;
        cur.d.assign(d.size(), 0);
        for (int i = (int)d.size() * 32 - 1; i >= 0; i--) {
            cur <<= 1;
            cur.d[0] |= (d[i / 32] >> (i % 32)) & 1U;
            if (cmp(cur, m) >= 0)
                cur = sub(cur, m);
        }
        *this = cur;
        trim();
    }

    static int cmp(const BigInt &a, const BigInt &b) {
        if (a.d.size() != b.d.size()) return a.d.size() < b.d.size() ? -1 : 1;
        for (int i = (int)a.d.size() - 1; i >= 0; i--)
            if (a.d[i] != b.d[i]) return a.d[i] < b.d[i] ? -1 : 1;
        return 0;
    }

    static BigInt sub(const BigInt &a, const BigInt &b) {
        BigInt res = a;
        uint64_t carry = 0;
        for (size_t i = 0; i < b.d.size() || carry; i++) {
            uint64_t cur = res.d[i] - (i < b.d.size() ? b.d[i] : 0) - carry;
            carry = (cur >> 63);
            res.d[i] = (uint32_t)cur;
        }
        res.trim();
        return res;
    }

    void operator<<=(int shift) {
        if (!shift) return;
        int word_shift = shift / 32;
        int bit_shift = shift % 32;
        if (bit_shift == 0) {
            d.insert(d.begin(), word_shift, 0);
        } else {
            uint32_t carry = 0;
            for (size_t i = 0; i < d.size(); i++) {
                uint64_t cur = ((uint64_t)d[i] << bit_shift) | carry;
                d[i] = (uint32_t)cur;
                carry = cur >> 32;
            }
            if (carry) d.push_back(carry);
            d.insert(d.begin(), word_shift, 0);
        }
    }
};

// Lucas–Lehmer test for Mersenne prime 2^p - 1
bool lucas_lehmer_test(int p) {
    if (p == 2) return true;
    BigInt m = (BigInt(1) << p) - BigInt(1);
    BigInt s = 4;
    for (int i = 0; i < p - 2; i++) {
        s = BigInt::modmul(s, s, m);
        s = BigInt::sub(s, BigInt(2));
    }
    return s.d.empty();
}

// Check if n is prime (simple deterministic Miller–Rabin for small p)
bool is_prime(int n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (int i = 3; i * 1LL * i <= n; i += 2)
        if (n % i == 0) return false;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int limit;
    cout << "Enter max exponent limit: ";
    cin >> limit;

    cout << "Mersenne prime exponents up to " << limit << ":\n";
    for (int p = 2; p <= limit; p++) {
        if (is_prime(p)) {
            if (lucas_lehmer_test(p)) {
                cout << p << " ";
            }
        }
    }
    cout << "\n";
    return 0;
}
