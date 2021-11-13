import datetime
from django.http.response import Http404
from django.shortcuts import redirect, render
from quizz.api.helpers import create_token
from quizz.api.helpers import auth
from quizz.models import Category, ProgrammingLanguage, Level, UserScore
from django.db.models import Sum

# Create your views here.
def response_with_404(request, exception=None):
    return render(request, 'quizz/404.html', status=404)



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

def play(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])
    levels = Level.objects.all()
    languages = ProgrammingLanguage.objects.all()
    categories = Category.objects.all()
    data = {
        'user': user,
        'levels': levels,
        'languages': languages,
        'categories': categories
    }
    return render(request, 'quizz/play.html', data)

def history(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])

    # xu li du lieu o day
    
    data = {
        'user': user
    }
    return render(request, 'quizz/history.html', data)

def profile(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])
    data = {
        'user': user,
    }
    return render(request,'quizz/profile.html',data) 

def overview(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])
    user_scores = UserScore.objects.filter(user=user)
    sum_score = user_scores.aggregate(total_score=Sum('score')).get('total_score')
    data = {
        'user': user,
        'user_scores': user_scores,
        'sum_score': sum_score
    }
    return render(request, 'quizz/overview.html', data)

def summary(request, id):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])
    try:
        details = UserScore.objects.get(id=id, user=user)
        data = {
            'user': user,
            'user_score': details
        }
        return render(request, 'quizz/summary.html', data)
    except:
        raise Http404('Not found')

def rank(request):
    if 'token' not in request.COOKIES.keys() or auth(request.COOKIES['token']) == None:
        return redirect('/login')
    user = auth(request.COOKIES['token'])
    user_rank = UserScore.objects.values('user__username').annotate(total_score=Sum('score')).order_by('-total_score')
    data = {
        'user': user,
        'user_rank': user_rank
    }
    return render(request, 'quizz/rank.html', data)