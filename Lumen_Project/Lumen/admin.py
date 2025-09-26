from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.forms.models import BaseInlineFormSet
from .models import Quiz, Question, Answer

class AnswerFormSet(BaseInlineFormSet):
    """Gwarantuje, że dokładnie jedna odpowiedź jest oznaczona jako poprawna."""
    def clean(self):
        super().clean()
        if any(self.errors):
            return
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
    """Umożliwia edycję Odpowiedzi w formie tabeli na stronie Pytania."""
    model = Answer
    formset = AnswerFormSet
    extra = 1
    fields = ('text', 'is_correct')

class QuestionInline(admin.TabularInline):
    """
    Umożliwia edycję Pytań w formie tabeli na stronie Quizu.
    Dodaje link do bezpośredniej edycji każdego pytania.
    """
    model = Question
    extra = 1
    ordering = ('order',)
    fields = ('text', 'order', 'time_limit', 'images ')
    show_change_link = True # dodaje link do edycji pytania


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Zaawansowana konfiguracja panelu admina для modelu Quiz."""
    # Akcje hurtowe
    actions = ['publish_quizzes', 'unpublish_quizzes']

    # Ulepszony widok listy
    list_display = ('title', 'category', 'is_published', 'question_count', 'created_by', 'created_at')
    list_filter = ('is_published', 'category', 'created_by')
    search_fields = ('title', 'description')

    # organizacja formularza edycji
    fieldsets = (
        (None, {'fields': ('title', 'description', 'category')}),
        ('Publikacja', {'fields': ('is_published',)}),
        ('Autor', {'fields': ('created_by', 'created_at')}),
    )
    readonly_fields = ('created_at', 'created_by')

    # Dołączenie panelu Pytań
    inlines = [QuestionInline]

    def get_queryset(self, request):
        """Optymalizuje zapytania do bazy danych, aby przyspieszyć ładowanie listy."""
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(q_count=Count('questions'))
        return queryset

    @admin.display(description='Liczba pytań', ordering='q_count')
    def question_count(self, obj):
        """Wyświetla liczbę pytań w quizie na liście."""
        return obj.q_count

    @admin.action(description='Opublikuj zaznaczone quizy')
    def publish_quizzes(self, request, queryset):
        """Akcja do publikowania wielu quizów na raz."""
        queryset.update(is_published=True)
        self.message_user(request, f"Opublikowano {queryset.count()} quizów.")

    @admin.action(description='Cofnij publikację zaznaczonych quizów')
    def unpublish_quizzes(self, request, queryset):
        """Akcja do cofania publikacji wielu quizów na raz."""
        queryset.update(is_published=False)
        self.message_user(request, f"Cofnięto publikację dla {queryset.count()} quizów.")

    def save_model(self, request, obj, form, change):
        """Automatycznie ustawia autora quizu przy pierwszym zapisie."""
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
    ordering = ('quiz', 'order')
