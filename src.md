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