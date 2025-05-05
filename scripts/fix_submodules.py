#!/usr/bin/env python3
"""
Script to detect and fix Git submodule issues in the repository.
This script checks for directories that might be Git repositories but aren't properly
configured as submodules, and helps set them up correctly.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import configparser


def run_command(cmd, cwd=None, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=False,
            shell=isinstance(cmd, str),
            capture_output=capture_output,
            text=True,
        )
        return result
    except subprocess.SubprocessError as e:
        print(f"Error running command {cmd}: {e}")
        return None


def is_git_repository(path):
    """Check if a directory is a Git repository."""
    git_dir = os.path.join(path, ".git")
    return os.path.exists(git_dir) and os.path.isdir(git_dir)


def get_remote_url(repo_path):
    """Get the remote URL of a Git repository."""
    result = run_command(["git", "remote", "get-url", "origin"], cwd=repo_path)
    if result and result.returncode == 0:
        return result.stdout.strip()
    return None


def get_configured_submodules(repo_path):
    """Get a list of configured submodules from .gitmodules file."""
    gitmodules_path = os.path.join(repo_path, ".gitmodules")
    if not os.path.exists(gitmodules_path):
        return {}

    config = configparser.ConfigParser()
    config.read(gitmodules_path)
    
    submodules = {}
    for section in config.sections():
        if section.startswith("submodule "):
            name = section[len("submodule "):]
            path = config[section].get("path", name)
            url = config[section].get("url", "")
            submodules[path] = {"name": name, "url": url}
    
    return submodules


def find_potential_submodules(repo_path, ignore_dirs=None):
    """Find directories that might be Git repositories but aren't configured as submodules."""
    if ignore_dirs is None:
        ignore_dirs = [".git", "venv", "node_modules", "__pycache__", ".vscode", ".idea"]
    
    configured_submodules = get_configured_submodules(repo_path)
    potential_submodules = []
    
    for root, dirs, _ in os.walk(repo_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for d in dirs:
            dir_path = os.path.join(root, d)
            rel_path = os.path.relpath(dir_path, repo_path)
            
            # Skip if already a configured submodule
            if rel_path in configured_submodules:
                continue
            
            # Check if it's a Git repository
            if is_git_repository(dir_path):
                remote_url = get_remote_url(dir_path)
                potential_submodules.append({
                    "path": rel_path,
                    "url": remote_url
                })
    
    return potential_submodules


def update_gitmodules(repo_path, submodules_to_add):
    """Update the .gitmodules file with new submodules."""
    gitmodules_path = os.path.join(repo_path, ".gitmodules")
    
    # Create config parser
    config = configparser.ConfigParser()
    
    # Read existing config if it exists
    if os.path.exists(gitmodules_path):
        config.read(gitmodules_path)
    
    # Add new submodules
    for submodule in submodules_to_add:
        section_name = f"submodule {os.path.basename(submodule['path'])}"
        if not config.has_section(section_name):
            config.add_section(section_name)
        
        config[section_name]["path"] = submodule["path"]
        config[section_name]["url"] = submodule["url"]
    
    # Write the updated config
    with open(gitmodules_path, "w") as f:
        config.write(f)
    
    return gitmodules_path


def initialize_submodules(repo_path):
    """Initialize and update all submodules."""
    result = run_command(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_path)
    return result.returncode == 0 if result else False


def main():
    """Main function to detect and fix submodule issues."""
    parser = argparse.ArgumentParser(description="Detect and fix Git submodule issues")
    parser.add_argument("--repo", "-r", default=".", help="Path to the Git repository")
    parser.add_argument("--auto-fix", "-a", action="store_true", help="Automatically fix detected issues")
    parser.add_argument("--ignore", "-i", nargs="+", help="Directories to ignore")
    args = parser.parse_args()
    
    # Get absolute path to the repository
    repo_path = os.path.abspath(args.repo)
    
    # Check if the path is a Git repository
    if not is_git_repository(repo_path):
        print(f"Error: {repo_path} is not a Git repository")
        return 1
    
    # Get list of directories to ignore
    ignore_dirs = [".git", "venv", "node_modules", "__pycache__", ".vscode", ".idea"]
    if args.ignore:
        ignore_dirs.extend(args.ignore)
    
    # Find potential submodules
    potential_submodules = find_potential_submodules(repo_path, ignore_dirs)
    
    if not potential_submodules:
        print("No potential submodules found that aren't already configured.")
        return 0
    
    print(f"Found {len(potential_submodules)} potential submodules:")
    for i, submodule in enumerate(potential_submodules, 1):
        print(f"{i}. Path: {submodule['path']}")
        print(f"   URL: {submodule['url'] or 'Unknown'}")
    
    if args.auto_fix:
        # Filter out submodules with unknown URLs
        submodules_to_add = [s for s in potential_submodules if s["url"]]
        
        if not submodules_to_add:
            print("No submodules with known URLs to add.")
            return 0
        
        # Update .gitmodules file
        gitmodules_path = update_gitmodules(repo_path, submodules_to_add)
        print(f"Updated {gitmodules_path} with {len(submodules_to_add)} new submodules")
        
        # Initialize submodules
        if initialize_submodules(repo_path):
            print("Successfully initialized and updated submodules")
        else:
            print("Failed to initialize submodules")
            return 1
    else:
        print("\nTo fix these issues:")
        print("1. Run this script with --auto-fix to automatically update .gitmodules")
        print("2. Or manually edit .gitmodules to add the missing submodules")
        print("3. Then run 'git submodule update --init --recursive'")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
