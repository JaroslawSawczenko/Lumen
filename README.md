# 🧠 Lumen – Platforma Quizowa w Django

**Lumen** to nowoczesna platforma quizowa stworzona w Django, umożliwiająca użytkownikom rozwiązywanie quizów, zapisywanie wyników oraz zarządzanie pytaniami z poziomu panelu administracyjnego.

Projekt został zaprojektowany tak, aby można go było **bez problemu uruchomić na innym komputerze**, bez ręcznego grzebania w kodzie.

---

## 📌 Spis treści

- [Opis projektu](#-opis-projektu)
- [Funkcjonalności](#-funkcjonalności)
- [Technologie](#-technologie)
- [Wymagania](#-wymagania)
- [Instalacja krok po kroku](#-instalacja-krok-po-kroku)
- [Konfiguracja środowiska (.env)](#-konfiguracja-środowiska-env)
- [Migracje i uruchomienie](#-migracje-i-uruchomienie)
- [Import pytań (OpenTDB)](#-import-pytań-opentdb)
- [Struktura projektu](#-struktura-projektu)
- [Dobre praktyki](#-dobre-praktyki)
- [Autor](#-autor)

---

## 📖 Opis projektu

Lumen to aplikacja webowa typu **Quiz Platform**, która umożliwia:

- rejestrację i logowanie użytkowników,
- rozwiązywanie quizów z różnych kategorii,
- zapisywanie historii wyników,
- zarządzanie pytaniami i odpowiedziami przez administratora,
- import pytań z zewnętrznego API (Open Trivia Database).

Aplikacja została napisana w Django z wykorzystaniem Django REST Framework i jest przygotowana pod dalszą rozbudowę (np. frontend SPA lub aplikację mobilną).

---

## ✨ Funkcjonalności

### 👤 Funkcje użytkownika
- Rejestracja i logowanie
- Profil użytkownika (avatar, opis)
- Rozwiązywanie quizów
- Automatyczne sprawdzanie odpowiedzi
- Zapisywanie wyników i statystyk

### 🔧 Funkcje administratora
- Panel administracyjny Django
- Zarządzanie pytaniami i odpowiedziami
- Zarządzanie kategoriami quizów
- Import pytań z Open Trivia Database
- API REST do obsługi danych

---

## 🛠 Technologie

- **Python 3.10+**
- **Django 5.2**
- **Django REST Framework**
- **SQLite** (domyślna baza danych)
- **PostgreSQL** (opcjonalnie)
- **HTML5 / CSS3**
- **Bootstrap 5**
- **Pillow** (obsługa avatarów)
- **python-dotenv**

---

## ⚙️ Wymagania

- Python 3.10 lub nowszy
- Git
- pip
- (opcjonalnie) PostgreSQL

---

## 💻 Instalacja krok po kroku

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/JaroslawSawczenko/Lumen.git
cd Lumen

2. Utworzenie wirtualnego środowiska
Windows
python -m venv venv
venv\Scripts\activate

Linux / macOS
python3 -m venv venv
source venv/bin/activate

3. Instalacja zależności
pip install -r requirements.txt

🔐 Konfiguracja środowiska (.env)

W katalogu głównym projektu znajduje się plik .env.example.

Skopiuj go i zmień nazwę na .env:

cp .env.example .env


Przykładowa zawartość pliku .env:

DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend


Plik .env nie powinien być dodawany do repozytorium.

🗄 Migracje i uruchomienie
Migracje bazy danych
python manage.py migrate

Utworzenie konta administratora
python manage.py createsuperuser

Uruchomienie serwera
python manage.py runserver


Aplikacja:

http://127.0.0.1:8000


Panel admina:

http://127.0.0.1:8000/admin

📥 Import pytań (OpenTDB)

Projekt zawiera komendę Django do importu pytań z Open Trivia Database.

python manage.py import_opentdb


Komenda automatycznie pobiera pytania i zapisuje je w bazie danych.

📁 Struktura projektu
Lumen/
├── Lumen_Project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Lumen/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── management/
│       └── commands/
│           └── import_opentdb.py
├── users/
├── templates/
├── static/
├── manage.py
└── requirements.txt
👤 Autor

Projekt wykonany w celach edukacyjnych oraz jako element portfolio.

Autor: Jarosław Sawczenko

GitHub: https://github.com/JaroslawSawczenko

LinkedIn: https://www.linkedin.com/in/jaroslaw-savchenko-5438a5320
