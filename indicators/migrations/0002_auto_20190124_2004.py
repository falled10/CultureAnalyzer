# Generated by Django 2.1.5 on 2019-01-24 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countryindicator',
            options={'ordering': ['iso_code', 'name'], 'verbose_name_plural': "countries' indicators"},
        ),
    ]