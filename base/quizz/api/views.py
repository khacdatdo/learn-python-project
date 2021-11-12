import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizz.models import Question, Choice, User, UserScore
from .serializers import QuestionSerializer, ChoiceSerializer, UserSerializer, UserScoreSerializer
from .helpers import create_token, hashPassword, response_with_errors, response_with_success, auth


class Register(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            return Response(response_with_errors({'username': 'Exist'}, 'Username is already exist'), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            request.data['password'] = hashPassword(request.data['password'])
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_with_success({ "username": request.data['username'] }, 'Create account successfully'), status=status.HTTP_201_CREATED)
            return Response(response_with_errors(serializer.errors, 'Error'), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Login(APIView):

    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            if user.password == hashPassword(request.data['password']):
                token = create_token()
                user.token = token
                user.save()
                response = Response(response_with_success(data={ "token": token }), status=status.HTTP_200_OK)
                response.set_cookie('token', token, max_age=60*60*24*7)
                return response
            else:
                return Response(response_with_errors({'password': 'Wrong'}, 'Wrong password'), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(response_with_errors({'username': 'Wrong'}, 'Wrong username'), status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    def post(self, request):
        try:
            user = User.objects.get(token=request.COOKIES['token'])
            if user.password == hashPassword(request.data['old_password']):
                user.password = hashPassword(request.data['new_password'])
                user.save()
                return Response(response_with_success({ "username": user.username }, 'Change password successfully'), status=status.HTTP_200_OK)
            else:
                return Response(response_with_errors({'password': 'Incorrect'}, 'Current password is incorrect'), status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(response_with_errors({'token': 'Wrong'}, 'Please login before sending request to this endpoint'), status=status.HTTP_401_UNAUTHORIZED)


class Questions(APIView):

    def get(self, request):
        if ("token" not in request.COOKIES.keys() or not auth(request.COOKIES['token'])):
            return Response(response_with_errors({'token': 'Wrong'}, 'Please login before sending request to this endpoint'), status=status.HTTP_401_UNAUTHORIZED)
        filter = {}
        if 'level' in request.GET and request.GET['level'].isnumeric():
            filter['level'] = int(request.GET['level'])
        if 'category' in request.GET and request.GET['category'].isnumeric():
            filter['category'] = int(request.GET['category'])
        if 'language' in request.GET and request.GET['language'].isnumeric():
            filter['language'] = int(request.GET['language'])
        questions = [QuestionSerializer(question).data for question in Question.objects.filter(**filter)]
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


class QuestionById(APIView):

    def get(self, request, id):
        try:
            question = Question.objects.get(id=id)
            choices = Choice.objects.filter(question=question)
        except Question.DoesNotExist:
            return Response(data=response_with_errors({ "id": "Not Found" }, "Not found this id"), status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question)
        result = serializer.data
        result['choices'] = ChoiceSerializer(choices, many=True).data
        return Response(response_with_success(result), status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response(data=response_with_errors({ "id": "Not Found" }, "Not found this id"), status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(response_with_errors(serializer.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class MyHistory(APIView):
    
    def get(self, request):
        if ("token" not in request.COOKIES.keys() or not auth(request.COOKIES['token'])):
            return Response(response_with_errors({'token': 'Wrong'}, 'Please login before sending request to this endpoint'), status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(token=request.COOKIES['token'])
        histories = UserScoreSerializer(UserScore.objects.filter(user=user), many=True).data
        return Response(response_with_success(data=histories), status=status.HTTP_200_OK)

    def post(self, request):
        if ("token" not in request.COOKIES.keys() or not auth(request.COOKIES['token'])):
            return Response(response_with_errors({'token': 'Wrong'}, 'Please login before sending request to this endpoint'), status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(token=request.COOKIES['token'])
        data = {
            'user': user.id,
            'details': str(request.data)
        }
        score = 0
        time = 0
        default_time = 10000
        for question in request.data:
            time += question['time']
            if question['correct']:
                defaultScore = Question.objects.get(id=question['id']).level.score
                if default_time - time > 0:
                    score += defaultScore * (default_time - time) / default_time
                else:
                    score += 0
        data['score'] = math.ceil(score)
        data['time'] = time / (len(request.data) * 1000)
        serializer = UserScoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_with_success(serializer.data['id']), status=status.HTTP_200_OK)
        return Response(response_with_errors(serializer.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)