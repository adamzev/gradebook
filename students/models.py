from django.db import models
from assignments.models import Assignment

class Group(models.Model):
    # Group of students (ie, a class, or section of a class)
    name = models.TextField()
    assignments = models.ManyToManyField(Assignment, related_name='Groups')

class Student(models.Model):
    name = models.TextField()
    groups = models.ManyToManyField(Group, related_name='Students')
