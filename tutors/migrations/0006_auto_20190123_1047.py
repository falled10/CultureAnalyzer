# Generated by Django 2.1.5 on 2019-01-23 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0005_auto_20190122_1835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='question',
            new_name='question_answer',
        ),
    ]
