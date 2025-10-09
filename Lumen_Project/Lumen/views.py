from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, QuizResult
from rest_framework import viewsets, permissions
from .serializers import QuizListSerializer , QuizDetailSerializer

@login_required
def play_quiz_view(request: HttpRequest, quiz_id: int, question_order: int) -> HttpResponse:
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if question_order == 1:
        request.session[f'quiz_{quiz_id}_score'] = 0

    if request.method == "POST":
        selected_answer_id = request.POST.get('answer')

        if selected_answer_id:
            selected_answer = get_object_or_404(Answer, pk=selected_answer_id)
            if selected_answer.is_correct:
                request.session[f'quiz_{quiz_id}_score'] += 10

        next_question_order = question_order + 1
        try:
            Question.objects.get(quiz=quiz, order=next_question_order)
            return redirect('play_quiz_view', quiz_id=quiz.id, question_order=next_question_order)

        except Question.DoesNotExist:
            # Koniec quizu - obliczamy ostateczny wynik
            raw_score = request.session.get(f'quiz_{quiz_id}_score', 0)

            # Policz, ile razy użytkownik już ukończył ten quiz
            previous_attempts = QuizResult.objects.filter(user=request.user, quiz=quiz).count()

            # Oblicz mnożnik. Za pierwszym razem (0 prób) mnożnik to 1.0,
            # za drugim (1 próba) to 0.5, za trzecim 0.25 itd.
            multiplier = 1.0 / (2 ** previous_attempts)
            final_score = int(raw_score * multiplier)

            QuizResult.objects.create(
                user=request.user,
                quiz = quiz,
                score=final_score
            )

            request.user.profile.add_xp(final_score)

            # Wyczyść wynik z sesji
            del request.session[f'quiz_{quiz_id}_score']
            return redirect('user_profile')

    try:
        question = Question.objects.get(quiz=quiz, order=question_order)
        answers = question.answers.all()

    except Question.DoesNotExist:
        return redirect('quiz_detail', quiz_id=quiz.id)

    context = {
        "quiz": quiz,
        'question': question,
        "answers": answers,
        "total_questions": quiz.questions.count(),
    }

    return render(request, "Lumen/play_quiz.html", context)

def quiz_list(request: HttpRequest) -> HttpResponse:
    """
    Wyświetla listę quizów.
    - Superuserzy widzą wszystkie quizy (opublikowane i nieopublikowane).
    - Zwykli użytkownicy widzą tylko opublikowane quizy.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        # Administrator widzi wszystkie quizy
        quizzes = Quiz.objects.all().order_by('-created_at')
    else:
        # Zwykły użytkownik widzi tylko opublikowane quizy
        quizzes = Quiz.objects.filter(is_published=True).order_by('-created_at')

    context = {
        'quizzes': quizzes
    }
    return render(request, 'Lumen/Main.html', context)

def quiz_detail(request: HttpRequest, quiz_id: int) -> HttpResponse:
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {
        "quiz": quiz
    }
    return render(request, 'Lumen/quiz_detail.html', context)


class QuizViewSet(viewsets.ModelViewSet):
    """
    Pełny ViewSet do zarządzania quizami.
    """
    # --- POPRAWKA: Usunięto .filter(is_published=True) ---
    # Administrator w API powinien widzieć wszystkie quizy, także te nieopublikowane.
    queryset = Quiz.objects.prefetch_related('questions__answers').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizListSerializer
        return QuizDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)