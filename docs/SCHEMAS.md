---
title: "Spectomate Data Schemas"
description: "Documentation of data schemas used in Spectomate for different package management formats"
author: "Spectomate Team"
keywords: "spectomate, data schemas, python, package management, pip, conda, poetry, requirements.txt, environment.yml, pyproject.toml"
lang: "en"
---

# Data Schemas in Spectomate

## Introduction

Data schemas in Spectomate define the data structure for individual package management formats and provide methods for parsing and generating files in these formats. They are a key element enabling conversion between different formats.

## Available Schemas

### 1. PipSchema

Schema for pip format (requirements.txt).

#### Methods

- `parse_requirement(req_line)` - parses a single line from a requirements.txt file
- `parse_file(file_path)` - parses an entire requirements.txt file
- `generate_requirements_txt(data)` - generates the content of a requirements.txt file based on data
- `write_requirements_txt(data, output_path)` - writes data to a requirements.txt file

#### Data Format

```python
{
    "format": "pip",
    "requirements": [
        # Can contain strings (simple format) or dictionaries (extended format)
        "numpy==1.22.0",
        "pandas>=1.4.0",
        # or
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
            "content": "# Comment"
        }
    ]
}
```

### 2. CondaSchema

Schema for conda format (environment.yml).

#### Methods

- `parse_file(file_path)` - parses an environment.yml file
- `extract_conda_dependencies(conda_data)` - extracts conda dependencies
- `extract_pip_dependencies(conda_data)` - extracts pip dependencies
- `generate_environment_yml(data)` - generates the content of an environment.yml file
- `write_environment_yml(data, output_path)` - writes data to an environment.yml file

#### Data Format

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

Schema for poetry format (pyproject.toml).

#### Methods

- `parse_file(file_path)` - parses a pyproject.toml file
- `extract_dependencies(poetry_data, include_dev)` - extracts dependencies
- `generate_pyproject_toml(data)` - generates the content of a pyproject.toml file
- `write_pyproject_toml(data, output_path)` - writes data to a pyproject.toml file
- `convert_from_pip(pip_data, project_name, version)` - converts data from pip format to poetry format

#### Data Format

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

## Handling Different Data Formats

Data schemas in Spectomate are designed to handle different formats and data representations:

1. **Simple format** - dependencies as strings (e.g., "numpy==1.22.0")
2. **Extended format** - dependencies as dictionaries with additional metadata

Conversion and parsing methods are designed to handle both formats, providing flexibility and compatibility with various tools and libraries.

## Creating Custom Schemas

To create your own data schema for a new format:

1. Create a new schema class with appropriate static methods
2. Implement methods for parsing files in that format
3. Implement methods for generating files in that format
4. Define the internal data structure for that format

You can then create converters that will use the new schema to convert between the new format and existing formats.
