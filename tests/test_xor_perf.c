/**
 * This test file evaluates the performance and correctness of the optimized XOR cipher implementation.
 * It compares the specialized 1-byte and 8-byte key paths against a baseline implementation to verify measurable speed improvements.
 * This code is AI-generated.
 */
#include "../vibe/include/vibe_crypt.h"
#include "../vibe/include/vibe_bench.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Baseline implementation (what was there before Bolt optimized it)
void baseline_xor_cipher(uint8_t* data, size_t len, const uint8_t* key, size_t key_len) {
    if (!data || !key || key_len == 0) return;
    size_t k = 0;
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key[k++];
        if (k == key_len) k = 0;
    }
}

int main() {
    size_t len = 50 * 1024 * 1024; // 50MB for test
    uint8_t* data = malloc(len);
    if (!data) return 1;

    uint8_t key1[1] = {0xAA};
    uint8_t key8[8] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};

    printf("--- Performance Benchmark ---\n");

    // Test 1-byte key
    memset(data, 0, len);
    VIBE_BENCHMARK("1-byte key (Baseline)", {
        baseline_xor_cipher(data, len, key1, 1);
    });

    memset(data, 0, len);
    VIBE_BENCHMARK("1-byte key (Optimized)", {
        vibe_xor_cipher(data, len, key1, 1);
    });

    // Test 8-byte key
    memset(data, 0, len);
    VIBE_BENCHMARK("8-byte key (Baseline)", {
        baseline_xor_cipher(data, len, key8, 8);
    });

    memset(data, 0, len);
    VIBE_BENCHMARK("8-byte key (Optimized)", {
        vibe_xor_cipher(data, len, key8, 8);
    });

    // Verification
    memset(data, 0x55, len);
    vibe_xor_cipher(data, len, key8, 8);
    // Apply again, should be 0x55
    vibe_xor_cipher(data, len, key8, 8);
    for (size_t i = 0; i < len; i++) {
        if (data[i] != 0x55) {
            printf("Error: Correctness check failed at index %zu\n", i);
            free(data);
            return 1;
        }
    }
    printf("Correctness check passed.\n");

    free(data);
    return 0;
}
