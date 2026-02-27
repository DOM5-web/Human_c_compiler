/**
 * This benchmark tool measures the performance gain of the optimized XOR cipher.
 * In version 1.5.6, it continues to compare specialized word-sized paths against a baseline loop.
 * This code is AI-generated.
 */
#include "../vibe/include/vibe_crypt.h"
#include "../vibe/include/vibe_bench.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * baseline_xor_cipher - Simple byte-wise XOR implementation for benchmarking comparison.
 */
void baseline_xor_cipher(uint8_t* data, size_t len, const uint8_t* key, size_t key_len) {
    if (!data || !key || key_len == 0) return;
    size_t k = 0;
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key[k++];
        if (k == key_len) k = 0;
    }
}

int main() {
    // Internal Logic: Allocate 100MB of data to ensure the cipher runs long enough for stable measurement.
    size_t len = 100 * 1024 * 1024; // 100MB for test
    uint8_t* data = malloc(len);
    if (!data) return 1;

    uint8_t key1[1] = {0xAA};
    uint8_t key4[4] = {0xDE, 0xAD, 0xBE, 0xEF};
    uint8_t key8[8] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};

    printf("--- Bolt XOR Performance Benchmark ---\n");

    // 1-byte
    memset(data, 0, len);
    VIBE_BENCHMARK("1-byte key (Baseline)", {
        baseline_xor_cipher(data, len, key1, 1);
    });
    memset(data, 0, len);
    VIBE_BENCHMARK("1-byte key (Current Optimized)", {
        vibe_xor_cipher(data, len, key1, 1);
    });

    // 4-byte
    memset(data, 0, len);
    VIBE_BENCHMARK("4-byte key (Baseline)", {
        baseline_xor_cipher(data, len, key4, 4);
    });
    memset(data, 0, len);
    VIBE_BENCHMARK("4-byte key (Current)", {
        vibe_xor_cipher(data, len, key4, 4);
    });

    // 8-byte
    memset(data, 0, len);
    VIBE_BENCHMARK("8-byte key (Baseline)", {
        baseline_xor_cipher(data, len, key8, 8);
    });
    memset(data, 0, len);
    VIBE_BENCHMARK("8-byte key (Current Optimized)", {
        vibe_xor_cipher(data, len, key8, 8);
    });

    // Verification
    printf("--- Correctness Check ---\n");
    uint8_t key_mixed[3] = {0x11, 0x22, 0x33};
    memset(data, 0xAA, len);

    // Test 1-byte
    vibe_xor_cipher(data, len, key1, 1);
    vibe_xor_cipher(data, len, key1, 1);
    for(size_t i = 0; i < len; i++) if(data[i] != 0xAA) { printf("Fail 1-byte\n"); return 1; }
    printf("1-byte OK\n");

    // Test 4-byte
    vibe_xor_cipher(data, len, key4, 4);
    vibe_xor_cipher(data, len, key4, 4);
    for(size_t i = 0; i < len; i++) if(data[i] != 0xAA) { printf("Fail 4-byte\n"); return 1; }
    printf("4-byte OK\n");

    // Test 8-byte
    vibe_xor_cipher(data, len, key8, 8);
    vibe_xor_cipher(data, len, key8, 8);
    for(size_t i = 0; i < len; i++) if(data[i] != 0xAA) { printf("Fail 8-byte\n"); return 1; }
    printf("8-byte OK\n");

    // Test fallback
    vibe_xor_cipher(data, len, key_mixed, 3);
    vibe_xor_cipher(data, len, key_mixed, 3);
    for(size_t i = 0; i < len; i++) if(data[i] != 0xAA) { printf("Fail fallback\n"); return 1; }
    printf("Fallback OK\n");

    free(data);
    return 0;
}
