# Generated by Django 4.0 on 2022-03-09 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_problem_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='rating',
            field=models.CharField(choices=[('1', '1 (Solved optimally as fast as I can type)'), ('2', '2 (Solved in <30 min with few bugs)'), ('3', '3 (Solved in 1 hr with some bugs)'), ('4', "4 (Couldn't solve myself, but understood solution)"), ('5', "5 (If interviewer asks this, I'm doomed)")], default='3', max_length=2, verbose_name='Self Difficulty Rating'),
        ),
    ]
