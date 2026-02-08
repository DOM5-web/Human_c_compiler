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
