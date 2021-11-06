from django.contrib import admin
from django.db import models
from quizz.models import Category, LanguageProgramming, Question, Choice, User

# Classes
class ChoicesInLine(admin.TabularInline):
    model = Choice
    extra = 1

class LevelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category', {'fields': ['category_key', 'category_title']}),
    ]
    ordering = ['id']
    list_display = ['id', 'category_key', 'category_title', 'questions']
    list_display_links = ['id', 'category_key', 'category_title']
    
class LanguagesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'lg_key', 'lg_title', 'questions']
    list_display_links = ['id', 'lg_key', 'lg_title']
  
class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [('Question', {'fields': ['question_text', 'category', 'language', 'level']})]
    inlines = [ChoicesInLine]
    ordering = ['id']
    list_display = ['id', 'question_text' , 'category_title', 'language_title', 'level_name']
    list_display_links = ['question_text']
    list_filter = ['category', 'language', 'level']
    search_fields = ['id', 'question_text']
  
class UsersAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'username', 'password', 'token']
    list_display_links = ['id', 'username', 'password', 'token']


# Register your models here.
admin.site.register(Question, QuestionsAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(LanguageProgramming, LanguagesAdmin)
admin.site.register(User, UsersAdmin)