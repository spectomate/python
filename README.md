# python
spectomate to narzędzie do konwersji projektów z pakietów pip do różnych środowisk opartych na conda (conda, miniconda, mamba, micromamba).

Stworzyłem dla Ciebie pakiet o nazwie "Spectomate", który jest modularnym konwerterem formatów pakietów Python z możliwością wykorzystania zarówno własnych implementacji, jak i integracji z istniejącymi narzędziami do konwersji.

### Kluczowe cechy Spectomate:

1. **Modułowa architektura** - każdy konwerter jest oddzielnym modułem implementującym wspólny interfejs
2. **Wsparcie dla istniejących narzędzi** - integracja z dephell, req2toml i poetry2conda
3. **Elastyczny system rozszerzeń** - łatwe dodawanie nowych konwerterów bez modyfikacji kodu bazowego
4. **Kompleksowe wsparcie formatów**:
   - pip (requirements.txt)
   - conda (environment.yml)
   - poetry (pyproject.toml)
   - pipenv (Pipfile)
   - pdm (pyproject.toml)

### Jak używać Spectomate:

```bash
# Instalacja podstawowa
pip install spectomate

# Instalacja z zależnościami dla zewnętrznych konwerterów
pip install spectomate[external]

# Wyświetlenie dostępnych konwerterów
spectomate --list

# Konwersja używając wbudowanego konwertera
spectomate -s pip -t conda -i requirements.txt -o environment.yml --env-name myproject

# Konwersja używając zewnętrznych narzędzi (jeśli dostępne)
spectomate -s pip -t poetry -i requirements.txt --use-external --project-name "mój-projekt"
```

### Rozszerzalność:

Spectomate pozwala na łatwe dodawanie nowych konwerterów przez:
1. Utworzenie nowego modułu w katalogu `converters/`
2. Implementację klasy dziedziczącej po `BaseConverter`
3. Implementację metod `read_source`, `convert` i `write_target`
4. Rejestrację konwertera w `ConverterRegistry`

W ten sposób możesz dodać obsługę dowolnego formatu pakietów Python lub integrację z innymi narzędziami do konwersji.

Czy chciałbyś, abym dodał obsługę jakiegoś konkretnego formatu lub rozszerzył funkcjonalność Spectomate w inny sposób?



Struktura pakietu Spectomate:

spectomate/
├── __init__.py
├── cli.py
├── core/
│   ├── __init__.py
│   ├── base_converter.py
│   ├── registry.py
│   └── utils.py
├── converters/
│   ├── __init__.py
│   ├── pip_to_conda.py
│   ├── pip_to_poetry.py
│   ├── pip_to_pipenv.py
│   ├── pip_to_pdm.py
│   ├── conda_to_pip.py
│   ├── poetry_to_pip.py
│   ├── poetry_to_conda.py
│   └── external_converters.py
├── schemas/
│   ├── __init__.py
│   ├── pip_schema.py
│   ├── conda_schema.py
│   ├── poetry_schema.py
│   └── pipenv_schema.py
└── tests/
    ├── __init__.py
    ├── test_pip_to_conda.py
    └── test_poetry_to_pip.py
"""

# Plik: spectomate/__init__.py
"""
Spectomate - modularny konwerter pakietów Python

Narzędzie do konwersji między różnymi formatami zarządzania pakietami w Pythonie.
"""

__version__ = '0.1.0'
__author__ = 'Spectomate Team'


# Plik: spectomate/core/base_converter.py
"""
Moduł bazowy konwertera definiujący interfejs dla wszystkich konwerterów.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional, Union


