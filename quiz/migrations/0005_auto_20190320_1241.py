# Generated by Django 2.1.5 on 2019-03-20 10:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20190219_1305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizzes',
            options={'permissions': (('view_test_player', 'Can view the test player'),)},
        ),
        migrations.AlterField(
            model_name='results',
            name='result',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
