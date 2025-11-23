from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Quiz, Question, Answer, QuizResult
from rest_framework import viewsets, permissions
from .serializers import QuizListSerializer, QuizDetailSerializer


def quiz_list(request: HttpRequest) -> HttpResponse:
    # Optymalizacja: select_related pobiera Autora w 1 zapytaniu, zamiast N zapytań
    base_qs = Quiz.objects.select_related('created_by').order_by('-created_at')

    if request.user.is_authenticated and request.user.is_superuser:
        quizzes = base_qs.all()
    else:
        quizzes = base_qs.filter(is_published=True)

    context = {'quizzes': quizzes}
    return render(request, 'Lumen/quiz_list.html', context)


def quiz_detail(request: HttpRequest, quiz_id: int) -> HttpResponse:
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {"quiz": quiz}
    return render(request, 'Lumen/quiz_detail.html', context)


@login_required
def play_quiz_view(request: HttpRequest, quiz_id: int, question_order: int) -> HttpResponse:
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Pobieramy pytanie lub przekierowujemy na koniec
    try:
        question = Question.objects.get(quiz=quiz, order=question_order)
    except Question.DoesNotExist:
        return redirect('finish_quiz_view', quiz_id=quiz.id)

    # Reset wyniku przy starcie (pytanie nr 1)
    if question_order == 1:
        request.session[f'quiz_{quiz_id}_score'] = 0

    if request.method == "POST":
        selected_answer_id = request.POST.get('answer')
        if not selected_answer_id:
            context = {
                'quiz': quiz,
                'question': question,
                'answers': question.answers.all(),
                'total_questions': quiz.questions.count(),
                'is_answered': False,
                'error_message': 'Musisz wybrać jedną z odpowiedzi.'
            }
            return render(request, "Lumen/play_quiz.html", context)

        selected_answer = get_object_or_404(Answer, pk=selected_answer_id)
        correct_answer = question.answers.filter(is_correct=True).first()

        # Zabezpieczenie: czy odpowiedź należy do tego pytania?
        if selected_answer.question != question:
            return HttpResponse("Nieprawidłowa odpowiedź", status=400)

        if selected_answer.is_correct:
            current_score = request.session.get(f'quiz_{quiz_id}_score', 0)
            request.session[f'quiz_{quiz_id}_score'] = current_score + 10

        context = {
            'quiz': quiz,
            'question': question,
            'total_questions': quiz.questions.count(),
            'is_answered': True,
            'selected_answer': selected_answer,
            'correct_answer': correct_answer
        }
        return render(request, "Lumen/play_quiz.html", context)

    context = {
        'quiz': quiz,
        'question': question,
        'answers': question.answers.all(),
        'total_questions': quiz.questions.count(),
        'is_answered': False
    }
    return render(request, "Lumen/play_quiz.html", context)


@login_required
@transaction.atomic  # Ważne: zapewnia spójność bazy danych
def finish_quiz_view(request: HttpRequest, quiz_id: int) -> HttpResponse:
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Używamy .pop(), aby pobrać wynik i usunąć go z sesji (zapobiega odświeżaniu strony dla punktów)
    raw_score = request.session.pop(f'quiz_{quiz_id}_score', 0)

    # Zliczamy poprzednie podejścia
    previous_attempts = QuizResult.objects.filter(user=request.user, quiz=quiz).count()

    # Algorytm: za każde kolejne podejście dostajesz 20% mniej punktów, ale nie mniej niż 10% oryginału
    multiplier = max(0.1, 1.0 - (previous_attempts * 0.2))
    final_score = int(raw_score * multiplier)

    # Zapisujemy wynik
    QuizResult.objects.create(user=request.user, quiz=quiz, score=final_score)

    # Dodajemy XP do profilu
    request.user.profile.add_xp(final_score)

    messages.success(request, f"Ukończono quiz! Zdobyto {final_score} XP (Mnożnik: {multiplier:.1f}x)")
    return redirect('user_profile')


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.prefetch_related('questions__answers').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return QuizListSerializer if self.action == 'list' else QuizDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)