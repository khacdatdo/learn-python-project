# Generated by Django 3.2.7 on 2021-09-27 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0002_choice_is_corrected'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='is_corrected',
            new_name='is_corrected_answer',
        ),
    ]
