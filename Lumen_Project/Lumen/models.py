from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Quiz(models.Model):
    title = models.CharField(_("Tytuł"), max_length=200)
    description = models.TextField(_("Opis"), blank=True)
    category = models.CharField(_("Kategoria"), max_length=100, blank=True)
    # Dodano slug i image (z poprzednich migracji)
    image = models.ImageField(upload_to="quiz_covers/", blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name=_("Autor")
    )
    created_at = models.DateTimeField(_("Data utworzenia"), auto_now_add=True)
    is_published = models.BooleanField(_("Opublikowany"), default=False, db_index=True)

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizy")
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(_("Treść pytania"))
    image = models.ImageField(upload_to="question_images/", blank=True, null=True)
    time_limit = models.IntegerField(_("Limit czasu (s)"), default=30)
    order = models.IntegerField(_("Kolejność"), default=0)

    class Meta:
        verbose_name = _("Pytanie")
        verbose_name_plural = _("Pytania")
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.quiz.title} - Pytanie {self.order}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(_("Treść odpowiedzi"), max_length=300)
    is_correct = models.BooleanField(_("Czy poprawna?"), default=False)

    class Meta:
        verbose_name = _("Odpowiedź")
        verbose_name_plural = _("Odpowiedzi")

    def __str__(self) -> str:
        return self.text


class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(_("Wynik"))
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Wynik Quizu")
        verbose_name_plural = _("Wyniki Quizów")

    def __str__(self) -> str:
        return f"{self.user.username} - {self.quiz.title} ({self.score} pkt)"