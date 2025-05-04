#!/usr/bin/env python
"""
Przykład użycia Spectomate do konwersji z formatu pip (requirements.txt) do formatu poetry (pyproject.toml).
"""

import sys
from pathlib import Path

from spectomate.converters.pip_to_poetry import PipToPoetryConverter


def main():
    """
    Główna funkcja przykładu.
    """
    # Sprawdzamy, czy podano argumenty
    if len(sys.argv) < 2:
        print("Użycie: python pip_to_poetry_example.py <ścieżka_do_requirements.txt> [<nazwa_projektu>] [<wersja>]")
        return 1
    
    # Pobieramy ścieżkę do pliku requirements.txt
    requirements_file = Path(sys.argv[1])
    
    # Sprawdzamy, czy plik istnieje
    if not requirements_file.exists():
        print(f"Błąd: Plik {requirements_file} nie istnieje.")
        return 1
    
    # Pobieramy nazwę projektu (opcjonalnie)
    project_name = "myproject"
    if len(sys.argv) > 2:
        project_name = sys.argv[2]
    
    # Pobieramy wersję projektu (opcjonalnie)
    version = "0.1.0"
    if len(sys.argv) > 3:
        version = sys.argv[3]
    
    # Tworzymy ścieżkę do pliku wyjściowego
    output_file = requirements_file.parent / "pyproject.toml"
    
    print(f"Konwersja {requirements_file} do {output_file}...")
    print(f"Nazwa projektu: {project_name}")
    print(f"Wersja: {version}")
    
    # Tworzymy konwerter
    converter = PipToPoetryConverter(
        source_file=requirements_file,
        target_file=output_file,
        options={
            "project_name": project_name,
            "version": version
        }
    )
    
    # Wykonujemy konwersję
    try:
        result_path = converter.execute()
        print(f"Konwersja zakończona pomyślnie. Wynik zapisano w: {result_path}")
        return 0
    except Exception as e:
        print(f"Błąd podczas konwersji: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
