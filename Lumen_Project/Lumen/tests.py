from http.client import responses

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Quiz
from django.urls import  reverse
from rest_framework.test import APITestCase
from rest_framework import status


class QuizVisibilityTest(TestCase):
    """Testuje logikę wyświetlania quizów dla różnych typów użytkowników."""

    def setUp(self):
        """Przygotowuje dane testowe przed każdym testem."""
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.user = User.objects.create_user('user', 'user@test.com', 'password')

        Quiz.objects.create(
            title="Opublikowany Quiz",
            created_by=self.superuser,
            is_published=True
        )
        Quiz.objects.create(
            title="Nieopublikowany Draft",
            created_by=self.superuser,
            is_published=False
        )

    def test_regular_user_sees_only_published_quizzes(self):
        """Zwykły użytkownik powinien widzieć tylko opublikowane quizy."""
        self.client.login(username='user', password='password')
        response = self.client.get('/') # Odpytujemy stronę główną
        self.assertContains(response, "Opublikowany Quiz")
        self.assertNotContains(response, "Nieopublikowany Draft")

    def test_superuser_sees_all_quizzes(self):
        """Superuser powinien widzieć wszystkie quizy."""
        self.client.login(username='admin', password='password')
        response = self.client.get('/')
        self.assertContains(response, "Opublikowany Quiz")
        self.assertContains(response, "Nieopublikowany Draft")


class QuizAPITest(APITestCase):
    def setUp(self):
        # Tworzymy użytkownika, który będzie autorem quizu
        self.user = User.objects.create_user('apiuser', 'api@test.com', 'apipassword')

    def test_create_quiz_via_api(self):
        """Sprawdza, czy API pozwala na utworzenie pełnego quizu."""
        # Logujemy użytkownika, aby móc wysyłać zapytania
        self.client.force_authenticate(user=self.user)

        url = reverse('quiz-list')  # Nazwa 'quiz-list' pochodzi z routera w urls.py
        data = {
            "title": "API Test Quiz",
            "description": "Quiz utworzony przez test API.",
            "category": "Testing",
            "is_published": True,
            "questions": [
                {
                    "text": "Jaka jest odpowiedź?",
                    "order": 1,
                    "answers": [
                        {"text": "Zła odpowiedź", "is_correct": False},
                        {"text": "Dobra odpowiedź", "is_correct": True},
                    ]
                }
            ]
        }

        response = self.client.post(url, data, format='json')

        # Sprawdzamy, czy serwer odpowiedział kodem 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Sprawdzamy, czy quiz faktycznie został zapisany w bazie
        self.assertEqual(Quiz.objects.count(), 2)  # 2, bo setUp z QuizVisibilityTest też tworzy quizy
        self.assertTrue(Quiz.objects.filter(title="API Test Quiz").exists())















