#!/bin/bash

# Ensure script fails on any error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Rozpoczynanie procesu publikacji na PyPI...${NC}"

# Sprawdź, czy jesteśmy w virtualenv
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}Błąd: Nie wykryto aktywnego środowiska wirtualnego!${NC}"
    echo "Uruchom skrypt version.sh, który aktywuje środowisko wirtualne."
    exit 1
fi

echo -e "${GREEN}Sprawdzanie stanu repozytorium Git...${NC}"
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}Uwaga: Wykryto niezapisane zmiany w repozytorium.${NC}"
    echo -e "Zalecane jest najpierw opublikowanie zmian na GitHub (bash update/git.sh)."
    read -p "Czy chcesz kontynuować mimo to? (t/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Tt]$ ]]; then
        echo -e "${RED}Przerwano publikację.${NC}"
        exit 1
    fi
fi

# Clean up previous builds
echo -e "${GREEN}Czyszczenie poprzednich buildów...${NC}"
rm -rf build/ dist/ *.egg-info/

# Install/upgrade build tools
echo -e "${GREEN}Aktualizacja narzędzi do budowania...${NC}"
python -m pip install --upgrade pip setuptools wheel build twine

# Build the package
echo -e "${GREEN}Budowanie pakietu...${NC}"
python -m build

# Check the distribution
echo -e "${GREEN}Sprawdzanie paczki dystrybucyjnej...${NC}"
twine check dist/*

# Ask for confirmation before uploading
echo -e "${YELLOW}Pakiet jest gotowy do publikacji na PyPI.${NC}"
read -p "Czy chcesz opublikować pakiet? (t/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Tt]$ ]]; then
    echo -e "${RED}Przerwano publikację.${NC}"
    exit 1
fi

echo -e "${GREEN}Publikowanie na PyPI...${NC}"
twine upload dist/*

echo -e "${GREEN}Pakiet został pomyślnie opublikowany na PyPI!${NC}"