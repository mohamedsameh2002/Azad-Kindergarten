# Generated by Django 5.0.6 on 2024-07-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0004_teacher_remove_homework_teacher_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='number',
            field=models.DecimalField(decimal_places=0, max_digits=5),
        ),
    ]
