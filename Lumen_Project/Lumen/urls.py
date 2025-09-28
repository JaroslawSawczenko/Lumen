from django.urls import path
from .views import quiz_list, quiz_detail, play_quiz_view

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path("quiz/<int:quiz_id>/pytanie/<int:question_order>", play_quiz_view, name="play_quiz_view" ),
]