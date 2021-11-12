from quizz.models import Question, Category, Choice, ProgrammingLanguage, User, Level, UserScore
from rest_framework import serializers
import re

class LevelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    score = serializers.IntegerField()

    class Meta:
        model = Level
        fields = ('id', 'name', 'score')

class QuestionSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset=ProgrammingLanguage.objects.all()) 

    class Meta:
        model = Question
        fields = ('id', 'context', 'category', 'language')


class ChoiceSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True)
    is_correct_answer = serializers.BooleanField()

    class Meta:
        model = Choice
        fields = ('id', 'context', 'question', 'is_correct_answer')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)

    class Meta:
        model = Category
        fields = ('id', 'name')


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)

    class Meta:
        model = ProgrammingLanguage
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, min_length=6)
    password = serializers.CharField(max_length=200, min_length=6)
    token = serializers.CharField(default=None)

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if re.match(r'[A-Za-z0-9]{6,200}', attrs['username']) is None:
            raise serializers.ValidationError("Username must contain only letters and numbers, between 6 and 200 characters.")
        return attrs

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')


class UserScoreSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    score = serializers.IntegerField()
    details = serializers.CharField()
    time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserScore
        fields = ('id', 'user', 'score', 'details', 'time')