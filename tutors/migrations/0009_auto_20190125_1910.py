# Generated by Django 2.1.5 on 2019-01-25 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0008_auto_20190124_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryquestion',
            name='parent_category',
            field=models.ForeignKey(blank=True, db_column='parent_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childrens', to='tutors.CategoryQuestion'),
        ),
    ]