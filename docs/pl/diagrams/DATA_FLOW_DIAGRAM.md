# Diagram Przepływu Danych w Spectomate

Poniższy diagram przedstawia przepływ danych podczas procesu konwersji między różnymi formatami zarządzania pakietami.

```mermaid
flowchart TD
    A[Plik źródłowy\nrequirements.txt/environment.yml/pyproject.toml] --> B[BaseConverter.read_source]
    B --> C[Schemat źródłowy\nparse_file]
    C --> D[Wewnętrzny format danych\n{format, dependencies, ...}]
    D --> E[BaseConverter.convert]
    E --> F[Schemat docelowy\nkonwersja danych]
    F --> G[Wewnętrzny format danych\nw formacie docelowym]
    G --> H[BaseConverter.write_target]
    H --> I[Schemat docelowy\ngenerate_file]
    I --> J[Plik docelowy\nrequirements.txt/environment.yml/pyproject.toml]
    
    subgraph "Proces konwersji"
        B
        E
        H
    end
    
    subgraph "Schematy danych"
        C
        F
        I
    end
    
    subgraph "Dane"
        D
        G
    end
```

Diagram pokazuje, jak dane przepływają przez system Spectomate podczas procesu konwersji:

1. Plik źródłowy jest odczytywany przez metodę `read_source` konwertera
2. Dane są parsowane przez odpowiedni schemat źródłowy do wewnętrznego formatu danych
3. Metoda `convert` konwertera transformuje dane z formatu źródłowego na format docelowy
4. Schemat docelowy generuje zawartość pliku w formacie docelowym
5. Metoda `write_target` konwertera zapisuje dane do pliku docelowego
