#!/bin/bash
set -e  # Stop script on first error

# Ustaw zmienną TERM, jeśli nie jest ustawiona
if [ -z "$TERM" ]; then
    export TERM=xterm
fi

# Clear screen and show start information
clear
echo "Starting publication process..."

# Check for environment variables to control script behavior
SKIP_TESTS=${SKIP_TESTS:-0}
SKIP_LINT=${SKIP_LINT:-0}
SKIP_MYPY=${SKIP_MYPY:-0}
SKIP_PUBLISH=${SKIP_PUBLISH:-0}
SKIP_SUBMODULES=${SKIP_SUBMODULES:-0}
VERBOSE=${VERBOSE:-0}

# Display configuration if verbose
if [ "$VERBOSE" = "1" ]; then
    echo "Script configuration:"
    echo "- Skip tests: $SKIP_TESTS"
    echo "- Skip lint: $SKIP_LINT"
    echo "- Skip mypy: $SKIP_MYPY"
    echo "- Skip publish: $SKIP_PUBLISH"
    echo "- Skip submodules check: $SKIP_SUBMODULES"
    echo "- Verbose: $VERBOSE"
fi

# Get project configuration
echo "Getting project configuration..."

# Determine the current working directory and the location of the update scripts
CURRENT_DIR=$(pwd)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Add the update directory to Python path
PROJECT_CONFIG=$(python3 -c "
import sys
import os
sys.path.append('$SCRIPT_DIR')
try:
    from env_manager import get_project_name, get_package_path, get_project_root
    
    # Ask user for project name if not defined
    project_name = get_project_name(True)
    package_path = get_package_path(True)
    project_root = get_project_root()
    
    # Get version files - use only pyproject.toml which is usually accessible
    version_files = []
    
    # Check pyproject.toml
    pyproject_path = os.path.join(project_root, 'pyproject.toml')
    if os.path.exists(pyproject_path) and os.access(pyproject_path, os.W_OK):
        version_files.append(pyproject_path)
    
    print(f\"PROJECT_NAME={project_name}\")
    print(f\"PACKAGE_PATH={package_path}\")
    print(f\"PROJECT_ROOT={project_root}\")
    print(f\"VERSION_FILES={';'.join(version_files)}\")
except Exception as e:
    print(f\"PROJECT_NAME=unknown\")
    print(f\"PACKAGE_PATH=unknown\")
    print(f\"PROJECT_ROOT=$CURRENT_DIR\")
    print(f\"VERSION_FILES=pyproject.toml\")
    print(f\"# Error: {e}\", file=sys.stderr)
")

# Process configuration
eval "$PROJECT_CONFIG"
echo "Project name: $PROJECT_NAME"
echo "Package path: $PACKAGE_PATH"
echo "Project root: $PROJECT_ROOT"
echo "Version files: $VERSION_FILES"

# Change to project root directory if it's not the current directory
if [ "$PROJECT_ROOT" != "$CURRENT_DIR" ]; then
    echo "Changing to project root directory: $PROJECT_ROOT"
    cd "$PROJECT_ROOT"
fi

# Check if virtualenv is already activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Creating and activating virtual environment..."
    # Create virtualenv if it doesn't exist
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    source venv/bin/activate
else
    echo "Virtual environment already active: $VIRTUAL_ENV"
fi

# Make sure we have the latest tools
echo "Upgrading build tools..."
pip install --upgrade pip build twine

# Check if we're in virtualenv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate virtual environment!"
    exit 1
fi

# Install project dependencies
echo "Installing project dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Uninstall and reinstall package in edit mode
echo "Reinstalling package in development mode..."
pip uninstall -y "$PROJECT_NAME" || true
pip install -e .

# Update version in source files
echo "Updating version number..."
if [ -n "$VERSION_FILES" ]; then
    IFS=';' read -ra FILES <<< "$VERSION_FILES"
    for file in "${FILES[@]}"; do
        if [ -w "$file" ]; then
            echo "Updating version in file: $file"
            python "$SCRIPT_DIR/src.py" -f "$file" --type patch || echo "Failed to update version in file $file"
        else
            echo "Skipped file $file (no write permission)"
        fi
    done
else
    echo "No files to update version"
    echo "Using default version from CHANGELOG.md"
fi

# Generate entry in CHANGELOG.md
echo "Generating entry in CHANGELOG.md..."
if [ -f "CHANGELOG.md" ] && [ ! -w "CHANGELOG.md" ]; then
    echo "Warning: No write permission to CHANGELOG.md file"
    echo "Creating temporary file CHANGELOG.md.new"
    python "$SCRIPT_DIR/changelog.py" --output CHANGELOG.md.new || echo "Failed to generate entry in CHANGELOG.md"
else
    python "$SCRIPT_DIR/changelog.py" || echo "Failed to generate entry in CHANGELOG.md"
fi

# Run code quality checks and tests if not skipped
if [ "$SKIP_TESTS" != "1" ] || [ "$SKIP_LINT" != "1" ]; then
    echo "Running code quality checks and tests..."
    echo "This step ensures your code meets quality standards and all tests pass."
    
    # Prepare test command options
    TEST_OPTIONS=""
    if [ "$SKIP_LINT" = "1" ]; then
        TEST_OPTIONS="$TEST_OPTIONS --no-lint"
    else
        TEST_OPTIONS="$TEST_OPTIONS --fix"
    fi
    
    if [ "$SKIP_TESTS" = "1" ]; then
        TEST_OPTIONS="$TEST_OPTIONS --no-test"
    fi
    
    if [ "$SKIP_MYPY" = "1" ]; then
        TEST_OPTIONS="$TEST_OPTIONS --no-mypy"
    fi
    
    bash "$SCRIPT_DIR/test.sh" $TEST_OPTIONS
    if [ $? -ne 0 ]; then
        echo "Code quality checks or tests failed. Please fix the issues before publishing."
        echo "You can run '$SCRIPT_DIR/test.sh --fix' to automatically fix some issues."
        exit 1
    fi
    echo "All code quality checks and tests passed!"
fi

# Check and fix Git submodules if not skipped
if [ "$SKIP_SUBMODULES" != "1" ]; then
    echo "Checking and fixing Git submodules..."
    bash "$SCRIPT_DIR/submodules.sh"
    if [ $? -ne 0 ]; then
        echo "Git submodule check failed. Please fix the issues before publishing."
        exit 1
    fi
    echo "Git submodules check passed!"
fi

# Publish to GitHub and PyPI if not skipped
if [ "$SKIP_PUBLISH" != "1" ]; then
    # Publish to GitHub
    echo "Push changes..."
    bash "$SCRIPT_DIR/git.sh"

    # Publish to PyPI
    echo "Publishing to PyPI..."
    bash "$SCRIPT_DIR/pypi.sh"
    
    echo "Publication process completed successfully!"
else
    echo "Skipping publication to GitHub and PyPI."
    echo "Update process completed successfully!"
fi
