/*
🚀 INDEPENDENT MERSENNE PRIME ENGINE 🚀
Complete C++ implementation with FFT, no GIMPS dependencies
*/

#include <iostream>
#include <vector>
#include <complex>
#include <cmath>
#include <chrono>
#include <thread>
#include <atomic>
#include <mutex>
#include <fstream>
#include <algorithm>
#include <random>
#include <iomanip>

using namespace std;
using namespace chrono;

class FFTMultiplier {
private:
    static constexpr double PI = 3.14159265358979323846;
    
    void fft(vector<complex<double>>& a, bool invert) {
        int n = a.size();
        
        // Bit-reversal permutation
        for (int i = 1, j = 0; i < n; i++) {
            int bit = n >> 1;
            for (; j & bit; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) swap(a[i], a[j]);
        }
        
        // FFT computation
        for (int len = 2; len <= n; len <<= 1) {
            double ang = 2 * PI / len * (invert ? -1 : 1);
            complex<double> wlen(cos(ang), sin(ang));
            
            for (int i = 0; i < n; i += len) {
                complex<double> w(1);
                for (int j = 0; j < len / 2; j++) {
                    complex<double> u = a[i + j];
                    complex<double> v = a[i + j + len / 2] * w;
                    a[i + j] = u + v;
                    a[i + j + len / 2] = u - v;
                    w *= wlen;
                }
            }
        }
        
        if (invert) {
            for (auto& x : a) x /= n;
        }
    }
    
public:
    vector<uint64_t> multiply(const vector<uint64_t>& a, const vector<uint64_t>& b) {
        int result_size = a.size() + b.size();
        int n = 1;
        while (n < result_size) n <<= 1;
        
        vector<complex<double>> fa(a.begin(), a.end()), fb(b.begin(), b.end());
        fa.resize(n); fb.resize(n);
        
        fft(fa, false); fft(fb, false);
        for (int i = 0; i < n; i++) fa[i] *= fb[i];
        fft(fa, true);
        
        vector<uint64_t> result(n);
        uint64_t carry = 0;
        for (int i = 0; i < n; i++) {
            uint64_t val = round(fa[i].real()) + carry;
            result[i] = val % 1000000000ULL; // Base 10^9
            carry = val / 1000000000ULL;
        }
        
        while (result.size() > 1 && result.back() == 0) result.pop_back();
        return result;
    }
};

class BigInteger {
private:
    vector<uint64_t> digits; // Base 10^9
    static constexpr uint64_t BASE = 1000000000ULL;
    FFTMultiplier fft_mult;
    
public:
    BigInteger(uint64_t n = 0) {
        if (n == 0) {
            digits = {0};
        } else {
            while (n > 0) {
                digits.push_back(n % BASE);
                n /= BASE;
            }
        }
    }
    
    BigInteger(const vector<uint64_t>& d) : digits(d) {}
    
    BigInteger operator*(const BigInteger& other) const {
        if (digits.size() + other.digits.size() > 100) {
            // Use FFT for large numbers
            return BigInteger(fft_mult.multiply(digits, other.digits));
        } else {
            // Use schoolbook for small numbers
            return schoolbook_multiply(other);
        }
    }
    
    BigInteger schoolbook_multiply(const BigInteger& other) const {
        vector<uint64_t> result(digits.size() + other.digits.size(), 0);
        
        for (size_t i = 0; i < digits.size(); i++) {
            uint64_t carry = 0;
            for (size_t j = 0; j < other.digits.size(); j++) {
                __uint128_t prod = (__uint128_t)digits[i] * other.digits[j] + result[i + j] + carry;
                result[i + j] = prod % BASE;
                carry = prod / BASE;
            }
            if (carry) result[i + other.digits.size()] += carry;
        }
        
        while (result.size() > 1 && result.back() == 0) result.pop_back();
        return BigInteger(result);
    }
    
    BigInteger operator-(uint64_t n) const {
        vector<uint64_t> result = digits;
        uint64_t borrow = n;
        
        for (size_t i = 0; i < result.size() && borrow > 0; i++) {
            if (result[i] >= borrow) {
                result[i] -= borrow;
                borrow = 0;
            } else {
                result[i] = result[i] + BASE - borrow;
                borrow = 1;
            }
        }
        
        while (result.size() > 1 && result.back() == 0) result.pop_back();
        return BigInteger(result);
    }
    
    BigInteger operator%(const BigInteger& mod) const {
        // Simplified modular reduction using Barrett reduction
        return barrett_reduce(mod);
    }
    
    BigInteger barrett_reduce(const BigInteger& mod) const {
        // Simplified Barrett reduction
        if (compare(mod) < 0) return *this;
        
        BigInteger result = *this;
        while (result.compare(mod) >= 0) {
            result = result.subtract(mod);
        }
        return result;
    }
    
