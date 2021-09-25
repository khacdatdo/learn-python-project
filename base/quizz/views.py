from django.shortcuts import render
from quizz.models import Category, LanguageProgramming

# Create your views here.
def index(request):
    data = {
        'categories': Category.objects.all(),
        'languages': LanguageProgramming.objects.all(),
    }
    return render(request, 'quizz/common.html', data)