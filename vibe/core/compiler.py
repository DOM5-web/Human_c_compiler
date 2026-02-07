import os
import subprocess
import shutil

class VibeCompiler:
    def __init__(self):
        # __file__ is vibe/core/compiler.py
        # dirname(dirname(dirname(__file__))) is the root directory
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.vibe_dir = os.path.join(self.base_dir, "vibe")
        self.include_dir = os.path.join(self.vibe_dir, "include")
        self.template_dir = os.path.join(self.vibe_dir, "templates")
        self.version_file = os.path.join(self.base_dir, "VERSION")

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
        # Basic sanitization
        if ".." in name or name.startswith("/") or name.startswith("~"):
            print("Error: Invalid project name.")
            return False

        if os.path.exists(name):
            print(f"Error: Directory '{name}' already exists.")
            return False

        template_path = os.path.join(self.template_dir, template)
        if not os.path.exists(template_path):
            print(f"Error: Template '{template}' not found. Using 'basic' instead.")
            template_path = os.path.join(self.template_dir, "basic")

        shutil.copytree(template_path, name)

        # Update vibe.json with project name
        config_path = os.path.join(name, "vibe.json")
        with open(config_path, "r") as f:
            content = f.read()
        content = content.replace("{{name}}", name)
        with open(config_path, "w") as f:
            f.write(content)

        os.makedirs(os.path.join(name, "build"), exist_ok=True)

        print(f"Project '{name}' initialized successfully.")
        return True

    def build_project(self, arch=None, lib_type=None):
        import json
        if not os.path.exists("vibe.json"):
            print("Error: Not a vibe project (vibe.json not found).")
            return False

        with open("vibe.json", "r") as f:
            config = json.load(f)

        proj_name = config.get("name", "app")
        proj_type = config.get("type", "executable")

        # Override project type if lib_type is specified
        if lib_type and lib_type != "none":
            proj_type = lib_type

        if not os.path.exists("build"):
            os.makedirs("build")

        # Find all .c files in src
        src_files = []
        for root, dirs, files in os.walk("src"):
            for file in files:
                if file.endswith(".c"):
                    src_files.append(os.path.join(root, file))

        if not src_files:
            print("Error: No source files found in src/")
            return False

        if proj_type == "static":
            output_name = f"build/lib{proj_name}.a"
        elif proj_type == "shared":
            output_name = f"build/lib{proj_name}.so"
        else:
            output_name = f"build/{proj_name}"

        cmd = ["clang", "-I" + self.include_dir]
        if arch:
            cmd += ["-target", arch]

        if proj_type == "shared":
            cmd += ["-shared", "-fPIC"]

        if proj_type == "static":
            # For static lib, we compile to .o then use ar
            obj_files = []
            for src in src_files:
                print(f"Compiling {src}...")
                # relative path to src
                rel_path = os.path.relpath(src, "src")
                obj = os.path.join("build", rel_path.replace(".c", ".o"))
                os.makedirs(os.path.dirname(obj), exist_ok=True)
                res = subprocess.run(["clang", "-I" + self.include_dir, "-c", src, "-o", obj])
                if res.returncode != 0:
                    print(f"Error compiling {src}")
                    return False
                obj_files.append(obj)
            print(f"Creating static library {output_name}...")
            res = subprocess.run(["ar", "rcs", output_name] + obj_files)
            if res.returncode != 0:
                print("Error creating static library")
                return False
        else:
            print(f"Compiling project...")
            cmd += src_files + ["-o", output_name]
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print("Build failed.")
                return False

        print(f"Build successful: {output_name}")
        return True

    def run_project(self):
        import json
        if not os.path.exists("vibe.json"):
            print("Error: vibe.json not found.")
            return

        with open("vibe.json", "r") as f:
            config = json.load(f)

        proj_name = config.get("name", "app")
        output_name = os.path.join("build", proj_name)

        if not os.path.exists(output_name):
            print(f"Error: Executable {output_name} not found. Build it first.")
            return

        print(f"Running {output_name}...")
        subprocess.run(["./" + output_name])

    def clean_project(self):
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("Cleaned build directory.")
        else:
            print("Nothing to clean.")

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

        import json
        try:
            with open("vibe.json", "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error reading vibe.json: {e}")
            return

        print("\n=== Vibe Project Status ===")
        print(f"Name:    {config.get('name', 'N/A')}")
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
