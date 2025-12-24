🧠 Lumen - Dokumentacja Techniczna

### 1.1 Cel Projektu

**Lumen** to nowoczesna, interaktywna platforma quizowa zbudowana w Django, zaprojektowana w celu:
- Umożliwienia użytkownikom rozwiązywania quizów z różnych kategorii tematycznych
- Śledzenia postępów i statystyk użytkowników
- Zarządzania bazą pytań przez administratorów
- Integracji z zewnętrznymi źródłami pytań (Open Trivia Database)
- Zapewnienia gamifikacji procesu nauki

### 1.2 Główne Funkcjonalności

#### Dla Użytkowników:
- **Rejestracja i Autentykacja**: Bezpieczny system logowania z walidacją
- **Profil Użytkownika**: Personalizacja z avatarem i opisem
- **Rozwiązywanie Quizów**: Interaktywny interfejs do odpowiadania na pytania
- **Historia Wyników**: Śledzenie postępów i statystyk
- **Ranking**: Porównywanie wyników z innymi użytkownikami

#### Dla Administratorów:
- **Panel Administracyjny**: Pełne zarządzanie systemem przez Django Admin
- **Zarządzanie Pytaniami**: CRUD operacje na pytaniach i odpowiedziach
- **Kategorie**: Organizacja pytań według tematyki
- **Import Danych**: Automatyczny import pytań z Open Trivia Database
- **API REST**: Endpoints do zarządzania danymi

### 1.3 Stack Technologiczny

#### Backend:
- **Python 3.10+**: Nowoczesna wersja języka
- **Django 5.2**: Framework webowy wysokiego poziomu
- **Django REST Framework**: Tworzenie RESTful API
- **SQLite/PostgreSQL**: Baza danych (SQLite domyślnie, PostgreSQL opcjonalnie)

#### Frontend:
- **HTML5/CSS3**: Struktura i stylizacja

#### Narzędzia Pomocnicze:
- **Pillow**: Przetwarzanie obrazów (avatary)
- **python-dotenv**: Zarządzanie zmiennymi środowiskowymi

---



###  Struktura Katalogów

```
Lumen/
│
├── Lumen_Project/              # Główny katalog projektu Django
│   ├── __init__.py
│   ├── settings.py            # Konfiguracja projektu
│   ├── urls.py                # Główne routing URLs
│   ├── wsgi.py                # WSGI config dla deployment
│   └── asgi.py                # ASGI config (opcjonalny)
│
├── Lumen/                     # Aplikacja quizowa (główna)
│   ├── __init__.py
│   ├── models.py              # Modele: Question, Answer, QuizAttempt
│   ├── views.py               # Widoki i logika quizów
│   ├── serializers.py         # Serializery DRF
│   ├── urls.py                # URLs specyficzne dla app
│   ├── admin.py               # Konfiguracja Django Admin
│   ├── forms.py               # Formularze Django
│   ├── tests.py               # Testy jednostkowe
│   │
│   ├── management/            # Custom Django commands
│   │   └── commands/
│   │       └── import_opentdb.py  # Import pytań z API
│   │
│   ├── migrations/            # Migracje bazy danych
│   │   └── 000X_*.py
│   │
│   └── templates/             # Templates HTML dla app
│       └── Lumen/
│           ├── quiz_list.html
│           ├── quiz_detail.html
│           └── results.html
│
├── users/                     # Aplikacja zarządzania użytkownikami
│   ├── __init__.py
│   ├── models.py              # Model: UserProfile
│   ├── views.py               # Logowanie, rejestracja, profil
│   ├── forms.py               # Formularze użytkownika
│   ├── urls.py
│   ├── admin.py
│   │
│   └── templates/
│       └── users/
│           ├── login.html
│           ├── register.html
│           └── profile.html
│
├── templates/                 # Globalne templates
│   ├── base.html             # Bazowy template
│   ├── home.html             # Strona główna
│   └── partials/
│       ├── navbar.html
│       └── footer.html
│
├── static/                    # Pliki statyczne
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── quiz.js
│   └── images/
│       └── logo.png
│
├── media/                     # Pliki uploadowane przez użytkowników
│   └── avatars/              # Avatary użytkowników
│
├── .env                       # Zmienne środowiskowe (nie w repo!)
├── .env.example              # Przykładowy plik .env
├── .gitignore                # Pliki ignorowane przez Git
├── requirements.txt          # Zależności Python
├── manage.py                 # Django management script
├── README.md                 # Dokumentacja podstawowa
└── LICENSE                   # Licencja projektu
```

### 2.3 Przepływ Danych

#### Przykład: Rozwiązywanie Quizu

```
1. Użytkownik →  GET /quiz/5/
                      ↓
2. urls.py → quiz_detail_view(request, quiz_id=5)
                      ↓
3. views.py → Pobranie pytań z bazy (Question.objects.filter...)
                      ↓
4. models.py → ORM wykonuje SQL query
                      ↓
5. Database → Zwraca dane pytań i odpowiedzi
                      ↓
6. views.py → Przygotowanie kontekstu dla template
                      ↓
7. templates/ → Renderowanie HTML z danymi
                      ↓
8. Response → HTML zwrócony do przeglądarki użytkownika
```

#### Przykład: Sprawdzanie Odpowiedzi (API)

