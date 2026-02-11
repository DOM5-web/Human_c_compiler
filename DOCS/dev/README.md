# Vibe C Compiler - Developer Documentation

Welcome to the internal documentation for Vibe C Compiler.

## Architecture Overview

The Vibe C Compiler is a Python-based driver that wraps Clang to provide a more streamlined C development experience.

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
- The `update` command is pinned to the compiler's root directory to prevent accidental modification of user projects.

### Internal Audit
The `audit` command uses simple but effective pattern matching to detect common C vulnerabilities (`gets`, `strcpy`, `system`, etc.) without requiring external dependencies.

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
