from django.urls import path
from .views import profile_view, signup_view, activate

urlpatterns = [
    path('profile/', profile_view, name='user_profile'),
    path('signup/', signup_view, name="signup"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]