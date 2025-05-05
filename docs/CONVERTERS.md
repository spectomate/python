---
title: "Spectomate Converters"
description: "Documentation of available converters in Spectomate and how to create custom ones"
author: "Tom Sapletta"
keywords: "spectomate, converters, python, package management, pip, conda, poetry, custom converters"
lang: "en"
---

# Converters in Spectomate

## Introduction

Converters are a key element of Spectomate, responsible for transforming data between different package management formats. Each converter implements a common interface defined in the `BaseConverter` base class.

## Available Converters

### 1. CondaToPipConverter

Converter from conda format (environment.yml) to pip format (requirements.txt).

#### Usage

```python
from spectomate.converters.conda_to_pip import CondaToPipConverter

converter = CondaToPipConverter(
    source_file="environment.yml",
    target_file="requirements.txt"
)
result_path = converter.execute()
```

#### Implementation

The converter performs the following steps:
1. Reads the environment.yml file and parses it into an internal data format
2. Converts conda dependencies to pip format, removing channel specifications
3. Adds pip dependencies from the pip section in the environment.yml file
4. Saves the result to a requirements.txt file

### 2. PipToCondaConverter

Converter from pip format (requirements.txt) to conda format (environment.yml).

#### Usage

```python
from spectomate.converters.pip_to_conda import PipToCondaConverter

converter = PipToCondaConverter(
    source_file="requirements.txt",
    target_file="environment.yml",
    options={"env_name": "myproject"}
)
result_path = converter.execute()
```

#### Implementation

The converter performs the following steps:
1. Reads the requirements.txt file and parses it into an internal data format
2. Creates a basic structure for the environment.yml file with the environment name
3. Checks which packages are available in conda and which are only in pip
4. Adds conda packages to the dependencies section
5. Adds pip packages to the pip subsection in dependencies
6. Saves the result to an environment.yml file

### 3. PipToPoetryConverter

Converter from pip format (requirements.txt) to poetry format (pyproject.toml).

#### Usage

```python
from spectomate.converters.pip_to_poetry import PipToPoetryConverter

converter = PipToPoetryConverter(
    source_file="requirements.txt",
    target_file="pyproject.toml",
    options={"project_name": "myproject", "version": "0.1.0"}
)
result_path = converter.execute()
```

#### Implementation

The converter performs the following steps:
1. Reads the requirements.txt file and parses it into an internal data format
2. Filters actual dependencies, skipping comments and options
3. Creates a basic structure for the pyproject.toml file with the project name and version
4. Converts version specifications from pip format to poetry format
5. Saves the result to a pyproject.toml file

## Creating Custom Converters

To create your own converter, you need to:

1. Create a new class inheriting from `BaseConverter`
2. Implement the abstract methods:
   - `get_source_format()` - returns the source format identifier
   - `get_target_format()` - returns the target format identifier
   - `read_source()` - reads the source file
   - `convert()` - converts the data
   - `write_target()` - writes the data to the target file
3. Register the converter using the `@register_converter` decorator

### Example

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
        # Implementation of reading the source file
        pass
    
    def convert(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation of data conversion
        pass
    
    def write_target(self, target_data: Dict[str, Any]) -> Path:
        # Implementation of writing data to the target file
        pass
