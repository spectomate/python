"""
Testy dla konwertera z formatu conda do formatu pip.
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from spectomate.converters.conda_to_pip import CondaToPipConverter
from spectomate.schemas.conda_schema import CondaSchema
from spectomate.schemas.pip_schema import PipSchema


class TestCondaToPipConverter:
    """
    Testy dla konwertera z formatu conda do formatu pip.
    """

    def setup_method(self):
        """Przygotowanie środowiska testowego."""
        # Tworzymy tymczasowy katalog na pliki testowe
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Tworzymy przykładowy plik environment.yml
        self.environment_file = self.temp_path / "environment.yml"

        # Tworzymy przykładowe środowisko conda
        conda_env = {
            "name": "testenv",
            "channels": ["defaults", "conda-forge"],
            "dependencies": [
                "python=3.9",
                "numpy=1.22.0",
                "pandas>=1.4.0",
                "matplotlib>=3.5.0",
                {"pip": ["requests>=2.27.0", "pyyaml>=6.0"]},
            ],
        }

        # Zapisujemy środowisko do pliku
        with open(self.environment_file, "w") as f:
            yaml.dump(conda_env, f, default_flow_style=False)

        # Ścieżka do pliku wyjściowego
        self.output_file = self.temp_path / "requirements.txt"

    def teardown_method(self):
        """Czyszczenie po testach."""
        self.temp_dir.cleanup()

    def test_read_source(self):
        """Test odczytu pliku environment.yml."""
        converter = CondaToPipConverter(source_file=self.environment_file)
        source_data = converter.read_source()

        assert source_data["name"] == "testenv"
        assert "defaults" in source_data["channels"]
        assert "conda-forge" in source_data["channels"]
        assert "dependencies" in source_data
        assert len(source_data["dependencies"]) == 5  # 4 conda deps + 1 pip dict

        # Sprawdzamy, czy zależności pip zostały poprawnie odczytane
        pip_deps = CondaSchema.extract_pip_dependencies(source_data)
        assert len(pip_deps) == 2
        assert "requests>=2.27.0" in pip_deps
        assert "pyyaml>=6.0" in pip_deps

    def test_convert(self):
        """Test konwersji danych z formatu conda do formatu pip."""
        converter = CondaToPipConverter(source_file=self.environment_file)

        source_data = converter.read_source()
        target_data = converter.convert(source_data)

        assert target_data["format"] == "pip"
        assert "requirements" in target_data

        # Sprawdzamy, czy wszystkie zależności zostały uwzględnione
        deps = target_data["requirements"]
        assert len(deps) > 0

        # Sprawdzamy, czy zależności conda zostały przekonwertowane
        assert "python=3.9" in deps
        assert "numpy=1.22.0" in deps
        assert "pandas>=1.4.0" in deps
        assert "matplotlib>=3.5.0" in deps

        # Sprawdzamy, czy zależności pip zostały uwzględnione
        assert "requests>=2.27.0" in deps
        assert "pyyaml>=6.0" in deps

    def test_write_target(self):
        """Test zapisu danych do pliku requirements.txt."""
        converter = CondaToPipConverter(
            source_file=self.environment_file, target_file=self.output_file
        )

        source_data = converter.read_source()
        target_data = converter.convert(source_data)
        result_path = converter.write_target(target_data)

        assert result_path == self.output_file
        assert self.output_file.exists()

        # Sprawdzamy, czy plik można odczytać jako poprawny requirements.txt
        with open(self.output_file, "r") as f:
            content = f.read()

        # Sprawdzamy, czy wszystkie zależności są w pliku
        assert "python=3.9" in content
        assert "numpy=1.22.0" in content
        assert "pandas>=1.4.0" in content
        assert "matplotlib>=3.5.0" in content
        assert "requests>=2.27.0" in content
        assert "pyyaml>=6.0" in content

    def test_execute(self):
        """Test pełnego procesu konwersji."""
        converter = CondaToPipConverter(
            source_file=self.environment_file, target_file=self.output_file
        )

        result_path = converter.execute()

        assert result_path == self.output_file
        assert self.output_file.exists()

        # Sprawdzamy, czy plik można odczytać jako poprawny requirements.txt
        with open(self.output_file, "r") as f:
            content = f.read()

        # Sprawdzamy, czy wszystkie zależności są w pliku
        assert "python=3.9" in content
        assert "numpy=1.22.0" in content
        assert "pandas>=1.4.0" in content
        assert "matplotlib>=3.5.0" in content
        assert "requests>=2.27.0" in content
        assert "pyyaml>=6.0" in content


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
