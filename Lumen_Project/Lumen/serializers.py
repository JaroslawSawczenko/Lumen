from rest_framework import serializers
from django.db import transaction
from .models import Quiz, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('is_correct', None)
        return ret

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        # --- POPRAWKA: Dodano 'order' do pól ---
        fields = ['id', 'text', 'order', 'answers']
        read_only_fields = ['id']


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)
    # --- POPRAWKA: Dodano pole 'is_published' ---
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'is_published', 'created_by', 'questions']

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            if 'order' not in question_data:
                question_data['order'] = Question.objects.filter(quiz=quiz).count() + 1
            question = Question.objects.create(quiz=quiz, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return quiz


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category']