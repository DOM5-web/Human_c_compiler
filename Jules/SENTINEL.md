# Sentinel Security Log 🛡️

## 2024-05-15 - Input Validation Enhancements

### 🔍 Found
- **Path Traversal Vulnerability**: The `init` command's `--template` argument was not sanitized. This allowed an attacker to use `..` sequences to copy arbitrary directories from the filesystem into a new project directory.
- **Missing Architecture Validation**: The `build` command's `--arch` argument was passed to Clang without validation. While `subprocess.run` was used with a list (preventing shell injection), an unvalidated `arch` string could still lead to argument injection or unexpected Clang behavior.

### 🎯 Impact
- **Path Traversal**: Unauthorized access and copying of directories if an attacker can control the template name.
- **Argument Injection**: Potential for passing unexpected flags to the compiler backend.

### 🔧 Fix
- Implemented strict regex validation for the `template` parameter in `init_project`. Only alphanumeric characters, underscores, and hyphens are allowed.
- Implemented regex validation for the `arch` parameter in `build_project`. Allowed characters include alphanumeric, dots, hyphens, and underscores.

### ✅ Verification
- Verified that `vcc init proj --template ../path` now returns an error.
- Verified that `vcc build --arch "x86_64 -o evil"` now returns an error.
- Confirmed that valid template names and architectures still work as expected.

## 2024-05-16 - Completed Input Validation & Audit Enhancement

### 🔍 Found
- **Missing Project Name Validation**: The `test` and `status` commands were using the project name from `vibe.json` without validation. This was an inconsistency as `build`, `run`, and `init` already had strict validation.
- **Path Traversal/Argument Injection Risk**: In `run_tests`, an unvalidated project name could potentially lead to linking against arbitrary static libraries (path traversal) or passing unexpected flags to the linker.

### 🎯 Impact
- **Path Traversal**: Potential to force the compiler to link with malicious libraries outside the project scope.
- **Inconsistency**: Weakens the security posture of the tool by leaving some entry points unvalidated.

### 🔧 Fix
- Applied the same strict regex validation (`^[a-zA-Z0-9_-]+$`) to the project name in `run_tests` and `project_status` methods.
- **Security Enhancement**: Expanded the internal C audit tool's pattern matching to include `system`, `popen`, and the `exec` family of functions, improving the built-in security analysis capabilities for users.

### ✅ Verification
- Verified that `vcc test` and `vcc status` now reject malicious project names (e.g., `../../../../etc/passwd`).
- Verified that `vcc audit` successfully detects `system()` and `popen()` calls in C source files.
- Confirmed that normal project operations remain unaffected.