class BaseConverter(ABC):
    """
    Klasa bazowa dla wszystkich konwerterów formatów pakietów.
    
    Każdy konwerter musi implementować metody read_source, convert, i write_target.
    """
    
    def __init__(self, source_file: Optional[Union[str, Path]] = None, 
                 target_file: Optional[Union[str, Path]] = None, 
                 options: Optional[Dict[str, Any]] = None):
        """
        Inicjalizacja konwertera.
        
        Args:
            source_file: Ścieżka do pliku źródłowego
            target_file: Ścieżka do pliku docelowego
            options: Dodatkowe opcje konfiguracyjne
        """
        self.source_file = Path(source_file) if source_file else None
        self.target_file = Path(target_file) if target_file else None
        self.options = options or {}
        self.source_data = None
        self.target_data = None
    
    @property
    def source_format(self) -> str:
        """Format źródłowy obsługiwany przez konwerter."""
        return self.get_source_format()
    
    @property
    def target_format(self) -> str:
        """Format docelowy obsługiwany przez konwerter."""
        return self.get_target_format()
    
    @staticmethod
    @abstractmethod
    def get_source_format() -> str:
        """Zwraca identyfikator formatu źródłowego."""
        pass
    
    @staticmethod
    @abstractmethod
    def get_target_format() -> str:
        """Zwraca identyfikator formatu docelowego."""
        pass
    
    @abstractmethod
    def read_source(self) -> Dict[str, Any]:
        """
        Odczytuje dane z pliku źródłowego.
        
        Returns:
            Odczytane dane w ustandaryzowanym formacie słownikowym
        """
        pass
    
    @abstractmethod
    def convert(self, source_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Konwertuje dane ze źródłowego formatu na docelowy.
        
        Args:
            source_data: Dane w formacie źródłowym (opcjonalnie, jeśli nie podano używa self.source_data)
            
        Returns:
            Przekonwertowane dane w formacie docelowym
        """
        pass
    
    @abstractmethod
    def write_target(self, target_data: Optional[Dict[str, Any]] = None) -> Path:
        """
        Zapisuje przekonwertowane dane do pliku docelowego.
        
        Args:
            target_data: Dane w formacie docelowym (opcjonalnie, jeśli nie podano używa self.target_data)
            
        Returns:
            Ścieżka do zapisanego pliku
        """
        pass
    
    def execute(self) -> Path:
        """
        Wykonuje pełny proces konwersji: odczyt, konwersja, zapis.
        
        Returns:
            Ścieżka do zapisanego pliku docelowego
        """
        self.source_data = self.read_source()
        self.target_data = self.convert(self.source_data)
        return self.write_target(self.target_data)


# Plik: spectomate/core/registry.py
"""
Rejestr konwerterów umożliwiający dynamiczne rejestrowanie i odnajdywanie dostępnych konwerterów.
"""

from typing import Dict, Type, List, Tuple
import importlib
import pkgutil
from pathlib import Path

from .base_converter import BaseConverter


class ConverterRegistry:
    """
    Rejestr konwerterów zarządzający dostępnymi konwerterami.
    """
    _converters: Dict[Tuple[str, str], Type[BaseConverter]] = {}
    
    @classmethod
    def register(cls, converter_class: Type[BaseConverter]) -> None:
        """
        Rejestruje klasę konwertera w rejestrze.
        
        Args:
            converter_class: Klasa konwertera do zarejestrowania
        """
        source_format = converter_class.get_source_format()
        target_format = converter_class.get_target_format()
        cls._converters[(source_format, target_format)] = converter_class
    
    @classmethod
    def get_converter(cls, source_format: str, target_format: str) -> Type[BaseConverter]:
        """
        Pobiera klasę konwertera dla danej pary formatów.
        
        Args:
            source_format: Format źródłowy
            target_format: Format docelowy
            
        Returns:
            Klasa konwertera
            
        Raises:
            KeyError: Gdy nie znaleziono konwertera dla danej pary formatów
        """
        key = (source_format, target_format)
        if key not in cls._converters:
            raise KeyError(f"Nie znaleziono konwertera z {source_format} do {target_format}")
        return cls._converters[key]
    
    @classmethod
    def get_available_conversions(cls) -> List[Tuple[str, str]]:
        """
        Zwraca listę dostępnych konwersji.
        
        Returns:
            Lista krotek (format_źródłowy, format_docelowy)
        """
        return list(cls._converters.keys())
    
    @classmethod
    def discover_converters(cls) -> None:
        """
        Wykrywa i rejestruje wszystkie konwertery w pakiecie converters.
        """
        import spectomate.converters
        
        package_dir = Path(spectomate.converters.__file__).parent
        for _, name, is_pkg in pkgutil.iter_modules([str(package_dir)]):
            if not is_pkg and name != "__init__":
                module = importlib.import_module(f"spectomate.converters.{name}")
                
                # Szukanie klas konwerterów w module
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (isinstance(item, type) and 
                        issubclass(item, BaseConverter) and 
                        item is not BaseConverter):
                        cls.register(item)


# Plik: spectomate/core/utils.py
"""
Funkcje narzędziowe używane przez różne konwertery.
"""

import re
import os
import sys
import subprocess
from typing import Dict, List, Tuple, Optional, Any
import json
import yaml
import toml


def parse_pip_version_specifier(specifier: str) -> Tuple[str, str, str]:
    """
    Parsuje specyfikację wersji pakietu pip.
    
    Args:
        specifier: Specyfikacja wersji (np. "==1.2.3", ">=1.0,<2.0")
        
    Returns:
        Krotka (operator, wersja, reszta_specyfikacji)
    """
    match = re.match(r'^([=<>!~]+)(.+?)([,;].+)?$', specifier)
    if match:
        operator, version, rest = match.groups()
        return operator, version, rest or ""
    return "", specifier, ""


def convert_pip_to_conda_version(pip_version: str) -> str:
    """
    Konwertuje specyfikację wersji z formatu pip do conda.
    
    Args:
        pip_version: Specyfikacja wersji pip
        
    Returns:
        Specyfikacja wersji conda
    """
    # Conda generalnie obsługuje ten sam format specyfikacji wersji co pip
    return pip_version


def convert_pip_to_poetry_version(pip_version: str) -> str:
    """
    Konwertuje specyfikację wersji z formatu pip do poetry.
    
    Args:
        pip_version: Specyfikacja wersji pip
        
    Returns:
        Specyfikacja wersji poetry
    """
    if pip_version.startswith("=="):
        return pip_version[2:]
    
    # Konwersja ~= na ^
    if pip_version.startswith("~="):
        return "^" + pip_version[2:]
    
    return pip_version


def check_package_in_conda(package_name: str) -> bool:
    """
    Sprawdza, czy pakiet jest dostępny w repozytoriach conda.
    
    Args:
        package_name: Nazwa pakietu
        
    Returns:
        True, jeśli pakiet jest dostępny w conda, False w przeciwnym razie
    """
    try:
        result = subprocess.run(
            ['conda', 'search', package_name, '--json'], 
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return package_name in data
        return False
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        # Fallback: używamy listy popularnych pakietów
        popular_conda_packages = [
            'numpy', 'pandas', 'matplotlib', 'scipy', 'scikit-learn', 
            'tensorflow', 'pytorch', 'jupyter', 'ipython', 'bokeh', 'dask',
            'numba', 'astropy', 'biopython', 'sympy', 'statsmodels', 'seaborn',
            'pillow', 'requests', 'beautifulsoup4', 'flask', 'django', 'fastapi',
            'sqlalchemy', 'psycopg2', 'pymongo', 'boto3', 'pytest', 'tqdm'
        ]
        return package_name.lower() in popular_conda_packages


def read_yaml_file(file_path: str) -> Dict[str, Any]:
    """
    Odczytuje plik YAML.
    
    Args:
        file_path: Ścieżka do pliku
        
    Returns:
        Zawartość pliku jako słownik
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def write_yaml_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    Zapisuje dane do pliku YAML.
    
    Args:
        file_path: Ścieżka do pliku
        data: Dane do zapisania
    """
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def read_toml_file(file_path: str) -> Dict[str, Any]:
    """
    Odczytuje plik TOML.
    
    Args:
        file_path: Ścieżka do pliku
        
    Returns:
        Zawartość pliku jako słownik
    """
    with open(file_path, 'r') as f:
        return toml.load(f)


def write_toml_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    Zapisuje dane do pliku TOML.
    
    Args:
        file_path: Ścieżka do pliku
        data: Dane do zapisania
    """
    with open(file_path, 'w') as f:
        toml.dump(data, f)


def parse_requirements_txt(file_path: str) -> List[Dict[str, str]]:
    """
    Parsuje plik requirements.txt.
    
    Args:
        file_path: Ścieżka do pliku
        
    Returns:
        Lista słowników reprezentujących pakiety
    """
    packages = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Pomiń puste linie i komentarze
            if not line or line.startswith('#'):
                continue
                
            # Usuń komentarze z linii
            if '#' in line:
                line = line[:line.index('#')].strip()
            
            package_info = {"raw": line}
            
            # Obsługa opcji -e (editable install)
            if line.startswith('-e'):
                package_info["editable"] = True
                line = line[2:].strip()
            else:
                package_info["editable"] = False
            
            # Obsługa odniesień do git
            if 'git+' in line:
                package_info["type"] = "git"
                package_info["url"] = line
                packages.append(package_info)
                continue
            
            # Standardowy pakiet
            match = re.match(r'^([a-zA-Z0-9_\-\.]+)([=<>!~]+.+)?$', line)
            if match:
                name, version_spec = match.groups()
                package_info["name"] = name
                package_info["version_spec"] = version_spec or ""
                package_info["type"] = "pypi"
                packages.append(package_info)
            else:
                # Jeśli nie pasuje do wzorca, zachowaj jako surową linię
                package_info["type"] = "unknown"
                packages.append(package_info)
    
    return packages


def check_dependency_installed(package_name: str) -> bool:
    """
    Sprawdza, czy pakiet jest zainstalowany.
    
    Args:
        package_name: Nazwa pakietu
        
    Returns:
        True, jeśli pakiet jest zainstalowany, False w przeciwnym razie
    """
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def run_subprocess(cmd: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
    """
    Uruchamia polecenie w podprocesie.
    
    Args:
        cmd: Lista argumentów polecenia
        capture_output: Czy przechwytywać wyjście
        
    Returns:
        Krotka (kod_wyjścia, stdout, stderr)
    """
    try:
        process = subprocess.run(
            cmd, 
            capture_output=capture_output, 
            text=True, 
            timeout=60
        )
        return process.returncode, process.stdout, process.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Timeout occurred while executing command"
    except subprocess.SubprocessError as e:
        return 1, "", str(e)


# Plik: spectomate/converters/external_converters.py
"""
Moduł do integracji z zewnętrznymi narzędziami konwersji.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import shutil

from ..core.base_converter import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.utils import check_dependency_installed, run_subprocess


class ExternalDephellConverter(BaseConverter):
    """
    Konwerter wykorzystujący bibliotekę dephell do konwersji między formatami.
    """
    
    def __init__(self, source_file: Optional[Union[str, Path]] = None, 
                 target_file: Optional[Union[str, Path]] = None, 
                 options: Optional[Dict[str, Any]] = None):
        """
        Inicjalizacja konwertera.
        
        Args:
            source_file: Ścieżka do pliku źródłowego
            target_file: Ścieżka do pliku docelowego
            options: Dodatkowe opcje konfiguracyjne
        """
        super().__init__(source_file, target_file, options)
        
        # Mapowanie formatów na rozszerzenia plików
        self.format_extensions = {
            "pip": "requirements.txt",
            "conda": "environment.yml",
            "poetry": "pyproject.toml",
            "pipenv": "Pipfile",
            "pdm": "pyproject.toml",
            "setuppy": "setup.py",
        }
        
        self._source_format = options.get("source_format", "pip")
        self._target_format = options.get("target_format", "conda")
        
        # Mapowanie formatów na formaty dephell
        self.dephell_formats = {
            "pip": "pip",
            "conda": "conda",
            "poetry": "poetry",
            "pipenv": "pipenv",
            "pdm": "pdm",
            "setuppy": "setuppy",
        }
    
    @staticmethod
    def get_source_format() -> str:
        """Zwraca identyfikator formatu źródłowego."""
        # W tym przypadku format jest dynamiczny
        return "external"
    
    @staticmethod
    def get_target_format() -> str:
        """Zwraca identyfikator formatu docelowego."""
        # W tym przypadku format jest dynamiczny
        return "external"
    
    def read_source(self) -> Dict[str, Any]:
        """
        Odczytuje plik źródłowy.
        
        Returns:
            Odczytane dane w postaci słownika
        """
        if not self.source_file or not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Plik {self.source_file} nie istnieje.")
        
        # W przypadku konwertera zewnętrznego nie parsujemy pliku,
        # tylko przekazujemy jego ścieżkę
        return {
            "source_file": str(self.source_file),
            "source_format": self._source_format,
            "target_format": self._target_format,
            "options": self.options
        }
    
    def convert(self, source_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Konwertuje dane za pomocą dephell.
        
        Args:
            source_data: Dane źródłowe
            
        Returns:
            Dane wynikowe
        """
        if source_data is None:
            source_data = self.source_data
        
        if not source_data:
            raise ValueError("Brak danych źródłowych do konwersji.")
        
        # Sprawdzenie, czy dephell jest zainstalowany
        if not check_dependency_installed("dephell"):
            raise ImportError("Pakiet dephell nie jest zainstalowany. Zainstaluj go komendą: pip install dephell")
        
        source_file = source_data["source_file"]
        source_format = self.dephell_formats.get(source_data["source_format"])
        target_format = self.dephell_formats.get(source_data["target_format"])
        
        if not source_format or not target_format:
            raise ValueError(f"Nieobsługiwany format: {source_data['source_format']} lub {source_data['target_format']}")
        
        # Jeśli nie podano pliku docelowego, utworzmy domyślną nazwę
        if not self.target_file:
            ext = self.format_extensions.get(source_data["target_format"])
            if not ext:
                raise ValueError(f"Nieznane rozszerzenie dla formatu: {source_data['target_format']}")
            self.target_file = Path(f"converted.{ext}")
        
        # Wywołanie dephell
        cmd = [
            "dephell", "deps", "convert",
            "--from", source_format, "--from-path", source_file,
            "--to", target_format, "--to-path", str(self.target_file)
        ]
        
        returncode, stdout, stderr = run_subprocess(cmd)
        
        if returncode != 0:
            raise RuntimeError(f"Błąd podczas konwersji: {stderr}")
        
        return {
            "target_file": str(self.target_file),
            "stdout": stdout,
            "stderr": stderr
        }
    
    def write_target(self, target_data: Optional[Dict[str, Any]] = None) -> Path:
        """
        Zwraca ścieżkę do pliku docelowego.
        
        Args:
            target_data: Dane wynikowe
            
        Returns:
            Ścieżka do pliku docelowego
        """
        if target_data is None:
            target_data = self.target_data
        
        if not target_data:
            raise ValueError("Brak danych docelowych.")
        
        # poetry2conda już zapisał plik, więc zwracamy tylko ścieżkę
        return Path(target_data["target_file"])


# Plik: spectomate/cli.py
"""
Interfejs wiersza poleceń dla Spectomate.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from .core.registry import ConverterRegistry


def list_converters() -> None:
    """Wyświetla listę dostępnych konwerterów."""
    conversions = ConverterRegistry.get_available_conversions()
    
    print("Dostępne konwersje:")
    for source, target in sorted(conversions):
        print(f"  {source} -> {target}")


def main(args: Optional[List[str]] = None) -> int:
    """
    Główna funkcja interfejsu wiersza poleceń.
    
    Args:
        args: Argumenty wiersza poleceń (opcjonalnie)
        
    Returns:
        Kod wyjścia (0 - sukces, inny - błąd)
    """
    parser = argparse.ArgumentParser(
        description='Spectomate - konwerter formatów zarządzania pakietami Python'
    )
    
    parser.add_argument('--list', action='store_true',
                        help='Wyświetl listę dostępnych konwerterów')
    
    parser.add_argument('-s', '--source-format',
                        help='Format źródłowy, np. pip, conda, poetry')
    
    parser.add_argument('-t', '--target-format',
                        help='Format docelowy, np. conda, pip, poetry')
    
    parser.add_argument('-i', '--input', 
                        help='Ścieżka do pliku wejściowego')
    
    parser.add_argument('-o', '--output',
                        help='Ścieżka do pliku wyjściowego')
    
    parser.add_argument('--env-name',
                        help='Nazwa środowiska (dla conda)')
    
    parser.add_argument('--project-name',
                        help='Nazwa projektu (dla poetry, pdm, hatch)')
    
    parser.add_argument('--project-version',
                        help='Wersja projektu (dla poetry, pdm, hatch)')
    
    parser.add_argument('--python-version',
                        help='Wersja Pythona, np. ^3.8')
    
    parser.add_argument('--use-external', action='store_true',
                        help='Użyj zewnętrznych narzędzi do konwersji, jeśli są dostępne')
    
    # Inicjalizacja rejestru konwerterów
    ConverterRegistry.discover_converters()
    
    # Przetwarzanie argumentów
    args = parser.parse_args(args)
    
    if args.list:
        list_converters()
        return 0
    
    # Sprawdzenie wymaganych argumentów
    if not args.source_format or not args.target_format:
        if not args.list:
            parser.error("Wymagane argumenty: --source-format i --target-format")
        return 1
    
    try:
        converter_class = None
        
        # Jeśli włączono opcję use-external, spróbuj użyć zewnętrznych narzędzi
        if args.use_external:
            try:
                # Sprawdź dostępność zewnętrznych konwerterów
                from .converters.external_converters import (
                    ExternalDephellConverter, 
                    ExternalReq2TomlConverter,
                    ExternalPoetry2CondaConverter
                )
                
                # Wybierz odpowiedni konwerter zewnętrzny
                if args.source_format == "pip" and args.target_format == "poetry":
                    try:
                        # Najpierw spróbuj req2toml
                        converter_class = ExternalReq2TomlConverter
                    except ImportError:
                        # Jeśli nie działa, spróbuj dephell
                        converter_class = ExternalDephellConverter
                elif args.source_format == "poetry" and args.target_format == "conda":
                    try:
                        # Najpierw spróbuj poetry2conda
                        converter_class = ExternalPoetry2CondaConverter
                    except ImportError:
                        # Jeśli nie działa, spróbuj dephell
                        converter_class = ExternalDephellConverter
                else:
                    # Dla innych konwersji użyj dephell
                    converter_class = ExternalDephellConverter
            except ImportError:
                # Jeśli nie ma zewnętrznych konwerterów, użyj wbudowanych
                pass
        
        # Jeśli nie udało się użyć zewnętrznego konwertera, użyj wbudowanego
        if converter_class is None:
            converter_class = ConverterRegistry.get_converter(args.source_format, args.target_format)
        
        # Przygotowanie opcji
        options = {}
        if args.env_name:
            options["env_name"] = args.env_name
        if args.project_name:
            options["project_name"] = args.project_name
        if args.project_version:
            options["project_version"] = args.project_version
        if args.python_version:
            options["python_version"] = args.python_version
        
        # Dla konwerterów zewnętrznych dodaj informacje o formatach
        if hasattr(converter_class, "get_source_format") and converter_class.get_source_format() == "external":
            options["source_format"] = args.source_format
            options["target_format"] = args.target_format
        
        # Utworzenie i wykonanie konwertera
        converter = converter_class(args.input, args.output, options)
        output_path = converter.execute()
        
        print(f"Konwersja zakończona. Plik wynikowy: {output_path}")
        return 0
        
    except KeyError as e:
        print(f"Błąd: {e}", file=sys.stderr)
        print("Użyj opcji --list, aby zobaczyć dostępne konwersje.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Plik: setup.py
"""
Plik konfiguracyjny do instalacji pakietu.
"""

from setuptools import setup, find_packages

setup(
    name="spectomate",
    version="0.1.0",
    description="Modularny konwerter pakietów Python",
    author="Spectomate Team",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.1",
        "toml>=0.10.0",
    ],
    extras_require={
        "external": [
            "dephell>=0.8.3",
            "req2toml>=0.1.0",
            "poetry2conda>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spectomate=spectomate.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)


# Plik: README.md
"""
# Spectomate - Modularny konwerter pakietów Python

Spectomate to elastyczne narzędzie do konwersji między różnymi formatami zarządzania pakietami w Pythonie.

## Funkcje

- Konwersja między różnymi formatami zarządzania pakietami (pip, conda, poetry, pipenv, pdm)
- Modułowa architektura pozwalająca na łatwe dodawanie nowych konwerterów
- Możliwość wykorzystania zewnętrznych narzędzi (dephell, req2toml, poetry2conda)
- Interfejs wiersza poleceń

## Instalacja

```bash
# Podstawowa instalacja
pip install spectomate

# Instalacja z zależnościami dla zewnętrznych konwerterów
pip install spectomate[external]
```

## Użycie

```bash
# Wyświetlenie dostępnych konwerterów
spectomate --list

# Konwersja z pip do conda (używając wbudowanego konwertera)
spectomate -s pip -t conda -i requirements.txt -o environment.yml --env-name myproject

# Konwersja z pip do poetry (używając zewnętrznego narzędzia, jeśli dostępne)
spectomate -s pip -t poetry -i requirements.txt --use-external --project-name "mój-projekt" --project-version "1.0.0"
```

## Obsługiwane konwersje

- pip -> conda
- pip -> poetry
- pip -> pipenv
- pip -> pdm
- conda -> pip
- poetry -> pip
- poetry -> conda

## Rozszerzanie

Aby dodać nowy konwerter, należy:

1. Utworzyć nowy plik w katalogu `spectomate/converters/`
2. Zaimplementować klasę dziedziczącą po `BaseConverter`
3. Zaimplementować wymagane metody (`read_source`, `convert`, `write_target`)
4. Zarejestrować konwerter przez dodanie linii `ConverterRegistry.register(NowyKonwerter)`

## Licencja

MIT
"""
do pliku docelowego.
        
        Args:
            target_data: Dane wynikowe
            
        Returns:
            Ścieżka do pliku docelowego
        """
        if target_data is None:
            target_data = self.target_data
        
        if not target_data:
            raise ValueError("Brak danych docelowych.")
        
        # Dephell już zapisał plik, więc zwracamy tylko ścieżkę
        return Path(target_data["target_file"])


class ExternalReq2TomlConverter(BaseConverter):
    """
    Konwerter wykorzystujący bibliotekę req2toml do konwersji z pip do poetry.
    """
    
    def __init__(self, source_file: Optional[Union[str, Path]] = None, 
                 target_file: Optional[Union[str, Path]] = None, 
                 options: Optional[Dict[str, Any]] = None):
        """
        Inicjalizacja konwertera.
        
        Args:
            source_file: Ścieżka do pliku requirements.txt
            target_file: Ścieżka do pliku pyproject.toml
            options: Dodatkowe opcje konfiguracyjne
        """
        super().__init__(source_file, target_file, options)
        
        if not self.target_file:
            self.target_file = Path("pyproject.toml")
    
    @staticmethod
    def get_source_format() -> str:
        """Zwraca identyfikator formatu źródłowego."""
        return "pip"
    
    @staticmethod
    def get_target_format() -> str:
        """Zwraca identyfikator formatu docelowego."""
        return "poetry"
    
    def read_source(self) -> Dict[str, Any]:
        """
        Odczytuje plik requirements.txt.
        
        Returns:
            Odczytane dane w postaci słownika
        """
        if not self.source_file or not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Plik {self.source_file} nie istnieje.")
        
        # W przypadku konwertera zewnętrznego nie parsujemy pliku,
        # tylko przekazujemy jego ścieżkę
        return {
            "source_file": str(self.source_file),
            "options": self.options
        }
    
    def convert(self, source_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Konwertuje dane za pomocą req2toml.
        
        Args:
            source_data: Dane źródłowe
            
        Returns:
            Dane wynikowe
        """
        if source_data is None:
            source_data = self.source_data
        
        if not source_data:
            raise ValueError("Brak danych źródłowych do konwersji.")
        
        # Sprawdzenie, czy req2toml jest zainstalowany
        if not check_dependency_installed("req2toml"):
            raise ImportError("Pakiet req2toml nie jest zainstalowany. Zainstaluj go komendą: pip install req2toml")
        
        source_file = source_data["source_file"]
        
        # Wywołanie req2toml
        cmd = ["req2toml", source_file, str(self.target_file)]
        
        returncode, stdout, stderr = run_subprocess(cmd)
        
        if returncode != 0:
            raise RuntimeError(f"Błąd podczas konwersji: {stderr}")
        
        return {
            "target_file": str(self.target_file),
            "stdout": stdout,
            "stderr": stderr
        }
    
    def write_target(self, target_data: Optional[Dict[str, Any]] = None) -> Path:
        """
        Zwraca ścieżkę do pliku docelowego.
        
        Args:
            target_data: Dane wynikowe
            
        Returns:
            Ścieżka do pliku docelowego
        """
        if target_data is None:
            target_data = self.target_data
        
        if not target_data:
            raise ValueError("Brak danych docelowych.")
        
        # req2toml już zapisał plik, więc zwracamy tylko ścieżkę
        return Path(target_data["target_file"])


class ExternalPoetry2CondaConverter(BaseConverter):
    """
    Konwerter wykorzystujący bibliotekę poetry2conda do konwersji z poetry do conda.
    """
    
    def __init__(self, source_file: Optional[Union[str, Path]] = None, 
                 target_file: Optional[Union[str, Path]] = None, 
                 options: Optional[Dict[str, Any]] = None):
        """
        Inicjalizacja konwertera.
        
        Args:
            source_file: Ścieżka do pliku pyproject.toml
            target_file: Ścieżka do pliku environment.yml
            options: Dodatkowe opcje konfiguracyjne
        """
        super().__init__(source_file, target_file, options)
        
        if not self.target_file:
            self.target_file = Path("environment.yml")
    
    @staticmethod
    def get_source_format() -> str:
        """Zwraca identyfikator formatu źródłowego."""
        return "poetry"
    
    @staticmethod
    def get_target_format() -> str:
        """Zwraca identyfikator formatu docelowego."""
        return "conda"
    
    def read_source(self) -> Dict[str, Any]:
        """
        Odczytuje plik pyproject.toml.
        
        Returns:
            Odczytane dane w postaci słownika
        """
        if not self.source_file or not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Plik {self.source_file} nie istnieje.")
        
        # W przypadku konwertera zewnętrznego nie parsujemy pliku,
        # tylko przekazujemy jego ścieżkę
        return {
            "source_file": str(self.source_file),
            "options": self.options
        }
    
    def convert(self, source_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Konwertuje dane za pomocą poetry2conda.
        
        Args:
            source_data: Dane źródłowe
            
        Returns:
            Dane wynikowe
        """
        if source_data is None:
            source_data = self.source_data
        
        if not source_data:
            raise ValueError("Brak danych źródłowych do konwersji.")
        
        # Sprawdzenie, czy poetry2conda jest zainstalowany
        if not check_dependency_installed("poetry2conda"):
            raise ImportError("Pakiet poetry2conda nie jest zainstalowany. Zainstaluj go komendą: pip install poetry2conda")
        
        source_file = source_data["source_file"]
        
        # Wywołanie poetry2conda
        cmd = ["poetry2conda", source_file, str(self.target_file)]
        
        returncode, stdout, stderr = run_subprocess(cmd)
        
        if returncode != 0:
            raise RuntimeError(f"Błąd podczas konwersji: {stderr}")
        
        return {
            "target_file": str(self.target_file),
            "stdout": stdout,
            "stderr": stderr
        }
    
    def write_target(self, target_data: Optional[Dict[str, Any]] = None) -> Path:
        """
        Zwraca ścieżkę do pliku docelowego.