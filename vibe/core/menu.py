import os
import sys

def run_menu(compiler):
    while True:
        print("\n=== Vibe C Compiler Menu ===")
        print("1. Initialize New Project")
        print("2. Build Project")
        print("3. Run Project")
        print("4. Clean Project")
        print("5. Exit")

        choice = input("\nSelect an option (1-5): ")

        if choice == "1":
            name = input("Enter project name: ")
            compiler.init_project(name)
        elif choice == "2":
            arch = input("Enter target architecture (leave blank for default): ")
            lib = input("Enter library type (none/static/shared, default=none): ") or "none"
            compiler.build_project(arch=arch if arch else None, lib_type=lib)
        elif choice == "3":
            compiler.run_project()
        elif choice == "4":
            compiler.clean_project()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
