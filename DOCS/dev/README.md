# Vibe C Compiler - Developer Documentation

Welcome to the internal documentation for Vibe C Compiler.

## Architecture Overview

The Vibe C Compiler is a Python-based driver that wraps Clang to provide a more streamlined C development experience. For a deep dive into the system components, see [Architecture](architecture.md).

### Directory Structure

- `vibe/`: Core package containing all compiler logic.
  - `core/`: Main Python logic.
    - `main.py`: Entry point and CLI argument parsing.
    - `compiler.py`: The `VibeCompiler` class, implementing all commands and build logic.
    - `menu.py`: TUI menu implementation.
  - `include/`: Custom C headers provided by Vibe C.
  - `templates/`: Project scaffolding templates (e.g., `basic`, `minimal`).
- `vibe_c_compiler`: Root executable script.
- `Jules/`: Internal developer logs and security records.
- `DOCS/`: Project documentation.

## Build System (Bolt ⚡)

The build system in `vibe/core/compiler.py` is designed for speed (Bolt philosophy).

### Parallel Compilation & Testing
We use `concurrent.futures.ThreadPoolExecutor` to parallelize both the compilation of source files and the execution of tests.
- **Builds**: Compiles multiple `.c` files in parallel.
- **Tests**: Compiles and runs multiple test files concurrently, significantly reducing the test cycle time.

### Incremental Logic
- **Centralized Scanning**: A reusable `_get_header_mtime` method performs a single-pass scan of `src/` and `vibe/include/` for headers.
- **Modification Times**: We compare the `mtime` of source files and headers against existing artifacts.
- **Build Incrementalism**: Checks `.c` and `.h` files against object files in `build/obj/`.
- **Test Incrementalism**: Checks test source files, project headers, and the compiled project library against test binaries in `build/tests/`.
- **NO-OP Optimization**: Before starting the thread pool, we filter out files that are already up-to-date. This avoids the overhead of managing a thread pool when nothing needs to be done (v1.4.1/v1.4.2).

## Security (Sentinel 🛡️)

Security is a core pillar of Vibe C (Sentinel philosophy).

### Input Validation
Every user-provided argument that affects file paths or shell commands is strictly validated using regex:
- Project names and templates: `^[a-zA-Z0-9_-]+$`
- Architecture targets: `^[a-zA-Z0-9._-]+$`

### Safe Execution
- We use `subprocess.run` with argument lists (not shell strings) to prevent command injection.
- Absolute paths are used where appropriate.
- **Command Anchoring**: The `update` command is pinned to the compiler's root directory (`self.base_dir`) in `subprocess.run(..., cwd=self.base_dir)` to prevent accidental modification of user projects (v1.4.4).

### Internal Audit
The `audit` command uses an optimized regex-based detection system to identify common C vulnerabilities and Python security anti-patterns.
- **Combined Regex**: Patterns are combined into a single pre-compiled regex with alternation to ensure $O(Lines)$ complexity, avoiding the $O(Lines \times Patterns)$ overhead of multiple passes (v1.4.4).
- **Named Groups**: Python pattern matching uses named capture groups for efficient identification of the specific vulnerability detected.
- **Word Boundaries**: C and Python patterns use `\b` word boundaries to prevent false positives (e.g., matching `execute` when searching for `exec`).

### Environment Sanitization
- **LD_LIBRARY_PATH**: In `run_tests`, we explicitly sanitize `LD_LIBRARY_PATH` by splitting it, filtering out empty entries (which are interpreted as the current directory `.` by the dynamic linker), and then prepending the `build` directory. This mitigates shared library injection vulnerabilities (v1.4.4).

### Secure Utilities
- **JSON Printing**: The `vibe_json.h` header includes a secure string printing helper that escapes double quotes and backslashes. This prevents JSON structure injection when printing user-provided strings from C applications (v1.4.4).

### Binary Hardening
Vibe C automatically applies security hardening flags during the compilation and linking phases to protect produced binaries against common exploits (v1.4.5):
- **Stack Protection**: Uses `-fstack-protector-strong` to protect against stack buffer overflows.
- **Fortify Source**: Enables `-D_FORTIFY_SOURCE=2` for additional run-time checks on standard library functions.
- **Format String Security**: Enforces `-Wformat`, `-Wformat-security`, and `-Werror=format-security` to prevent format string vulnerabilities.
- **ASLR (PIE)**: Compiles with `-fPIE` and links with `-pie` to ensure Position Independent Executables, enabling Address Space Layout Randomization.
- **Linker Hardening**: Uses `-Wl,-z,relro,-z,now` for full Relocation Read-Only (RELRO) and immediate binding to protect the Global Offset Table (GOT).

## Contributing

When making changes:
1.  **Keep it fast**: Ensure that build times remain low.
2.  **Keep it secure**: Always validate new inputs.
3.  **Document everything**: Update the relevant `MD` files and this dev log.

---

## Project Navigation

- [Home (README)](../../README.md)
- [Documentation](../README.md)
- [Developer Docs](README.md)
- [Security Policy](../../SECURITY.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Contributors](../../CONTRIBUTORS.md)
- [Code of Conduct](../../CODE_OF_CONDUCT.md)
