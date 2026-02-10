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
