from django.urls import path
from .views import profile_view, signup_view

urlpatterns = [
    path('profile/', profile_view, name='user_profile'),
    path('signup/', signup_view, name="signup")
]