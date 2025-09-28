from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, QuizResult

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
            final_score = request.session.get(f'quiz_{quiz_id}_score', 0)
            QuizResult.objects.create(
                user=request.user,
                quiz=quiz,
                score=final_score
            )
            request.user.profile.add_xp(final_score)
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
    quizzes = Quiz.objects.filter(is_published=True)
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