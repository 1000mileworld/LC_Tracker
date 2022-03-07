# Generated by Django 4.0 on 2022-03-06 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_problem_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='rating',
            field=models.CharField(choices=[('1', '1 (Easiest)'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 (Hardest)')], default='3', max_length=2, verbose_name='self rating'),
        ),
    ]