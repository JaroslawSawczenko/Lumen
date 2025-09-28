from django.urls import path
from .views import profile_view, SignUpView

urlpatterns = [
    path('profile/', profile_view, name='user_profile'),
    path('signup/', SignUpView.as_view(), name="signup")
]