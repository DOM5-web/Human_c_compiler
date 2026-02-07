# Security Log - Vibe C Compiler

This log tracks all security-related changes and audits performed on the Vibe C Compiler.

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

### Tools Used
- **Bandit**: Scanned Python core logic.
- **Cppcheck**: Scanned custom C headers.
- **Manual Review**: Performed a line-by-line audit of critical paths.
