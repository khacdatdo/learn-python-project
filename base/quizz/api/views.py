from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizz.models import Question, Choice, Category, LanguageProgramming, User
from .serializers import QuestionSerializer, CategorySerializer, ChoiceSerializer, LanguageProgrammingSerializer, UserSerializer
from .helpers import create_token, response_with_errors, response_with_success, auth


class RegisterRoute(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            return Response(response_with_errors({'username': 'Exist'}, 'Username is already exist'), status=status.HTTP_400_BAD_REQUEST)
        except:
            token = create_token()
            request.data['token'] = token
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_with_success({ "token": token }, 'Create account successfully'), status=status.HTTP_201_CREATED)
            return Response(response_with_errors(serializer.errors, 'Error'), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginRoute(APIView):

    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            if user.password == request.data['password']:
                token = create_token()
                user.token = token
                user.save()
                response = Response(response_with_success(data={ "token": token }), status=status.HTTP_200_OK)
                response.set_cookie('token', token)
                return response
            else:
                return Response(response_with_errors({'password': 'Wrong'}, 'Wrong password'), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(response_with_errors({'username': 'Wrong'}, 'Wrong username'), status=status.HTTP_400_BAD_REQUEST)

class QuestionsRoute(APIView):

    def get(self, request):
        if ("token" not in request.GET.keys() or not auth(request.GET['token'])):
            return Response(response_with_errors({'token': 'Wrong'}, 'Wrong token'), status=status.HTTP_400_BAD_REQUEST)
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