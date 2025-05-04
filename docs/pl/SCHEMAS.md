# Schematy danych w Spectomate

## Wprowadzenie

Schematy danych w Spectomate definiują strukturę danych dla poszczególnych formatów zarządzania pakietami oraz dostarczają metody do parsowania i generowania plików w tych formatach. Są one kluczowym elementem umożliwiającym konwersję między różnymi formatami.

## Dostępne schematy

### 1. PipSchema

Schemat dla formatu pip (requirements.txt).

#### Metody

- `parse_requirement(req_line)` - parsuje pojedynczą linię z pliku requirements.txt
- `parse_file(file_path)` - parsuje cały plik requirements.txt
- `generate_requirements_txt(data)` - generuje zawartość pliku requirements.txt na podstawie danych
- `write_requirements_txt(data, output_path)` - zapisuje dane do pliku requirements.txt

#### Format danych

```python
{
    "format": "pip",
    "requirements": [
        # Może zawierać stringi (prosty format) lub słowniki (rozszerzony format)
        "numpy==1.22.0",
        "pandas>=1.4.0",
        # lub
        {
            "type": "package",
            "name": "numpy",
            "version_spec": {
                "operator": "==",
                "version": "1.22.0"
            }
        },
        {
            "type": "comment",
            "content": "# Komentarz"
        }
    ]
}
```

### 2. CondaSchema

Schemat dla formatu conda (environment.yml).

#### Metody

- `parse_file(file_path)` - parsuje plik environment.yml
- `extract_conda_dependencies(conda_data)` - wyodrębnia zależności conda
- `extract_pip_dependencies(conda_data)` - wyodrębnia zależności pip
- `generate_environment_yml(data)` - generuje zawartość pliku environment.yml
- `write_environment_yml(data, output_path)` - zapisuje dane do pliku environment.yml

#### Format danych

```python
{
    "format": "conda",
    "name": "myproject",
    "channels": ["conda-forge", "defaults"],
    "dependencies": [
        "python=3.9",
        "numpy=1.22.0",
        "pandas>=1.4.0",
        {"pip": ["requests>=2.27.0", "pyyaml>=6.0"]}
    ]
}
```

### 3. PoetrySchema

Schemat dla formatu poetry (pyproject.toml).

#### Metody

- `parse_file(file_path)` - parsuje plik pyproject.toml
- `extract_dependencies(poetry_data, include_dev)` - wyodrębnia zależności
- `generate_pyproject_toml(data)` - generuje zawartość pliku pyproject.toml
- `write_pyproject_toml(data, output_path)` - zapisuje dane do pliku pyproject.toml
- `convert_from_pip(pip_data, project_name, version)` - konwertuje dane z formatu pip do formatu poetry

#### Format danych

```python
{
    "format": "poetry",
    "name": "myproject",
    "version": "0.1.0",
    "description": "",
    "authors": ["Your Name <your.email@example.com>"],
    "readme": "README.md",
    "dependencies": {
        "python": "^3.9",
        "numpy": "==1.22.0",
        "pandas": ">=1.4.0"
    },
    "dev-dependencies": {
        "pytest": "^7.0.0"
    }
}
```

## Obsługa różnych formatów danych

Schematy danych w Spectomate są zaprojektowane, aby obsługiwać różne formaty i reprezentacje danych:

1. **Prosty format** - zależności jako stringi (np. "numpy==1.22.0")
2. **Rozszerzony format** - zależności jako słowniki z dodatkowymi metadanymi

Metody konwersji i parsowania są zaprojektowane tak, aby obsługiwać oba formaty, co zapewnia elastyczność i kompatybilność z różnymi narzędziami i bibliotekami.

## Tworzenie własnych schematów

Aby utworzyć własny schemat danych dla nowego formatu:

1. Utwórz nową klasę schematu z odpowiednimi metodami statycznymi
2. Zaimplementuj metody do parsowania plików w danym formacie
3. Zaimplementuj metody do generowania plików w danym formacie
4. Zdefiniuj strukturę danych wewnętrzną dla danego formatu

Następnie możesz utworzyć konwertery, które będą korzystać z nowego schematu do konwersji między nowym formatem a istniejącymi formatami.
