#!/bin/bash

# Ensure script fails on any error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Checking Git submodules...${NC}"

# Get the repository root directory
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Check if .gitmodules file exists
if [ ! -f .gitmodules ]; then
    echo -e "${YELLOW}No .gitmodules file found. Creating one...${NC}"
    touch .gitmodules
fi

# Find potential Git repositories that aren't properly configured as submodules
echo -e "${GREEN}Scanning for potential Git submodules...${NC}"

# Find directories containing .git
POTENTIAL_SUBMODULES=$(find . -type d -name ".git" -not -path "./.git" | sed 's/\/.git$//')

# Check each potential submodule
for DIR in $POTENTIAL_SUBMODULES; do
    # Get relative path from repository root
    REL_PATH=${DIR#./}
    
    # Check if this directory is already in .gitmodules
    if grep -q "path = $REL_PATH" .gitmodules; then
        echo -e "Submodule already configured: ${YELLOW}$REL_PATH${NC}"
        continue
    fi
    
    echo -e "Found potential submodule: ${YELLOW}$REL_PATH${NC}"
    
    # Get remote URL
    cd "$DIR"
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
    cd "$REPO_ROOT"
    
    if [ -z "$REMOTE_URL" ]; then
        echo -e "${RED}Warning: No remote URL found for $REL_PATH${NC}"
        continue
    fi
    
    echo -e "Remote URL: $REMOTE_URL"
    
    # Add to .gitmodules
    echo -e "${GREEN}Adding $REL_PATH to .gitmodules...${NC}"
    
    # Extract submodule name from path
    SUBMODULE_NAME=$(basename "$REL_PATH")
    
    # Add submodule configuration to .gitmodules
    cat >> .gitmodules << EOF

[submodule "$SUBMODULE_NAME"]
	path = $REL_PATH
	url = $REMOTE_URL
EOF
    
    echo -e "${GREEN}Added submodule $SUBMODULE_NAME to .gitmodules${NC}"
done

# Initialize and update submodules
echo -e "${GREEN}Initializing and updating submodules...${NC}"
git submodule update --init --recursive

echo -e "${GREEN}Git submodules check completed.${NC}"
