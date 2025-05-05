#!/usr/bin/env python3
"""
Script to run all tests and code quality checks for the Spectomate package.
This provides a convenient way to run the same checks locally that are run in CI.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def run_command(cmd: List[str], cwd: Optional[str] = None) -> int:
    """Run a command and return the exit code."""
    try:
        process = subprocess.run(cmd, cwd=cwd)
        return process.returncode
    except Exception as e:
        console.print(f"[red]Error running command: {e}[/red]")
        return 1


def main() -> int:
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Run tests for Spectomate")
    parser.add_argument(
        "--src", default="spectomate", help="Source directory to test (default: spectomate)"
    )
    parser.add_argument(
        "--tests", default="tests", help="Tests directory (default: tests)"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Fix issues automatically where possible"
    )
    parser.add_argument(
        "--skip-lint", action="store_true", help="Skip linting checks"
    )
    parser.add_argument(
        "--skip-tests", action="store_true", help="Skip unit tests"
    )
    parser.add_argument(
        "--skip-mypy", action="store_true", help="Skip mypy type checking"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show verbose output"
    )
    
    args = parser.parse_args()
    
    # Get the project root directory (parent of the scripts directory)
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    results = {}
    
    console.print(Panel("Running tests for Spectomate", style="blue"))
    
    if not args.skip_lint:
        # Run black
        console.print("\n[bold]Running black code formatter...[/bold]")
        black_cmd = ["black"]
        if not args.fix:
            black_cmd.append("--check")
        if args.verbose:
            black_cmd.append("--verbose")
        black_cmd.extend([args.src, args.tests])
        
        black_result = run_command(black_cmd)
        results["black"] = {
            "success": black_result == 0,
            "message": "Code formatting passed" if black_result == 0 else "Code formatting issues found"
        }
        
        # Run isort
        console.print("\n[bold]Running isort import sorter...[/bold]")
        isort_cmd = ["isort"]
        if not args.fix:
            isort_cmd.append("--check-only")
        if args.verbose:
            isort_cmd.append("--verbose")
        isort_cmd.extend(["--profile", "black", args.src, args.tests])
        
        isort_result = run_command(isort_cmd)
        results["isort"] = {
            "success": isort_result == 0,
            "message": "Import sorting passed" if isort_result == 0 else "Import sorting issues found"
        }
        
        # Run flake8
        console.print("\n[bold]Running flake8 linting...[/bold]")
        flake8_cmd = ["flake8", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics", args.src]
        
        flake8_result = run_command(flake8_cmd)
        results["flake8"] = {
            "success": flake8_result == 0,
            "message": "Flake8 checks passed" if flake8_result == 0 else "Critical linting errors found"
        }
    
    if not args.skip_mypy:
        # Run mypy
        console.print("\n[bold]Running mypy type checking...[/bold]")
        mypy_cmd = ["mypy", "--ignore-missing-imports", args.src]
        
        mypy_result = run_command(mypy_cmd)
        results["mypy"] = {
            "success": mypy_result == 0,
            "message": "Type checking passed" if mypy_result == 0 else "Type checking issues found"
        }
    
    if not args.skip_tests:
        # Run pytest
        console.print("\n[bold]Running pytest unit tests...[/bold]")
        pytest_cmd = ["pytest"]
        if args.verbose:
            pytest_cmd.append("-v")
        pytest_cmd.extend(["--cov=" + args.src, args.tests])
        
        pytest_result = run_command(pytest_cmd)
        results["pytest"] = {
            "success": pytest_result == 0,
            "message": "Unit tests passed" if pytest_result == 0 else "Unit tests failed"
        }
    
    # Display summary
    console.print("\n[bold]Test Summary:[/bold]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Test")
    table.add_column("Status")
    table.add_column("Message")
    
    all_success = True
    
    for test_name, result in results.items():
        status = "[green]PASS[/green]" if result["success"] else "[red]FAIL[/red]"
        table.add_row(test_name, status, result["message"])
        if not result["success"]:
            all_success = False
    
    console.print(table)
    
    if not all_success:
        console.print("[red]Some tests failed![/red]")
        return 1
    else:
        console.print("[green]All tests passed![/green]")
        return 0


if __name__ == "__main__":
    sys.exit(main())
