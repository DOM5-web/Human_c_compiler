# Vibe C Compiler (v1.1.0)

The Vibe C Compiler is a project management and compilation suite designed to make C development easier and more intuitive than using GCC directly. It wraps around Clang to provide seamless cross-compilation support and project directory management.

## Features

- **Global Installation**: Use `vcc` command from anywhere after running `install`.
- **Simple CLI**: Easy commands like `init`, `build`, `run`, `install`.
- **Project Management**: Manages your project structure (`src/`, `build/`, `vibe.json`).
- **Interactive Menu**: A simple TUI for those who prefer menus.
- **Cross-Compilation**: Easily target any architecture supported by Clang.
- **Library Support**: Effortlessly create static and shared libraries.
- **20+ Custom Headers**: Built-in headers for advanced features (SIMD, Math, Networking, UI, etc.).

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

4. **Open the Menu**:
   ```bash
   vcc menu
   ```

## Documentation

See [DOCS.md](DOCS.md) for full details on headers and advanced usage.
