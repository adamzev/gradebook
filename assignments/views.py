import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from .models import Task
from students.models import Group, Student
from assignments.models import Assignment

logger = logging.getLogger(__name__)

@login_required
def new_task(request):
    if request.POST['group_for_task'] == 'all':
        group = Group.objects.create(name='all')
        students = list(Student.objects.all())
        group.Students.add(*students)
        group.save()
    
    task = Task.objects.create(name=request.POST['name'], creator=request.user)
    for student in group.Students.all():
        Assignment.objects.create(student=student, task=task)
    task.Groups.add(group)
    task.save()
    return_page = request.POST.get('return_page', '/')
    return redirect(return_page)

@login_required
def show_tasks(request):
    tasks = Task.objects.filter(creator=request.user)
    tasks_for_view = []
    for task in tasks:
        task.groups = task.Groups.all()
        task.students = []
        for group in task.groups:
            
            task.students += group.Students.all()
        tasks_for_view.append(task)

    view_data = {
        "tasks": tasks_for_view
    }

    return render(request, 'tasks.html', view_data)