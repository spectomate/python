# Spectomate Mypy Helper

The Spectomate Mypy Helper is a set of tools designed to help users identify and fix common mypy type checking issues. It provides both automated and interactive solutions to make working with mypy easier and more productive.

## Features

- **Analyze mypy errors**: Run mypy and get detailed analysis of issues with suggested fixes
- **Automatically fix common issues**: Apply automated fixes for common mypy problems
- **Generate type stubs**: Create stub files for modules with missing type annotations
- **Add type ignore comments**: Selectively add `# type: ignore` comments to problematic lines
- **Create mypy configuration**: Generate a customized mypy configuration file
- **MonkeyType integration**: Use runtime type collection to generate annotations

## Installation

The mypy helper is included with Spectomate. If you have Spectomate installed, you already have access to these tools.

```bash
pip install spectomate
```

## Usage

### Basic Commands

```bash
# Check a project for mypy issues
spectomate mypy check /path/to/project

# Try to fix common mypy issues
spectomate mypy fix /path/to/project

# Add type: ignore comments to problematic lines
spectomate mypy ignore /path/to/project

# Generate stub files for a module
spectomate mypy stubs module_name

# Use MonkeyType to generate type annotations
spectomate mypy monkeytype /path/to/script.py

# Create a mypy configuration file
spectomate mypy config /path/to/project
```

### Command Details

#### Check Command

The `check` command runs mypy on your project and provides detailed analysis of any issues found:

```bash
spectomate mypy check /path/to/project [OPTIONS]
```

Options:
- `--config, -c PATH`: Path to mypy config file
- `--strict`: Run mypy in strict mode
- `--verbose, -v`: Show verbose output with detailed suggestions

#### Fix Command

The `fix` command attempts to automatically fix common mypy issues:

```bash
spectomate mypy fix /path/to/project [OPTIONS]
```

Options:
- `--auto`: Automatically apply fixes where possible
- `--interactive, -i`: Interactively prompt for fixes (default)
- `--verbose, -v`: Show verbose output

#### Ignore Command

The `ignore` command adds `# type: ignore` comments to lines with mypy issues:

```bash
spectomate mypy ignore /path/to/project [OPTIONS]
```

Options:
- `--selective, -s`: Only add ignores for certain types of issues
- `--verbose, -v`: Show verbose output

#### Stubs Command

The `stubs` command generates stub files for modules:

```bash
spectomate mypy stubs MODULE_NAME [OPTIONS]
```

Options:
- `--output, -o PATH`: Output directory for stubs

#### MonkeyType Command

The `monkeytype` command uses runtime type collection to generate annotations:

```bash
spectomate mypy monkeytype SCRIPT_PATH [OPTIONS]
```

Options:
- `--module, -m MODULE`: Module name to apply types to
- `--apply`: Apply the generated types

#### Config Command

The `config` command creates a mypy configuration file:

```bash
spectomate mypy config DIRECTORY [OPTIONS]
```

Options:
- `--strict`: Enable strict mode
- `--ignore-missing-imports`: Ignore missing imports (default: True)
- `--disallow-untyped-defs`: Disallow untyped function definitions
- `--disallow-incomplete-defs`: Disallow incomplete function definitions

## Common Mypy Issues and Solutions

### Missing Imports

**Problem**: `Cannot find implementation or library stub for module named 'module_name'`

**Solutions**:
1. Install type stubs: `pip install types-module_name`
2. Generate stubs: `spectomate mypy stubs module_name`
3. Add `# type: ignore` comment: `spectomate mypy ignore /path/to/file.py --selective`
4. Configure mypy to ignore missing imports in `mypy.ini`:
   ```ini
   [mypy]
   ignore_missing_imports = True
   ```

### Missing Type Annotations

**Problem**: `Function is missing a return type annotation` or `Variable "x" is not annotated`

**Solutions**:
1. Add type annotations manually
2. Use MonkeyType to generate annotations: `spectomate mypy monkeytype /path/to/script.py --module your_module --apply`
3. Use the interactive fixer: `spectomate mypy fix /path/to/file.py --interactive`

### Incompatible Types

**Problem**: `Incompatible types in assignment (expression has type "Type1", variable has type "Type2")`

**Solutions**:
1. Fix the type mismatch
2. Use `typing.cast()` to explicitly cast types
3. Use `Union[Type1, Type2]` for variables that can have multiple types
4. Add a type check before assignment

### Optional and Union Access

**Problem**: `Item "None" of "Optional[Type]" has no attribute "x"`

**Solutions**:
1. Add a None check before accessing attributes
2. Use the `or` operator with a default value: `x or default_value`
3. Use conditional expressions: `x.attr if x is not None else default`

## Best Practices for Mypy

1. **Start with the basics**: Begin by adding type annotations to function signatures
2. **Use a gradual approach**: Enable mypy checks incrementally
3. **Create a mypy.ini file**: Configure mypy to match your project's needs
4. **Use type stubs for third-party libraries**: Install or create stubs for external dependencies
5. **Add type annotations to new code**: Make it a habit to add types to new code
6. **Use MonkeyType for existing code**: Generate annotations for legacy code
7. **Be selective with type: ignore**: Only use it when necessary and with specific error codes

## Advanced Usage

### Creating Custom Type Stubs

For third-party libraries without type stubs, you can create your own:

```bash
# Generate initial stubs
spectomate mypy stubs external_module -o ./stubs

# Edit the stubs to improve type information
# Add the stubs directory to your MYPYPATH
```

### Integrating with CI/CD

Add mypy checking to your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Type Check

on: [push, pull_request]

jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mypy
          pip install -e .
      - name: Run mypy
        run: mypy --ignore-missing-imports your_package
```

Spectomate includes a pre-configured GitHub Actions workflow in `.github/workflows/python-tests.yml` that runs mypy checks along with other tests. This workflow automatically runs on push to the main/master branch and on pull requests.

## Integration with Spectomate Test CLI

The mypy helper functionality is also integrated with the Spectomate test CLI, allowing you to run mypy checks as part of your testing workflow:

```bash
# Run mypy checks using the test CLI
spectomate test all

# Skip mypy checks if needed
spectomate test all --skip-mypy
```

For more information about the testing CLI, see the [Testing Guide](TESTING.md).

## Contributing

Contributions to the mypy helper are welcome! If you have ideas for new features or improvements, please open an issue or submit a pull request on GitHub.

## License

Spectomate is licensed under the MIT License. See the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **MonkeyType not working**: Ensure you have the module installed (`pip install monkeytype`)
2. **Stub generation failing**: Check if the module can be imported in your environment
3. **Auto-fixes not working**: Some issues require manual intervention
4. **Mypy not found**: Install mypy (`pip install mypy`)

### Getting Help

If you encounter any issues with the mypy helper tools, please:

1. Check the documentation
2. Run commands with `--verbose` for more information
3. Report issues on the Spectomate GitHub repository
