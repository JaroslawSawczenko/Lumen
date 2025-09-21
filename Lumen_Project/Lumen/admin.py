from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import Quiz, Question, Answer

class AnswerFormSet(BaseInlineFormSet):
    """Gwarantuje, że dokładnie jedna odpowiedź jest oznaczona jako poprawna."""

    def clean(self):
        super().clean()
        correct_answers_count = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                continue
            if form.cleaned_data.get('is_correct'):
                correct_answers_count += 1

        if correct_answers_count == 0:
            raise ValidationError('Musisz oznaczyć przynajmniej jedną odpowiedź jako poprawną.')
        if correct_answers_count > 1:
            raise ValidationError('Tylko jedna odpowiedź może być oznaczona jako poprawna.')

class AnswerInline(admin.TabularInline):
    """Umożliwia edycję Odpowiedzi bezpośrednio na stronie Pytania."""
    model = Answer
    formset = AnswerFormSet
    extra = 1  # Pokaż jedno dodatkowe puste pole


class QuestionInline(admin.StackedInline):
    """Umożliwia edycję Pytań bezpośrednio na stronie Quizu."""
    model = Question
    extra = 1
    fields = ('text', 'image', 'time_limit', 'order')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Konfiguracja panelu admina dla modelu Quiz."""
    list_display = ('title', 'category', 'created_by', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_by')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]  # Dołączamy panel Pytań

    # Automatyczne ustawienie 'created_by' na zalogowanego użytkownika
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Konfiguracja panelu admina dla modelu Question."""
    list_display = ('text', 'quiz', 'order', 'time_limit')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Prosta konfiguracja panelu admina dla modelu Answer."""
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)