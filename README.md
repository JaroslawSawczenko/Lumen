# 🧠 Lumen Quiz Platform

**Profesjonalna platforma e-learningowa stworzona w Django.**  
Aplikacja umożliwia rozwiązywanie quizów, śledzenie postępów, rywalizację o wyniki oraz dynamiczne zarządzanie bazą pytań.

---

## 📋 Spis Treści

1. [O Projekcie](#-o-projekcie)  
2. [Funkcjonalności](#-funkcjonalności)  
3. [Technologie](#-technologie)  
4. [Instalacja — krok po kroku](#-instalacja-krok-po-kroku)  
5. [Konfiguracja (.env)](#-konfiguracja-env)  
6. [Importowanie pytań (OpenTDB)](#-importowanie-pytań-opentdb)  
7. [Struktura projektu](#-struktura-projektu)  
8. [Autor i kontakt](#-autor-i-kontakt)

---

## 🚀 O Projekcie

**Lumen** to nowoczesna aplikacja webowa typu Quiz, łącząca prosty, responsywny interfejs z solidnym backendem. Została zaprojektowana z myślą o skalowalności i łatwej rozbudowie. System wspiera rejestrację użytkowników, profile z awatarami oraz zaawansowaną logikę punktacji i historii wyników.

---

## ✨ Funkcjonalności

### 👤 Dla użytkownika
- **System kont:** rejestracja, logowanie i bezpieczne sesje.  
- **Profil użytkownika:** awatar, biogram, statystyki (wyniki, XP).  
- **Interaktywne quizy:** natychmiastowa informacja zwrotna.  
- **Historia wyników:** zapis każdego podejścia z procentowym wynikiem.

### ⚙️ Dla administratora
- **Panel admina:** zarządzanie pytaniami, odpowiedziami, kategoriami.  
- **Importer pytań:** automatyczne pobieranie pytań z Open Trivia Database.  
- **API REST:** gotowe endpointy dla zewnętrznych klientów (frontend, mobile).

---

## 🛠 Technologie

- **Backend:** Python 3.10+ / Django 5.2  
- **API:** Django REST Framework  
- **Baza danych:** SQLite (dev) / PostgreSQL (prod)  
- **Frontend:** HTML5, CSS3, Bootstrap 5  
- **Grafika:** Pillow (obsługa awatarów)  
- **Konfiguracja:** python-dotenv

---

## 💻 Instalacja — krok po kroku

> Instrukcja zakłada posiadanie zainstalowanego Pythona i Gita.

1. **Sklonuj repozytorium**
```bash
git clone https://github.com/jaroslawsawczenko/lumen.git
cd lumen ```
2. Utwórz wirtualne środowisko

