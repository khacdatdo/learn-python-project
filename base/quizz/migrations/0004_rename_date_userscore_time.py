# Generated by Django 3.2.8 on 2021-11-06 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0003_userscore'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userscore',
            old_name='date',
            new_name='time',
        ),
    ]