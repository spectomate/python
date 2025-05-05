#!/usr/bin/env python
"""
Skrypt testowy do sprawdzenia działania wszystkich konwerterów w Spectomate.
"""

import os
import sys
from pathlib import Path

from spectomate.converters.pip_to_conda import PipToCondaConverter
from spectomate.converters.conda_to_pip import CondaToPipConverter
from spectomate.converters.pip_to_poetry import PipToPoetryConverter


def create_test_requirements():
    """Tworzy przykładowy plik requirements.txt do testów."""
    requirements_content = """
# Zależności podstawowe
numpy==1.22.0
pandas>=1.4.0
matplotlib>=3.5.0
# Zależności opcjonalne
requests>=2.27.0
pyyaml>=6.0
"""
    with open("test_requirements.txt", "w") as f:
        f.write(requirements_content)
    
    print("Utworzono plik test_requirements.txt")
    return Path("test_requirements.txt")


def test_pip_to_conda(requirements_file) -> None:
    """Testuje konwersję z formatu pip do formatu conda."""
    print("\n=== Test konwersji pip -> conda ===")
    
    output_file = Path("test_environment.yml")
    
    converter = PipToCondaConverter(
        source_file=requirements_file,
        target_file=output_file,
        options={"env_name": "testenv"}
    )
    
    try:
        result_path = converter.execute()
        print(f"Konwersja zakończona pomyślnie. Wynik zapisano w: {result_path}")
        
        # Wyświetlamy zawartość pliku
        print("\nZawartość pliku environment.yml:")
        with open(result_path, "r") as f:
            print(f.read())
        
        return result_path
    except Exception as e:
        print(f"Błąd podczas konwersji: {e}")
        return None


def test_conda_to_pip(environment_file):
    """Testuje konwersję z formatu conda do formatu pip."""
    print("\n=== Test konwersji conda -> pip ===")
    
    output_file = Path("test_requirements_from_conda.txt")
    
    converter = CondaToPipConverter(
        source_file=environment_file,
        target_file=output_file
    )
    
    try:
        result_path = converter.execute()
        print(f"Konwersja zakończona pomyślnie. Wynik zapisano w: {result_path}")
        
        # Wyświetlamy zawartość pliku
        print("\nZawartość pliku requirements.txt:")
        with open(result_path, "r") as f:
            print(f.read())
        
        return result_path
    except Exception as e:
        print(f"Błąd podczas konwersji: {e}")
        return None


def test_pip_to_poetry(requirements_file):
    """Testuje konwersję z formatu pip do formatu poetry."""
    print("\n=== Test konwersji pip -> poetry ===")
    
    output_file = Path("test_pyproject.toml")
    
    converter = PipToPoetryConverter(
        source_file=requirements_file,
        target_file=output_file,
        options={"project_name": "testproject", "version": "1.0.0"}
    )
    
    try:
        result_path = converter.execute()
        print(f"Konwersja zakończona pomyślnie. Wynik zapisano w: {result_path}")
        
        # Wyświetlamy zawartość pliku
        print("\nZawartość pliku pyproject.toml:")
        with open(result_path, "r") as f:
            print(f.read())
        
        return result_path
    except Exception as e:
        print(f"Błąd podczas konwersji: {e}")
        return None


def cleanup(files):
    """Usuwa pliki testowe."""
    print("\n=== Czyszczenie plików testowych ===")
    
    for file_path in files:
        if file_path and file_path.exists():
            os.remove(file_path)
            print(f"Usunięto plik: {file_path}")


def main():
    """Główna funkcja testowa."""
    print("=== Rozpoczęcie testów konwerterów Spectomate ===")
    
    # Tworzymy przykładowy plik requirements.txt
    requirements_file = create_test_requirements()
    
    # Lista plików do wyczyszczenia
    files_to_cleanup = [requirements_file]
    
    # Test konwersji pip -> conda
    environment_file = test_pip_to_conda(requirements_file)
    if environment_file:
        files_to_cleanup.append(environment_file)
    
    # Test konwersji conda -> pip
    if environment_file:
        requirements_from_conda = test_conda_to_pip(environment_file)
        if requirements_from_conda:
            files_to_cleanup.append(requirements_from_conda)
    
    # Test konwersji pip -> poetry
    pyproject_file = test_pip_to_poetry(requirements_file)
    if pyproject_file:
        files_to_cleanup.append(pyproject_file)
    
    # Czyszczenie plików testowych
    cleanup(files_to_cleanup)
    
    print("\n=== Zakończenie testów konwerterów Spectomate ===")


if __name__ == "__main__":
    main()