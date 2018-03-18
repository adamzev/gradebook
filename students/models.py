from django.db import models
from assignments.models import Assignment

class Group(models.Model):
    # Group of students (ie, a class, or section of a class)
    assignments = models.ManyToManyField(Assignment)

class Student(models.Model):
    name = models.TextField()
    groups = models.ManyToManyField(Group)
