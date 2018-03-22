""" assignment models """
from django.db import models
from students.models import Student
from users.models import User

class Task(models.Model):
    """ Model for Tasks
    Tasks can be worksheets, reading assignments or anything else that may be assigned to a student
    """
    name = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignment(models.Model):
    """ Model for Assignments
    Assignments creates (and stores info about) the connection between the student and the task
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    grade = models.IntegerField(null=True)
    due_date = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
