#!/bin/bash
set -e  # Stop script on first error

# Parse command line arguments
SKIP_TESTS=0
SKIP_LINT=0
SKIP_MYPY=0
FIX_MODE=0

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --no-test)
            SKIP_TESTS=1
            shift
            ;;
        --no-lint)
            SKIP_LINT=1
            shift
            ;;
        --no-mypy)
            SKIP_MYPY=1
            shift
            ;;
        --fix)
            FIX_MODE=1
            shift
            ;;
        *)
            echo "Unknown option: $key"
            echo "Usage: $0 [--no-test] [--no-lint] [--no-mypy] [--fix]"
            exit 1
            ;;
    esac
done

# Determine the current working directory and the location of the update scripts
CURRENT_DIR=$(pwd)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get project configuration
echo "Getting project configuration..."
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
    
    print(f\"PROJECT_NAME={project_name}\")
    print(f\"PACKAGE_PATH={package_path}\")
    print(f\"PROJECT_ROOT={project_root}\")
except Exception as e:
    print(f\"PROJECT_NAME=unknown\")
    print(f\"PACKAGE_PATH=unknown\")
    print(f\"PROJECT_ROOT=$CURRENT_DIR\")
    print(f\"# Error: {e}\", file=sys.stderr)
")

# Process configuration
eval "$PROJECT_CONFIG"
echo "Project name: $PROJECT_NAME"
echo "Package path: $PACKAGE_PATH"
echo "Project root: $PROJECT_ROOT"

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

# Install project dependencies
echo "Installing project dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install test dependencies
echo "Installing test dependencies..."
pip install pytest flake8 black isort mypy tox

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

# Prepare test_code.py arguments
TEST_CODE_ARGS=""

if [ "$SKIP_TESTS" -eq 1 ]; then
    TEST_CODE_ARGS="$TEST_CODE_ARGS --skip-tests"
fi

if [ "$SKIP_LINT" -eq 1 ]; then
    TEST_CODE_ARGS="$TEST_CODE_ARGS --skip-lint"
fi

if [ "$SKIP_MYPY" -eq 1 ]; then
    TEST_CODE_ARGS="$TEST_CODE_ARGS --no-mypy"
fi

if [ "$FIX_MODE" -eq 1 ]; then
    TEST_CODE_ARGS="$TEST_CODE_ARGS --fix"
fi

# Run the tests
echo "Running code quality checks and tests..."
python "$SCRIPT_DIR/test_code.py" $TEST_CODE_ARGS

# Store the exit code
EXIT_CODE=$?

# Return the exit code
exit $EXIT_CODE
