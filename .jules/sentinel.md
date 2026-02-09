## 2024-05-15 - Incomplete Input Sanitization in Project Initialization
**Vulnerability:** Path traversal via unvalidated `--template` argument.
**Learning:** While project names were sanitized, the template argument was overlooked.
**Prevention:** Apply consistent sanitization to all user-provided strings.

## 2024-05-16 - Inconsistent Sanitization across Commands
**Vulnerability:** Missing project name validation in `run_tests` and `project_status`.
**Learning:** Security fixes often target obvious entry points but miss secondary ones using the same data.
**Prevention:** Audit all locations where user-controlled data is consumed.
