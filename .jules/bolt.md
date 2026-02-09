# Bolt's Performance Journal

## 2024-05-24 - Parallel and Incremental Build System
**Learning:** Python's `ThreadPoolExecutor` is an excellent tool for parallelizing external process calls (like `clang`). In this codebase, the build process was entirely sequential, making it a major bottleneck as the project grows. Adding a coarse-grained incremental check (any header change triggers recompile) is a safe and effective way to speed up the development cycle without the complexity of a full dependency graph.
**Action:** Always check if core loops involve independent external process calls that can be parallelized. Use `os.path.getmtime` for simple but effective incremental build logic.
