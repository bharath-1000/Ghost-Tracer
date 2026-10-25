#!/usr/bin/env python3
"""
Packaging script for GHOST TRACER HackerRank submission (code.zip).
Packages code/, docs/, README.md, and evaluation reports without bundling dataset/ or caches.
"""

import os
import zipfile

def package_code():
    zip_filename = "code.zip"
    print(f"Creating submission package {zip_filename}...")
    
    # Excluded directories and patterns
    exclude_dirs = {"__pycache__", ".venv", "venv", "node_modules", ".git", ".idea", "dist", "dataset"}
    exclude_exts = {".pyc", ".DS_Store"}

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Include README.md and root files if present
        for root_file in ["README.md", "metadata.json", "package.json"]:
            if os.path.exists(root_file):
                zipf.write(root_file, root_file)
                print(f"  Added {root_file}")

        # Include code/ directory
        for root, dirs, files in os.walk("code"):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path)

        # Include docs/ directory
        if os.path.exists("docs"):
            for root, dirs, files in os.walk("docs"):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    if any(file.endswith(ext) for ext in exclude_exts):
                        continue
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path)

        # Include scripts/ directory
        if os.path.exists("scripts"):
            for root, dirs, files in os.walk("scripts"):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    if any(file.endswith(ext) for ext in exclude_exts):
                        continue
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path)

    print(f"Successfully created {zip_filename} ({os.path.getsize(zip_filename)} bytes).")

    # Verify archive contents
    with zipfile.ZipFile(zip_filename, "r") as zipf:
        namelist = zipf.namelist()
        print(f"Verified archive containing {len(namelist)} items.")
        assert "code/main.py" in namelist, "code/main.py missing"
        assert "code/evaluation/evaluation_report.md" in namelist, "evaluation_report.md missing"
        assert "code/evaluation/usage_report.md" in namelist, "usage_report.md missing"
        assert not any("dataset/" in item for item in namelist), "dataset/ improperly included in code.zip"
        print("Archive verification PASSED: zero forbidden directories bundled.")

if __name__ == "__main__":
    package_code()
