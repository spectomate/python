#!/usr/bin/env python3
"""
Script to fix Black configuration in pyproject.toml files.
This helps resolve formatting issues between local and CI environments.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
import tomli
import tomli_w


def find_pyproject_toml(start_dir=None):
    """Find the pyproject.toml file in the current directory or parent directories."""
    if start_dir is None:
        start_dir = Path.cwd()
    
    current_dir = Path(start_dir).resolve()
    
    while current_dir != current_dir.parent:
        pyproject_path = current_dir / "pyproject.toml"
        if pyproject_path.exists():
            return pyproject_path
        current_dir = current_dir.parent
    
    return None


def read_pyproject_toml(file_path):
    """Read a pyproject.toml file and return its contents as a dictionary."""
    try:
        with open(file_path, "rb") as f:
            return tomli.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def write_pyproject_toml(file_path, data):
    """Write data to a pyproject.toml file."""
    try:
        with open(file_path, "wb") as f:
            tomli_w.dump(data, f)
        return True
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False


def get_python_version():
    """Get the current Python version."""
    major, minor, _ = sys.version_info[:3]
    return f"py{major}{minor}"


def ensure_black_config(pyproject_data, python_version=None):
    """Ensure that the pyproject.toml file has a proper Black configuration."""
    if python_version is None:
        python_version = get_python_version()
    
    # Create tool section if it doesn't exist
    if "tool" not in pyproject_data:
        pyproject_data["tool"] = {}
    
    # Create black section if it doesn't exist
    if "black" not in pyproject_data["tool"]:
        pyproject_data["tool"]["black"] = {}
    
    black_config = pyproject_data["tool"]["black"]
    
    # Set default values if they don't exist
    if "line-length" not in black_config:
        black_config["line-length"] = 88
    
    if "target-version" not in black_config:
        black_config["target-version"] = [python_version]
    
    if "include" not in black_config:
        black_config["include"] = r"\.pyi?$"
    
    if "exclude" not in black_config:
        black_config["exclude"] = r'''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
    
    return pyproject_data


def find_unformatted_files(directory="."):
    """Find files that would be reformatted by Black."""
    try:
        result = subprocess.run(
            ["black", "--check", directory, "--quiet"],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            # Extract files that would be reformatted
            files = []
            for line in result.stderr.split("\n"):
                match = re.search(r"would reformat (.+)$", line)
                if match:
                    files.append(match.group(1))
            
            return files
        
        return []
    except Exception as e:
        print(f"Error running Black: {e}")
        return []


def fix_line_endings(file_path):
    """Fix line endings to use LF (Unix) instead of CRLF (Windows)."""
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        # Replace CRLF with LF
        content = content.replace(b"\r\n", b"\n")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error fixing line endings in {file_path}: {e}")
        return False


def format_files_with_black(files):
    """Format files with Black."""
    if not files:
        return True
    
    try:
        result = subprocess.run(
            ["black"] + files,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            print(f"Error formatting files with Black: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"Error running Black: {e}")
        return False


def fix_black_config(directory=None, auto_format=False, fix_line_endings_flag=False):
    """Fix Black configuration in pyproject.toml and optionally format files."""
    if directory is None:
        directory = Path.cwd()
    
    # Find pyproject.toml
    pyproject_path = find_pyproject_toml(directory)
    if pyproject_path is None:
        print("Error: pyproject.toml not found")
        return False
    
    # Read pyproject.toml
    pyproject_data = read_pyproject_toml(pyproject_path)
    if pyproject_data is None:
        return False
    
    # Get Python version from project config if available
    python_version = None
    if "project" in pyproject_data and "requires-python" in pyproject_data["project"]:
        requires_python = pyproject_data["project"]["requires-python"]
        match = re.search(r">=\s*3\.(\d+)", requires_python)
        if match:
            minor_version = match.group(1)
            python_version = f"py3{minor_version}"
    
    # Ensure Black config
    pyproject_data = ensure_black_config(pyproject_data, python_version)
    
    # Write updated pyproject.toml
    if not write_pyproject_toml(pyproject_path, pyproject_data):
        return False
    
    print(f"Updated Black configuration in {pyproject_path}")
    
    # Find unformatted files
    unformatted_files = find_unformatted_files(directory)
    
    if unformatted_files:
        print(f"Found {len(unformatted_files)} files that need formatting:")
        for file in unformatted_files:
            print(f"  - {file}")
        
        if fix_line_endings_flag:
            print("\nFixing line endings...")
            for file in unformatted_files:
                if fix_line_endings(file):
                    print(f"  - Fixed line endings in {file}")
        
        if auto_format:
            print("\nFormatting files with Black...")
            if format_files_with_black(unformatted_files):
                print("All files formatted successfully")
            else:
                print("Failed to format some files")
        else:
            print("\nTo format these files, run:")
            print(f"  black {' '.join(unformatted_files)}")
    else:
        print("All files are already properly formatted")
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix Black configuration in pyproject.toml")
    parser.add_argument("--directory", "-d", help="Directory to search for pyproject.toml")
    parser.add_argument("--auto-format", "-f", action="store_true", help="Automatically format files")
    parser.add_argument("--fix-line-endings", "-l", action="store_true", help="Fix line endings (CRLF -> LF)")
    
    args = parser.parse_args()
    
    success = fix_black_config(
        directory=args.directory,
        auto_format=args.auto_format,
        fix_line_endings_flag=args.fix_line_endings,
    )
    
    sys.exit(0 if success else 1)
