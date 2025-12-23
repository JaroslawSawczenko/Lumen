# 🧠 Lumen -  Dokumentacja Projektu

## Spis Treści

1. [Wprowadzenie](#wprowadzenie)
2. [Architektura Projektu](#architektura-projektu)
3. [Instalacja i Konfiguracja](#instalacja-i-konfiguracja)
4. [Struktura Kodu](#struktura-kodu)
5. [Modele Danych](#modele-danych)
6. [Widoki i API](#widoki-i-api)
7. [System Autentykacji](#system-autentykacji)


---

## 1. Wprowadzenie

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

## 2. Architektura Projektu

### 2.1 Wzorzec Architektoniczny: MTV (Model-Template-View)

Django implementuje wzorzec MTV, który jest wariacją MVC:

```
┌─────────────────────────────────────────────────────┐
│                    UŻYTKOWNIK                        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                   URLs (urls.py)                     │
│         Routing żądań do odpowiednich widoków        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                  Views (views.py)                    │
│          Logika biznesowa i przetwarzanie            │
└───────────┬─────────────────────────┬────────────────┘
            │                         │
            ▼                         ▼
┌─────────────────────┐    ┌─────────────────────────┐
│  Models (models.py) │    │ Templates (*.html)      │
│   Struktura danych  │    │   Prezentacja danych    │
│   ORM - baza danych │    │   HTML + Django Tags    │
└─────────────────────┘    └─────────────────────────┘
```

### 2.2 Struktura Katalogów

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

### 3.3 Import Przykładowych Danych

#### Import Pytań z Open Trivia Database

```bash
python manage.py import_opentdb

# Z określoną kategorią i liczbą pytań:
python manage.py import_opentdb --category=9 --amount=50

# Kategorie OpenTDB:
# 9: General Knowledge
# 17: Science & Nature
# 18: Science: Computers
# 21: Sports
# 23: History
```

**Weryfikacja:**
```bash
python manage.py shell
```

```python
from Lumen.models import Question
print(Question.objects.count())  # Liczba pytań
```

---

## 4. Struktura Kodu

### 4.1 settings.py - Konfiguracja Projektu

#### Kluczowe Sekcje:

```python
# Lumen_Project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    
    # Local apps
    'Lumen',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Lumen_Project.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Email Configuration
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'
)

# Custom User Model (jeśli używane)
# AUTH_USER_MODEL = 'users.CustomUser'

# Login URLs
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### 4.2 urls.py - Routing

#### Główny URLs (Lumen_Project/urls.py):

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Aplikacja główna (quizy)
    path('', include('Lumen.urls')),
    
    # Aplikacja użytkowników
    path('users/', include('users.urls')),
    
    # API
    path('api/', include('Lumen.api_urls')),
]

# Serwowanie plików media w development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

#### URLs Aplikacji Lumen (Lumen/urls.py):

```python
from django.urls import path
from . import views

app_name = 'Lumen'

urlpatterns = [
    # Strona główna
    path('', views.home, name='home'),
    
    # Lista quizów
    path('quizzes/', views.quiz_list, name='quiz_list'),
    
    # Szczegóły quizu
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    
    # Rozpoczęcie quizu
    path('quiz/<int:quiz_id>/start/', views.quiz_start, name='quiz_start'),
    
    # Wysłanie odpowiedzi
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    
    # Wyniki quizu
    path('quiz/<int:quiz_id>/results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),
    
    # Historia użytkownika
    path('my-quizzes/', views.user_quiz_history, name='user_quiz_history'),
    
    # Ranking
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
```

---

## 5. Modele Danych

### 5.1 Diagram ERD (Entity Relationship Diagram)

```
┌─────────────────────┐
│       User          │ (Django built-in)
│─────────────────────│
│ id (PK)             │
│ username            │
│ email               │
│ password            │
│ is_staff            │
│ date_joined         │
└──────────┬──────────┘
           │ 1
           │
           │ N
┌──────────▼──────────┐
│    UserProfile      │
│─────────────────────│
│ id (PK)             │
│ user_id (FK)        │──┐
│ avatar              │  │ OneToOne
│ bio                 │  │
│ total_score         │  │
│ quizzes_completed   │◄─┘
└─────────────────────┘


┌─────────────────────┐
│     Category        │
│─────────────────────│
│ id (PK)             │
│ name                │
│ description         │
│ created_at          │
└──────────┬──────────┘
           │ 1
           │
           │ N
┌──────────▼──────────┐
│     Question        │
│─────────────────────│
│ id (PK)             │
│ category_id (FK)    │
│ text                │
│ difficulty          │───┐
│ question_type       │   │
│ created_at          │   │
│ is_active           │   │
└──────────┬──────────┘   │
           │ 1            │
           │              │
           │ N            │
┌──────────▼──────────┐   │
│      Answer         │   │
│─────────────────────│   │
│ id (PK)             │   │
│ question_id (FK)    │   │
│ text                │   │
│ is_correct          │   │
│ created_at          │   │
└─────────────────────┘   │
                          │
                          │
┌─────────────────────────┐
│    QuizAttempt          │
│─────────────────────────│
│ id (PK)                 │
│ user_id (FK)            │
│ question_id (FK)        │◄─┘
│ selected_answer_id (FK) │
│ is_correct              │
│ time_taken              │
│ attempted_at            │
└─────────────────────────┘
```

### 5.2 Szczegółowe Opisy Modeli

#### Model: Category

```python
# Lumen/models.py

from django.db import models

class Category(models.Model):
    """
    Kategoria tematyczna dla pytań quizowych.
    
    Attributes:
        name (str): Nazwa kategorii (np. "Nauka", "Historia")
        description (str): Opis kategorii
        slug (str): URL-friendly wersja nazwy
        created_at (datetime): Data utworzenia
        updated_at (datetime): Data ostatniej aktualizacji
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nazwa kategorii"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Opis"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_question_count(self):
        """Zwraca liczbę pytań w tej kategorii."""
        return self.questions.filter(is_active=True).count()
```

#### Model: Question

```python
class Question(models.Model):
    """
    Pytanie quizowe.
    
    Attributes:
        category (FK): Kategoria pytania
        text (str): Treść pytania
        difficulty (str): Poziom trudności (easy/medium/hard)
        question_type (str): Typ pytania (multiple_choice/true_false)
        explanation (str): Wyjaśnienie odpowiedzi (opcjonalne)
        points (int): Liczba punktów za poprawną odpowiedź
        is_active (bool): Czy pytanie jest aktywne
        created_at (datetime): Data utworzenia
    """
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Łatwe'),
        ('medium', 'Średnie'),
        ('hard', 'Trudne'),
    ]
    
    TYPE_CHOICES = [
        ('multiple_choice', 'Wielokrotnego wyboru'),
        ('true_false', 'Prawda/Fałsz'),
    ]
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Kategoria"
    )
    text = models.TextField(verbose_name="Treść pytania")
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name="Poziom trudności"
    )
    question_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='multiple_choice',
        verbose_name="Typ pytania"
    )
    explanation = models.TextField(
        blank=True,
        verbose_name="Wyjaśnienie"
    )
    points = models.IntegerField(
        default=10,
        verbose_name="Punkty"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktywne"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pytanie"
        verbose_name_plural = "Pytania"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.text[:50]}..."
    
    def get_correct_answer(self):
        """Zwraca poprawną odpowiedź."""
        return self.answers.filter(is_correct=True).first()
    
    def get_all_answers(self):
        """Zwraca wszystkie odpowiedzi w losowej kolejności."""
        return self.answers.all().order_by('?')
```

#### Model: Answer

```python
class Answer(models.Model):
    """
    Odpowiedź na pytanie quizowe.
    
    Attributes:
        question (FK): Pytanie, do którego należy odpowiedź
        text (str): Treść odpowiedzi
        is_correct (bool): Czy odpowiedź jest poprawna
        created_at (datetime): Data utworzenia
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Pytanie"
    )
    text = models.CharField(
        max_length=200,
        verbose_name="Treść odpowiedzi"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Poprawna odpowiedź"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Odpowiedź"
        verbose_name_plural = "Odpowiedzi"
    
    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.text}"
```

#### Model: QuizAttempt

```python
class QuizAttempt(models.Model):
    """
    Próba rozwiązania pytania przez użytkownika.
    
    Attributes:
        user (FK): Użytkownik
        question (FK): Pytanie
        selected_answer (FK): Wybrana odpowiedź
        is_correct (bool): Czy odpowiedź była poprawna
        time_taken (int): Czas w sekundach
        points_earned (int): Zdobyte punkty
        attempted_at (datetime): Data rozwiązania
    """
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name="Użytkownik"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name="Pytanie"
    )
    selected_answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Wybrana odpowiedź"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Poprawna"
    )
    time_taken = models.IntegerField(
        default=0,
        verbose_name="Czas (sekundy)"
    )
    points_earned = models.IntegerField(
        default=0,
        verbose_name="Zdobyte punkty"
    )
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Próba quizu"
        verbose_name_plural = "Próby quizów"
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"
    
    def save(self, *args, **kwargs):
        """Override save to automatically set is_correct and points."""
        if self.selected_answer:
            self.is_correct = self.selected_answer.is_correct
            if self.is_correct:
                self.points_earned = self.question.points
        super().save(*args, **kwargs)
```

#### Model: UserProfile (w aplikacji users)

```python
# users/models.py

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    """
    Rozszerzony profil użytkownika.
    
    Attributes:
        user (OneToOne): Powiązany użytkownik Django
        avatar (ImageField): Avatar użytkownika
        bio (str): Biografia
        total_score (int): Łączna liczba punktów
        quizzes_completed (int): Liczba ukończonych quizów
        created_at (datetime): Data utworzenia profilu
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Użytkownik"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        verbose_name="Avatar"
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="O mnie"
    )
    total_score = models.IntegerField(
        default=0,
        verbose_name="Łączne punkty"
    )
    quizzes_completed = models.IntegerField(
        default=0,
        verbose_name="Ukończone quizy"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil użytkownika"
        verbose_name_plural = "Profile użytkowników"
    
    def __str__(self):
        return f"Profil: {self.user.username}"
    
    def save(self, *args, **kwargs):
        """Override save to resize avatar."""
        super().save(*args, **kwargs)
        
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    
    def get_accuracy(self):
        """Oblicza dokładność odpowiedzi użytkownika."""
        attempts = self.user.quiz_attempts.all()
        if not attempts.exists():
            return 0
        correct = attempts.filter(is_correct=True).count()
        return round((correct / attempts.count()) * 100, 2)
```

### 5.3 Sygnały Django (Signals)

```python
# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatyczne tworzenie profilu przy rejestracji użytkownika."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatyczny zapis profilu przy aktualizacji użytkownika."""
    instance.profile.save()
```

**Rejestracja sygnałów (users/apps.py):**
```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import users.signals  # Importuj sygnały
```

---

## 6. Widoki i API

### 6.1 Views - Function-Based Views (FBV)

#### Przykład: Lista Quizów

```python
# Lumen/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Category, Question, QuizAttempt

def quiz_list(request):
    """
    Wyświetla listę dostępnych kategorii quizów.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Renderowany template z listą kategorii
    """
    # Pobierz wszystkie kategorie z liczbą aktywnych pytań
    categories = Category.objects.annotate(
        question_count=Count('questions', filter=Q(questions__is_active=True))
    ).filter(question_count__gt=0)
    
    # Wyszukiwanie
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'Lumen/quiz_list.html', context)
```

#### Przykład: Rozpoczęcie Quizu

```python
@login_required
def quiz_start(request, quiz_id):
    """
    Rozpoczyna nowy quiz dla danej kategorii.
    
    Args:
        request: HttpRequest
        quiz_id (int): ID kategorii
        
    Returns:
        HttpResponse: Redirect do pierwszego pytania
    """
    category = get_object_or_404(Category, id=quiz_id)
    
    # Pobierz 10 losowych pytań z kategorii
    questions = Question.objects.filter(
        category=category,
        is_active=True
    ).order_by('?')[:10]
    
    if not questions.exists():
        messages.error(request, "Brak dostępnych pytań w tej kategorii.")
        return redirect('Lumen:quiz_list')
    
    # Zapisz pytania w sesji
    request.session['quiz_questions'] = list(questions.values_list('id', flat=True))
    request.session['current_question'] = 0
    request.session['quiz_start_time'] = str(timezone.now())
    
    messages.success(request, f"Rozpoczęto quiz: {category.name}")
    return redirect('Lumen:quiz_detail', quiz_id=quiz_id)
```

#### Przykład: Wyświetlanie Pytania

```python
@login_required
def quiz_detail(request, quiz_id):
    """
    Wyświetla aktualne pytanie quizu.
    
    Args:
        request: HttpRequest
        quiz_id (int): ID kategorii
        
    Returns:
        HttpResponse: Renderowany template z pytaniem
    """
    category = get_object_or_404(Category, id=quiz_id)
    
    # Sprawdź czy quiz jest w sesji
    if 'quiz_questions' not in request.session:
        return redirect('Lumen:quiz_start', quiz_id=quiz_id)
    
    question_ids = request.session['quiz_questions']
    current_index = request.session.get('current_question', 0)
    
    # Sprawdź czy quiz się skończył
    if current_index >= len(question_ids):
        return redirect('Lumen:quiz_results', quiz_id=quiz_id)
    
    # Pobierz aktualne pytanie
    question = get_object_or_404(Question, id=question_ids[current_index])
    answers = question.get_all_answers()
    
    # Oblicz postęp
    progress = ((current_index + 1) / len(question_ids)) * 100
    
    context = {
        'category': category,
        'question': question,
        'answers': answers,
        'current_index': current_index + 1,
        'total_questions': len(question_ids),
        'progress': progress,
    }
    return render(request, 'Lumen/quiz_detail.html', context)
```

#### Przykład: Wysyłanie Odpowiedzi

```python
@login_required
def quiz_submit(request, quiz_id):
    """
    Obsługuje wysłanie odpowiedzi na pytanie.
    
    Args:
        request: HttpRequest (POST)
        quiz_id (int): ID kategorii
        
    Returns:
        HttpResponse: Redirect do następnego pytania lub wyników
    """
    if request.method != 'POST':
        return redirect('Lumen:quiz_detail', quiz_id=quiz_id)
    
    # Pobierz dane z sesji
    question_ids = request.session.get('quiz_questions', [])
    current_index = request.session.get('current_question', 0)
    
    if current_index >= len(question_ids):
        return redirect('Lumen:quiz_results', quiz_id=quiz_id)
    
    # Pobierz pytanie i odpowiedź
    question = get_object_or_404(Question, id=question_ids[current_index])
    answer_id = request.POST.get('answer_id')
    
    if not answer_id:
        messages.error(request, "Proszę wybrać odpowiedź.")
        return redirect('Lumen:quiz_detail', quiz_id=quiz_id)
    
    selected_answer = get_object_or_404(Answer, id=answer_id, question=question)
    
    # Zapisz próbę
    QuizAttempt.objects.create(
        user=request.user,
        question=question,
        selected_answer=selected_answer,
    )
    
    # Przejdź do następnego pytania
    request.session['current_question'] = current_index + 1
    
    # Sprawdź czy to było ostatnie pytanie
    if current_index + 1 >= len(question_ids):
        return redirect('Lumen:quiz_results', quiz_id=quiz_id)
    
    return redirect('Lumen:quiz_detail', quiz_id=quiz_id)
```

### 6.2 Django REST Framework - Serializers

```python
# Lumen/serializers.py

from rest_framework import serializers
from .models import Category, Question, Answer, QuizAttempt

class AnswerSerializer(serializers.ModelSerializer):
    """Serializer dla odpowiedzi (bez informacji o poprawności)."""
    
    class Meta:
        model = Answer
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer dla pytań z odpowiedziami."""
    answers = AnswerSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id',
            'category_name',
            'text',
            'difficulty',
            'question_type',
            'points',
            'answers'
        ]

class QuizAttemptSerializer(serializers.ModelSerializer):
    """Serializer dla prób quizowych."""
    question_text = serializers.CharField(source='question.text', read_only=True)
    selected_answer_text = serializers.CharField(
        source='selected_answer.text',
        read_only=True
    )
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id',
            'question_text',
            'selected_answer_text',
            'is_correct',
            'points_earned',
            'time_taken',
            'attempted_at'
        ]
        read_only_fields = ['is_correct', 'points_earned']

class QuizSubmitSerializer(serializers.Serializer):
    """Serializer dla wysyłania odpowiedzi na quiz."""
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()
    time_taken = serializers.IntegerField(default=0)
    
    def validate_question_id(self, value):
        """Walidacja czy pytanie istnieje."""
        if not Question.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Nieprawidłowe pytanie.")
        return value
    
    def validate_answer_id(self, value):
        """Walidacja czy odpowiedź istnieje."""
        if not Answer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Nieprawidłowa odpowiedź.")
        return value
    
    def validate(self, data):
        """Walidacja czy odpowiedź należy do pytania."""
        question = Question.objects.get(id=data['question_id'])
        answer = Answer.objects.get(id=data['answer_id'])
        
        if answer.question != question:
            raise serializers.ValidationError(
                "Odpowiedź nie należy do tego pytania."
            )
        return data
```

### 6.3 API ViewSets

```python
# Lumen/api_views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, Question, QuizAttempt
from .serializers import (
    QuestionSerializer,
    QuizAttemptSerializer,
    QuizSubmitSerializer
)

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet dla quizów.
    
    list: GET /api/quizzes/ - Lista wszystkich kategorii
    retrieve: GET /api/quizzes/{id}/ - Szczegóły kategorii
    questions: GET /api/quizzes/{id}/questions/ - Pytania z kategorii
    submit: POST /api/quizzes/{id}/submit/ - Wysłanie odpowiedzi
    """
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """
        Pobiera losowe pytania z danej kategorii.
        
        Query params:
            amount (int): Liczba pytań (domyślnie 10)
            difficulty (str): Poziom trudności (easy/medium/hard)
        """
        category = self.get_object()
        amount = int(request.query_params.get('amount', 10))
        difficulty = request.query_params.get('difficulty', None)
        
        questions = Question.objects.filter(
            category=category,
            is_active=True
        )
        
        if difficulty:
            questions = questions.filter(difficulty=difficulty)
        
        questions = questions.order_by('?')[:amount]
        serializer = QuestionSerializer(questions, many=True)
        
        return Response({
            'category': category.name,
            'total_questions': amount,
            'questions': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Wysyła odpowiedź na pytanie.
        
        Body:
            {
                "question_id": 1,
                "answer_id": 3,
                "time_taken": 15
            }
        """
        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question = get_object_or_404(
            Question,
            id=serializer.validated_data['question_id']
        )
        answer = get_object_or_404(
            Answer,
            id=serializer.validated_data['answer_id']
        )
        
        # Utwórz próbę
        attempt = QuizAttempt.objects.create(
            user=request.user,
            question=question,
            selected_answer=answer,
            time_taken=serializer.validated_data.get('time_taken', 0)
        )
        
        return Response({
            'success': True,
            'is_correct': attempt.is_correct,
            'points_earned': attempt.points_earned,
            'correct_answer': question.get_correct_answer().text if not attempt.is_correct else None,
            'explanation': question.explanation if question.explanation else None
        }, status=status.HTTP_201_CREATED)
```

---

