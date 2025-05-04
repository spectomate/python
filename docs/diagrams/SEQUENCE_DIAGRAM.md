# Conversion Process Sequence Diagram in Spectomate

The following sequence diagram shows the interactions between system components during the conversion process from pip format to poetry format.

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
    CLI-->>User: Conversion completed successfully
```

The diagram shows the sequence of interactions between system components during the conversion from pip format to poetry format:

1. The user invokes the CLI command
2. The CLI retrieves the appropriate converter from the registry
3. The converter reads the source file and parses it using the pip schema
4. The converter transforms the data from pip format to poetry format
5. The converter generates the pyproject.toml file content and writes it to the target file
6. The CLI informs the user about the completion of the conversion
