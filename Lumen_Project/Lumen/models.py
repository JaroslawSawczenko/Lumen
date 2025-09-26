from django.db import models
from django.conf import settings

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")
    text = models.TextField()
    image = models.ImageField(upload_to="question_images/", blank=True, null=True)
    time_limit = models.IntegerField(default=30)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quiz.title} - Pytanie {self.order}"

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="answers")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:50]} - {self.text}"

class QuizResult(models.Model):
    """
    Model przechowujący wynik ukończonego przez użytkownika quizu.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score} pkt)"



