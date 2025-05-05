# Aktualizacja pakietu Spectomate

Ten dokument opisuje proces aktualizacji pakietu Spectomate, w tym zwiększanie numeru wersji, uruchamianie testów i publikację.

## Używanie komendy `update`

Pakiet Spectomate zawiera wbudowaną komendę `update`, która umożliwia łatwe aktualizowanie wersji pakietu i publikowanie go. Komenda ta jest dostępna po zainstalowaniu pakietu.

### Podstawowe użycie

```bash
# Uruchom pełną aktualizację z testami i publikacją
spectomate update
```

Domyślnie komenda `update` wykonuje następujące operacje:
1. Aktualizuje numer wersji w plikach źródłowych
2. Generuje wpis w pliku CHANGELOG.md
3. Uruchamia testy i sprawdzanie jakości kodu
4. Publikuje zmiany do GitHuba
5. Publikuje pakiet do PyPI

### Opcje komendy

Komenda `update` obsługuje następujące opcje:

- `--no-test` - pomija uruchamianie testów
- `--no-lint` - pomija sprawdzanie jakości kodu (linting)
- `--no-mypy` - pomija sprawdzanie typów mypy
- `--no-publish` - pomija publikację do GitHuba i PyPI
- `--verbose` - wyświetla szczegółowe informacje podczas aktualizacji

### Przykłady użycia

```bash
# Pełna aktualizacja z testami i publikacją
spectomate update

# Aktualizacja bez uruchamiania testów
spectomate update --no-test

# Aktualizacja bez sprawdzania jakości kodu
spectomate update --no-lint

# Aktualizacja bez sprawdzania typów mypy
spectomate update --no-mypy

# Aktualizacja bez publikacji
spectomate update --no-publish

# Aktualizacja z pominięciem testów i publikacji
spectomate update --no-test --no-publish

# Aktualizacja z pominięciem wszystkich testów
spectomate update --no-test --no-lint --no-mypy

# Aktualizacja z wyświetlaniem szczegółowych informacji
spectomate update --verbose
```

### Użycie w projektach zewnętrznych

Komenda `update` automatycznie wykrywa katalog projektu, w którym jest uruchamiana. Możesz używać jej w dowolnym projekcie, który korzysta z pakietu Spectomate:

```bash
cd /ścieżka/do/twojego/projektu
spectomate update --no-publish
```

Komenda wykryje katalog projektu na podstawie plików takich jak `pyproject.toml`, `setup.py` lub `.git`.

## Ręczne uruchamianie skryptów aktualizacji

Oprócz komendy `update`, można również ręcznie uruchamiać skrypty aktualizacji znajdujące się w katalogu `update`:

```bash
# Uruchom główny skrypt aktualizacji
bash update/version.sh

# Uruchom tylko testy
bash update/test.sh

# Uruchom testy z opcjami
bash update/test.sh --no-test  # Pomiń testy jednostkowe
bash update/test.sh --no-lint  # Pomiń sprawdzanie linterem
bash update/test.sh --fix      # Automatycznie napraw problemy z formatowaniem
```

## Rozwiązywanie problemów

### Błąd podczas publikacji do GitHuba

Jeśli podczas publikacji do GitHuba pojawi się błąd:
```
Updates were rejected because the remote contains work that you do not have locally
```

Należy wykonać `git pull` przed ponownym uruchomieniem skryptu:
```bash
git pull
spectomate update
```

### Tag już istnieje

Jeśli tag już istnieje:
```
fatal: tag 'vX.Y.Z' already exists
```

Należy usunąć istniejący tag przed ponownym uruchomieniem skryptu:
```bash
git tag -d vX.Y.Z
git push origin --delete vX.Y.Z
spectomate update
```
