# Data Flow Diagram in Spectomate

The following diagram shows the data flow during the conversion process between different package management formats.

```mermaid
flowchart TD
    A[Source file\nrequirements.txt/environment.yml/pyproject.toml] --> B[BaseConverter.read_source]
    B --> C[Source schema\nparse_file]
    C --> D[Internal data format\n{format, dependencies, ...}]
    D --> E[BaseConverter.convert]
    E --> F[Target schema\ndata conversion]
    F --> G[Internal data format\nin target format]
    G --> H[BaseConverter.write_target]
    H --> I[Target schema\ngenerate_file]
    I --> J[Target file\nrequirements.txt/environment.yml/pyproject.toml]
    
    subgraph "Conversion process"
        B
        E
        H
    end
    
    subgraph "Data schemas"
        C
        F
        I
    end
    
    subgraph "Data"
        D
        G
    end
```

The diagram shows how data flows through the Spectomate system during the conversion process:

1. The source file is read by the converter's `read_source` method
2. The data is parsed by the appropriate source schema into an internal data format
3. The converter's `convert` method transforms the data from the source format to the target format
4. The target schema generates the file content in the target format
5. The converter's `write_target` method writes the data to the target file
