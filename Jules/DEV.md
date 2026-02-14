# Vibe C Compiler Development Log

## Overview
This log tracks major changes and improvements made to the Vibe C Compiler suite.

## Change-log

### [1.4.5] - 2026-06-15
#### Added
- **Security Hardening**: (Sentinel 🛡️) Implemented comprehensive security hardening flags (-fstack-protector-strong, PIE, RELRO, etc.) for all compilation and linking processes.
- **Upgrade Alias**: Added `upgrade` as an alias for the `update` command and updated the `install` message to improve discoverability of self-update features.

### [1.4.4] - 2026-02-13
#### Added
- **Command Anchoring**: (Sentinel 🛡️) The `update` command now explicitly sets `cwd=self.base_dir` to ensure updates target the compiler repository instead of the user's workspace.
- **Environment Sanitization**: (Sentinel 🛡️) Implemented `LD_LIBRARY_PATH` sanitization in `run_tests` to prevent shared library injection via empty path entries.
- **Expanded Security Audit**: (Sentinel 🛡️) Added detection for `mktemp`, `realpath`, `strtok`, `vfork`, and `strncat` in C, and `yaml.load` in Python.
- **Comprehensive Scanning**: (Sentinel 🛡️) The `audit` command now scans the `tests/` directory and identifies multiple vulnerabilities per line in Python.
- **Secure JSON Printing**: (Sentinel 🛡️) Added `_vibe_json_print_escaped` to `vibe_json.h` to properly handle double quotes and backslashes, preventing JSON injection. Added support for all JSON types (NULL, ARRAY, OBJECT) in `vibe_json_print`.
- **Cached Header Scanning**: (Bolt ⚡) Added caching for global Vibe headers modification time to speed up the build process.
- **Test Pre-filtering**: (Bolt ⚡) Implemented pre-filtering for tests to avoid thread pool overhead when tests are already up-to-date.

#### Changed
- **Optimized File Scanning**: (Bolt ⚡) Replaced `os.walk` with `os.scandir` in build, test, audit, and status commands for improved I/O performance.
- **Improved Build Logic**: (Bolt ⚡) The `build` command now skips redundant linking checks if compilation occurred during the same run.
- **Version Bump**: Updated all components to version 1.4.4.

### [1.4.3] - 2025-02-11
#### Changed
- **Optimized Security Audit**: (Bolt ⚡) Re-engineered the security audit logic to use combined regular expressions with named capture groups. This reduces search complexity per line from $O(M)$ to $O(1)$ relative to the number of patterns, resulting in a ~25-30x speedup for the audit command.

### [1.4.2] - 2024-05-24
#### Added
- **Parallel and Incremental Test Execution**: (Bolt ⚡) Implemented `ThreadPoolExecutor` for parallel test execution and added incremental compilation checks for tests. This significantly speeds up the test cycle by only recompiling changed tests and running them concurrently.

#### Changed
- **Centralized Header Scanning**: Refactored header scanning into a reusable `_get_header_mtime` method to improve maintainability and consistency between build and test commands.

### [1.4.1] - 2024-05-24
#### Changed
- **Optimized Incremental Builds**: (Bolt ⚡) Re-engineered the build system to perform incremental checks in the main thread before parallelization. This reduces NO-OP build times by ~65% by avoiding ThreadPoolExecutor overhead for up-to-date files.
- **Efficient File Scanning**: Combined source file collection and header mtime scanning into a single-pass `os.walk` traversal.
- **Simplified Compiler Driver**: Refactored `_compile_src` to remove redundant stat calls during the compilation phase.

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

