# Projekt: Analiza i Predykcja Cen Samochodów Volkswagen Passat



## Opis plików

### 1. `cleaning_correcting.py`

Zawiera funkcje do oczyszczania i korekty danych samochodów, takie jak usuwanie wartości odstających, przypisywanie
brakujących pochodzeń oraz korygowanie pojemności silników i mocy.

### 2. `data_processing_pipeline.py`

Plik tworzący bazę danych MySQL, tabelę `passats`, uploadujący tam dane z pliku `passats_raw.csv` oraz przeprowadza
szereg operacji oczyszczania i korekty danych, aby zaktualizować zawartość tabeli w bazie.

### 3. `otomoto_category_scraper.py`

Pobiera linki do ogłoszeń samochodów z kategorii na Otomoto, zapisując je do pliku.

### 4. `otomoto_car_page_scraper.py`

Scrapuje dane ogłoszeń na Otomoto z linków w pliku urls.txt oraz uploaduje je do bazy danych.

### 5. `passats.csv`

Plik CSV zawierający dane samochodów Volkswagen Passat B8 używane do analizy i treningu modeli predykcyjnych.

### 6. `passats_data_profiling_report.html`

Zawiera szczegółowy raport ydata_profiling z profilowania danych samochodów Volkswagen Passat.

### 7. `passats_raw.csv`

Zawiera surowe dane dotyczące samochodów Volkswagen Passat, które zostały zebrane przed przeprowadzeniem procesu
oczyszczania i korekty danych.

### 8. `profiling.py`

Zawiera skrypt wykorzystany do wygenerowania raportu z ydata_profiling.

### 9. `training_best.py`

Zawiera skrypt do trenowania i ewaluacji różnych modeli regresyjnych, z wykorzystaniem domyślnych parametrów oraz
porównaniem wyników tych modeli.

### 10. `utils.py`

Zawiera narzędzia do zarządzania bazą danych MySQL, w tym klasę DBConnector do obsługi połączeń, wstawiania, pobierania
i backupu danych oraz funkcje do zapisu i odczytu URLi.

### 11. `visualization.py`

Zawiera funkcje do generowania wykresów z danych o samochodach, w tym rozkładów cen, roczników, przebiegów, parametrów
technicznych oraz macierzy korelacji.

### 12. `README.md`

Niniejszy plik zawierający opis projektu i plików.

## Instrukcje dla modelu predykcyjnego

1. Instalacja wymaganych bibliotek:
   ```pip install matplotlib pandas catboost scikit-learn```
2. Uruchomienie skryptu training_best.py:
   ```python training_best.py```

## Instrukcja dla załadowania danych oraz proccessingu

1. Instalacja wymaganych bibliotek:
   ```pip install matplotlib pandas seaborn mysql-connector-python ydata-profiling```
2. Załączenie bazy Mysql na urządzeniu.
3. Ustawienie danych do połączenia z bazą w pliku utils.py
4. Uruchomienie skryptu data_processing_pipeline.py:
   ```python data_processing_pipeline.py```
5. W bazie danych pojawi się tabela passats z przetworzonymi danymi.
6. Można teraz korzystać wszystkich nie wymienionych wyżej funkcjonalności projektu m.in wizualizacji danych,
   scrapowania danych, czy generowania raportu y_data_profiling.

## Instrukcja dla scrapowania danych

1. Instalacja wymaganych bibliotek:
   ```pip install cloudscraper beautifulsoup4```
2. Wykonanie instrukcji powyżej.
3. Uruchomienie skryptu otomoto_category_scraper.py:
   ```python otomoto_category_scraper.py```
4. Uruchomienie skryptu otomoto_car_page_scraper.py:
   ```python otomoto_car_page_scraper.py```
5. Dane zostaną zescrapowane i zapisane w bazie danych