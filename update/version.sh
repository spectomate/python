#!/bin/bash
set -e  # Zatrzymaj skrypt przy pierwszym błędzie

# Wyczyść ekran i pokaż informację o rozpoczęciu procesu
clear
echo "Starting publication process..."

# Sprawdź, czy virtualenv jest już aktywowany
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Tworzenie i aktywacja środowiska wirtualnego..."
    # Utwórz virtualenv, jeśli nie istnieje
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    source venv/bin/activate
else
    echo "Środowisko wirtualne już aktywne: $VIRTUAL_ENV"
fi

# Upewnij się, że mamy najnowsze narzędzia
echo "Upgrading build tools..."
pip install --upgrade pip build twine

# Sprawdź, czy jesteśmy w virtualenv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Błąd: Nie udało się aktywować środowiska wirtualnego!"
    exit 1
fi

# Zainstaluj zależności projektu
echo "Instalacja zależności projektu..."
pip install -r requirements.txt

# Odinstaluj i zainstaluj ponownie pakiet w trybie edycji
echo "Reinstalacja pakietu w trybie deweloperskim..."
pip uninstall -y spectomate
pip install -e .

# Aktualizacja wersji w plikach źródłowych
echo "Aktualizacja numeru wersji..."
python update/src.py -f spectomate/__init__.py --type patch
python update/src.py -f spectomate/_version.py --type patch
python update/src.py -f pyproject.toml --type patch

# Generowanie wpisu w CHANGELOG.md
echo "Generowanie wpisu w CHANGELOG.md..."
python update/changelog.py

# Publikacja na GitHub
echo "push changes..."
bash update/git.sh

# Publikacja na PyPI
echo "Publikacja na PyPI..."
bash update/pypi.sh

echo "Proces publikacji zakończony pomyślnie!"
