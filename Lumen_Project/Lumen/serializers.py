from rest_framework import serializers
from django.db import transaction
from .models import Quiz, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']

    def to_representation(self, instance):
        # Ukrywa pole 'is_correct' przed zwykłymi użytkownikami API.
        ret = super().to_representation(instance)
        if not self.context['request'].user.is_staff:
            ret.pop('is_correct', None)
        return ret

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'answers']
        read_only_fields = ['id']

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'is_published', 'created_by', 'questions']

    def validate_questions(self, questions_data):
        """
        Walidacja na poziomie API:
        1. Quiz musi mieć co najmniej jedno pytanie.
        2. Każde pytanie musi mieć dokładnie jedną poprawną odpowiedź.
        """
        if not questions_data:
            raise serializers.ValidationError("Quiz musi zawierać przynajmniej jedno pytanie.")

        for question_data in questions_data:
            answers = question_data.get('answers', [])
            correct_answers_count = sum(1 for answer in answers if answer.get('is_correct'))

            if correct_answers_count != 1:
                question_text = question_data.get('text', 'N/A')
                raise serializers.ValidationError(
                    f"Pytanie '{question_text[:30]}...' musi mieć dokładnie jedną poprawną odpowiedź. "
                    f"Znaleziono: {correct_answers_count}."
                )
        return questions_data

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return quiz

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category']