# Generated by Django 5.0.6 on 2024-07-17 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=200)),
                ('homework', models.TextField(max_length=2000)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
