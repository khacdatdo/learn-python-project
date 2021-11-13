from django.contrib import admin
from django.db import models
from quizz.models import Category, ProgrammingLanguage, Question, Choice, User, Level, UserScore

# Classes
class ChoicesInLine(admin.TabularInline):
    model = Choice
    extra = 1

class LevelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'score']
    list_display_links = ['id', 'name', 'score']

class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category', {'fields': ['name']}),
    ]
    ordering = ['id']
    list_display = ['id', 'name', 'questions']
    list_display_links = ['id', 'name']
    
class LanguagesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'questions']
    list_display_links = ['id', 'name']
  
class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [('Question', {'fields': ['context', 'category', 'language', 'level']})]
    inlines = [ChoicesInLine]
    ordering = ['id']
    list_display = ['id', 'context' , 'category', 'language', 'level_name']
    list_display_links = ['context']
    list_filter = ['category', 'language', 'level']
    search_fields = ['id', 'context']
  
class UsersAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'username', 'password', 'token']
    list_display_links = ['id', 'username', 'password', 'token']

class UserScoreAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'user', 'score', 'average_time', 'time']

# Register your models here.
admin.site.register(Level, LevelAdmin)
admin.site.register(Question, QuestionsAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(ProgrammingLanguage, LanguagesAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(UserScore, UserScoreAdmin)