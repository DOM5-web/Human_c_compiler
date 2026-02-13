# Security Log - Vibe C Compiler

This log tracks all security-related changes and audits performed on the Vibe C Compiler.

## [1.4.4] - 2026-02-13

### Security Improvements & Fixes
- **Safe Self-Updates**: (Sentinel 🛡️) Fixed a vulnerability in the `update` command where git operations were performed in the caller's CWD. The command is now explicitly anchored to the compiler's installation directory (`self.base_dir`).
- **Environment Safety**: (Sentinel 🛡️) Sanitized `LD_LIBRARY_PATH` construction in `run_tests` to prevent shared library injection via empty entries (interpret as current directory `.`).
- **Enhanced Audit Capabilities**: (Sentinel 🛡️) Upgraded `_internal_c_audit` and `_internal_python_audit` to use regular expressions for more robust detection.
- **Audit Tool Robustness**: (Sentinel 🛡️) Enhanced Python audit tool with word boundaries (`\b`) to prevent false positives and implemented `re.finditer` to catch multiple issues per line.
- **Audit Tool Gaps**: (Sentinel 🛡️) Expanded C audit patterns with `mktemp`, `realpath`, `strtok`, `vfork`, `strncat`, and format string risks (`printf`, `fprintf`, etc.).
- **Audit Tool Gaps**: (Sentinel 🛡️) Expanded Python audit patterns with `yaml.load`, `os.system`, `os.popen`, `os.spawn*`, and `pickle.load/loads`.
- **Secure JSON Printing**: (Sentinel 🛡️) Implemented proper escaping for double quotes and backslashes in `vibe_json.h` and added support for all JSON types.

### Verification
- Verified `LD_LIBRARY_PATH` construction logic.
- Verified audit tool with safe and unsafe test cases.
- Verified `vibe_json_print` with special character strings.

## [1.4.0] - 2024-05-16

### Security Improvements & Fixes
- **Comprehensive Input Validation**: Applied strict regex validation to project names in `test` and `status` commands to prevent path traversal and argument injection via `vibe.json`.
- **Audit Enhancement**: Expanded internal C audit to include `system`, `popen`, and `exec` family functions.
- **Project Sanitization**: Implemented strict regex validation for `--template` and `--arch` arguments in `init` and `build` commands.

## [1.2.0] - 2024-02-07

### Security Audit Findings
- **Path Traversal**: Identified potential path traversal in `init_project` via the `name` argument.
- **JSON Injection**: Found that `vibe.json` was updated using string replacement, which could lead to malformed JSON or injection if a project name contained double quotes.
- **Subprocess Safety**: Verified that `subprocess.run` is used with argument lists, preventing shell injection.
- **C Header Safety**: Found several custom C headers that did not check for `malloc` failures or had incomplete memory freeing logic.

### Improvements & Fixes
- **Input Validation**: Implemented strict regex validation for project names (`^[a-zA-Z0-9_-]+$`).
- **Secure JSON Handling**: Replaced string-based updates of `vibe.json` with the standard `json` library.
- **Robust Subprocesses**: Refined subprocess calls to use absolute paths for executables where appropriate.
- **Memory Safety**: Updated `vibe_file.h` and `vibe_json.h` to include NULL checks for memory allocations and proper error handling for file operations.
- **Recursive Free**: Fully implemented recursive `vibe_json_free` for all JSON types including objects and arrays.
- **Audit Tooling**: Integrated a new `vcc audit` command with built-in, dependency-free pattern matching for common C and Python vulnerabilities. It optionally integrates with `bandit` and `cppcheck`.

---

## Project Navigation

- [Home (README)](../README.md)
- [Documentation](../DOCS/README.md)
- [Developer Docs](../DOCS/dev/README.md)
- [Security Policy](../SECURITY.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Contributors](../CONTRIBUTORS.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
