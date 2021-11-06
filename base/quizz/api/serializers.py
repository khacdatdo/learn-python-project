from quizz.models import Question, Category, Choice, LanguageProgramming, User, Level
from rest_framework import serializers


class LevelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    score = serializers.IntegerField()
    
    class Meta:
        model = Level
        fields = ('id', 'name', 'score')

class QuestionSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset=LanguageProgramming.objects.all()) 

    class Meta:
        model = Question
        fields = ('id', 'context', 'category', 'language')


class ChoiceSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    is_correct_answer = serializers.BooleanField()

    class Meta:
        model = Choice
        fields = ('id', 'context', 'question', 'is_correct_answer')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)

    class Meta:
        model = Category
        fields = ('id', 'name')


class LanguageProgrammingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)

    class Meta:
        model = LanguageProgramming
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, min_length=6)
    password = serializers.CharField(max_length=200, min_length=6)
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')