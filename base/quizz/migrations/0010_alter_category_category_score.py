# Generated by Django 3.2.8 on 2021-10-31 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0009_alter_category_category_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_score',
            field=models.IntegerField(default=0),
        ),
    ]