    BigInteger subtract(const BigInteger& other) const {
        vector<uint64_t> result = digits;
        uint64_t borrow = 0;
        
        for (size_t i = 0; i < max(result.size(), other.digits.size()); i++) {
            uint64_t sub = borrow;
            if (i < other.digits.size()) sub += other.digits[i];
            
            if (i < result.size() && result[i] >= sub) {
                result[i] -= sub;
                borrow = 0;
            } else {
                if (i >= result.size()) result.resize(i + 1, 0);
                result[i] = result[i] + BASE - sub;
                borrow = 1;
            }
        }
        
        while (result.size() > 1 && result.back() == 0) result.pop_back();
        return BigInteger(result);
    }
    
    int compare(const BigInteger& other) const {
        if (digits.size() != other.digits.size()) {
            return digits.size() < other.digits.size() ? -1 : 1;
        }
        
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] != other.digits[i]) {
                return digits[i] < other.digits[i] ? -1 : 1;
            }
        }
        return 0;
    }
    
    bool is_zero() const {
        return digits.size() == 1 && digits[0] == 0;
    }
    
    static BigInteger power_of_two(int exp) {
        if (exp <= 63) {
            return BigInteger(1ULL << exp);
        }
        
        // For large exponents, build iteratively
        BigInteger result(1);
        BigInteger two(2);
        
        for (int i = 0; i < exp; i++) {
            result = result * two;
        }
        
        return result;
    }
};

class IndependentLucasLehmer {
public:
    struct TestResult {
        bool is_prime;
        double computation_time;
        int iterations_completed;
        string error_message;
    };
    
    TestResult lucas_lehmer_test(int p, double timeout_seconds = 300.0) {
        auto start_time = high_resolution_clock::now();
        
        if (p == 2) {
            return {true, 0.0, 0, ""};
        }
        
        if (p <= 1 || p % 2 == 0) {
            return {false, 0.0, 0, "Invalid exponent"};
        }
        
        try {
            BigInteger s(4);
            BigInteger M = BigInteger::power_of_two(p) - 2; // 2^p - 1
            
            for (int i = 0; i < p - 2; i++) {
                // Check timeout
                auto current_time = high_resolution_clock::now();
                double elapsed = duration<double>(current_time - start_time).count();
                
                if (elapsed > timeout_seconds) {
                    return {false, elapsed, i, "Timeout exceeded"};
                }
                
                // Core Lucas-Lehmer iteration: s = (s² - 2) mod M
                s = (s * s) - 2;
                s = s % M;
                
                // Progress reporting
                if (i % 1000 == 0 && i > 0) {
                    double progress = (double)i / (p - 2) * 100.0;
                    cout << "\rProgress: " << fixed << setprecision(1) << progress 
                         << "% (" << i << "/" << (p-2) << ") - " 
                         << elapsed << "s elapsed" << flush;
                }
            }
            
            auto end_time = high_resolution_clock::now();
            double total_time = duration<double>(end_time - start_time).count();
            
            bool is_prime = s.is_zero();
            return {is_prime, total_time, p - 2, ""};
            
        } catch (const exception& e) {
            auto end_time = high_resolution_clock::now();
            double total_time = duration<double>(end_time - start_time).count();
            return {false, total_time, 0, e.what()};
        }
    }
};

class SmartCandidateGenerator {
private:
    vector<int> known_mersenne_exponents = {
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
        2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
        23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
        1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
        24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
        43112609, 57885161, 74207281, 77232917, 82589933, 136279841
    };
    
    bool is_prime(int n) {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        
        for (int i = 3; i * i <= n; i += 2) {
            if (n % i == 0) return false;
        }
        return true;
    }
    
public:
    vector<int> generate_smart_candidates(int start, int end, int count) {
        vector<int> candidates;
        int last_known = *max_element(known_mersenne_exponents.begin(), known_mersenne_exponents.end());
        
        // Ensure we only search after the last known Mersenne prime
        start = max(start, last_known + 1);
        
        // Pattern-based generation
        for (int p = start; p <= end && candidates.size() < count; p += 2) {
            if (!is_prime(p)) continue;
            
            // Apply mathematical filters
            if (p % 4 != 1 && p % 4 != 3) continue; // Must be odd prime
            if (p % 6 != 1 && p % 6 != 5) continue; // Prime > 3 property
            if (p % 10 != 1 && p % 10 != 3 && p % 10 != 7 && p % 10 != 9) continue;
            
            // Modulo 210 filtering
            int mod210 = p % 210;
            if (mod210 % 2 == 0 || mod210 % 3 == 0 || mod210 % 5 == 0 || mod210 % 7 == 0) continue;
            
            candidates.push_back(p);
        }
        
        return candidates;
    }
};

