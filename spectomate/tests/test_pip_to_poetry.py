"""
Testy dla konwertera z formatu pip do formatu poetry.
"""

import os
import tempfile
from pathlib import Path

import pytest
import toml

from spectomate.converters.pip_to_poetry import PipToPoetryConverter
from spectomate.schemas.pip_schema import PipSchema
from spectomate.schemas.poetry_schema import PoetrySchema


class TestPipToPoetryConverter:
    """
    Testy dla konwertera z formatu pip do formatu poetry.
    """

    def setup_method(self) -> None:
        """Przygotowanie środowiska testowego."""
        # Tworzymy tymczasowy katalog na pliki testowe
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Tworzymy przykładowy plik requirements.txt
        self.requirements_file = self.temp_path / "requirements.txt"
        with open(self.requirements_file, "w") as f:
            f.write(
                "\n".join(
                    [
                        "# Zależności podstawowe",
                        "numpy==1.22.0",
                        "pandas>=1.4.0",
                        "matplotlib>=3.5.0",
                        "# Zależności opcjonalne",
                        "requests>=2.27.0",
                        "pyyaml>=6.0",
                    ]
                )
            )

        # Ścieżka do pliku wyjściowego
        self.output_file = self.temp_path / "pyproject.toml"

    def teardown_method(self) -> None:
        """Czyszczenie po testach."""
        self.temp_dir.cleanup()

    def test_read_source(self) -> None:
        """Test odczytu pliku requirements.txt."""
        converter = PipToPoetryConverter(source_file=self.requirements_file)
        source_data = converter.read_source()

        assert "dependencies" in source_data
        assert len(source_data["dependencies"]) == 5
        assert "numpy==1.22.0" in source_data["dependencies"]
        assert "pandas>=1.4.0" in source_data["dependencies"]
        assert "matplotlib>=3.5.0" in source_data["dependencies"]
        assert "requests>=2.27.0" in source_data["dependencies"]
        assert "pyyaml>=6.0" in source_data["dependencies"]

    def test_convert(self) -> None:
        """Test konwersji danych z formatu pip do formatu poetry."""
        converter = PipToPoetryConverter(
            source_file=self.requirements_file,
            options={"project_name": "testproject", "version": "1.0.0"},
        )

        source_data = converter.read_source()
        target_data = converter.convert(source_data)

        assert target_data["name"] == "testproject"
        assert target_data["version"] == "1.0.0"
        assert "dependencies" in target_data

        # Sprawdzamy, czy wszystkie zależności zostały uwzględnione
        deps = target_data["dependencies"]
        assert "numpy" in deps
        assert deps["numpy"] == "==1.22.0"
        assert "pandas" in deps
        assert deps["pandas"] == ">=1.4.0"
        assert "matplotlib" in deps
        assert deps["matplotlib"] == ">=3.5.0"
        assert "requests" in deps
        assert deps["requests"] == ">=2.27.0"
        assert "pyyaml" in deps
        assert deps["pyyaml"] == ">=6.0"

    def test_write_target(self) -> None:
        """Test zapisu danych do pliku pyproject.toml."""
        converter = PipToPoetryConverter(
            source_file=self.requirements_file,
            target_file=self.output_file,
            options={"project_name": "testproject", "version": "1.0.0"},
        )

        source_data = converter.read_source()
        target_data = converter.convert(source_data)
        result_path = converter.write_target(target_data)

        assert result_path == self.output_file
        assert self.output_file.exists()

        # Sprawdzamy, czy plik można odczytać jako poprawny TOML
        with open(self.output_file, "r") as f:
            pyproject_data = toml.load(f)

        assert "tool" in pyproject_data
        assert "poetry" in pyproject_data["tool"]
        poetry_data = pyproject_data["tool"]["poetry"]

        assert poetry_data["name"] == "testproject"
        assert poetry_data["version"] == "1.0.0"
        assert "dependencies" in poetry_data

        # Sprawdzamy, czy wszystkie zależności są w pliku
        deps = poetry_data["dependencies"]
        assert "numpy" in deps
        assert deps["numpy"] == "==1.22.0"
        assert "pandas" in deps
        assert deps["pandas"] == ">=1.4.0"
        assert "matplotlib" in deps
        assert deps["matplotlib"] == ">=3.5.0"
        assert "requests" in deps
        assert deps["requests"] == ">=2.27.0"
        assert "pyyaml" in deps
        assert deps["pyyaml"] == ">=6.0"

    def test_execute(self) -> None:
        """Test pełnego procesu konwersji."""
        converter = PipToPoetryConverter(
            source_file=self.requirements_file,
            target_file=self.output_file,
            options={"project_name": "testproject", "version": "1.0.0"},
        )

        result_path = converter.execute()

        assert result_path == self.output_file
        assert self.output_file.exists()

        # Sprawdzamy, czy plik można odczytać jako poprawny TOML
        with open(self.output_file, "r") as f:
            pyproject_data = toml.load(f)

        assert "tool" in pyproject_data
        assert "poetry" in pyproject_data["tool"]
        poetry_data = pyproject_data["tool"]["poetry"]

        assert poetry_data["name"] == "testproject"
        assert poetry_data["version"] == "1.0.0"
        assert "dependencies" in poetry_data


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
