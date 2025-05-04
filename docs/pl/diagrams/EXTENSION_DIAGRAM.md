# Diagram Rozszerzania Systemu Spectomate

Poniższy diagram przedstawia proces rozszerzania systemu Spectomate o nowe konwertery i formaty.

```mermaid
flowchart TD
    A[Identyfikacja potrzeby\nnowego konwertera] --> B[Implementacja nowego schematu\njako klasy SchemaXYZ]
    B --> C{Czy schemat\njuż istnieje?}
    C -->|Tak| D[Implementacja konwertera\ndziedziczącego po BaseConverter]
    C -->|Nie| E[Implementacja metod parsowania\ni generowania plików]
    E --> D
    D --> F[Implementacja metod\nget_source_format i get_target_format]
    F --> G[Implementacja metody read_source\nwykorzystującej schemat źródłowy]
    G --> H[Implementacja metody convert\ntransformującej dane]
    H --> I[Implementacja metody write_target\nwykorzystującej schemat docelowy]
    I --> J[Rejestracja konwertera\nza pomocą dekoratora @register_converter]
    J --> K[Testowanie konwertera\nw różnych scenariuszach]
    K --> L[Integracja z systemem\ni dokumentacja]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style J fill:#bfb,stroke:#333,stroke-width:2px
    style L fill:#fbf,stroke:#333,stroke-width:2px
```

Diagram przedstawia proces rozszerzania systemu Spectomate o nowe konwertery i formaty:

1. Identyfikacja potrzeby nowego konwertera (np. konwersja z formatu X do formatu Y)
2. Sprawdzenie, czy schematy dla formatów X i Y już istnieją
3. Jeśli nie, implementacja nowych schematów z metodami do parsowania i generowania plików
4. Implementacja nowego konwertera dziedziczącego po klasie BaseConverter
5. Implementacja wymaganych metod abstrakcyjnych
6. Rejestracja konwertera w systemie za pomocą dekoratora @register_converter
7. Testowanie i dokumentacja nowego konwertera
