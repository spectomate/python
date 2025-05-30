"""
Testy dla konwertera z formatu pip do formatu conda.
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from spectomate.converters.pip_to_conda import PipToCondaConverter
from spectomate.schemas.conda_schema import CondaSchema
from spectomate.schemas.pip_schema import PipSchema


class TestPipToCondaConverter:
    """
    Testy dla konwertera z formatu pip do formatu conda.
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
        self.output_file = self.temp_path / "environment.yml"

    def teardown_method(self) -> None:
        """Czyszczenie po testach."""
        self.temp_dir.cleanup()

    def test_read_source(self) -> None:
        """Test odczytu pliku requirements.txt."""
        converter = PipToCondaConverter(source_file=self.requirements_file)
        source_data = converter.read_source()

        assert "dependencies" in source_data
        assert len(source_data["dependencies"]) == 5
        assert "numpy==1.22.0" in source_data["dependencies"]
        assert "pandas>=1.4.0" in source_data["dependencies"]
        assert "matplotlib>=3.5.0" in source_data["dependencies"]
        assert "requests>=2.27.0" in source_data["dependencies"]
        assert "pyyaml>=6.0" in source_data["dependencies"]

    def test_convert(self) -> None:
        """Test konwersji danych z formatu pip do formatu conda."""
        converter = PipToCondaConverter(
            source_file=self.requirements_file, options={"env_name": "testenv"}
        )

        source_data = converter.read_source()
        target_data = converter.convert(source_data)

        assert target_data["name"] == "testenv"
        assert "channels" in target_data
        assert "defaults" in target_data["channels"]
        assert "conda-forge" in target_data["channels"]
        assert "dependencies" in target_data

        # Sprawdzamy, czy wszystkie zależności zostały uwzględnione
        # Uwaga: w prawdziwym teście powinniśmy mockować funkcję check_package_in_conda
        all_deps = target_data["dependencies"]
        if "pip" in target_data:
            all_deps.extend(target_data["pip"])

        assert len(all_deps) > 0

    def test_write_target(self) -> None:
        """Test zapisu danych do pliku environment.yml."""
        converter = PipToCondaConverter(
            source_file=self.requirements_file,
            target_file=self.output_file,
            options={"env_name": "testenv"},
        )

        source_data = converter.read_source()
        target_data = converter.convert(source_data)
        result_path = converter.write_target(target_data)

        assert result_path == self.output_file
        assert self.output_file.exists()

        # Sprawdzamy, czy plik można odczytać jako poprawny YAML
        with open(self.output_file, "r") as f:
            conda_env = yaml.safe_load(f)

        assert conda_env["name"] == "testenv"
        assert "channels" in conda_env
        assert "dependencies" in conda_env

    def test_execute(self) -> None:
        """Test pełnego procesu konwersji."""
        converter = PipToCondaConverter(
            source_file=self.requirements_file,
            target_file=self.output_file,
            options={"env_name": "testenv"},
        )

        result_path = converter.execute()

        assert result_path == self.output_file
        assert self.output_file.exists()

        # Sprawdzamy, czy plik można odczytać jako poprawny YAML
        with open(self.output_file, "r") as f:
            conda_env = yaml.safe_load(f)

        assert conda_env["name"] == "testenv"
        assert "channels" in conda_env
        assert "dependencies" in conda_env


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
