from django.shortcuts import render
from quizz.api.helpers import auth
from quizz.models import Category, LanguageProgramming

# Create your views here.
def index(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return login(request)

    data = {
        'categories': Category.objects.all(),
        'languages': LanguageProgramming.objects.all(),
    }
    return render(request, 'quizz/common.html', data)

def login(request):
    return render(request, 'quizz/login.html')

def signup(request):
    return render(request, 'quizz/sign-up.html')