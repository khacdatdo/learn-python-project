from django.contrib import admin
from quizz.models import Category, LanguageProgramming, Question, Choice

# Classes
class ChoicesInLine(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [('Question', {'fields': ['question_text', 'category', 'language']})]
    inlines = [ChoicesInLine]
    ordering = ['id']
    list_display = ['id', 'question_text' , 'category_title', 'language_title', 'choices']
    list_display_links = ['question_text']
    list_filter = ['category', 'language']
    search_fields = ['id', 'question_text']

class CategoriesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'category_key', 'category_title', 'questions']
    list_display_links = ['id', 'category_key', 'category_title']
    
class LanguagesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'lg_key', 'lg_title', 'questions']
    list_display_links = ['id', 'lg_key', 'lg_title']
    

# Register your models here.
admin.site.register(Question, QuestionsAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(LanguageProgramming, LanguagesAdmin)