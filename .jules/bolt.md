# Bolt's Performance Journal

## 2024-05-24 - Parallel and Incremental Build System
**Learning:** Python's `ThreadPoolExecutor` is an excellent tool for parallelizing external process calls (like `clang`). In this codebase, the build process was entirely sequential, making it a major bottleneck as the project grows. Adding a coarse-grained incremental check (any header change triggers recompile) is a safe and effective way to speed up the development cycle without the complexity of a full dependency graph.
**Action:** Always check if core loops involve independent external process calls that can be parallelized. Use `os.path.getmtime` for simple but effective incremental build logic.

## 2024-05-24 - Efficient Incremental Scanning
**Learning:** Python's `ThreadPoolExecutor` and `subprocess` calls have significant overhead when called hundreds of times for "no-op" tasks. Moving incremental checks (mtime comparisons) out of the worker function and into a pre-filtering step in the main thread drastically reduces no-op build time (e.g., from 0.22s to 0.08s for 50 files). Combining source file collection and header mtime scanning into a single `os.walk` pass further minimizes expensive I/O operations.
**Action:** In build systems or batch processors, always pre-filter tasks in the main thread before engaging parallel workers. Consolidate file system traversals to minimize 'stat' calls.

## 2024-05-24 - Parallel Test Execution
**Learning:** Parallelizing only the compilation step is not enough if the tasks themselves (e.g., running tests) are also time-consuming. Parallelizing execution while capturing output to prevent interleaving provides a much better developer experience. Incremental builds should extend to tests to avoid redundant compilation of unchanged test files.
**Action:** Always look for opportunities to parallelize independent execution tasks, not just build tasks. Ensure incremental logic is applied consistently across all parts of the toolchain.

## 2025-02-11 - Combined Regex for Multi-Pattern Matching
**Learning:** Performing multiple independent `re.search` calls in a loop over every line of every file is a significant bottleneck ($O(Lines \times Patterns)$). Combining all patterns into a single regex with alternation and using named groups for identification reduces the complexity to $O(Lines)$ and leverages the regex engine's internal optimizations (e.g., Aho-Corasick like matching). This yielded a ~25-30x speedup for the matching logic in this codebase.
**Action:** In scanners or log parsers, always combine multiple patterns into a single pre-compiled regex instead of looping through them.

## 2025-05-14 - os.scandir for Efficient Metadata Access
**Learning:** Using `os.scandir` instead of `os.walk` or manual `os.path.getmtime` calls significantly reduces system calls, especially when traversing large directory trees for file metadata. `DirEntry` objects often cache stat information retrieved during directory listing, making `entry.stat().st_mtime` much faster than `os.path.getmtime(entry.path)`.
**Action:** Use `os.scandir` for any recursive directory traversal that requires file metadata (mtime, size, etc.) to leverage cached stat info.

## 2026-02-13 - Bulk Metadata Collection with os.scandir
**Learning:** In build systems with many files, performing individual 'stat' calls for every source and object file to check for updates is a significant bottleneck. Using a single recursive 'os.scandir' pass to collect all metadata into a dictionary reduces system calls from O(N) to O(D) (number of directories). This optimization is especially effective for 'no-op' builds where most files are already up-to-date.
**Action:** When performing incremental checks across a large set of files, use a bulk directory scan to pre-collect metadata instead of checking files individually in a loop.
