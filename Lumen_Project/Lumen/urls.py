from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import quiz_list, quiz_detail, play_quiz_view, finish_quiz_view, QuizViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path("quiz/<int:quiz_id>/pytanie/<int:question_order>/", play_quiz_view, name="play_quiz_view"),
    path('quiz/<int:quiz_id>/finish/', finish_quiz_view, name='finish_quiz_view'),
    # Adresy URL wygenerowane przez router DRF dla naszego API
    path('api/', include(router.urls))
]