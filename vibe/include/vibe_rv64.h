/**
 * This header contains definitions and macros specifically for the RISC-V 64-bit architecture.
 * In version 1.5.6, it defines VIBE_ARCH_RISCV for RISC-V targets to allow for target-specific optimizations.
 * This code is AI-generated.
 */
#ifndef VIBE_RV64_H
#define VIBE_RV64_H

// Internal Logic: Define the architecture macro if the compiler target is RISC-V.
#ifdef __riscv
#define VIBE_ARCH_RISCV
#endif

#endif
