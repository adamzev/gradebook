# Generated by Django 2.0.2 on 2018-03-20 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='students.Student'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='assignments.Task'),
        ),
    ]