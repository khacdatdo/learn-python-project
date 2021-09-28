from django.db import models

# Create your models here.

class Category(models.Model):
    def __str__(self):
        return self.category_key.capitalize()
    def questions(self):
        return len(self.question_set.all())

    category_key = models.CharField(max_length=200)
    category_title = models.CharField(max_length=500)
    category_score = models.IntegerField(default=0)

class LanguageProgramming(models.Model):
    def __str__(self):
        return self.lg_key.capitalize()
    def questions(self):
        return len(self.question_set.all())

    lg_key = models.CharField(max_length=100)
    lg_title = models.CharField(max_length=100)

class Question(models.Model):
    def __str__(self):
        return self.question_text
    def category_title(self):
        return self.category.category_title
    def language_title(self):
        return self.language.lg_title
    def choices(self):
        return len(self.choice_set.all())

    question_text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageProgramming, on_delete=models.CASCADE)

class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()
    is_correct_answer = models.BooleanField(default=False)