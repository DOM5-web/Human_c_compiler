# Vibe C Compiler Documentation

## CLI Commands

- `init <name>`: Creates a new Vibe C project.
- `build`: Compiles the project.
  - `--arch <target>`: Specify target architecture (e.g., `aarch64-linux-gnu`).
  - `--lib <type>`: Build as `static` or `shared` library.
- `run`: Builds and executes the project.
- `clean`: Removes the `build/` directory.
- `menu`: Opens the interactive menu.
- `version`: Shows the current version.

## Custom Headers

Vibe C comes with 21 custom headers located in `vibe/include/`. You can include them in your source code using `#include <vibe_xxx.h>`.

### Core Headers
- `vibe_std.h`: Core types and version info.
- `vibe_io.h`: Simple printing macros.
- `vibe_math.h`: Math constants and min/max macros.
- `vibe_string.h`: String comparison helpers.
- `vibe_sys.h`: OS detection macros.

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
- `vibe_json.h`: JSON parsing placeholder.
- `vibe_thread.h`: Simple pthread wrapper.
- `vibe_net.h`: Networking headers.

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
