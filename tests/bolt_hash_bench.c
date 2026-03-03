/**
 * This benchmark measures the performance of the vibe_simple_hash function.
 * It hashes a 1024-byte string 1,000,000 times and reports the elapsed time.
 * This code is AI-generated.
 */
#include <stdio.h>
#include <string.h>
#include "vibe_crypt.h"
#include "vibe_time.h"

// Non-optimized version for baseline comparison
__attribute__((noinline))
uint64_t baseline_hash(const char* str) {
    if (!str) return 0;
    uint64_t hash = 5381;
    unsigned char c;
    while ((c = (unsigned char)*str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

// We also need to prevent vibe_simple_hash from being inlined if we want a fair comparison
// but it's defined as static inline in the header.
// Let's use a volatile sink to prevent the loop from being optimized away.

int main() {
    char buffer[1024];
    memset(buffer, 'A', sizeof(buffer));
    buffer[1023] = '\0';

    int iterations = 1000000;
    volatile uint64_t sink = 0;

    // Warm up
    for(int i=0; i<100000; i++) sink = baseline_hash(buffer);

    printf("Benchmarking baseline_hash with %d iterations on 1024-byte string...\n", iterations);
    double start = vibe_get_time();
    for (int i = 0; i < iterations; i++) {
        sink = baseline_hash(buffer);
    }
    double end = vibe_get_time();
    double baseline_time = end - start;
    printf("Baseline time: %.6f seconds\n", baseline_time);

    sink = 0;
    // Warm up
    for(int i=0; i<100000; i++) sink = vibe_simple_hash(buffer);

    printf("Benchmarking optimized vibe_simple_hash with %d iterations on 1024-byte string...\n", iterations);
    start = vibe_get_time();
    for (int i = 0; i < iterations; i++) {
        sink = vibe_simple_hash(buffer);
    }
    end = vibe_get_time();
    double optimized_time = end - start;
    printf("Optimized time: %.6f seconds\n", optimized_time);

    printf("Speedup: %.2fx\n", baseline_time / optimized_time);
    printf("Improvement: %.2f%%\n", (baseline_time - optimized_time) / baseline_time * 100.0);

    (void)sink;
    return 0;
}
