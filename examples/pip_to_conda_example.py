#!/usr/bin/env python
"""
Przykład użycia Spectomate do konwersji z formatu pip (requirements.txt) do formatu conda (environment.yml).
"""

import sys
from pathlib import Path

from spectomate.converters.pip_to_conda import PipToCondaConverter


def main():
    """
    Główna funkcja przykładu.
    """
    # Sprawdzamy, czy podano argumenty
    if len(sys.argv) < 2:
        print("Użycie: python pip_to_conda_example.py <ścieżka_do_requirements.txt> [<nazwa_środowiska>]")
        return 1
    
    # Pobieramy ścieżkę do pliku requirements.txt
    requirements_file = Path(sys.argv[1])
    
    # Sprawdzamy, czy plik istnieje
    if not requirements_file.exists():
        print(f"Błąd: Plik {requirements_file} nie istnieje.")
        return 1
    
    # Pobieramy nazwę środowiska (opcjonalnie)
    env_name = "myenv"
    if len(sys.argv) > 2:
        env_name = sys.argv[2]
    
    # Tworzymy ścieżkę do pliku wyjściowego
    output_file = requirements_file.parent / "environment.yml"
    
    print(f"Konwersja {requirements_file} do {output_file}...")
    print(f"Nazwa środowiska: {env_name}")
    
    # Tworzymy konwerter
    converter = PipToCondaConverter(
        source_file=requirements_file,
        target_file=output_file,
        options={"env_name": env_name}
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
