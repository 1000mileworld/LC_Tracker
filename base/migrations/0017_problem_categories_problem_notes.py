# Generated by Django 4.0 on 2022-03-06 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_problem_companies'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='categories',
            field=models.TextField(blank=True, default='', verbose_name='Category Tags (comma separated)'),
        ),
        migrations.AddField(
            model_name='problem',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
    ]