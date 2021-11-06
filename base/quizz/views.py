from django.shortcuts import redirect, render
from quizz.api.helpers import create_token
from quizz.api.helpers import auth
from quizz.models import Category, ProgrammingLanguage, Level

# Create your views here.
def index(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')

    user = auth(request.COOKIES['token'])
    data = {
        'levels': Level.objects.all(),
        'categories': Category.objects.all(),
        'languages': ProgrammingLanguage.objects.all(),
        'user': user
    }
    return render(request, 'quizz/common.html', data)

def signup(request):
    return render(request, 'quizz/sign-up.html')

def login(request):
    return render(request, 'quizz/login.html')

def logout(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])
    user.token = create_token()
    user.save()
    return redirect('/login')
