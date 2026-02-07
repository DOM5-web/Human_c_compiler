#ifndef VIBE_SIMD_H
#define VIBE_SIMD_H
#if defined(__x86_64__)
    #include <immintrin.h>
#elif defined(__aarch64__)
    #include <arm_neon.h>
#endif
#endif
