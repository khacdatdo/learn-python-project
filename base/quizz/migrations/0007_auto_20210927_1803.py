# Generated by Django 3.2.7 on 2021-09-27 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0006_alter_choice_is_correct_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='languageprogramming',
            name='lg_title',
            field=models.CharField(max_length=100),
        ),
    ]