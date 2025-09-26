from django.shortcuts import render, get_object_or_404
from .models import Quiz
from django.http import HttpRequest, HttpResponse

def quiz_list(request: HttpRequest) -> HttpResponse:
    """
    Widok strony głównej, który wyświetla listę opublikowanych quizów.
    """
    quizzes = Quiz.objects.filter(is_published=True)
    context = {
        'quizzes': quizzes
    }
    return render(request, 'Lumen/Main.html', context)

def quiz_detail(request: HttpRequest, quiz_id: int) -> HttpResponse:
    """
    Widok wyświetlający stronę startową ("lobby") pojedynczego quizu.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {
        "quiz": quiz
    }
    return render(request, 'Lumen/quiz_detail.html', context)