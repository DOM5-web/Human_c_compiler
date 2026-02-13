import os
import subprocess
import shutil
import re
import json
from concurrent.futures import ThreadPoolExecutor # BOLT: Parallel compilation

class VibeCompiler:
    def __init__(self):
        # __file__ is vibe/core/compiler.py
        # dirname(dirname(dirname(__file__))) is the root directory
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.vibe_dir = os.path.join(self.base_dir, "vibe")
        self.include_dir = os.path.join(self.vibe_dir, "include")
        self.template_dir = os.path.join(self.vibe_dir, "templates")
        self.version_file = os.path.join(self.base_dir, "VERSION")
        self._vibe_include_mtime_cache = None # BOLT: Cache for compiler headers

    def _get_header_mtime(self, scan_src=True):
        """BOLT: Get the latest modification time among all headers using efficient scanning."""
        # Check cache for global vibe headers if they haven't been scanned yet
        if self._vibe_include_mtime_cache is None:
            self._vibe_include_mtime_cache = self._scan_for_mtime(self.include_dir, (".h",))

        header_mtime = self._vibe_include_mtime_cache

        if scan_src and os.path.exists("src"):
            header_mtime = max(header_mtime, self._scan_for_mtime("src", (".h",)))

        return header_mtime

    def _scan_for_mtime(self, path, extensions):
        """BOLT: Recursive helper to scan for latest mtime using os.scandir for performance."""
        max_mtime = 0
        try:
            if not os.path.exists(path):
                return 0
            for entry in os.scandir(path):
                if entry.is_file():
                    if entry.name.endswith(extensions):
                        max_mtime = max(max_mtime, entry.stat().st_mtime)
                elif entry.is_dir():
                    max_mtime = max(max_mtime, self._scan_for_mtime(entry.path, extensions))
        except OSError:
            pass
        return max_mtime

    def _compile_src(self, src, arch, proj_type, obj_root):
        """BOLT: Helper to compile a single source file to an object file."""
        rel_path = os.path.relpath(src, "src")
        obj = os.path.join(obj_root, os.path.splitext(rel_path)[0] + ".o")
        os.makedirs(os.path.dirname(obj), exist_ok=True)

        print(f"Compiling {src}...")
        cmd = ["clang", "-I" + self.include_dir, "-c", src, "-o", obj]
        if arch:
            cmd += ["-target", arch]
        if proj_type == "shared":
            cmd += ["-fPIC"]

        res = subprocess.run(cmd)
        return obj if res.returncode == 0 else None

    def show_version(self):
        try:
            with open(self.version_file, "r") as f:
                version = f.read().strip()
                print(f"Vibe C Compiler v{version}")
                return version
        except Exception as e:
            print(f"Error reading version: {e}")
            return "unknown"

    def init_project(self, name, template="basic"):
        # Improved sanitization: only allow alphanumeric, underscores, and hyphens
        if not re.match(r"^[a-zA-Z0-9_-]+$", name):
            print("Error: Invalid project name. Use only alphanumeric characters, underscores, and hyphens.")
            return False

        # Sanitize template name to prevent path traversal
        if not re.match(r"^[a-zA-Z0-9_-]+$", template):
            print(f"Error: Invalid template name '{template}'. Use only alphanumeric characters, underscores, and hyphens.")
            return False

        if os.path.exists(name):
            print(f"Error: Directory '{name}' already exists.")
            return False

        template_path = os.path.join(self.template_dir, template)
        if not os.path.exists(template_path):
            print(f"Error: Template '{template}' not found. Using 'basic' instead.")
            template_path = os.path.join(self.template_dir, "basic")

        shutil.copytree(template_path, name)

        # Update vibe.json with project name using proper JSON handling
        config_path = os.path.join(name, "vibe.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)

            # If the template used {{name}}, it might not be valid JSON if it's not quoted
            # But usually templates should have valid JSON with a placeholder.
            # If it's literally {{name}} without quotes, json.load will fail.
            # Let's check the templates.
        except json.JSONDecodeError:
            # Fallback to string replacement if JSON is invalid due to placeholders
            with open(config_path, "r") as f:
                content = f.read()
            content = content.replace("{{name}}", name)
            # Try to validate after replacement
            try:
                config = json.loads(content)
            except json.JSONDecodeError:
                print("Error: Failed to generate valid vibe.json")
                return False

        config["name"] = name
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        os.makedirs(os.path.join(name, "build"), exist_ok=True)

        print(f"Project '{name}' initialized successfully.")
        return True

    def build_project(self, arch=None, lib_type=None):
        if not os.path.exists("vibe.json"):
            print("Error: Not a vibe project (vibe.json not found).")
            return False

        with open("vibe.json", "r") as f:
            config = json.load(f)

        proj_name = config.get("name", "app")
        # Sanitize proj_name from config to prevent path traversal/command injection
        if not re.match(r"^[a-zA-Z0-9_-]+$", proj_name):
            print("Error: Invalid project name in vibe.json.")
            return False

        proj_type = config.get("type", "executable")

        # Override project type if lib_type is specified
        if lib_type and lib_type != "none":
            proj_type = lib_type

        # BOLT: Centralized object directory
        obj_root = os.path.join("build", "obj")
        os.makedirs(obj_root, exist_ok=True)

        # BOLT: Efficient single-pass scanning of src/ for .c files and headers using os.scandir
        src_files = []
        header_mtime = self._get_header_mtime(scan_src=False)

        def _collect_src(path):
            nonlocal header_mtime
            try:
                for entry in os.scandir(path):
                    if entry.is_file():
                        if entry.name.endswith(".c"):
                            src_files.append((entry.path, entry.stat().st_mtime))
                        elif entry.name.endswith(".h"):
                            header_mtime = max(header_mtime, entry.stat().st_mtime)
                    elif entry.is_dir():
                        _collect_src(entry.path)
            except OSError as e:
                print(f"Warning: Could not scan source directory '{path}': {e}")

        if os.path.exists("src"):
            _collect_src("src")

        if not src_files:
            print("Error: No source files found in src/")
            return False

        if proj_type == "static":
            output_name = f"build/lib{proj_name}.a"
        elif proj_type == "shared":
            output_name = f"build/lib{proj_name}.so"
        else:
            output_name = f"build/{proj_name}"

        if arch and not re.match(r"^[a-zA-Z0-9._-]+$", arch):
            print(f"Error: Invalid architecture name '{arch}'.")
            return False

        # BOLT: Pre-filter files that actually need compilation
        to_compile = []
        obj_files = []
        for src_path, src_mtime in src_files:
            rel_path = os.path.relpath(src_path, "src")
            obj_path = os.path.join(obj_root, os.path.splitext(rel_path)[0] + ".o")
            obj_files.append(obj_path)

            needs_compile = True
            if os.path.exists(obj_path):
                obj_mtime = os.path.getmtime(obj_path)
                if obj_mtime > src_mtime and obj_mtime > header_mtime:
                    needs_compile = False

            if needs_compile:
                to_compile.append(src_path)

        # BOLT: Target-level incremental check
        link_needed = not os.path.exists(output_name)

        # BOLT: Only use ThreadPoolExecutor if compilation is needed
        if to_compile:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda s: self._compile_src(s, arch, proj_type, obj_root), to_compile))
                if None in results:
                    print("Build failed: Some files failed to compile.")
                    return False
            # BOLT: If we compiled anything, we definitely need to link
            link_needed = True

        if not obj_files:
            print("Build failed: No object files to link.")
            return False

        # BOLT: If no compilation happened, check if any object file is newer than target
        if not link_needed:
            target_mtime = os.path.getmtime(output_name)
            if any(os.path.getmtime(obj) > target_mtime for obj in obj_files):
                link_needed = True

        if link_needed:
            if proj_type == "static":
                print(f"Creating static library {output_name}...")
                res = subprocess.run(["ar", "rcs", output_name] + obj_files)
            else:
                print(f"Linking project...")
                link_cmd = ["clang"]
                if arch: link_cmd += ["-target", arch]
                if proj_type == "shared": link_cmd += ["-shared", "-fPIC"]
                link_cmd += obj_files + ["-o", output_name]
                res = subprocess.run(link_cmd)

            if res.returncode != 0:
                print("Build failed.")
                return False

        print(f"Build successful: {output_name}")
        return True
    def run_project(self):
        if not os.path.exists("vibe.json"):
            print("Error: vibe.json not found.")
            return

        with open("vibe.json", "r") as f:
            config = json.load(f)

        proj_name = config.get("name", "app")
        # Sanitize proj_name from config
        if not re.match(r"^[a-zA-Z0-9_-]+$", proj_name):
            print("Error: Invalid project name in vibe.json.")
            return

        output_name = os.path.join("build", proj_name)

        if not os.path.exists(output_name):
            print(f"Error: Executable {output_name} not found. Build it first.")
            return

        print(f"Running {output_name}...")
        # Use absolute path for safety and to avoid confusion
        abs_output_path = os.path.abspath(output_name)
        subprocess.run([abs_output_path])

    def clean_project(self):
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("Cleaned build directory.")
        else:
            print("Nothing to clean.")

    def run_tests(self):
        if not os.path.exists("tests"):
            print("No tests/ directory found.")
            return

        # BOLT: Efficiently collect test files using os.scandir
        test_files = []
        def _collect_tests(path):
            try:
                for entry in os.scandir(path):
                    if entry.is_file() and entry.name.endswith(".c"):
                        test_files.append(entry.path)
                    elif entry.is_dir():
                        _collect_tests(entry.path)
            except OSError as e:
                print(f"Warning: Could not scan test directory '{path}': {e}")
        _collect_tests("tests")

        if not test_files:
            print("No test files (.c) found in tests/.")
            return

        if not os.path.exists("build/tests"):
            os.makedirs("build/tests", exist_ok=True)

        # Check if we should link with the project library
        link_args = []
        lib_mtime = 0
        if os.path.exists("vibe.json"):
            try:
                with open("vibe.json", "r") as f:
                    config = json.load(f)
                proj_name = config.get("name", "app")
                # Sanitize proj_name from config to prevent path traversal/argument injection
                if not re.match(r"^[a-zA-Z0-9_-]+$", proj_name):
                    print("Error: Invalid project name in vibe.json.")
                    return

                proj_type = config.get("type", "executable")

                if proj_type == "static":
                    lib_path = f"build/lib{proj_name}.a"
                elif proj_type == "shared":
                    lib_path = f"build/lib{proj_name}.so"
                else:
                    lib_path = None

                if lib_path and os.path.exists(lib_path):
                    lib_mtime = os.path.getmtime(lib_path)
                    if proj_type == "static":
                        link_args = [lib_path]
                    else:
                        link_args = ["-Lbuild", f"-l{proj_name}"]
            except Exception:
                pass

        # BOLT: Calculate header_mtime for tests to enable incremental compilation
        header_mtime = self._get_header_mtime(scan_src=True)

        def _compile_test(test_file):
            test_name = os.path.splitext(os.path.basename(test_file))[0]
            output_bin = os.path.join("build/tests", test_name)

            print(f"Compiling {test_file}...")
            cmd = ["clang", "-I" + self.include_dir, "-Isrc", test_file] + link_args + ["-o", output_bin]
            res = subprocess.run(cmd, capture_output=True)
            return {
                "file": test_file,
                "name": test_name,
                "bin": output_bin,
                "success": res.returncode == 0,
                "error": res.stderr.decode() if res.returncode != 0 else ""
            }

        # BOLT: Pre-filter tests that actually need compilation to avoid thread overhead
        to_compile = []
        compilation_results = []

        for test_file in test_files:
            test_name = os.path.splitext(os.path.basename(test_file))[0]
            output_bin = os.path.join("build/tests", test_name)

            needs_compile = True
            if os.path.exists(output_bin):
                bin_mtime = os.path.getmtime(output_bin)
                if bin_mtime > os.path.getmtime(test_file) and \
                   bin_mtime > header_mtime and \
                   bin_mtime > lib_mtime:
                    needs_compile = False

            if needs_compile:
                to_compile.append(test_file)
            else:
                compilation_results.append({
                    "file": test_file,
                    "name": test_name,
                    "bin": output_bin,
                    "success": True,
                    "error": ""
                })

        if to_compile:
            print(f"Compiling {len(to_compile)} tests in parallel...")
            with ThreadPoolExecutor() as executor:
                compilation_results.extend(list(executor.map(_compile_test, to_compile)))

        # BOLT: Run tests in parallel
        print(f"Running {len(compilation_results)} tests in parallel...")

        def _run_single_test(result):
            if not result["success"]:
                return False, f"\n[!] Failed to compile {result['file']}:\n{result['error']}"

            env = os.environ.copy()
            ld_path = os.path.abspath("build")

            # Sentinel: Sanitize LD_LIBRARY_PATH to avoid empty entries (which mean '.')
            # Prepend build directory and filter out any empty components from existing path
            ld_parts = [ld_path]
            existing_ld_path = env.get("LD_LIBRARY_PATH")
            if existing_ld_path:
                ld_parts.extend([p for p in existing_ld_path.split(":") if p])

            env["LD_LIBRARY_PATH"] = ":".join(ld_parts)

            res = subprocess.run([os.path.abspath(result["bin"])], env=env, capture_output=True, text=True)
            if res.returncode == 0:
                return True, f"  [+] {result['name']} passed."
            else:
                return False, f"  [-] {result['name']} failed.\n{res.stdout}\n{res.stderr}"

        with ThreadPoolExecutor() as executor:
            execution_results = list(executor.map(_run_single_test, compilation_results))

        passed = sum(1 for success, _ in execution_results if success)
        failed = len(execution_results) - passed
        for _, output in execution_results:
            print(output)

        print("\n=== Test Results ===")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Total:  {len(test_files)}")

    def install_globally(self):
        source_script = os.path.join(self.base_dir, "vibe_c_compiler")
        target_dir = os.path.expanduser("~/.local/bin")
        target_link = os.path.join(target_dir, "vcc")

        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except Exception as e:
                print(f"Error creating {target_dir}: {e}")
                return

        if os.path.exists(target_link):
            os.remove(target_link)

        try:
            os.symlink(source_script, target_link)
            print(f"Successfully installed 'vcc' to {target_link}")
            print(f"Make sure {target_dir} is in your PATH.")
        except Exception as e:
            print(f"Error creating symlink: {e}")

    def uninstall_globally(self):
        target_dir = os.path.expanduser("~/.local/bin")
        target_link = os.path.join(target_dir, "vcc")

        if os.path.exists(target_link):
            try:
                os.remove(target_link)
                print(f"Successfully uninstalled 'vcc' from {target_link}")
            except Exception as e:
                print(f"Error removing symlink: {e}")
        else:
            print(f"'vcc' is not installed in {target_dir}")

    def list_headers(self):
        if not os.path.exists(self.include_dir):
            print("Error: Include directory not found.")
            return

        headers = [f for f in os.listdir(self.include_dir) if f.endswith(".h")]
        headers.sort()

        if not headers:
            print("No Vibe headers found.")
        else:
            print("\nAvailable Vibe Headers:")
            for header in headers:
                print(f"  - {header}")

    def list_templates(self):
        if not os.path.exists(self.template_dir):
            print("Error: Template directory not found.")
            return

        templates = [d for d in os.listdir(self.template_dir) if os.path.isdir(os.path.join(self.template_dir, d))]
        templates.sort()

        if not templates:
            print("No Vibe templates found.")
        else:
            print("\nAvailable Vibe Templates:")
            for template in templates:
                print(f"  - {template}")

    def project_status(self):
        if not os.path.exists("vibe.json"):
            print("Error: Not in a Vibe project directory (vibe.json not found).")
            return

        try:
            with open("vibe.json", "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error reading vibe.json: {e}")
            return

        proj_name = config.get("name", "app")
        # Sanitize proj_name from config
        if not re.match(r"^[a-zA-Z0-9_-]+$", proj_name):
            print("Error: Invalid project name in vibe.json.")
            return

        print("\n=== Vibe Project Status ===")
        print(f"Name:    {proj_name}")
        print(f"Version: {config.get('version', 'N/A')}")
        print(f"Type:    {config.get('type', 'executable')}")

        src_count = 0
        if os.path.exists("src"):
            for root, dirs, files in os.walk("src"):
                for file in files:
                    if file.endswith(".c"):
                        src_count += 1
        print(f"Sources: {src_count} .c files")

        if os.path.exists("build"):
            build_files = [f for f in os.listdir("build") if os.path.isfile(os.path.join("build", f))]
            print(f"Build:   {len(build_files)} artifacts in build/")
        else:
            print("Build:   No build directory found.")

    def _internal_c_audit(self, src_dir):
        print(f"\n--- Internal C Audit: {src_dir} ---")
        # Sentinel: Expanded list of unsafe functions and use of regex for better detection
        unsafe_funcs = {
            "gets": "Extremely unsafe, use fgets instead.",
            "strcpy": "Unsafe, use strncpy or strlcpy instead.",
            "strcat": "Unsafe, use strncat or strlcat instead.",
            "sprintf": "Unsafe, use snprintf instead.",
            "vsprintf": "Unsafe, use vsnprintf instead.",
            "scanf": "Can be unsafe, use with field widths or use fgets/sscanf.",
            "system": "Unsafe, can lead to command injection.",
            "popen": "Unsafe, can lead to command injection.",
            "execl": "Potential for command injection if arguments are not controlled.",
            "execv": "Potential for command injection if arguments are not controlled.",
            "execle": "Potential for command injection if arguments are not controlled.",
            "execve": "Potential for command injection if arguments are not controlled.",
            "execlp": "Potential for command injection if arguments are not controlled.",
            "execvp": "Potential for command injection if arguments are not controlled.",
            "printf": "Potential format string vulnerability if first argument is not a literal.",
            "fprintf": "Potential format string vulnerability if first argument is not a literal.",
            "vprintf": "Potential format string vulnerability if first argument is not a literal.",
            "vibe_print": "Potential format string vulnerability if first argument is not a literal.",
            "vibe_error": "Potential format string vulnerability if first argument is not a literal.",
            "tmpnam": "Insecure, use mkstemp instead.",
            "tempnam": "Insecure, use mkstemp instead.",
            "mktemp": "Insecure, use mkstemp instead.",
            "realpath": "Can be unsafe if not checking return value or using a fixed-size buffer.",
            "strtok": "Not thread-safe, use strtok_r instead.",
            "vfork": "Unsafe, use fork or posix_spawn instead.",
            "strncat": "Can be tricky to use safely, ensure size argument is correct.",
        }

        # BOLT: Pre-compile a combined regex for O(1) pass per line
        combined_pattern = re.compile(rf"\b({'|'.join(re.escape(f) for f in unsafe_funcs.keys())})\s*\(")

        issues_found = 0
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith((".c", ".h")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", errors="ignore") as f:
                            for i, line in enumerate(f, 1):
                                # BOLT: Use single combined regex search
                                match = combined_pattern.search(line)
                                if match:
                                    func = match.group(1)
                                    desc = unsafe_funcs[func]
                                    print(f"  [!] {path}:{i} - Found potential unsafe function '{func}': {desc}")
                                    issues_found += 1
                    except Exception as e:
                        print(f"  [?] Could not read {path}: {e}")

        if issues_found == 0:
            print("  No obvious unsafe C functions found.")
        else:
            print(f"  Found {issues_found} potential issues.")

    def _internal_python_audit(self, py_dir):
        print(f"\n--- Internal Python Audit: {py_dir} ---")
        # Sentinel: Expanded list of unsafe Python patterns and use of regex with word boundaries
        unsafe_patterns = {
            r"\beval\s*\(": "Unsafe, allows execution of arbitrary code.", # nosec
            r"\bexec\s*\(": "Unsafe, allows execution of arbitrary code.", # nosec
            r"shell\s*=\s*True": "Potential shell injection vulnerability.", # nosec
            r"\bos\.system\s*\(": "Unsafe, can lead to command injection.", # nosec
            r"\bos\.popen\s*\(": "Unsafe, can lead to command injection.", # nosec
            r"\bos\.spawn": "Potential for command injection if arguments are not controlled.", # nosec
            r"\bpickle\.load": "Insecure deserialization can lead to arbitrary code execution.", # nosec
            r"\byaml\.load\s*\(": "Insecure deserialization can lead to arbitrary code execution if not using SafeLoader.", # nosec
            r"\btempfile\.mktemp": "Insecure, use tempfile.mkstemp instead.", # nosec
        }

        # BOLT: Pre-compile a combined regex for O(1) pass per line using named groups
        pattern_keys = list(unsafe_patterns.keys())
        combined_pattern = re.compile("|".join(f"(?P<p{i}>(?:{p}))" for i, p in enumerate(pattern_keys)))

        issues_found = 0
        for root, dirs, files in os.walk(py_dir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", errors="ignore") as f:
                            for i, line in enumerate(f, 1):
                                if "# nosec" in line:
                                    continue
                                # Sentinel: Use finditer to catch multiple issues on one line
                                for match in combined_pattern.finditer(line):
                                    # Find which pattern matched by checking group names
                                    for name, value in match.groupdict().items():
                                        if value is not None and name.startswith('p'):
                                            idx = int(name[1:])
                                            desc = unsafe_patterns[pattern_keys[idx]]
                                            print(f"  [!] {path}:{i} - Found unsafe pattern: {desc}")
                                            issues_found += 1
                                            break
                    except Exception as e:
                        print(f"  [?] Could not read {path}: {e}")

        if issues_found == 0:
            print("  No obvious unsafe Python patterns found.")
        else:
            print(f"  Found {issues_found} potential issues.")

    def run_audit(self):
        print("\n=== Vibe Security Audit ===")

        # Run internal audits first (no dependencies)
        self._internal_python_audit(self.vibe_dir)
        if os.path.exists("src"):
            self._internal_c_audit("src")

        if os.path.exists("tests"):
            self._internal_c_audit("tests")

        if not os.path.exists("src") and not os.path.exists("tests"):
            print("\nNote: No src/ or tests/ directory found for C audit.")

        # Check for optional external tools
        print("\n--- Checking for advanced audit tools ---")

        # Check for bandit (Python security)
        try:
            import bandit
            print("\n[Optional] Running Bandit for deeper Python analysis...")
            res = subprocess.run(["bandit", "-r", self.vibe_dir])
            if res.returncode == 0:
                print("Bandit: No major issues found.")
            else:
                print("Bandit: Some issues were found.")
        except ImportError:
            pass # Silent if not installed

        # Check for cppcheck (C security)
        if os.path.exists("src"):
            try:
                # We check if it exists by running version
                subprocess.run(["cppcheck", "--version"], capture_output=True, check=True)
                print("\n[Optional] Running Cppcheck for deeper C analysis...")
                res = subprocess.run(["cppcheck", "--enable=warning,style,performance,portability", "src"])
                if res.returncode == 0:
                    print("Cppcheck: Completed.")
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass # Silent if not installed

        print("\nAudit complete. Always follow best security practices!")

    def update_compiler(self):
        print("Checking for updates...")
        try:
            # Check if we are in a git repository
            res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True, cwd=self.base_dir)
            if res.returncode != 0:
                print("Error: Not a git repository. Cannot update automatically.")
                return

            print("Fetching latest version from GitHub...")
            res = subprocess.run(["git", "pull", "origin", "main"], cwd=self.base_dir)
            if res.returncode == 0:
                print("Successfully updated Vibe C Compiler.")
                # After update, version might have changed
                self.show_version()
            else:
                print("Failed to update. Please check your internet connection or run 'git pull' manually.")
        except Exception as e:
            print(f"An error occurred during update: {e}")
