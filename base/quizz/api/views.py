from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizz.models import Question, Choice, Category, LanguageProgramming
from .serializers import QuestionSerializer, CategorySerializer, ChoiceSerializer, LanguageProgrammingSerializer
from .helpers import response_with_errors, response_with_success


class QuestionsRoute(APIView):

    def get(self, request):
        questions = [QuestionSerializer(question).data for question in Question.objects.all()]
        for question in questions:
            choices = Choice.objects.filter(question=question['id'])
            question['choices'] = [ChoiceSerializer(choice).data for choice in choices]
        return Response(response_with_success(data=questions), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(response_with_errors(serializer.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class QuestionByIdRoute(APIView):

    def get(self, request, id):
        try:
            question = Question.objects.get(id=id)
            choices = Choice.objects.filter(question=question)
        except Question.DoesNotExist:
            return Response(data=response_with_errors({ "id": "Not Found" }), status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question)
        result = serializer.data
        result['choices'] = ChoiceSerializer(choices, many=True).data
        return Response(response_with_success(result), status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response(data=response_with_errors({ "id": "Not Found" }), status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(response_with_errors(serializer.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
