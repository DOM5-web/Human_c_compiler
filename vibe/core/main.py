import argparse
import sys
import os
from .compiler import VibeCompiler
from .menu import run_menu

def main():
    parser = argparse.ArgumentParser(description="Vibe C Compiler - The easier C compiler")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("name", help="Name of the project")

    # build
    build_parser = subparsers.add_parser("build", help="Build the current project")
    build_parser.add_argument("--arch", help="Target architecture (e.g. x86_64, aarch64)")
    build_parser.add_argument("--lib", choices=["static", "shared", "none"], default="none", help="Build as a library")

    # run
    run_parser = subparsers.add_parser("run", help="Build and run the current project")

    # clean
    clean_parser = subparsers.add_parser("clean", help="Clean build artifacts")

    # menu
    menu_parser = subparsers.add_parser("menu", help="Open the simple menu")

    # version
    version_parser = subparsers.add_parser("version", help="Show version")

    args = parser.parse_args()

    compiler = VibeCompiler()

    if args.command == "init":
        compiler.init_project(args.name)
    elif args.command == "build":
        compiler.build_project(arch=args.arch, lib_type=args.lib)
    elif args.command == "run":
        if compiler.build_project():
            compiler.run_project()
    elif args.command == "clean":
        compiler.clean_project()
    elif args.command == "menu":
        run_menu(compiler)
    elif args.command == "version":
        version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "VERSION")
        with open(version_file, "r") as f:
            print(f"Vibe C Compiler v{f.read().strip()}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
