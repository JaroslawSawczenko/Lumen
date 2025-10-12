from django.test import TestCase
from django.contrib.auth.models import User
from .models import Quiz

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



