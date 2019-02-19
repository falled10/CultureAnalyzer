# Generated by Django 2.1.5 on 2019-01-29 20:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('feedbacks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='indicator',
            field=models.CharField(
                choices=[('PDI', 'PDI'), ('IND', 'IND'), ('MAS', 'MAS'),
                         ('UAI', 'UAI'), ('LTO', 'LTO'),
                         ('IVR', 'IVR')], default='PDI', max_length=3),
        ),
        migrations.AddField(
            model_name='feedback',
            name='max_value',
            field=models.PositiveSmallIntegerField(
                default=10,
                validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='min_value',
            field=models.PositiveSmallIntegerField(
                default=0,
                validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
    ]
