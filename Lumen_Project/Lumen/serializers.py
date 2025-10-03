from rest_framework import serializers
from .models import Quiz, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    """Serializer tylko dla odpowiedzi."""
    class Meta:
        model = Answer
        fields = ['id', 'text'] # Nie pokazujemy, czy jest poprawna, żeby nie psuć zabawy!

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer dla pytania, który zagnieżdża odpowiedzi."""
    answers = AnswerSerializer(many=True, read_only=True) # Zagnieżdżamy odpowiedzi

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'answers']

class QuizListSerializer(serializers.ModelSerializer):
    """
    Prosty serializer do wyświetlania na liście quizów.
    Pokazuje tylko podstawowe informacje, bez pytań.
    """
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category']

class QuizDetailSerializer(serializers.ModelSerializer):
    """
    Szczegółowy serializer dla pojedynczego quizu.
    Zagnieżdża wszystkie powiązane z nim pytania.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'created_by', 'created_at', 'questions']
        read_only_fields = ['created_by']