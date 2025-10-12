import requests
import sys
import html
import random
from typing import Dict, Any, List

# --- STAŁE ---
LUMEN_API_URL: str = "http://127.0.0.1:8000/api/quizzes/"
LOGIN_URL: str = "http://127.0.0.1:8000/users/login/"
OPENTDB_API_URL: str = "https://opentdb.com/api.php"

# Lista ciekawych kategorii z Open Trivia DB
CATEGORIES = {
    "Historia": 23, "Geografia": 22, "Nauka i Natura": 17, "Komputery": 18,
    "Filmy": 11, "Muzyka": 12, "Gry Wideo": 15, "Mitologia": 20,
}


def authenticate_and_get_csrf(session: requests.Session) -> str | None:
    """
    Uwierzytelnia sesję w aplikacji Lumen i pozyskuje token CSRF.

    Funkcja symuluje zalogowanego użytkownika poprzez ustawienie ciasteczka 'sessionid'.
    Następnie pozyskuje token CSRF, który jest niezbędny do wykonywania
    bezpiecznych zapytań typu POST.

    Args:
        session: Obiekt sesji z biblioteki 'requests', który przechowuje stan
                 (np. ciasteczka) pomiędzy zapytaniami.

    Returns:
        Token CSRF jako string, jeśli uwierzytelnienie się powiodło.
        None w przypadku błędu.
    """
    print("--- Krok 1: Uwierzytelnienie ---")
    print("Proszę podać 'sessionid' z ciasteczek przeglądarki po zalogowaniu do panelu admina.")
    session_id = input("Wklej wartość sessionid: ").strip()
    if not session_id:
        print("\nBŁĄD: Session ID nie może być puste.", file=sys.stderr)
        return None

    session.cookies.set('sessionid', session_id)
    try:
        response = session.get(LOGIN_URL)
        response.raise_for_status()
        csrf_token = session.cookies.get('csrftoken')
        if not csrf_token:
            print("\nBŁĄD: Nie udało się uzyskać tokena CSRF. Sprawdź, czy sessionid jest poprawne.", file=sys.stderr)
            return None
        # POPRAWKA: Usunięto emoji
        print("SUCCESS: Pomyślnie uzyskano dane uwierzytelniające.")
        return csrf_token
    except requests.RequestException:
        print(f"\nBŁĄD: Nie udało się połączyć z serwerem Lumen. Upewnij się, że serwer działa w drugim terminalu.",
              file=sys.stderr)
        return None


def fetch_quizzes_from_opentdb(amount: int, category_id: int, category_name: str) -> List[Dict[str, Any]]:
    """
    Pobiera zdefiniowaną liczbę pytań z wybranej kategorii z Open Trivia DB API.

    Args:
        amount: Liczba pytań do pobrania.
        category_id: Numeryczny identyfikator kategorii w API OpenTDB.
        category_name: Nazwa kategorii (używana do logowania).

    Returns:
        Lista słowników, gdzie każdy słownik reprezentuje jedno pytanie,
        lub pusta lista w przypadku błędu.
    """
    params = {'amount': amount, 'category': category_id, 'type': 'multiple'}
    try:
        response = requests.get(OPENTDB_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("response_code") != 0:
            print(f"BŁĄD: Brak pytań w kategorii '{category_name}'. Spróbuj ponownie.", file=sys.stderr)
            return []
        # POPRAWKA: Usunięto emoji
        print(f"SUCCESS: Pobrano {len(data.get('results', []))} pytań z kategorii '{category_name}'.")
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się połączyć z Open Trivia DB API: {e}", file=sys.stderr)
        return []


def post_quiz_to_lumen(session: requests.Session, quiz_payload: Dict[str, Any], csrf_token: str) -> bool:
    """
    Wysyła przygotowany quiz w formacie JSON do API aplikacji Lumen.

    Args:
        session: Uwierzytelniony obiekt sesji 'requests'.
        quiz_payload: Słownik zawierający pełne dane quizu (tytuł, pytania, odpowiedzi).
        csrf_token: Token CSRF wymagany do autoryzacji zapytania.

    Returns:
        True, jeśli quiz został pomyślnie utworzony.
        False w przypadku błędu.
    """
    headers = {'X-CSRFToken': csrf_token, 'Referer': LOGIN_URL}
    try:
        response = session.post(LUMEN_API_URL, json=quiz_payload, headers=headers)
        if 200 <= response.status_code < 300:
            # POPRAWKA: Usunięto emoji
            print(f"SUCCESS: Quiz '{quiz_payload.get('title')}' został pomyślnie utworzony!")
            return True
        else:
            print(f"BŁĄD: Serwer Lumen odpowiedział ze statusem {response.status_code}", file=sys.stderr)
            print(f"Odpowiedź serwera: {response.text}", file=sys.stderr)
            return False
    except requests.RequestException as e:
        print(f"\nBŁĄD: Nie udało się wysłać quizu do Lumen API: {e}", file=sys.stderr)
        return False


def transform_data(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Konwertuje surowe dane pytań z OpenTDB na strukturę zgodną z API Lumen.

    Funkcja czyści tekst z encji HTML, tasuje odpowiedzi i buduje zagnieżdżoną
    strukturę JSON gotową do wysłania.

    Args:
        questions: Lista pytań pobrana z API OpenTDB.

    Returns:
        Kompletny słownik reprezentujący quiz, gotowy do serializacji na JSON.
    """
    category_name = html.unescape(questions[0]['category'])
    questions_payload = []

    for i, q in enumerate(questions):
        answers_data = [{'text': html.unescape(ans), 'is_correct': False} for ans in q['incorrect_answers']]
        answers_data.append({'text': html.unescape(q['correct_answer']), 'is_correct': True})
        random.shuffle(answers_data)

        questions_payload.append({
            "text": html.unescape(q['question']),
            "order": i + 1,
            "answers": answers_data
        })

    quiz_payload = {
        "title": f"Quiz o {category_name}",
        "description": f"Quiz wygenerowany automatycznie z {len(questions)} pytaniami.",
        "category": category_name,
        "is_published": True,
        "questions": questions_payload
    }
    return quiz_payload


def main() -> None:
    """
    Główna funkcja orkiestrująca działanie skryptu.
    """
    with requests.Session() as session:
        csrf_token = authenticate_and_get_csrf(session)
        if not csrf_token:
            sys.exit(1)

        category_name, category_id = random.choice(list(CATEGORIES.items()))

        print(f"\n--- Krok 2: Pobieranie danych dla kategorii: {category_name} ---")
        questions = fetch_quizzes_from_opentdb(amount=10, category_id=category_id, category_name=category_name)
        if not questions:
            return

        print("\n--- Krok 3: Przetwarzanie i wysyłanie ---")
        full_quiz_payload = transform_data(questions)
        post_quiz_to_lumen(session, full_quiz_payload, csrf_token)

if __name__ == "__main__":
    main()