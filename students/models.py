from django.db import models
#from assignments.models import Task

# TODO relate Student to assignment through grade https://stackoverflow.com/questions/12567151/how-to-add-column-in-manytomany-table-django

class Group(models.Model):
    # Group of students (ie, a class, or section of a class)
    name = models.TextField()
    tasks = models.ManyToManyField('assignments.Task', related_name='Groups')

class Student(models.Model):
    name = models.TextField()
    groups = models.ManyToManyField(Group, related_name='Students')
    tasks = models.ManyToManyField('assignments.Task', through='assignments.Assignment')
