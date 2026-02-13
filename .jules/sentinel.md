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
