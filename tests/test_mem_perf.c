#include "../vibe/include/vibe_mem.h"
#include "../vibe/include/vibe_bench.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

void baseline_secure_memzero(void* p, size_t len) {
    if (!p) return;
    volatile unsigned char* ptr = (volatile unsigned char*)p;
    while (len--) {
        *ptr++ = 0;
    }
}

int main() {
    size_t len = 100 * 1024 * 1024; // 100MB
    void* data = malloc(len + 8);
    if (!data) return 1;

    // Test with unaligned pointer
    void* p = (void*)((uintptr_t)data + 1);

    printf("--- Secure Memzero Performance Benchmark ---\n");

    VIBE_BENCHMARK("Baseline Secure Memzero", {
        baseline_secure_memzero(p, len);
    });

    VIBE_BENCHMARK("Optimized vibe_secure_memzero", {
        vibe_secure_memzero(p, len);
    });

    free(data);
    return 0;
}
