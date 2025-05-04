# update/

Skrypty do aktualizacji wersji, zarządzania zmianami i publikacji pakietu Spectomate.

## Zawartość
- `version.sh` — główny skrypt do aktualizacji wersji i publikacji pakietu
- `src.py` — skrypt do aktualizacji numeru wersji w plikach źródłowych
- `changelog.py` — skrypt do generowania i aktualizacji pliku CHANGELOG.md
- `git.sh` — skrypt do publikacji nowej wersji na GitHub
- `pypi.sh` — skrypt do publikacji pakietu na PyPI

## Użycie

Aby zaktualizować wersję i opublikować pakiet:

```bash
# Uruchom główny skrypt aktualizacji
bash update/version.sh
```

Skrypt wykona następujące operacje:
1. Utworzy i aktywuje środowisko wirtualne
2. Zaktualizuje numer wersji w plikach źródłowych
3. Wygeneruje wpis w CHANGELOG.md
4. Opublikuje zmiany na GitHub
5. Opublikuje pakiet na PyPI

## Rozwiązywanie problemów

Jeśli podczas publikacji na GitHub pojawi się błąd:
```
Updates were rejected because the remote contains work that you do not have locally
```

Należy wykonać `git pull` przed ponownym uruchomieniem skryptu:
```bash
git pull
bash update/version.sh
```

Jeśli tag już istnieje:
```
fatal: tag 'vX.Y.Z' already exists
```

Należy usunąć istniejący tag przed ponownym uruchomieniem skryptu:
```bash
git tag -d vX.Y.Z
git push origin --delete vX.Y.Z
bash update/version.sh
