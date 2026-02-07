# Security Policy

## Security Audit (v1.1.0)

A preliminary security audit has been performed on the Vibe C Compiler core and its custom headers.

### Core Compiler Logic
- **Subprocess Safety**: All calls to external tools (Clang, ar, etc.) use `subprocess.run` with argument lists instead of shell strings, preventing shell injection vulnerabilities.
- **Path Sanitization**: The compiler uses `os.path.join` and basic path checks to manage project directories.

### Custom Headers
- **Memory Management**: Headers like `vibe_file.h` and `vibe_json.h` now include checks for `malloc` failures.
- **Buffer Safety**: Utilities that handle external data are designed to be length-aware where possible.
- **Cryptography**: `vibe_crypt.h` provides a simple XOR cipher which is intended for obfuscation and educational purposes only. It is **not** suitable for securing sensitive data against determined attackers.

## Reporting a Vulnerability

If you find a security vulnerability in Vibe C Compiler, please do not open a public issue. Instead, follow these steps:
1. Contact the maintainers privately (see `CONTRIBUTORS.md` or repository meta).
2. Provide a detailed description of the vulnerability and a proof-of-concept if possible.

## Security Best Practices for Vibe C Projects
- Always check the return values of `vibe_alloc` and other memory-related functions.
- Be cautious when using `vibe_net.h` in production environments; ensure proper input validation on data received from the network.
- Use `vibe_regex.h` with trusted patterns to avoid potential ReDoS (Regular Expression Denial of Service).
