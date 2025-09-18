from django.shortcuts import render
from .models import Question


def question_list(request):
    """
    Widok, który pobiera wszystkie pytania z bazy danych
    i przekazuje je do szablonu.
    """
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'Lumen/question_list.html', context)