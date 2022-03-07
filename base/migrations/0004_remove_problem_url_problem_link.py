# Generated by Django 4.0 on 2022-03-06 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_problem_difficulty_problem_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='url',
        ),
        migrations.AddField(
            model_name='problem',
            name='link',
            field=models.URLField(default='', max_length=500),
        ),
    ]
