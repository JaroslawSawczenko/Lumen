🧠 Lumen Quiz Platform

Profesjonalna platforma e-learningowa stworzona w Django. Aplikacja umożliwia rozwiązywanie quizów, śledzenie postępów, rywalizację o wyniki oraz dynamiczne zarządzanie bazą pytań.
📋 Spis Treści

    O Projekcie

    Funkcjonalności

    Technologie

    Instalacja Krok po Kroku

    Konfiguracja (.env)

    Importowanie Pytań (OpenTDB)

    Struktura Projektu

🚀 O Projekcie

Lumen to nowoczesna aplikacja webowa typu Quiz, która łączy w sobie elegancję interfejsu z potężnym backendem. Została zaprojektowana z myślą o skalowalności i łatwości rozbudowy. System obsługuje rejestrację użytkowników, profile z awatarami oraz rozbudowaną logikę naliczania punktów.
✨ Funkcjonalności
👤 Dla Użytkownika:

    System Kont: Rejestracja, logowanie i bezpieczne zarządzanie sesją.

    Profil Użytkownika: Możliwość ustawienia własnego awatara oraz edycji biogramu.

    Interaktywne Quizy: Rozwiązywanie testów z natychmiastową informacją zwrotną.

    Historia Wyników: Każde podejście do quizu jest zapisywane wraz z uzyskanym wynikiem procentowym.

⚙️ Dla Administratora:

    Panel Administracyjny: Pełna kontrola nad pytaniami, odpowiedziami i kategoriami quizów.

    Importer Pytań: Wbudowane narzędzie do automatycznego pobierania pytań z zewnętrznego API (Open Trivia Database).

    API REST: Endpointy przygotowane pod przyszłą aplikację mobilną lub frontend JS.

🛠 Technologie

Projekt wykorzystuje nowoczesny stack technologiczny:

    Backend: Python 3.10+, Django 5.2

    API: Django Rest Framework

    Baza Danych: SQLite (deweloperska) / PostgreSQL (produkcyjna)

    Frontend: HTML5, CSS3, Bootstrap 5 (Responsive Design)

    Grafika: Pillow (obsługa obrazów)

    Zarządzanie: python-dotenv (zmienne środowiskowe)

💻 Instalacja Krok po Kroku (Jak uruchomić?)

Aby uruchomić ten projekt na swoim komputerze, wykonaj poniższe kroki. Instrukcja zakłada, że masz zainstalowanego Pythona oraz Git.
1. Pobierz kod

Otwórz terminal (konsolę) i wpisz:
Bash

git clone https://github.com/jaroslawsawczenko/lumen.git
cd lumen

2. Utwórz Wirtualne Środowisko

To odizoluje biblioteki projektu od Twojego systemu.

    Windows:
    Bash

python -m venv venv
venv\Scripts\activate

MacOS / Linux:
Bash

    python3 -m venv venv
    source venv/bin/activate

3. Zainstaluj Zależności

Zainstaluj wszystkie wymagane biblioteki jednym poleceniem:
Bash

pip install -r requirements.txt

4. Skonfiguruj Plik .env

Projekt wymaga pliku konfiguracyjnego. Stworzyliśmy dla Ciebie szablon. Skopiuj go:

    Windows:
    Bash

copy .env.example .env

MacOS / Linux:
Bash

    cp .env.example .env

Teraz projekt użyje bezpiecznych ustawień domyślnych i bazy SQLite.
5. Przygotuj Bazę Danych

Utwórz tabele w bazie danych:
Bash

python manage.py migrate

6. (Opcjonalnie) Stwórz Administratora

Aby mieć dostęp do panelu admina, utwórz superużytkownika:
Bash

python manage.py createsuperuser

7. Uruchom Serwer!
Bash

python manage.py runserver

Wejdź w przeglądarce na adres: http://127.0.0.1:8000
🔐 Konfiguracja Zmiennych Środowiskowych

Plik .env steruje działaniem aplikacji. Oto najważniejsze zmienne:
Zmienna	Opis	Wartość Domyślna (Dev)
DEBUG	Tryb debugowania. Na produkcji MUSI być False.	True
SECRET_KEY	Klucz kryptograficzny Django.	(Losowy ciąg w .env)
DB_ENGINE	Silnik bazy danych.	django.db.backends.sqlite3
DB_NAME	Nazwa bazy danych.	db.sqlite3
EMAIL_*	Konfiguracja wysyłki maili (SMTP).	Console (wypisuje w terminalu)

Uwaga: Projekt jest gotowy do współpracy z bazą PostgreSQL – wystarczy zmienić DB_ENGINE i podać dane logowania w .env.
📥 Importowanie Pytań (OpenTDB)

Nie musisz dodawać pytań ręcznie! Aplikacja posiada skrypt do pobierania pytań z bazy wiedzy.

Aby zaimportować pytania z kategorii "Komputery", wpisz w terminalu:
Bash

python manage.py import_opentdb

Skrypt ten pobiera pytania, tłumaczy strukturę JSON i zapisuje je w Twojej bazie danych jako obiekty Django.
📂 Struktura Projektu
Plaintext

Lumen_Project/
├── Lumen_Project/      # Główne ustawienia (settings.py, urls.py)
├── Lumen/              # Aplikacja Quizowa
│   ├── models.py       # Modele: Quiz, Pytanie, Odpowiedź, Wynik
│   ├── views.py        # Logika wyświetlania quizów
│   ├── api/            # Serializery Django Rest Framework
│   └── management/     # Skrypty (import_opentdb.py)
├── users/              # Zarządzanie Użytkownikami
│   ├── models.py       # Profil użytkownika (Avatar, Bio)
│   └── signals.py      # Automatyczne tworzenie profilu po rejestracji
├── static/             # Pliki CSS, JS, Obrazy
├── templates/          # Szablony HTML (Bootstrap)
├── manage.py           # Menedżer zadań Django
└── requirements.txt    # Lista zależności

Autor

Projekt wykonany w celach edukacyjnych i portfolio. Kontakt: https://www.linkedin.com/in/jaroslaw-savchenko-5438a5320?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app  telegram: t.me/Jaroslaw_I
