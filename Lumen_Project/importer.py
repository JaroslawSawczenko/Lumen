import requests
import sys
import html
import random
from typing import Dict, Any, List, Optional

LUMEN_API_URL: str = "http://127.0.0.1:8000/api/quizzes/"
OPENTDB_API_URL: str = "https://opentdb.com/api.php"

def get_session_id() -> str:
    """Prosi użytkownika o podanie session_id i sprawdza, czy nie jest puste."""
    print("--- Krok 1: Uwierzytelnienie ---")
    print("1. Otwórz przeglądarkę i zaloguj się do panelu admina Lumen.")
    print("2. Otwórz narzędzia deweloperskie (F12) -> Application -> Cookies.")
    print("3. Znajdź cookie o nazwie 'sessionid' i skopiuj jego wartość.")
    session_id: str = input("Wklej skopiowaną wartość sessionid tutaj: ").strip()
    if not session_id:
        print("\nBŁĄD: Session ID nie może być puste. Przerywam.", file=sys.stderr)
        sys.exit(1)
    return session_id


def fetch_quizzes_from_opentdb(amount: int, category: int) -> List[Dict[str, Any]]:
    """Pobiera pytania z Open Trivia DB."""
    params: Dict[str, Any] = {'amount': amount, 'category': category, 'type': 'multiple'}
    try:
        response: requests.Response = requests.get(OPENTDB_API_URL, params=params)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        if data.get("response_code") != 0:
            print(
                f"BŁĄD: API Open Trivia DB zwróciło kod błędu. Być może nie ma wystarczającej liczby pytań dla tej kategorii.",
                file=sys.stderr)
            return []
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się połączyć z Open Trivia DB API: {e}", file=sys.stderr)
        return []


def post_quiz_to_lumen(quiz_payload: Dict[str, Any], session_id: str) -> bool:
    """Wysyła w pełni sformatowany quiz do API Lumen."""
    # --- POPRAWKA: Dodano nagłówek X-CSRFToken dla pełnego uwierzytelnienia sesji ---
    headers: Dict[str, str] = {
        'Cookie': f'sessionid={session_id}',
        'X-CSRFToken': session_id
    }
    try:
        response: requests.Response = requests.post(LUMEN_API_URL, json=quiz_payload, headers=headers)
        if 200 <= response.status_code < 300:
            print(f"SUCCESS: Quiz '{quiz_payload.get('title', 'Bez tytułu')}' został pomyślnie utworzony.")
            return True
        else:
            print(f"BŁĄD: Serwer Lumen odpowiedział ze statusem {response.status_code}", file=sys.stderr)
            print(f"Odpowiedź serwera: {response.text}", file=sys.stderr)
            if response.status_code == 403:
                print(
                    "INFO: Błąd 403 (Forbidden) najczęściej oznacza problem z session_id. Upewnij się, że jesteś zalogowany i skopiowałeś poprawną wartość.",
                    file=sys.stderr)
            return False
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się wysłać quizu do Lumen API: {e}", file=sys.stderr)
        return False


def transform_data(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Transformuje dane z OpenTDB na format oczekiwany przez API Lumen."""
    category_name: str = html.unescape(questions[0]['category'])

    questions_payload: List[Dict[str, Any]] = []
    for i, q in enumerate(questions):
        answers_data: List[Dict[str, Any]] = [
            {'text': html.unescape(ans), 'is_correct': False} for ans in q['incorrect_answers']
        ]
        answers_data.append({'text': html.unescape(q['correct_answer']), 'is_correct': True})
        random.shuffle(answers_data)

        # --- POPRAWKA: Dodano automatyczne numerowanie pytań ('order') ---
        questions_payload.append({
            "text": html.unescape(q['question']),
            "order": i + 1,
            "answers": answers_data
        })

    quiz_payload: Dict[str, Any] = {
        "title": f"Quiz: {category_name} (Auto-Import)",
        "description": f"Quiz z {len(questions)} pytaniami.",
        "category": category_name,
        "is_published": True,
        "questions": questions_payload
    }
    return quiz_payload


def main() -> None:
    """Główna funkcja orkiestrująca."""
    session_id: str = get_session_id()

    questions_amount: int = 15
    # --- POPRAWKA: Zmieniono ID na poprawne dla "Science: Computers" ---
    category_id: int = 18

    print(f"\n--- Krok 2: Pobieranie danych ---")
    questions: List[Dict[str, Any]] = fetch_quizzes_from_opentdb(questions_amount, category_id)
    if not questions:
        print("Nie pobrano pytań. Zakończono.")
        return

    print(f"Pobrano {len(questions)} pytań. Transformuję dane...")
    full_quiz_payload: Dict[str, Any] = transform_data(questions)

    print(f"\n--- Krok 3: Wysyłanie do Lumen API ---")
    post_quiz_to_lumen(full_quiz_payload, session_id)

if __name__ == "__main__":
    main()