from django.db import models

# Create your models here.

class Category(models.Model):
    category_key = models.CharField(max_length=200)
    category_title = models.TextField(max_length=1000)

class LanguageProgramming(models.Model):
    lg_key = models.CharField(max_length=100)
    lg_title = models.TextField(max_length=100)

class Question(models.Model):
    question_text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageProgramming, on_delete=models.CASCADE)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()