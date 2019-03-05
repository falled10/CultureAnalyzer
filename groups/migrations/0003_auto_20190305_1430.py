# Generated by Django 2.1.5 on 2019-03-05 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_dateofquiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shedule',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group'),
        ),
        migrations.AlterField(
            model_name='shedule',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quizzes'),
        ),
    ]
