from django.contrib import admin
from quizz.models import Category, LanguageProgramming, Question, Choice

# Register your models here.
admin.site.register([Category, LanguageProgramming, Question, Choice])