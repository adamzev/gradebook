# Generated by Django 2.0.2 on 2018-03-19 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='include_students',
            field=models.TextField(default=''),
        ),
    ]
