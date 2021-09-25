from django.db import models

# Create your models here.

class Category(models.Model):
    def __str__(self):
        return str(self.id) + " - " + self.category_key

    category_key = models.CharField(max_length=200)
    category_title = models.TextField(max_length=1000)

class LanguageProgramming(models.Model):
    def __str__(self):
        return str(self.id) + " - " + self.lg_key

    lg_key = models.CharField(max_length=100)
    lg_title = models.TextField(max_length=100)

class Question(models.Model):
    def __str__(self):
        return str(self.id) + " - " + self.question_text

    question_text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageProgramming, on_delete=models.CASCADE)

class Choice(models.Model):
    def __str__(self):
        return str(self.id) + " - " + self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()