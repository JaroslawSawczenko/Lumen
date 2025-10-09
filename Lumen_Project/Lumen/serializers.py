from rest_framework import serializers
from django.db import transaction
import random

from .models import Quiz, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    """Serializer dla odpowiedzi. Umożliwia zarówno odczyt, jak i zapis."""

    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        # Ukrywamy pole is_correct, gdy dane są tylko do odczytu.
        read_only_fields = ['id']

    def to_representation(self, instance):
        """Modyfikuje sposób wyświetlania odpowiedzi - ukrywa pole 'is_correct'."""
        ret = super().to_representation(instance)
        ret.pop('is_correct', None)  # Usuń pole 'is_correct' z wyjściowego JSON
        return ret


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer dla pytań, obsługujący zagnieżdżony zapis odpowiedzi."""
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']
        read_only_fields = ['id']


class QuizDetailSerializer(serializers.ModelSerializer):
    """
    Pełny serializer dla quizu, obsługujący zagnieżdżony zapis pytań i odpowiedzi.
    """
    questions = QuestionSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'created_by', 'questions']

    @transaction.atomic  # Gwarancja, że albo wszystko się uda, albo nic.
    def create(self, validated_data):
        """
        Nadpisana metoda create, aby obsłużyć zagnieżdżone tworzenie
        pytań i odpowiedzi razem z quizem.
        """
        # Wyciągamy dane pytań z głównych danych quizu
        questions_data = validated_data.pop('questions')

        # Tworzymy główny obiekt Quiz
        quiz = Quiz.objects.create(**validated_data)

        # Tworzymy każde pytanie i jego odpowiedzi w pętli
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return quiz


class QuizListSerializer(serializers.ModelSerializer):
    """Prosty serializer do wyświetlania na liście quizów."""

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category']