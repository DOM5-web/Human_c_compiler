# Vibe C Compiler Development Log

## Overview
This log tracks major changes and improvements made to the Vibe C Compiler suite.

## Change-log

### [1.4.0] - 2024-05-16
#### Added
- **Enhanced Security Audit**: Expanded the internal C audit tool to detect `system`, `popen`, and `exec` family functions.
- **Improved Input Validation**: Applied strict regex validation to project names in `test` and `status` commands to prevent path traversal and argument injection.

#### Changed
- **Version Bump**: Updated all components to version 1.4.0.

### [1.3.0] - 2024-02-08
#### Added
- **Parallel and Incremental Builds**: (Bolt) Implemented `ThreadPoolExecutor` for parallel compilation and added incremental build checks based on file modification times.
- **Test Command**: Added `test` command to automatically find, compile, and run C tests in the `tests/` directory.
- **Argument Parsing Header**: Added `vibe_arg.h` for simple CLI argument handling.
- **Test Enhancements**: Improved `vibe_test.h` with more robust assertion macros (`VIBE_ASSERT_EQ`, `VIBE_ASSERT_STR_EQ`) and a test summary reporter.

#### Changed
- **Menu Improvements**: Integrated `test`, `audit`, and `update` commands into the interactive TUI menu.
- **Version Bump**: Updated all components to version 1.3.0.

### [1.2.0] - 2024-02-07
#### Added
- **Uninstall Command**: Added `uninstall` command to remove the global `vcc` symlink.
- **Templates Command**: Added `templates` command to list available project templates.
- **Headers Command**: Added `headers` command to list all built-in Vibe C headers.
- **Status Command**: Added `status` command to show information about the current project (name, version, type, source files, build artifacts).
- **Minimal Template**: Added a new `minimal` template for lightweight project initialization.
- **Menu Improvements**: Integrated `install`, `uninstall`, `templates`, `headers`, and `status` into the interactive TUI menu.

#### Changed
- **Project Initialization**: The `init` command now supports a `--template` argument (defaults to `basic`).
- **Build Output**: Improved build output to show real-time compilation progress.
- **Version Management**: Centralized version display logic in the `VibeCompiler` class.
- **Menu Header**: The interactive menu now displays the current compiler version.
- **Security Audit Command**: Added `audit` command with built-in checks for C and Python vulnerabilities, plus optional `bandit` and `cppcheck` integration.
- **Update Command**: Added `update` command to perform a `git pull` from the main repository.

#### Fixed
- **Input Sanitization**: Project names are now validated with a strict regex to prevent directory traversal and other injection attacks.
- **JSON Security**: Switched from string replacement to using the `json` library for updating `vibe.json`, preventing malformed JSON or injection.
- **Header Safety**: Improved memory allocation checks and file I/O robustness in `vibe_file.h` and `vibe_json.h`.

## Technical Details

### Uninstall Logic
The uninstall command specifically targets `~/.local/bin/vcc` and removes the symlink if it exists, providing a clean way to remove the global shortcut.

### Template System
Introduced a more flexible template system by allowing the `init` command to pull from different subdirectories in `vibe/templates/`.

### Project Status
The `status` command parses `vibe.json` and scans the `src/` and `build/` directories to provide a quick overview of the project's health and size.
