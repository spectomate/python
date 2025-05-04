#!/bin/bash
# Przykłady użycia interfejsu wiersza poleceń Spectomate

# Wyświetlanie pomocy
echo "=== Wyświetlanie pomocy ==="
python -m spectomate.cli --help

# Wyświetlanie dostępnych formatów i konwerterów
echo -e "\n=== Wyświetlanie dostępnych formatów i konwerterów ==="
python -m spectomate.cli list-formats

# Tworzenie przykładowego pliku requirements.txt
echo -e "\n=== Tworzenie przykładowego pliku requirements.txt ==="
cat > ./requirements_example.txt << EOF
# Zależności podstawowe
numpy==1.22.0
pandas>=1.4.0
matplotlib>=3.5.0
# Zależności opcjonalne
requests>=2.27.0
pyyaml>=6.0
EOF

echo "Utworzono plik requirements_example.txt"

# Konwersja z formatu pip do formatu conda
echo -e "\n=== Konwersja z formatu pip do formatu conda ==="
python -m spectomate.cli convert \
    --source-format pip \
    --target-format conda \
    --input-file ./requirements_example.txt \
    --output-file ./environment_example.yml \
    --env-name myenv \
    --verbose

# Wyświetlanie zawartości wygenerowanego pliku environment.yml
echo -e "\n=== Zawartość wygenerowanego pliku environment_example.yml ==="
cat ./environment_example.yml

# Konwersja z formatu conda do formatu pip
echo -e "\n=== Konwersja z formatu conda do formatu pip ==="
python -m spectomate.cli convert \
    --source-format conda \
    --target-format pip \
    --input-file ./environment_example.yml \
    --output-file ./requirements_converted.txt \
    --verbose

# Wyświetlanie zawartości wygenerowanego pliku requirements.txt
echo -e "\n=== Zawartość wygenerowanego pliku requirements_converted.txt ==="
cat ./requirements_converted.txt

echo -e "\nGotowe! Wszystkie przykłady zostały wykonane."
