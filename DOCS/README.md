# Vibe C Compiler Documentation

## CLI Commands

- `install`: Installs the compiler globally as the `vcc` command.
- `uninstall`: Removes the global `vcc` symlink from `~/.local/bin`.
- `init <name>`: Creates a new Vibe C project.
  - `--template <name>`: Use a specific project template (e.g., `basic`, `minimal`).
- `build`: Compiles the project using parallel and incremental builds.
  - `--arch <target>`: Specify target architecture (e.g., `aarch64-linux-gnu`).
  - `--lib <type>`: Build as `static` or `shared` library.
- `run`: Builds and executes the project.
- `test`: Automatically finds, compiles (in parallel), and runs C tests in the `tests/` directory.
- `clean`: Removes the `build/` directory.
- `menu`: Opens the interactive menu.
- `version`: Shows the current version.
- `audit`: Runs a security audit on the compiler and your project.
- `update` / `upgrade`: Updates the Vibe C Compiler from its GitHub repository.
- `status`: Displays current project information (name, version, type, sources, and build artifacts).
- `headers`: Lists all available Vibe C custom headers.
- `templates`: Lists all available project templates.

## Custom Headers

Vibe C comes with 25 custom headers located in `vibe/include/`. You can include them in your source code using `#include <vibe_xxx.h>`.

### Core Headers
- `vibe_std.h`: Core types and version info. Includes `stdint.h`, `stdbool.h`, and `stdio.h`.
- `vibe_io.h`: Simple printing macros like `vibe_print()`.
- `vibe_math.h`: Math constants and min/max macros.
- `vibe_string.h`: String comparison helpers like `vibe_str_eq()`.
- `vibe_sys.h`: OS detection macros (`VIBE_LINUX`, `VIBE_WINDOWS`, `VIBE_MACOS`).
- `vibe_arg.h`: Simple command-line argument parsing utilities (`vibe_arg_has`, `vibe_arg_get`).

### Architecture & Optimization
- `vibe_arch.h`: Top-level architecture include.
- `vibe_simd.h`: SIMD intrinsics wrapper.
- `vibe_x86_64.h`: x86_64 specific definitions.
- `vibe_arm64.h`: ARM64 specific definitions.
- `vibe_rv64.h`: RISC-V specific definitions.

### Utilities
- `vibe_mem.h`: Memory allocation wrappers.
- `vibe_time.h`: High-resolution monotonic timer.
- `vibe_log.h`: Logging macros (`INFO`, `WARN`, `ERROR`).
- `vibe_bench.h`: Micro-benchmarking macro.
- `vibe_test.h`: Simple unit testing assertions.
- `vibe_color.h`: ANSI terminal color codes.
- `vibe_ui.h`: Simple UI/Terminal helpers.
- `vibe_file.h`: Easy file reading utility.
- `vibe_json.h`: JSON parsing and printing.
- `vibe_thread.h`: Simple pthread wrapper.
- `vibe_net.h`: TCP listening and connecting.
- `vibe_crypt.h`: Simple XOR and hashing.
- `vibe_regex.h`: POSIX regex wrapper.
- `vibe_thread_pool.h`: Worker thread pool implementation.

## Project Configuration

Every project contains a `vibe.json` file:

```json
{
  "name": "my_project",
  "version": "1.0.0",
  "type": "executable"
}
```

## Cross-Compilation

To cross-compile for another architecture, use the `--arch` flag:

```bash
./vibe_c_compiler build --arch aarch64-linux-gnu
```

This uses Clang's `-target` flag internally.

## Security Audit

Vibe C includes a built-in security audit command to help identify potential vulnerabilities:

```bash
vcc audit
```

This command performs:
1.  **Internal Audit**: Built-in pattern-based checks for common C and Python security issues. As of v1.4.4, it features an optimized regex-based detection system that scans `src/` and `tests/` for unsafe functions (like `gets`, `strcpy`, `system`, `popen`, `printf` format risks) and Python anti-patterns with O(1) matching complexity per line. It supports detecting multiple issues per line in Python scripts.
2.  **Bandit** (Optional): A deeper security linter for Python (runs only if `bandit` is installed).
3.  **Cppcheck** (Optional): A more advanced static analysis tool for C/C++ (runs only if `cppcheck` is installed).

It is recommended to run this command regularly during development.

## Project Templates

Vibe C supports different project templates when initializing a project:

- `basic`: Standard project structure with `src/`, `build/`, and a sample `main.c`.
- `minimal`: A lightweight template for small projects.

Use the `--template` flag with the `init` command:

```bash
vcc init my_project --template minimal
```

You can list all available templates with `vcc templates`.

## Build System (Bolt ⚡)

Vibe C features a high-performance build system optimized for developer productivity:

- **Parallel Compilation & Testing**: Uses a worker thread pool to compile multiple source files and run tests simultaneously (v1.4.4).
- **Incremental Builds & Tests**: Automatically detects changed source, headers, and libraries to only recompile and rerun what is necessary.
- **Optimized NO-OP**: Efficient `os.scandir` scanning, cached header `mtime`, and multi-pattern matching ensure that builds, tests, and security audits are high-performance (v1.4.4).

---

## Project Navigation

- [Home (README)](../README.md)
- [Documentation](README.md)
- [Developer Docs](dev/README.md)
- [Security Policy](../SECURITY.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Contributors](../CONTRIBUTORS.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
