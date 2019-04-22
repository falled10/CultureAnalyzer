# Generated by Django 2.1.5 on 2019-02-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0002_auto_20190130_2333'),
        ('tutors', '0010_auto_20190204_2155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='title',
            new_name='question_number',
        ),
        migrations.AddField(
            model_name='answers',
            name='answer_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='questions',
            unique_together={('quiz', 'question_number')},
        ),
    ]
