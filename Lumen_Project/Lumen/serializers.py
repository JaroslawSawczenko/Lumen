from rest_framework import serializers
from django.db import transaction
from .models import Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """Ukrywa pole is_correct przed zwykłymi użytkownikami."""
        ret = super().to_representation(instance)
        request = self.context.get('request')
        # Jeśli nie ma requesta lub user nie jest administratorem -> usuń flagę poprawnej odpowiedzi
        if not request or not request.user.is_staff:
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
        if not questions_data:
            raise serializers.ValidationError("Quiz musi zawierać przynajmniej jedno pytanie.")

        for question_data in questions_data:
            answers = question_data.get('answers', [])
            correct_count = sum(1 for a in answers if a.get('is_correct'))

            if correct_count != 1:
                raise serializers.ValidationError(
                    f"Pytanie musi mieć dokładnie jedną poprawną odpowiedź. Znaleziono: {correct_count}")
        return questions_data

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(quiz=quiz, **question_data)

            Answer.objects.bulk_create([
                Answer(question=question, **ans) for ans in answers_data
            ])
        return quiz


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'image', 'slug']