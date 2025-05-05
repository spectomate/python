#!/usr/bin/env python3
"""
Script to fix common mypy issues in the codebase.

This script specifically targets missing return type annotations in test files.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def find_test_files(root_dir: Path) -> List[Path]:
    """Find all Python test files in the given directory."""
    test_files = []
    for path in root_dir.glob("**/test_*.py"):
        test_files.append(path)
    return test_files


def fix_missing_return_types(file_path: Path) -> Tuple[bool, int]:
    """
    Fix missing return type annotations in the given file.
    
    Returns:
        Tuple of (whether file was modified, number of functions fixed)
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
        
        # Skip empty files
        if not content.strip():
            return False, 0
        
        tree = ast.parse(content)
        
        lines = content.splitlines()
        modified_lines = lines.copy()
        modified = False
        functions_fixed = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.returns is None:
                # Skip if function already has a return annotation
                if "-> " in lines[node.lineno - 1]:
                    continue
                    
                # Check if this is a test function or any function in a test file
                if True:  # We'll fix all functions in test files
                    # Find the line with the closing parenthesis
                    lineno = node.lineno - 1
                    while lineno < len(lines):
                        if "):" in lines[lineno]:
                            # Add return type annotation
                            line = modified_lines[lineno]
                            colon_idx = line.index("):")
                            new_line = line[:colon_idx+1] + " -> None" + line[colon_idx+1:]
                            modified_lines[lineno] = new_line
                            modified = True
                            functions_fixed += 1
                            break
                        lineno += 1
        
        if modified:
            with open(file_path, "w") as f:
                f.write("\n".join(modified_lines))
        
        return modified, functions_fixed
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0


def main() -> None:
    """Main function to fix mypy issues in the codebase."""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path.cwd()
    
    test_files = find_test_files(root_dir)
    print(f"Found {len(test_files)} test files")
    
    total_fixed = 0
    for file_path in test_files:
        try:
            modified, count = fix_missing_return_types(file_path)
            if modified:
                print(f"Fixed {count} functions in {file_path}")
                total_fixed += count
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
    
    print(f"Total functions fixed: {total_fixed}")


if __name__ == "__main__":
    main()
