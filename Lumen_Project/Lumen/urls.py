from django.urls import path
from .views import question_list

urlpatterns = [
    path('', question_list, name="question_list"),
]