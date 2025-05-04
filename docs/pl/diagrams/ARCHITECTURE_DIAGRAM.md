# Diagram Architektury Spectomate

Poniższy diagram przedstawia architekturę systemu Spectomate, pokazując główne komponenty i ich relacje.

```mermaid
classDiagram
    class BaseConverter {
        <<abstract>>
        +source_file: Path
        +target_file: Path
        +options: Dict
        +read_source() Dict
        +convert(source_data: Dict) Dict
        +write_target(target_data: Dict) Path
        +execute() Path
        +get_source_format()* str
        +get_target_format()* str
    }
    
    class ConverterRegistry {
        +register_converter(converter_class)
        +get_converter(source_format, target_format) BaseConverter
        +list_converters() List
    }
    
    class PipSchema {
        +parse_requirement(req_line) Dict
        +parse_file(file_path) Dict
        +generate_requirements_txt(data) str
        +write_requirements_txt(data, output_path) Path
    }
    
    class CondaSchema {
        +parse_file(file_path) Dict
        +extract_conda_dependencies(conda_data) List
        +extract_pip_dependencies(conda_data) List
        +generate_environment_yml(data) str
        +write_environment_yml(data, output_path) Path
    }
    
    class PoetrySchema {
        +parse_file(file_path) Dict
        +extract_dependencies(poetry_data, include_dev) List
        +generate_pyproject_toml(data) str
        +write_pyproject_toml(data, output_path) Path
        +convert_from_pip(pip_data, project_name, version) Dict
    }
    
    class CondaToPipConverter {
        +get_source_format() str
        +get_target_format() str
        +read_source() Dict
        +convert(source_data: Dict) Dict
        +write_target(target_data: Dict) Path
    }
    
    class PipToCondaConverter {
        +get_source_format() str
        +get_target_format() str
        +read_source() Dict
        +convert(source_data: Dict) Dict
        +write_target(target_data: Dict) Path
    }
    
    class PipToPoetryConverter {
        +get_source_format() str
        +get_target_format() str
        +read_source() Dict
        +convert(source_data: Dict) Dict
        +write_target(target_data: Dict) Path
    }
    
    BaseConverter <|-- CondaToPipConverter
    BaseConverter <|-- PipToCondaConverter
    BaseConverter <|-- PipToPoetryConverter
    
    ConverterRegistry --> BaseConverter : rejestruje
    
    CondaToPipConverter --> CondaSchema : używa
    CondaToPipConverter --> PipSchema : używa
    
    PipToCondaConverter --> PipSchema : używa
    PipToCondaConverter --> CondaSchema : używa
    
    PipToPoetryConverter --> PipSchema : używa
    PipToPoetryConverter --> PoetrySchema : używa
```

Diagram pokazuje hierarchię klas i relacje między nimi. `BaseConverter` jest klasą abstrakcyjną, z której dziedziczą wszystkie konwertery. Każdy konwerter korzysta z odpowiednich schematów danych do parsowania i generowania plików w różnych formatach. `ConverterRegistry` zarządza rejestracją i dostępem do konwerterów.
