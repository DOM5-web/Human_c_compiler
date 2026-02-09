## 2024-05-15 - Incomplete Input Sanitization in Project Initialization
**Vulnerability:** Path traversal via unvalidated `--template` argument.
**Learning:** While project names were sanitized, the template argument was overlooked, allowing directory traversal through `os.path.join`.
**Prevention:** Always apply consistent sanitization to all user-provided strings used in filesystem operations or subprocess arguments.

## 2024-05-16 - Inconsistent Sanitization across Commands
**Vulnerability:** Missing project name validation in `run_tests` and `project_status`, despite being present in `build` and `run`.
**Learning:** Security fixes often target the most obvious entry points but may miss secondary ones that use the same data.
**Prevention:** Audit all locations where a particular piece of user-controlled data is consumed, not just the primary ones.
