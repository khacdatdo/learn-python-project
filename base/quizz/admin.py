from django.contrib import admin
from quizz.models import Category, LanguageProgramming, Question, Choice

# Classes
class ChoicesAdmin(admin.StackedInline):
    model = Choice
    extra = 4

class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [('Question', {'fields': ['question_text', 'category', 'language']})]
    inlines = [ChoicesAdmin]

# Register your models here.
admin.site.register(Question, QuestionsAdmin)
admin.site.register([Category, LanguageProgramming])