# Vibe C Compiler - Architecture

## Overview

The Vibe C Compiler is a high-level project manager and compiler driver for C. It is designed to simplify the development workflow by providing a structured project environment, high-performance builds, and built-in security auditing.

## Core Components

### 1. The Compiler Driver (`VibeCompiler`)
Located in `vibe/core/compiler.py`, this class is the heart of the system. It encapsulates all project management and compilation logic.

- **Project Lifecycle**: Methods like `init_project`, `build_project`, `run_project`, and `clean_project` manage the standard development cycle.
- **Incremental Build Engine**: Uses file modification times (`os.path.getmtime`) and cached header metadata to skip redundant compilation steps.
- **Parallel Task Runner**: Leverages `ThreadPoolExecutor` for concurrent compilation, test execution, and security auditing.
- **Security Auditor**: Implements a high-performance, parallelized regex-based scanning system for vulnerabilities.

### 2. Built-in Headers (`vibe/include/`)
Vibe C provides a suite of 25 custom headers that offer a "standard library" experience for common tasks like SIMD, JSON parsing, networking, and UI.

### 3. Template System (`vibe/templates/`)
Supports quick project initialization using pre-defined directory structures (e.g., `basic`, `minimal`).

### 4. CLI Interface (`main.py` & `vibe_c_compiler`)
A clean command-line interface built with `argparse`, and an optional interactive TUI menu (`menu.py`).

## Compilation Flow

1.  **Project Discovery**: The compiler reads `vibe.json` to understand the project configuration (name, type, etc.).
2.  **Header Scanning**: Performs a recursive scan of `src/` and the global `vibe/include/` directory to find the latest modification time among all `.h` files.
3.  **Source Filtering**: Identifies `.c` files in `src/` that are newer than their corresponding `.o` files in `build/obj/` or newer than the latest header change.
4.  **Parallel Compilation**: Spawns worker threads to run `clang` on each source file that needs compilation.
5.  **Linking**: Combines object files into the final executable, static library, or shared library.

## Security Architecture (Sentinel 🛡️)

- **Defense in Depth**: Combines input validation, safe subprocess management, and static analysis.
- **Input Sanitization**: All CLI arguments and `vibe.json` values are validated against strict regex patterns before being used in file paths or commands.
- **Sanitized Environments**: Ensures environment variables like `LD_LIBRARY_PATH` do not contain empty entries that could lead to library hijacking.
- **Binary Hardening**: Automatically applies industry-standard security flags (`-fstack-protector-strong`, PIE, RELRO, etc.) to all compiled binaries and tests to mitigate memory corruption exploits (v1.4.5).
- **Audit System Optimization**: Uses `re.finditer` and $O(\log N)$ line-numbering for rapid scanning, with word-boundary matching to prevent bypasses (v1.4.7). As of v1.4.8, it also performs self-auditing of internal headers and includes expanded pattern detection.
- **Secure Memory Primitives**: Implemented `vibe_secure_memzero` in `vibe_mem.h` to reliably clear sensitive data (v1.4.8).
- **String Security**: Implemented `vibe_str_eq_constant_time` to mitigate timing attacks on sensitive string comparisons (v1.4.9).
- **Library Robustness**: Core headers include NULL pointer checks and secure, fully-compliant JSON escaping (v1.4.7/v1.4.9).

## Performance Engineering (Bolt ⚡)

- **Minimizing I/O**: Efficient `os.scandir` traversal and metadata caching for global headers.
- **Optimized Regex**: Use of combined regular expressions for $O(1)$ pattern matching per line in the security auditor.
- **Concurrency**: Maximum utilization of CPU cores for CPU-bound compilation tasks.

---

## Project Navigation

- [Home (README)](../../README.md)
- [Documentation](../README.md)
- [Developer Docs](README.md)
- [Security Policy](../../SECURITY.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Contributors](../../CONTRIBUTORS.md)
- [Code of Conduct](../../CODE_OF_CONDUCT.md)
