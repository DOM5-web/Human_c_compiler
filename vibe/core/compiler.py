import os
import subprocess
import shutil

class VibeCompiler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.include_dir = os.path.join(self.base_dir, "include")
        self.template_dir = os.path.join(self.base_dir, "templates")

    def init_project(self, name):
        if os.path.exists(name):
            print(f"Error: Directory '{name}' already exists.")
            return False

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

    def build_project(self, arch=None, lib_type="none"):
        if not os.path.exists("vibe.json"):
            print("Error: Not a vibe project (vibe.json not found).")
            return False

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

        output_name = "build/app"
        if lib_type == "static":
            output_name = "build/libapp.a"
        elif lib_type == "shared":
            output_name = "build/libapp.so"

        cmd = ["clang", "-I" + self.include_dir]
        if arch:
            cmd += ["-target", arch]

        if lib_type == "shared":
            cmd += ["-shared", "-fPIC"]

        cmd += src_files

        if lib_type == "static":
            # For static lib, we compile to .o then use ar
            obj_files = []
            for src in src_files:
                obj = src.replace("src/", "build/").replace(".c", ".o")
                os.makedirs(os.path.dirname(obj), exist_ok=True)
                subprocess.run(["clang", "-I" + self.include_dir, "-c", src, "-o", obj])
                obj_files.append(obj)
            subprocess.run(["ar", "rcs", output_name] + obj_files)
        else:
            cmd += ["-o", output_name]
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print("Build failed.")
                return False

        print(f"Build successful: {output_name}")
        return True

    def run_project(self):
        output_name = "build/app"
        if not os.path.exists(output_name):
            print("Error: Executable not found. Build it first.")
            return

        print(f"Running {output_name}...")
        subprocess.run(["./" + output_name])

    def clean_project(self):
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("Cleaned build directory.")
        else:
            print("Nothing to clean.")