```
1. Frontend → POST /api/quiz/5/submit/
   Body: {"answers": [{"question_id": 1, "answer_id": 3}, ...]}
                      ↓
2. urls.py → quiz_submit_api(request, quiz_id=5)
                      ↓
3. views.py → Walidacja danych (serializer)
                      ↓
4. Logika → Porównanie odpowiedzi z correct_answer
                      ↓
5. models.py → Zapis QuizAttempt do bazy
                      ↓
6. Response → JSON: {"score": 8, "total": 10, "percentage": 80}
```

---

## 3. Instalacja i Konfiguracja

### 3.1 Wymagania Systemowe

#### Minimalne Wymagania:
- **Python**: 3.10 lub nowszy
- **RAM**: Minimum 2GB (4GB rekomendowane)
- **Dysk**: 500MB wolnego miejsca
- **System Operacyjny**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)

#### Wymagane Oprogramowanie:
- Git
- Python 3.10+
- pip (package manager)
- (Opcjonalnie) PostgreSQL 12+

### 3.2 Instalacja Krok po Kroku

#### Krok 1: Klonowanie Repozytorium

```bash
# Klonowanie repo
git clone https://github.com/JaroslawSawczenko/Lumen.git

# Przejście do katalogu
cd Lumen
```

#### Krok 2: Utworzenie Wirtualnego Środowiska

**Windows:**
```bash
# Utworzenie venv
python -m venv venv

# Aktywacja
venv\Scripts\activate
```

**Linux/macOS:**
```bash
# Utworzenie venv
python3 -m venv venv

# Aktywacja
source venv/bin/activate
```

**Weryfikacja:**
```bash
# Sprawdzenie aktywacji (w prompt powinno być (venv))
which python  # Linux/macOS
where python  # Windows
```

#### Krok 3: Instalacja Zależności

```bash
# Aktualizacja pip
pip install --upgrade pip

# Instalacja wszystkich zależności
pip install -r requirements.txt

# Weryfikacja instalacji
pip list
```

**Oczekiwane główne pakiety:**
- Django>=5.2
- djangorestframework>=3.14
- Pillow>=10.0
- python-dotenv>=1.0
- requests>=2.31

#### Krok 4: Konfiguracja Zmiennych Środowiskowych

```bash
# Kopiowanie pliku przykładowego
cp .env.example .env

# Edycja pliku .env
nano .env  # lub vim, code, notepad++
```

**Zawartość .env:**
```env
# Debug Mode (NIGDY True na produkcji!)
DEBUG=True

# Secret Key (wygeneruj nowy dla produkcji!)
SECRET_KEY=your-very-secret-and-long-random-key-here-change-it

# Allowed Hosts (domeny dozwolone do serwowania aplikacji)
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Dla PostgreSQL:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=lumen_db
# DB_USER=lumen_user
# DB_PASSWORD=secure_password
# DB_HOST=localhost
# DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# Dla prawdziwego emaila:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# OpenTDB API (opcjonalne)
OPENTDB_API_URL=https://opentdb.com/api.php
```

**Generowanie SECRET_KEY:**
```python
# W Python shell:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### Krok 5: Konfiguracja Bazy Danych

**Opcja A: SQLite (Domyślna)**
```bash
# SQLite nie wymaga dodatkowej konfiguracji
# Plik db.sqlite3 zostanie utworzony automatycznie
```

**Opcja B: PostgreSQL**
```bash
# 1. Instalacja PostgreSQL (przykład dla Ubuntu)
sudo apt update
sudo apt install postgresql postgresql-contrib

# 2. Utworzenie bazy i użytkownika
sudo -u postgres psql
```

```sql
-- W konsoli PostgreSQL:
CREATE DATABASE lumen_db;
CREATE USER lumen_user WITH PASSWORD 'secure_password';
ALTER ROLE lumen_user SET client_encoding TO 'utf8';
ALTER ROLE lumen_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE lumen_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lumen_db TO lumen_user;
\q
```

```bash
# 3. Instalacja adaptera psycopg2
pip install psycopg2-binary

# 4. Aktualizacja .env (patrz przykład wyżej)
```

#### Krok 6: Migracje Bazy Danych

```bash
# Przejście do katalogu z manage.py
cd Lumen_Project  # (jeśli manage.py jest w tym katalogu)

# Utworzenie migracji
python manage.py makemigrations

# Aplikacja migracji
python manage.py migrate

# Weryfikacja
python manage.py showmigrations
```

**Wynik:**
```
[X] 0001_initial
[X] 0002_add_categories
[X] 0003_quiz_attempts
...
```

#### Krok 7: Utworzenie Superusera (Administratora)

```bash
python manage.py createsuperuser
```

**Podaj:**
- Username: `admin`
- Email: `admin@example.com`
- Password: `SecurePassword123!` (minimum 8 znaków)
- Password (again): `SecurePassword123!`

#### Krok 8: Zbieranie Plików Statycznych (dla produkcji)

```bash
# Tylko dla produkcji (development używa staticfiles)
python manage.py collectstatic --noinput
```

#### Krok 9: Uruchomienie Serwera Deweloperskiego

```bash
python manage.py runserver
```

**Dostęp:**
- Aplikacja: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin/`
- API: `http://127.0.0.1:8000/api/`

**Testowanie:**
1. Otwórz `http://127.0.0.1:8000/`
2. Zarejestruj nowego użytkownika
3. Zaloguj się
4. Przejdź do `/admin/` i zaloguj jako superuser


