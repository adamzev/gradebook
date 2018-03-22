""" assignment views """
import logging

from django.shortcuts import redirect, render, reverse

from assignments.models import Assignment
from students.models import Group, Student

from .forms import UpdateAssignmentForm
from .models import Task

logger = logging.getLogger('gradebook')

def new_task(request):
    """ save a new task from POST data"""
    # TODO change this to use form validation
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

def show_tasks(request):
    """ display a table of tasks """
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

def update_assignment(request, pk):
    """updates any field in the assignment model for an existing assignment
    Args:
        request
        pk (integer): pk of an assignment
    Returns:
        redirect to the dashboard
    """

    if request.method == 'POST':
        form = UpdateAssignmentForm(request.POST)
        if form.is_valid():
            Assignment.objects.filter(pk=pk).update(**form.cleaned_data)
    return redirect(reverse('dashboard'))
