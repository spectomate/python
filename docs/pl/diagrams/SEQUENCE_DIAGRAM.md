# Diagram Sekwencji Procesu Konwersji w Spectomate

Poniższy diagram sekwencji pokazuje interakcje między komponentami systemu podczas procesu konwersji z formatu pip do formatu poetry.

```mermaid
sequenceDiagram
    actor User
    participant CLI
    participant Registry as ConverterRegistry
    participant Converter as PipToPoetryConverter
    participant PipSchema
    participant PoetrySchema
    participant FileSystem
    
    User->>CLI: spectomate -s pip -t poetry -i requirements.txt -o pyproject.toml
    CLI->>Registry: get_converter("pip", "poetry")
    Registry-->>CLI: PipToPoetryConverter
    CLI->>Converter: new(source_file, target_file, options)
    CLI->>Converter: execute()
    
    Converter->>Converter: read_source()
    Converter->>FileSystem: read requirements.txt
    FileSystem-->>Converter: file content
    Converter->>PipSchema: parse_file(requirements.txt)
    PipSchema-->>Converter: parsed data
    
    Converter->>Converter: convert(source_data)
    Converter->>PoetrySchema: convert_from_pip(pip_data, project_name, version)
    PoetrySchema-->>Converter: poetry data
    
    Converter->>Converter: write_target(target_data)
    Converter->>PoetrySchema: generate_pyproject_toml(data)
    PoetrySchema-->>Converter: pyproject.toml content
    Converter->>FileSystem: write pyproject.toml
    
    Converter-->>CLI: target_file path
    CLI-->>User: Konwersja zakończona pomyślnie
```

Diagram pokazuje sekwencję interakcji między komponentami systemu podczas konwersji z formatu pip do formatu poetry:

1. Użytkownik wywołuje polecenie CLI
2. CLI pobiera odpowiedni konwerter z rejestru
3. Konwerter odczytuje plik źródłowy i parsuje go za pomocą schematu pip
4. Konwerter konwertuje dane z formatu pip na format poetry
5. Konwerter generuje zawartość pliku pyproject.toml i zapisuje ją do pliku docelowego
6. CLI informuje użytkownika o zakończeniu konwersji
