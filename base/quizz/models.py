from django.db import models

# Create your models here.

class Level(models.Model):
    def __str__(self):
        return self.name
    def questions(self):
        return len(self.question_set.all())

    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

class Category(models.Model):
    def __str__(self):
        return self.name.capitalize()
    def questions(self):
        return len(self.question_set.all())

    name = models.CharField(max_length=500)

class ProgrammingLanguage(models.Model):
    def __str__(self):
        return self.name.capitalize()
    def questions(self):
        return len(self.question_set.all())

    name = models.CharField(max_length=100)

class Question(models.Model):
    def __str__(self):
        return self.context
    def category(self):
        return self.category.name
    def language(self):
        return self.language.name
    def level_name(self):
        return self.level.name
    def choices(self):
        return len(self.choice_set.all())

    context = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

class Choice(models.Model):
    def __str__(self):
        return self.context

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    context = models.TextField()
    is_correct_answer = models.BooleanField(default=False)


class User(models.Model):
    def __str__(self) -> str:
        return self.username

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    token = models.TextField(null=True)


class UserScore(models.Model):
    def __str__(self) -> str:
        return self.user.username

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    details = models.TextField()
    average_time = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)