# Generated by Django 5.0.6 on 2024-07-31 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0006_deletehomework'),
    ]

    operations = [
        migrations.CreateModel(
            name='Years',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DeleteHomework',
        ),
        migrations.AlterField(
            model_name='homework',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.years'),
        ),
    ]
