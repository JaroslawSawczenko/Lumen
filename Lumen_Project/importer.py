import requests
import sys
import html
import random
from typing import Dict, Any, List, Optional

LUMEN_API_URL: str = "http://127.0.0.1:8000/api/quizzes/"
LOGIN_URL: str = "http://127.0.0.1:8000/users/login/"  # Potrzebny do pobrania CSRF tokena
OPENTDB_API_URL: str = "https://opentdb.com/api.php"


def get_credentials() -> Dict[str, str]:
    """Pobiera od użytkownika sessionid i na jego podstawie zdobywa csrftoken."""
    print("--- Krok 1: Uwierzytelnienie ---")
    print("1. Zaloguj się do panelu admina Lumen w przeglądarce.")
    print("2. Otwórz narzędzia deweloperskie (F12) -> Application -> Cookies.")
    print("3. Znajdź i skopiuj wartość cookie o nazwie 'sessionid'.")
    session_id: str = input("Wklej wartość sessionid: ").strip()
    if not session_id:
        print("\nBŁĄD: Session ID nie może być puste.", file=sys.stderr)
        sys.exit(1)

    try:
        # Używamy sesji, aby automatycznie zarządzać ciasteczkami
        with requests.Session() as s:
            s.cookies.set('sessionid', session_id)
            # Wykonujemy zapytanie GET, aby serwer odesłał nam CSRF token
            response = s.get(LOGIN_URL)
            response.raise_for_status()
            # Wyciągamy csrftoken z ciasteczek sesji
            csrf_token = s.cookies.get('csrftoken')
            if not csrf_token:
                print("\nBŁĄD: Nie udało się uzyskać tokena CSRF. Sprawdź, czy sessionid jest poprawne.",
                      file=sys.stderr)
                sys.exit(1)

            print("SUCCESS: Pomyślnie uzyskano dane uwierzytelniające.")
            return {'session_id': session_id, 'csrf_token': csrf_token}
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się połączyć z serwerem Lumen w celu uzyskania CSRF: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_quizzes_from_opentdb(amount: int, category: int) -> List[Dict[str, Any]]:
    # ... (ta funkcja pozostaje bez zmian)
    params: Dict[str, Any] = {'amount': amount, 'category': category, 'type': 'multiple'}
    try:
        response: requests.Response = requests.get(OPENTDB_API_URL, params=params)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        if data.get("response_code") != 0:
            print(f"BŁĄD: API Open Trivia DB zwróciło błąd.", file=sys.stderr)
            return []
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się połączyć z Open Trivia DB API: {e}", file=sys.stderr)
        return []


def post_quiz_to_lumen(quiz_payload: Dict[str, Any], credentials: Dict[str, str]) -> bool:
    """Wysyła w pełni sformatowany quiz do API Lumen z poprawnym uwierzytelnieniem."""
    headers: Dict[str, str] = {
        'Cookie': f"sessionid={credentials['session_id']}; csrftoken={credentials['csrf_token']}",
        'X-CSRFToken': credentials['csrf_token'],
        'Referer': LOGIN_URL  # Dodatkowy nagłówek często wymagany przez Django
    }
    try:
        response: requests.Response = requests.post(LUMEN_API_URL, json=quiz_payload, headers=headers)
        if 201 <= response.status_code < 300:
            print(
                f"SUCCESS: Quiz '{quiz_payload.get('title')}' został pomyślnie utworzony (Status: {response.status_code}).")
            return True
        else:
            print(f"BŁĄD: Serwer Lumen odpowiedział ze statusem {response.status_code}", file=sys.stderr)
            print(f"Odpowiedź serwera: {response.text}", file=sys.stderr)
            return False
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się wysłać quizu do Lumen API: {e}", file=sys.stderr)
        return False


def transform_data(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    # ... (ta funkcja pozostaje bez zmian)
    category_name: str = html.unescape(questions[0]['category'])
    questions_payload: List[Dict[str, Any]] = []
    for i, q in enumerate(questions):
        answers_data: List[Dict[str, Any]] = [{'text': html.unescape(ans), 'is_correct': False} for ans in
                                              q['incorrect_answers']]
        answers_data.append({'text': html.unescape(q['correct_answer']), 'is_correct': True})
        random.shuffle(answers_data)
        questions_payload.append({"text": html.unescape(q['question']), "order": i + 1, "answers": answers_data})
    quiz_payload: Dict[str, Any] = {"title": f"Quiz: {category_name} (Auto-Import)",
                                    "description": f"Quiz z {len(questions)} pytaniami.", "category": category_name,
                                    "is_published": True, "questions": questions_payload}
    return quiz_payload


def main() -> None:
    """Główna funkcja orkiestrująca."""
    credentials = get_credentials()

    questions_amount: int = 15
    category_id: int = 18

    print(f"\n--- Krok 2: Pobieranie danych ---")
    questions: List[Dict[str, Any]] = fetch_quizzes_from_opentdb(questions_amount, category_id)
    if not questions:
        return

    print(f"Pobrano {len(questions)} pytań. Transformuję dane...")
    full_quiz_payload: Dict[str, Any] = transform_data(questions)

    print(f"\n--- Krok 3: Wysyłanie do Lumen API ---")
    post_quiz_to_lumen(full_quiz_payload, credentials)


if __name__ == "__main__":
    main()