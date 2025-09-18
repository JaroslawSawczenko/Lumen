from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"Profil {self.user.username}"
