import requests
import html
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Lumen.models import Quiz, Question, Answer

User = get_user_model()


class Command(BaseCommand):
    help = 'Pobiera quizy z Open Trivia DB i zapisuje w bazie danych'

    CATEGORIES = {
        "Historia": 23, "Geografia": 22, "Nauka i Natura": 17,
        "Komputery": 18, "Filmy": 11, "Muzyka": 12,
        "Gry Wideo": 15, "Mitologia": 20,
    }
    OPENTDB_API_URL = "https://opentdb.com/api.php"

    def handle(self, *args, **options):
        category_name, category_id = random.choice(list(self.CATEGORIES.items()))
        self.stdout.write(f"Pobieranie pytań dla kategorii: {category_name}...")

        params = {'amount': 10, 'category': category_id, 'type': 'multiple'}

        try:
            response = requests.get(self.OPENTDB_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("response_code") != 0:
                self.stdout.write(self.style.WARNING(f"Brak pytań dla {category_name}."))
                return

            results = data.get('results', [])
            self.create_quiz_from_data(category_name, results)

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Błąd połączenia: {e}"))

    def create_quiz_from_data(self, category_name, questions_data):
        # Tworzymy bota systemowego, jeśli nie istnieje
        bot_user, _ = User.objects.get_or_create(username='LumenBot', defaults={'email': 'bot@lumen.com'})

        quiz = Quiz.objects.create(
            title=f"Quiz o {category_name}",
            description=f"Automatycznie wygenerowany quiz z {len(questions_data)} pytaniami.",
            category=category_name,
            created_by=bot_user,
            is_published=True
        )

        questions_to_create = []
        answers_to_create = []

        for i, q_data in enumerate(questions_data):
            question = Question.objects.create(
                quiz=quiz,
                text=html.unescape(q_data['question']),
                order=i + 1
            )

            # Przygotowanie odpowiedzi
            ans_list = []
            ans_list.append(Answer(question=question, text=html.unescape(q_data['correct_answer']), is_correct=True))
            for incorrect in q_data['incorrect_answers']:
                ans_list.append(Answer(question=question, text=html.unescape(incorrect), is_correct=False))

            random.shuffle(ans_list)
            answers_to_create.extend(ans_list)

        # Bulk create dla wydajności (zapisuje wszystkie odpowiedzi jednym zapytaniem SQL)
        Answer.objects.bulk_create(answers_to_create)

        self.stdout.write(self.style.SUCCESS(f"Sukces! Utworzono quiz: '{quiz.title}'"))