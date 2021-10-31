from quizz.models import Question, Category, Choice, LanguageProgramming
from rest_framework import serializers

class QuestionSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset=LanguageProgramming.objects.all()) 

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'category', 'language')


class ChoiceSerializer(serializers.ModelSerializer):
    choice_text = serializers.CharField()
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    is_correct_answer = serializers.BooleanField()

    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'question', 'is_correct_answer')


class CategorySerializer(serializers.ModelSerializer):
    category_key = serializers.CharField(max_length=200)
    category_title = serializers.CharField(max_length=500)
    category_score = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('id', 'category_key', 'category_title', 'category_score')


class LanguageProgrammingSerializer(serializers.ModelSerializer):
    lg_key = serializers.CharField(max_length=100)
    lg_title = serializers.CharField(max_length=100)

    class Meta:
        model = LanguageProgramming
        fields = ('id', 'lg_key', 'lg_title')