## 2024-05-15 - Incomplete Input Sanitization in Project Initialization
**Vulnerability:** Path traversal via unvalidated `--template` argument.
**Learning:** While project names were sanitized, the template argument was overlooked.
**Prevention:** Apply consistent sanitization to all user-provided strings.

## 2024-05-16 - Inconsistent Sanitization across Commands
**Vulnerability:** Missing project name validation in `run_tests` and `project_status`.
**Learning:** Security fixes often target obvious entry points but miss secondary ones using the same data.
**Prevention:** Audit all locations where user-controlled data is consumed.

## 2026-02-10 - Subprocess Execution in Non-Standard Working Directory
**Vulnerability:** The `update` command performed git operations in the caller's CWD instead of the application's root directory.
**Learning:** Tools that manage themselves (like self-updaters) must explicitly anchor their operations to their own installation path to avoid interfering with user data.
**Prevention:** Always use the `cwd` parameter in `subprocess` calls when the desired operation is context-specific to the application's installation rather than the user's workspace.

## 2026-05-22 - Robustness in Built-in Security Auditing
**Vulnerability:** Brittle string matching in `audit` command led to both false negatives and false positives.
**Learning:** Security tools themselves must be implemented with robust patterns (like regex) to avoid giving a false sense of security. Simple containment checks (`"func(" in line`) are easily bypassed by stylistic variations (e.g., spaces).
**Prevention:** Use regular expressions with boundary markers (`\b`) and handle whitespace variations in all security-scanning logic.

## 2026-05-23 - Insecure LD_LIBRARY_PATH Construction
**Vulnerability:** Prepending paths to `LD_LIBRARY_PATH` without sanitizing the existing value can introduce empty entries (e.g., `path::existing` or `path:`), which the dynamic linker interprets as the current directory (.).
**Learning:** Environmental variable manipulation must be done with awareness of the underlying system's interpretation of special characters like colons.
**Prevention:** Always split environmental variables by their delimiter, filter out empty parts, and then join them back when modifying them.

## 2026-05-24 - Comprehensive Line Auditing and JSON Escaping
**Vulnerability:** Audit tool missed multiple vulnerabilities on a single line; JSON library allowed injection.
**Learning:** Security scanners must use iterative matching (e.g., `finditer`) to be thorough. Library functions that output structured data (like JSON) MUST handle escaping even if they seem "internal" or "simple".
**Prevention:** Always use `finditer` for security scanning patterns. Ensure all data output functions for structured formats implement proper escaping.

## 2026-06-15 - Regex-based Security Audit Bypass
**Vulnerability:** The C security audit regex (`\bfunc\s*\(`) could be bypassed by parenthesizing the function name (e.g., `(printf)("data")`), as the trailing parenthesis prevents the expected `\(` from matching immediately after the function name.
**Learning:** Security scanning patterns that rely on syntactic assumptions (like a function name always being followed by an opening parenthesis) are fragile.
**Prevention:** Use more flexible regex patterns or full AST parsing for security audits. For simple regex checks, focusing on the symbol itself with word boundaries (`\bfunc\b`) is often more robust.

## 2026-06-16 - Syntactic Bypasses in Security Auditing
**Vulnerability:** Security auditors that rely on specific syntactic markers (like a trailing parenthesis for function calls) are easily bypassed by alternative but valid syntax (e.g., `(printf)(buf)`).
**Learning:** In security scanning, it is safer to flag the symbol itself as a whole word (`\bfunc\b`) rather than assuming a specific calling convention. While this may increase false positives (e.g., if a variable shares a name with an unsafe function), it significantly reduces false negatives and forces better naming practices.
**Prevention:** Always use word boundaries and avoid making assumptions about the syntactic context following a sensitive symbol.

## 2026-06-17 - Incomplete Security Audit Coverage
**Vulnerability:** Audit tool skipped internal compiler headers and missed several dangerous function patterns.
**Learning:** A security scanning tool is only as good as its pattern library and its scope; failing to audit internal components or secondary languages (like Python scripts in a C project) can lead to a false sense of security.
**Prevention:** Ensure security tools have a comprehensive pattern list and audit the entire codebase, including bundled libraries and build scripts.

## 2026-06-18 - String Security and Timing Attack Mitigation
**Vulnerability:** Lack of constant-time string comparison in core library.
**Learning:** Standard string comparison functions like `strcmp` are unsuitable for sensitive data as they leak information via execution time.
**Prevention:** Always provide and use constant-time comparison primitives for security-sensitive string operations.

## 2026-06-19 - Uninitialized Memory in Network Structures
**Vulnerability:** Information leakage via uninitialized `sockaddr_in` fields.
**Learning:** Network structures in C often contain padding or reserved fields (like `sin_zero`) that must be explicitly zeroed to prevent leaking stack data to the kernel or the network.
**Prevention:** Always use zero-initialization (e.g., `struct sockaddr_in addr = {0};`) for all network and system structures.