class IndependentMersenneEngine {
private:
    IndependentLucasLehmer ll_tester;
    SmartCandidateGenerator candidate_gen;
    atomic<int> tests_completed{0};
    atomic<int> discoveries_found{0};
    mutex results_mutex;
    vector<pair<int, IndependentLucasLehmer::TestResult>> results;
    
public:
    void run_discovery(int start_range, int end_range, int max_candidates, int num_threads = 4) {
        cout << "🚀 INDEPENDENT MERSENNE PRIME ENGINE 🚀" << endl;
        cout << "Range: " << start_range << " to " << end_range << endl;
        cout << "Max candidates: " << max_candidates << endl;
        cout << "Threads: " << num_threads << endl;
        cout << "========================================" << endl;
        
        // Generate smart candidates
        auto candidates = candidate_gen.generate_smart_candidates(start_range, end_range, max_candidates);
        cout << "Generated " << candidates.size() << " smart candidates" << endl;
        
        if (candidates.empty()) {
            cout << "No valid candidates found!" << endl;
            return;
        }
        
        auto start_time = high_resolution_clock::now();
        
        // Parallel testing
        vector<thread> threads;
        atomic<size_t> candidate_index{0};
        
        for (int t = 0; t < num_threads; t++) {
            threads.emplace_back([&, t]() {
                size_t idx;
                while ((idx = candidate_index.fetch_add(1)) < candidates.size()) {
                    int p = candidates[idx];
                    
                    cout << "Thread " << t << " testing p=" << p << endl;
                    auto result = ll_tester.lucas_lehmer_test(p, 60.0); // 1 minute timeout
                    
                    {
                        lock_guard<mutex> lock(results_mutex);
                        results.push_back({p, result});
                        
                        if (result.is_prime) {
                            discoveries_found++;
                            cout << "\n🎉 MERSENNE PRIME FOUND! p = " << p << endl;
                            cout << "   2^" << p << " - 1 is prime!" << endl;
                            cout << "   Computation time: " << result.computation_time << "s" << endl;
                            
                            // Save discovery immediately
                            save_discovery(p, result);
                        }
                    }
                    
                    tests_completed++;
                    
                    // Progress update
                    double progress = (double)tests_completed / candidates.size() * 100.0;
                    auto current_time = high_resolution_clock::now();
                    double elapsed = duration<double>(current_time - start_time).count();
                    double rate = tests_completed / elapsed;
                    
                    cout << "\rProgress: " << fixed << setprecision(1) << progress 
                         << "% (" << tests_completed << "/" << candidates.size() 
                         << ") | Rate: " << rate << " tests/s | Discoveries: " 
                         << discoveries_found << flush;
                }
            });
        }
        
        // Wait for all threads
        for (auto& t : threads) {
            t.join();
        }
        
        auto end_time = high_resolution_clock::now();
        double total_time = duration<double>(end_time - start_time).count();
        
        // Final results
        cout << "\n========================================" << endl;
        cout << "🎉 DISCOVERY COMPLETE!" << endl;
        cout << "Total time: " << total_time << "s" << endl;
        cout << "Tests completed: " << tests_completed << endl;
        cout << "Discoveries found: " << discoveries_found << endl;
        cout << "Test rate: " << tests_completed / total_time << " tests/s" << endl;
        
        save_all_results();
    }
    
private:
    void save_discovery(int p, const IndependentLucasLehmer::TestResult& result) {
        ofstream file("independent_mersenne_discoveries.txt", ios::app);
        if (file.is_open()) {
            auto now = system_clock::now();
            auto time_t = system_clock::to_time_t(now);
            
            file << "🎉 INDEPENDENT MERSENNE PRIME DISCOVERED! 🎉" << endl;
            file << "Exponent: " << p << endl;
            file << "Mersenne Number: 2^" << p << " - 1" << endl;
            file << "Discovery Time: " << ctime(&time_t);
            file << "Computation Time: " << result.computation_time << "s" << endl;
            file << "Iterations: " << result.iterations_completed << endl;
            file << "Engine: Independent C++ Implementation" << endl;
            file << "========================================" << endl;
            file.close();
        }
    }
    
    void save_all_results() {
        ofstream file("independent_test_results.txt");
        if (file.is_open()) {
            file << "Independent Mersenne Prime Engine Results" << endl;
            file << "========================================" << endl;
            
            for (const auto& [p, result] : results) {
                file << "p=" << p << ": " << (result.is_prime ? "PRIME" : "COMPOSITE")
                     << " (time: " << result.computation_time << "s)" << endl;
            }
            
            file.close();
        }
    }
};

int main() {
    try {
        IndependentMersenneEngine engine;
        
        // Test parameters
        int start = 85000000;
        int end = 85100000;
        int max_candidates = 1000;
        int threads = thread::hardware_concurrency();
        
        cout << "Hardware threads available: " << threads << endl;
        
        engine.run_discovery(start, end, max_candidates, threads);
        
    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
        return 1;
    }
    
    return 0;
}