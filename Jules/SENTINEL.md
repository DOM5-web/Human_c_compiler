# Sentinel Security Log 🛡️

## 2024-05-15 - Initial Input Validation Enhancements

### 🔍 Found
- **Path Traversal Vulnerability**: The `init` command's `--template` argument was not sanitized.
- **Missing Architecture Validation**: The `build` command's `--arch` argument was passed without validation.

### 🔧 Fix
- Implemented strict regex validation for `template` and `arch`.

## 2024-05-16 - Completed Input Validation & Audit Enhancement

### 🔍 Found
- **Missing Project Name Validation**: The `test` and `status` commands were using the project name from `vibe.json` without validation.
- **Path Traversal/Argument Injection Risk**: Potential to link against arbitrary libraries via malicious project name in `vibe.json`.

### 🎯 Impact
- **Path Traversal & Linker Injection**: Unauthorized access and linking of arbitrary files.

### 🔧 Fix
- Applied regex validation (`^[a-zA-Z0-9_-]+$`) to `proj_name` in `run_tests` and `project_status`.
- **Security Enhancement**: Expanded internal C audit to include `system`, `popen`, and `exec` family.

### ✅ Verification
- Verified `vcc test` and `vcc status` reject malicious names.
- Verified `vcc audit` detects unsafe functions.

## 2026-02-10 - Fixed Unexpected Working Directory in Update Command

### 🔍 Found
- **Unexpected Working Directory Execution**: The `update` command was executing `git pull` in the current working directory instead of the compiler's installation directory.

### 🎯 Impact
- **Unintended Repository Modification**: Users running `vcc update` inside their own projects could have their code unexpectedly merged or overwritten if they had a remote named 'origin' and a branch named 'main'.
- **Potential Code Execution**: If a user is tricked into running the command in a malicious directory, it could lead to fetching and merging untrusted code.

### 🔧 Fix
- Modified `vibe/core/compiler.py` to explicitly set the `cwd` (current working directory) for `subprocess.run` calls in the update method to `self.base_dir`.

### ✅ Verification
- Verified by running `vcc update` from a separate project directory with a different 'origin' remote and confirming that git targeted the compiler root instead.

## 2026-05-22 - Enhanced Security Audit Capabilities

### 🔍 Found
- **Limited Security Audit**: The internal audit tool used simple string matching which was prone to false negatives (e.g., missing calls with spaces like `strcpy (`) and false positives (matching `my_strcpy`).
- **Missing Unsafe Patterns**: Several critical unsafe functions (e.g., `printf` format string risks, `os.system`, `pickle.load`) were missing from the audit list.

### 🎯 Impact
- **Undetected Vulnerabilities**: Developers relying on `vcc audit` might miss critical security flaws in their projects or the compiler itself.

### 🔧 Fix
- Upgraded `_internal_c_audit` and `_internal_python_audit` to use regular expressions for robust detection.
- Expanded C audit to include `printf`, `fprintf`, `vsprintf`, `vprintf`, `vibe_print`, `vibe_error`, `tmpnam`, and `tempnam`.
- Expanded Python audit to include `os.system`, `os.popen`, `os.spawn*`, and `pickle.load/loads`.

### ✅ Verification
- Verified with test cases containing various unsafe patterns (e.g., `shell = True`, `printf(buf)`) and confirmed they are now correctly detected.

## 2026-05-23 - Fixed LD_LIBRARY_PATH Vulnerability & Enhanced Audit Tool

### 🔍 Found
- **Shared Library Injection Vulnerability**: In `run_tests`, the `LD_LIBRARY_PATH` construction was susceptible to introducing empty entries (e.g., if the existing `LD_LIBRARY_PATH` had leading/trailing colons or was empty). Empty entries in `LD_LIBRARY_PATH` are interpreted by the dynamic linker as the current directory (.), allowing for DLL hijacking if a malicious library is placed in the project root.
- **Audit Tool False Positives**: The Python audit tool used simple regex that matched substrings (e.g., `execute` matched when searching for `exec`).
- **Audit Tool Gaps**: Missing detection for `mktemp`, `realpath`, `strtok` (C) and `yaml.load` (Python).

### 🎯 Impact
- **Code Execution**: Malicious libraries could be loaded during test execution.
- **Audit Inaccuracy**: False positives reduce the utility of the security tool, while gaps leave vulnerabilities undetected.

### 🔧 Fix
- Sanitized `LD_LIBRARY_PATH` by splitting, filtering out empty strings, and then joining with the build directory.
- Enhanced `_internal_python_audit` regex with word boundaries (`\b`).
- Expanded C audit patterns with `mktemp`, `realpath`, and `strtok`.
- Expanded Python audit patterns with `yaml.load`.

### ✅ Verification
- Verified `LD_LIBRARY_PATH` construction with various input combinations.
- Verified audit tool with dummy files containing both unsafe patterns and safe variants (like `execute`).

## 2026-05-24 - Fixed JSON Injection & Enhanced Audit Robustness

### 🔍 Found
- **JSON Injection Vulnerability**: The `vibe_json_print` function in `vibe_json.h` did not escape double quotes or backslashes in strings. This allowed for JSON structure injection if a string contained these characters.
- **Incomplete JSON Support**: `vibe_json_print` was missing support for `NULL`, `ARRAY`, and `OBJECT` types, leading to data loss in printed output.
- **Audit Tool Gaps**: The C security audit did not scan the `tests/` directory, and the Python audit only reported the first vulnerability found on each line.

### 🎯 Impact
- **Security Bypass**: JSON injection can lead to unauthorized data modification or logic bypass in systems parsing the output.
- **Undetected Test Vulnerabilities**: Security flaws in test code remained unmonitored.

### 🔧 Fix
- Implemented `_vibe_json_print_escaped` helper in `vibe/include/vibe_json.h` to properly escape strings.
- Updated `vibe_json_print` to support all JSON types recursively.
- Enhanced `run_audit` in `vibe/core/compiler.py` to include the `tests/` directory.
- Refactored `_internal_python_audit` to use `re.finditer` for comprehensive line scanning.
- Added `vfork` and `strncat` to C audit patterns.

### ✅ Verification
- Verified `vibe_json_print` with strings containing quotes; output is now correctly escaped.
- Verified `vcc audit` now detects vulnerabilities in `tests/` and multiple issues per line in Python scripts.
