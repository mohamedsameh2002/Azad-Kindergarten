# Generated by Django 5.0.6 on 2024-07-31 11:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0007_years_delete_deletehomework_alter_homework_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 7, 31, 11, 3, 25, 197860, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='homework',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
