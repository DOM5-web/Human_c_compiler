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
