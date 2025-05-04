# Architektura Spectomate

## Przegląd

Spectomate jest zbudowany na modułowej architekturze, która umożliwia łatwe rozszerzanie i dodawanie nowych konwerterów między różnymi formatami zarządzania pakietami w Pythonie.

## Kluczowe komponenty

### 1. Klasa bazowa `BaseConverter`

Wszystkie konwertery dziedziczą po klasie bazowej `BaseConverter`, która definiuje wspólny interfejs i podstawową funkcjonalność:

- `read_source()` - odczytuje plik źródłowy i konwertuje go na wewnętrzny format danych
- `convert()` - konwertuje dane z formatu źródłowego na format docelowy
- `write_target()` - zapisuje dane w formacie docelowym do pliku
- `execute()` - wykonuje pełny proces konwersji (odczyt, konwersja, zapis)
- `get_source_format()` - zwraca identyfikator formatu źródłowego
- `get_target_format()` - zwraca identyfikator formatu docelowego

### 2. Schematy danych

Każdy format ma swój schemat danych, który definiuje strukturę danych i metody do pracy z danym formatem:

- `PipSchema` - schemat dla formatu pip (requirements.txt)
- `CondaSchema` - schemat dla formatu conda (environment.yml)
- `PoetrySchema` - schemat dla formatu poetry (pyproject.toml)

### 3. Konwertery

Konwertery implementują logikę konwersji między różnymi formatami:

- `CondaToPipConverter` - konwersja z formatu conda do formatu pip
- `PipToCondaConverter` - konwersja z formatu pip do formatu conda
- `PipToPoetryConverter` - konwersja z formatu pip do formatu poetry

### 4. Rejestr konwerterów

System rejestracji konwerterów umożliwia dynamiczne odkrywanie i używanie dostępnych konwerterów:

- `register_converter` - dekorator do rejestracji konwertera
- `get_converter` - funkcja do pobierania konwertera na podstawie formatów źródłowego i docelowego
- `list_converters` - funkcja do listowania wszystkich dostępnych konwerterów

## Przepływ danych

1. Użytkownik wybiera format źródłowy i docelowy oraz ścieżki do plików
2. System wybiera odpowiedni konwerter na podstawie formatów
3. Konwerter odczytuje plik źródłowy za pomocą odpowiedniego schematu
4. Dane są konwertowane na format docelowy
5. Wynik jest zapisywany do pliku docelowego za pomocą odpowiedniego schematu

## Rozszerzanie systemu

Aby dodać nowy konwerter:

1. Utwórz nową klasę dziedziczącą po `BaseConverter`
2. Zaimplementuj metody `read_source()`, `convert()`, `write_target()`, `get_source_format()` i `get_target_format()`
3. Zarejestruj konwerter za pomocą dekoratora `@register_converter`

Aby dodać nowy format:

1. Utwórz nowy schemat danych z metodami do parsowania i generowania plików w danym formacie
2. Zaimplementuj konwertery między nowym formatem a istniejącymi formatami
