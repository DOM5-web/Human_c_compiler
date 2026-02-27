/**
 * This header provides a portable wrapper for SIMD (Single Instruction, Multiple Data) intrinsics.
 * In version 1.5.6, it continues to automatically include correct intrinsic headers based on the architecture.
 * This code is AI-generated.
 */
#ifndef VIBE_SIMD_H
#define VIBE_SIMD_H

// Internal Logic: Detect architecture and include the corresponding SIMD intrinsic header.
#if defined(__x86_64__)
    #include <immintrin.h>
#elif defined(__aarch64__)
    #include <arm_neon.h>
#endif

#endif
