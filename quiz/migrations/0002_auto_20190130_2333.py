# Generated by Django 2.1.5 on 2019-01-30 21:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizzes',
            name='numbers_of_questions',
        ),
        migrations.AddField(
            model_name='quizzes',
            name='type_of_quiz',
            field=models.IntegerField(
                choices=[(1, 'Business'), (2, 'General')], default=1),
        ),
    ]
