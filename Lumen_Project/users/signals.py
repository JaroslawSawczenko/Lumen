from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs)-> None:
    """
    Sygnał, który automatycznie tworzy UserProfile,
    gdy tylko nowy obiekt User zostanie zapisany w bazie danych.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender: type[User], instance: User, **kwargs) -> None:
    """
    Sygnał, który zapisuje UserProfile za każdym razem,
    gdy obiekt User jest zapisywany.
    """
    instance.profile.save()