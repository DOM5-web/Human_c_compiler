# Bolt's Performance Journal

## 2024-05-24 - Parallel and Incremental Build System
**Learning:** Python's `ThreadPoolExecutor` is an excellent tool for parallelizing external process calls (like `clang`). In this codebase, the build process was entirely sequential, making it a major bottleneck as the project grows. Adding a coarse-grained incremental check (any header change triggers recompile) is a safe and effective way to speed up the development cycle without the complexity of a full dependency graph.
**Action:** Always check if core loops involve independent external process calls that can be parallelized. Use `os.path.getmtime` for simple but effective incremental build logic.

## 2024-05-24 - Efficient Incremental Scanning
**Learning:** Python's `ThreadPoolExecutor` and `subprocess` calls have significant overhead when called hundreds of times for "no-op" tasks. Moving incremental checks (mtime comparisons) out of the worker function and into a pre-filtering step in the main thread drastically reduces no-op build time (e.g., from 0.22s to 0.08s for 50 files). Combining source file collection and header mtime scanning into a single `os.walk` pass further minimizes expensive I/O operations.
**Action:** In build systems or batch processors, always pre-filter tasks in the main thread before engaging parallel workers. Consolidate file system traversals to minimize 'stat' calls.
