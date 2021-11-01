from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizz.models import Question, Choice, Category, LanguageProgramming
from .serializers import QuestionSerializer, CategorySerializer, ChoiceSerializer, LanguageProgrammingSerializer

class Hello(APIView):

    def get(self, request):
        return Response({'message': 'Hi, What do you want to find?'}, status=status.HTTP_200_OK)

class QuestionsRoute(APIView):

    def get(self, request):
        questions = [QuestionSerializer(question).data for question in Question.objects.all()]
        for question in questions:
            choice = Choice.objects.filter(question=question['id'])
            question['choices'] = [ChoiceSerializer(choice).data for choice in choice]
        return Response(data=questions, status=status.HTTP_200_OK)
