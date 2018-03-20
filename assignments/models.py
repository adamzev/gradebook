from django.db import models
from students.models import Student

class Task(models.Model):
    name = models.TextField()

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    grade = models.IntegerField(null=True)
    due_date = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
