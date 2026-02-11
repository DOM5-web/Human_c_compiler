# Vibe C Compiler (v1.4.3)

The Vibe C Compiler is a project management and compilation suite designed to make C development easier and more intuitive than using GCC directly. It wraps around Clang to provide seamless cross-compilation support and project directory management.

## Features

- **Global Installation**: Use `vcc` command from anywhere after running `install`.
- **Simple CLI**: Easy commands like `init`, `build`, `run`, `test`, `install`, `uninstall`, `audit`, and `update`.
- **Fast Incremental Builds & Tests**: Optimized for speed with parallel execution and efficient NO-OP checks (v1.4.2/v1.4.3).
- **Parallel and Incremental Test Execution**: High-speed testing that only recompiles changed tests and runs them concurrently (v1.4.2).
- **Project Management**: Manages your project structure (`src/`, `build/`, `vibe.json`).
- **Interactive Menu**: A simple TUI for those who prefer menus.
- **Cross-Compilation**: Easily target any architecture supported by Clang.
- **Library Support**: Effortlessly create static and shared libraries.
- **25 Custom Headers**: Built-in headers for advanced features (SIMD, Math, Networking, UI, etc.).

## Quick Start

1. **Initialize a project**:
   ```bash
   ./vibe_c_compiler init my_cool_project
   cd my_cool_project
   ```

2. **Install Globally**:
   ```bash
   ./vibe_c_compiler install
   ```
   Now you can use `vcc` instead of `./vibe_c_compiler`.

3. **Build and Run**:
   ```bash
   vcc run
   ```

4. **Uninstall Globally**:
   ```bash
   vcc uninstall
   ```

5. **Open the Menu**:
   ```bash
   vcc menu
   ```

6. **Run Security Audit**:
   ```bash
   vcc audit
   ```

7. **Update Compiler**:
   ```bash
   vcc update
   ```

## Documentation

See [Documentation](DOCS/README.md) for full details on headers and advanced usage.

---

## Project Navigation

- [Home (README)](README.md)
- [Documentation](DOCS/README.md)
- [Developer Docs](DOCS/dev/README.md)
- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Contributors](CONTRIBUTORS.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
