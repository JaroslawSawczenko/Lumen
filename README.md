# 🧠 Lumen - Platforma E-learningowa z Gamifikacją

> **Lumen** to nowoczesna aplikacja webowa typu Quiz oparta na frameworku Django. Projekt łączy klasyczne testy wiedzy z zaawansowanymi mechanizmami grywalizacji (XP, poziomy, awatary), oferując jednocześnie pełne REST API oraz integrację z zewnętrznymi bazami pytań.

---

## 📋 Spis Treści
1. [O Projekcie](#-o-projekcie)
2. [Kluczowe Funkcjonalności](#-kluczowe-funkcjonalności)
3. [Stack Technologiczny](#-stack-technologiczny)
4. [Instalacja i Konfiguracja](#-instalacja-i-konfiguracja)
5. [Struktura Zmiennych Środowiskowych (.env)](#-struktura-zmiennych-środowiskowych-env)
6. [Dokumentacja API](#-dokumentacja-api)
7. [Algorytmy i Logika Biznesowa](#-algorytmy-i-logika-biznesowa)
8. [Zarządzanie (Management Commands)](#-zarządzanie-management-commands)
9. [Testy](#-testy)

---

## 🚀 O Projekcie

System **Lumen** został zaprojektowany w architekturze monolitycznej z wyraźnym podziałem na domeny logiczne:
* **Core (Lumen):** Zarządzanie quizami, pytaniami, odpowiedziami i sesjami gier.
* **Users:** Obsługa profili użytkowników, system poziomów (Leveling System) i historia wyników.

Aplikacja kładzie nacisk na optymalizację zapytań do bazy danych (wykorzystanie `select_related`, `prefetch_related`) oraz bezpieczeństwo danych (transakcyjność operacji `atomic`).

---

## ⭐ Kluczowe Funkcjonalności

### Dla Użytkownika
* **System Progresji:** Zdobywanie punktów doświadczenia (XP) i awansowanie na kolejne poziomy.
* **Mechanizm "Diminishing Returns":** System zapobiegający "farmieniu" punktów – każde kolejne podejście do tego samego quizu daje mniejszą nagrodę punktową.
* **Profile:** Personalizacja konta (wgrywanie awatarów), podgląd statystyk i paska postępu.
* **Interaktywne Quizy:** Obsługa limitów czasowych na pytania oraz pytań ilustrowanych obrazami.

### Dla Administratora / Dewelopera
* **Import Pytań:** Automatyczne pobieranie quizów z Open Trivia Database (OpenTDB) za pomocą komendy systemowej.
* **Panel Administracyjny:** Pełne zarządzanie treścią z poziomu Django Admin.
* **REST API:** Wystawione endpointy dla zewnętrznych aplikacji klienckich.

---

## 🛠 Stack Technologiczny

| Kategoria | Technologia | Wersja |
|-----------|-------------|--------|
| **Backend** | Python | 3.10+ |
| **Framework** | Django | 5.2.6 |
| **API** | Django REST Framework | 3.16.1 |
| **Baza Danych** | SQLite (Dev) / PostgreSQL (Prod) | Konfigurowalne w .env |
| **Przetwarzanie Obrazu** | Pillow | 11.3.0 |
| **Frontend** | Django Templates + CSS3 | Responsive Design |

---

## 💻 Instalacja i Konfiguracja

### Wymagania wstępne
* Python 3.10 lub nowszy
* Git

### Krok 1: Klonowanie repozytorium
```bash
git clone [https://github.com/TwojeRepo/Lumen.git](https://github.com/TwojeRepo/Lumen.git)
cd Lumen
```
### Krok 2: Utworzenie środowiska wirtualnego
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### Krok 3: Instalacja zależności
```bash
pip install -r requirements.txt
```
### Krok 4: Konfiguracja zmiennych środowiskowych

Utwórz plik .env w głównym katalogu projektu, bazując na pliku .env.example.
### Krok 5: Migracje i Uruchomienie
```bash
python manage.py migrate
python manage.py createsuperuser  # Utwórz konto administratora
python manage.py runserver
```
Aplikacja będzie dostępna pod adresem: http://127.0.0.1:8000/
## 🔐 Struktura Zmiennych Środowiskowych (.env)

Plik .env jest kluczowy dla bezpieczeństwa i konfiguracji projektu.
Ini, TOML

# Główna konfiguracja
DEBUG=True
SECRET_KEY=twoj-unikalny-sekretny-klucz
ALLOWED_HOSTS=127.0.0.1,localhost

# Baza Danych (Domyślnie SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Opcjonalnie: Konfiguracja PostgreSQL
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=lumen_db
# DB_USER=postgres
# DB_PASSWORD=haslo
# DB_HOST=localhost
# DB_PORT=5432

# Konfiguracja Email (Dla deweloperki - logi w konsoli)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

## 📡 Dokumentacja API

System udostępnia REST API pod ścieżką /api/.
Endpoints
Metoda	Ścieżka	Opis	Autoryzacja
GET	/api/quizzes/	Lista dostępnych quizów	Publiczny
POST	/api/quizzes/	Utworzenie nowego quizu	Wymagana (IsAuthenticated)
GET	/api/quizzes/{id}/	Szczegóły quizu i pytania	Publiczny
Uwagi do Serializerów

Serializer AnswerSerializer posiada dynamiczną logikę bezpieczeństwa – pole is_correct (informacja o poprawnej odpowiedzi) jest usuwane z odpowiedzi API dla użytkowników, którzy nie są administratorami (is_staff), aby zapobiec oszustwom.
🧮 Algorytmy i Logika Biznesowa
1. Skalowanie Poziomów (Level Scaling)

Wymagane punkty doświadczenia (XP) na kolejny poziom są obliczane wykładniczo. Formuła: $$ XP_{required} = 100 \times (Level^{1.5}) $$ Zaimplementowane w: users/models.py.
2. System Punktacji Malejącej (Score Decay)

W celu balansu rozgrywki, wielokrotne rozwiązywanie tego samego quizu przynosi mniejsze korzyści. Formuła: $$ Mnożnik = \max(0.1, \ 1.0 - (LiczbaPodejść \times 0.2)) $$ Oznacza to, że każde podejście zmniejsza nagrodę o 20%, aż do minimalnego progu 10% wartości bazowej. Zaimplementowane w: Lumen/views.py (funkcja finish_quiz_view).
🛠 Zarządzanie (Management Commands)
Import Quizów z OpenTDB

Projekt posiada wbudowane narzędzie do zasilania bazy danych pytaniami z Open Trivia Database.

Użycie:
Bash

python manage.py import_opentdb

Działanie skryptu:

    Losuje kategorię (np. Historia, Nauka, Filmy).

    Pobiera 10 pytań z API.

    Tworzy systemowego użytkownika LumenBot (jeśli nie istnieje).

    Zapisuje Quiz, Pytania i Odpowiedzi w bazie (używając bulk_create dla wydajności).

🧪 Testy

Projekt posiada zestaw testów jednostkowych weryfikujących logikę biznesową oraz widoczność danych.

Aby uruchomić testy:
Bash

python manage.py test

Zakres testów:

    Logika XP: Weryfikacja dodawania punktów i awansowania na poziomy.

    Rejestracja: Walidacja unikalności adresów email.

    Widoczność Quizów: Sprawdzenie, czy nieopublikowane quizy są ukryte dla zwykłych użytkowników.

    API: Testowanie tworzenia quizów przez endpointy REST.

© 2025 Lumen Project. Autor: Jarosław Sawczenko.

