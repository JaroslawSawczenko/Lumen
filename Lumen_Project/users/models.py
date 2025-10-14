from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"Profil {self.user.username}"

    @property
    def xp_required_for_next_level(self) -> int:
        """
        Oblicza, ile XP potrzeba, by osiągnąć następny poziom.
        Używa algorytmu wykładniczego, aby każdy poziom był trudniejszy.
        """
        if self.level < 1:
            return 100
        return int(100 * (self.level ** 1.5))

    @property
    def xp_progress_percentage(self) -> float:
        """Oblicza postęp XP jako procent potrzebny do następnego poziomu."""
        required_xp = self.xp_required_for_next_level
        # Unikamy dzielenia przez zero, jeśli z jakiegoś powodu wymagane XP będzie 0
        if required_xp == 0:
            return 100
        progress = (self.xp / required_xp) * 100
        return min(progress, 100)

    def add_xp(self, amount: int) -> None:
        """Dodaje punkty XP i sprawdza, czy użytkownik powinien awansować."""
        if amount < 0:
            return  # Ignoruj ujemne wartości

        self.xp += amount
        # Pętla while na wypadek, gdyby użytkownik zdobył tyle XP, by awansować o kilka poziomów na raz
        while self.xp >= self.xp_required_for_next_level:
            self.xp -= self.xp_required_for_next_level
            self.level += 1
        self.save()