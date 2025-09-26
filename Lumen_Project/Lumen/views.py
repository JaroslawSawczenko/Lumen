from django.shortcuts import render , get_object_or_404
from django.shortcuts import render
from .models import Quiz

def quiz_list(request):
    """
    Widok wyświetlający listę wszystkich opublikowanych quizów.
    """
    quizzes = Quiz.objects.filter(is_published=True)

    context = {
        'quizzes': quizzes
    }
    return render(request, 'Lumen/Main.html', context)

def registration(request) -> None:
    return render(request, 'Lumen/registration.html')


def profile(request) -> None:
    return render(request, 'Lumen/profile.html')


def quiz_detail(request, quiz_id:int) -> None:
    """
    Widok wyświetlający stronę startową pojedynczego quizu.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {"quiz":quiz}


    return render(request, 'Lumen/quiz_detail.html',context)
