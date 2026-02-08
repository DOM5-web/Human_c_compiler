## 2024-05-15 - Incomplete Input Sanitization in Project Initialization
**Vulnerability:** Path traversal via unvalidated `--template` argument.
**Learning:** While project names were sanitized, the template argument was overlooked, allowing directory traversal through `os.path.join`.
**Prevention:** Always apply consistent sanitization to all user-provided strings used in filesystem operations or subprocess arguments.
