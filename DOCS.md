# Vibe C Compiler Documentation

## CLI Commands

- `install`: Installs the compiler globally as the `vcc` command.
- `init <name>`: Creates a new Vibe C project.
- `build`: Compiles the project.
  - `--arch <target>`: Specify target architecture (e.g., `aarch64-linux-gnu`).
  - `--lib <type>`: Build as `static` or `shared` library.
- `run`: Builds and executes the project.
- `clean`: Removes the `build/` directory.
- `menu`: Opens the interactive menu.
- `version`: Shows the current version.
- `audit`: Runs a security audit using `bandit` and `cppcheck`.
- `update`: Updates the Vibe C Compiler from its GitHub repository.
- `status`: Displays current project information (name, version, type).
- `headers`: Lists all available Vibe C custom headers.
- `templates`: Lists all available project templates.

## Custom Headers

Vibe C comes with 24 custom headers located in `vibe/include/`. You can include them in your source code using `#include <vibe_xxx.h>`.

### Core Headers
- `vibe_std.h`: Core types and version info. Includes `stdint.h`, `stdbool.h`, and `stdio.h`.
- `vibe_io.h`: Simple printing macros like `vibe_print()`.
- `vibe_math.h`: Math constants and min/max macros.
- `vibe_string.h`: String comparison helpers like `vibe_str_eq()`.
- `vibe_sys.h`: OS detection macros (`VIBE_LINUX`, `VIBE_WINDOWS`, `VIBE_MACOS`).

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

Vibe C v1.2.0 includes a built-in security audit command:

```bash
vcc audit
```

This command performs:
1.  **Internal Audit**: Built-in pattern-based checks for common C and Python security issues (requires no external dependencies).
2.  **Bandit** (Optional): A deeper security linter for Python (runs only if `bandit` is installed).
3.  **Cppcheck** (Optional): A more advanced static analysis tool for C/C++ (runs only if `cppcheck` is installed).

It is recommended to run this command regularly during development to catch potential vulnerabilities early.
