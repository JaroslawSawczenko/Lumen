from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileXPTest(TestCase):
    """Testuje mechanizm dodawania XP i awansowania na wyższe poziomy."""

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.profile = self.user.profile

    def test_add_xp_and_level_up(self):
        """Testuje, czy dodanie wystarczającej ilości XP powoduje awans."""
        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.xp, 0)

        # Poziom 1 wymaga 100 XP
        self.profile.add_xp(50)
        self.assertEqual(self.profile.xp, 50)
        self.assertEqual(self.profile.level, 1)

        self.profile.add_xp(60) # Łącznie 110 XP
        # Powinien awansować na poziom 2 i mieć 10 XP
        self.assertEqual(self.profile.level, 2)
        self.assertEqual(self.profile.xp, 10)



















