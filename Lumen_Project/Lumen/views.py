from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, QuizResult
from rest_framework import viewsets, permissions
from .serializers import QuizListSerializer, QuizDetailSerializer

def quiz_list(request: HttpRequest) -> HttpResponse:
    """
    Wyświetla listę quizów.
    - Superuserzy widzą wszystkie quizy.
    - Zwykli użytkownicy widzą tylko opublikowane quizy.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        quizzes = Quiz.objects.all().order_by('-created_at')
    else:
        quizzes = Quiz.objects.filter(is_published=True).order_by('-created_at')

    context = {'quizzes': quizzes}
    return render(request, 'Lumen/quiz_list.html', context)

def quiz_detail(request: HttpRequest, quiz_id: int) -> HttpResponse:
    """Wyświetla szczegóły konkretnego quizu."""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {"quiz": quiz}
    return render(request, 'Lumen/quiz_detail.html', context)

@login_required
def play_quiz_view(request: HttpRequest, quiz_id: int, question_order: int) -> HttpResponse:
    """
    Główna logika rozgrywki. Obsługuje wyświetlanie pytań i walidację odpowiedzi.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    try:
        question = Question.objects.get(quiz=quiz, order=question_order)
    except Question.DoesNotExist:
        # Jeśli pytanie o danym numerze nie istnieje, przekieruj na stronę quizu
        return redirect('quiz_detail', quiz_id=quiz.id)

    # Inicjalizacja sesji na pierwszym pytaniu
    if question_order == 1:
        request.session[f'quiz_{quiz_id}_score'] = 0

    if request.method == "POST":
        selected_answer_id = request.POST.get('answer')
        if not selected_answer_id:
            # Jeśli nie wybrano odpowiedzi, wyrenderuj stronę ponownie z komunikatem o błędzie
            context = {
                'quiz': quiz,
                'question': question,
                'answers': question.answers.all(),
                'total_questions': quiz.questions.count(),
                'is_answered': False,
                'error_message': 'Musisz wybrać jedną z odpowiedzi.'  # Dodajemy błąd do kontekstu
            }
            return render(request, "Lumen/play_quiz.html", context)

        selected_answer = get_object_or_404(Answer, pk=selected_answer_id)
        correct_answer = question.answers.get(is_correct=True)

        if selected_answer.is_correct:
            request.session[f'quiz_{quiz_id}_score'] = request.session.get(f'quiz_{quiz_id}_score', 0) + 10
            request.session.save()

        context = {
            'quiz': quiz,
            'question': question,
            'total_questions': quiz.questions.count(),
            'is_answered': True,
            'selected_answer': selected_answer,
            'correct_answer': correct_answer
        }
        return render(request, "Lumen/play_quiz.html", context)

    # Logika dla metody GET (pierwsze wyświetlenie pytania)
    context = {
        'quiz': quiz,
        'question': question,
        'answers': question.answers.all(),
        'total_questions': quiz.questions.count(),
        'is_answered': False
    }
    return render(request, "Lumen/play_quiz.html", context)


@login_required
def finish_quiz_view(request: HttpRequest, quiz_id: int) -> HttpResponse:
    """
    Kończy quiz, oblicza ostateczny wynik, zapisuje go i przyznaje XP.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    raw_score = request.session.get(f'quiz_{quiz_id}_score', 0)

    previous_attempts = QuizResult.objects.filter(user=request.user, quiz=quiz).count()
    multiplier = 1.0 / (2 ** previous_attempts)
    final_score = int(raw_score * multiplier)

    QuizResult.objects.create(user=request.user, quiz=quiz, score=final_score)
    request.user.profile.add_xp(final_score)

    # Wyczyść wynik z sesji, aby nie został przy następnej próbie
    if f'quiz_{quiz_id}_score' in request.session:
        del request.session[f'quiz_{quiz_id}_score']

    return redirect('user_profile')


class QuizViewSet(viewsets.ModelViewSet):
    """ Pełny ViewSet do zarządzania quizami przez API. """
    queryset = Quiz.objects.prefetch_related('questions__answers').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return QuizListSerializer if self.action == 'list' else QuizDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)