# Security Policy

## Security Audit (v1.4.2)

A comprehensive security audit has been performed on the Vibe C Compiler v1.4.2 core and its custom headers.

### Core Compiler Logic
- **Input Validation**: All user-provided inputs (project names, templates, architectures) are now strictly validated against regex patterns across all commands (`init`, `build`, `run`, `test`, `status`, etc.) to mitigate path traversal and argument injection.
- **JSON Security**: The `vibe.json` configuration file is updated using the standard `json` library, preventing JSON injection vulnerabilities.
- **Subprocess Safety**: All calls to external tools (Clang, ar, etc.) use `subprocess.run` with argument lists and explicit working directories.
- **Safe Self-Updates**: The `vcc update` command explicitly executes within the compiler's installation directory, preventing unintended modifications to the user's workspace.
- **Audit Tooling**: The `vcc audit` command features built-in, dependency-free pattern matching for common vulnerabilities in C and Python. As of v1.4.0, it detects unsafe functions like `gets`, `strcpy`, `system`, `popen`, and the `exec` family.

### Custom Headers
- **Robust File I/O**: `vibe_file.h` now includes checks for `ftell` failures and ensures that `fread` completes successfully, preventing issues with malformed files.
- **Memory Management**: All custom headers now check for `malloc`/`strdup` failures.
- **JSON Parsing**: `vibe_json.h` has improved memory management with a recursive `vibe_json_free` function and added NULL checks.
- **Cryptography**: `vibe_crypt.h` provides a simple XOR cipher which is intended for obfuscation and educational purposes only. It is **not** suitable for securing sensitive data against determined attackers.

## Reporting a Vulnerability

If you find a security vulnerability in Vibe C Compiler, please do not open a public issue. Instead, follow these steps:
1. Contact the maintainers privately (see `CONTRIBUTORS.md` or repository meta).
2. Provide a detailed description of the vulnerability and a proof-of-concept if possible.

## Security Best Practices for Vibe C Projects
- Always check the return values of `vibe_alloc` and other memory-related functions.
- Be cautious when using `vibe_net.h` in production environments; ensure proper input validation on data received from the network.
- Use `vibe_regex.h` with trusted patterns to avoid potential ReDoS (Regular Expression Denial of Service).

---

## Project Navigation

- [Home (README)](README.md)
- [Documentation](DOCS/README.md)
- [Developer Docs](DOCS/dev/README.md)
- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Contributors](CONTRIBUTORS.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
