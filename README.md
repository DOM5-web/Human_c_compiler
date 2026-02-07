# Vibe C Compiler (v1.0.0)

The Vibe C Compiler is a project management and compilation suite designed to make C development easier and more intuitive than using GCC directly. It wraps around Clang to provide seamless cross-compilation support and project directory management.

## Features

- **Simple CLI**: Easy commands like `init`, `build`, `run`.
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

2. **Build and Run**:
   ```bash
   ../vibe_c_compiler run
   ```

3. **Open the Menu**:
   ```bash
   ../vibe_c_compiler menu
   ```

## Documentation

See [DOCS.md](DOCS.md) for full details on headers and advanced usage.
