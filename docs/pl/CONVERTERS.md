# Konwertery w Spectomate

## Wprowadzenie

Konwertery są kluczowym elementem Spectomate, odpowiedzialnym za transformację danych między różnymi formatami zarządzania pakietami. Każdy konwerter implementuje wspólny interfejs zdefiniowany w klasie bazowej `BaseConverter`.

## Dostępne konwertery

### 1. CondaToPipConverter

Konwerter z formatu conda (environment.yml) do formatu pip (requirements.txt).

#### Użycie

```python
from spectomate.converters.conda_to_pip import CondaToPipConverter

converter = CondaToPipConverter(
    source_file="environment.yml",
    target_file="requirements.txt"
)
result_path = converter.execute()
```

#### Implementacja

Konwerter wykonuje następujące kroki:
1. Odczytuje plik environment.yml i parsuje go do wewnętrznego formatu danych
2. Konwertuje zależności conda na format pip, usuwając specyfikacje kanałów
3. Dodaje zależności pip z sekcji pip w pliku environment.yml
4. Zapisuje wynik do pliku requirements.txt

### 2. PipToCondaConverter

Konwerter z formatu pip (requirements.txt) do formatu conda (environment.yml).

#### Użycie

```python
from spectomate.converters.pip_to_conda import PipToCondaConverter

converter = PipToCondaConverter(
    source_file="requirements.txt",
    target_file="environment.yml",
    options={"env_name": "myproject"}
)
result_path = converter.execute()
```

#### Implementacja

Konwerter wykonuje następujące kroki:
1. Odczytuje plik requirements.txt i parsuje go do wewnętrznego formatu danych
2. Tworzy podstawową strukturę pliku environment.yml z nazwą środowiska
3. Sprawdza, które pakiety są dostępne w conda, a które tylko w pip
4. Dodaje pakiety conda do sekcji dependencies
5. Dodaje pakiety pip do podsekcji pip w dependencies
6. Zapisuje wynik do pliku environment.yml

### 3. PipToPoetryConverter

Konwerter z formatu pip (requirements.txt) do formatu poetry (pyproject.toml).

#### Użycie

```python
from spectomate.converters.pip_to_poetry import PipToPoetryConverter

converter = PipToPoetryConverter(
    source_file="requirements.txt",
    target_file="pyproject.toml",
    options={"project_name": "myproject", "version": "0.1.0"}
)
result_path = converter.execute()
```

#### Implementacja

Konwerter wykonuje następujące kroki:
1. Odczytuje plik requirements.txt i parsuje go do wewnętrznego formatu danych
2. Filtruje rzeczywiste zależności, pomijając komentarze i opcje
3. Tworzy podstawową strukturę pliku pyproject.toml z nazwą projektu i wersją
4. Konwertuje specyfikacje wersji z formatu pip na format poetry
5. Zapisuje wynik do pliku pyproject.toml

## Tworzenie własnych konwerterów

Aby utworzyć własny konwerter, należy:

1. Utworzyć nową klasę dziedziczącą po `BaseConverter`
2. Zaimplementować metody abstrakcyjne:
   - `get_source_format()` - zwraca identyfikator formatu źródłowego
   - `get_target_format()` - zwraca identyfikator formatu docelowego
   - `read_source()` - odczytuje plik źródłowy
   - `convert()` - konwertuje dane
   - `write_target()` - zapisuje dane do pliku docelowego
3. Zarejestrować konwerter za pomocą dekoratora `@register_converter`

### Przykład

```python
from spectomate.core.base_converter import BaseConverter
from spectomate.core.registry import register_converter

@register_converter
class MyCustomConverter(BaseConverter):
    @staticmethod
    def get_source_format() -> str:
        return "format_a"
    
    @staticmethod
    def get_target_format() -> str:
        return "format_b"
    
    def read_source(self) -> Dict[str, Any]:
        # Implementacja odczytu pliku źródłowego
        pass
    
    def convert(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementacja konwersji danych
        pass
    
    def write_target(self, target_data: Dict[str, Any]) -> Path:
        # Implementacja zapisu danych do pliku docelowego
        pass
```
