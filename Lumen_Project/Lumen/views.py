from django.shortcuts import render, get_object_or_404
from .models import Quiz

def quiz_list(request):
    """
    Widok strony głównej, który wyświetla listę opublikowanych quizów.
    """
    quizzes = Quiz.objects.filter(is_published=True)
    context = {
        'quizzes': quizzes
    }
    return render(request, 'Lumen/Main.html', context)

def quiz_detail(request, quiz_id):
    """
    Widok wyświetlający stronę startową ("lobby") pojedynczego quizu.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {
        "quiz": quiz
    }
    return render(request, 'Lumen/quiz_detail.html', context)