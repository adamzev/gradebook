import logging

from django.shortcuts import render
from students.models import Student
from assignments.models import Task

logger = logging.getLogger('gradebook')

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def dashboard(request):
    students = Student.objects.all()
    tasks = Task.objects.all().prefetch_related()
    
    tasks_for_view = []
    '''    for task in tasks:
        logger.debug(task.assignments.all())
        task.groups = task.Groups.all()
        task.students = []
        for group in task.groups:
            task.students += group.Students.all()
        tasks_for_view.append(task)
    '''
    
    view_data = {
        "students": students,
        "tasks": tasks,
    }
    return render(request, 'dashboard.html', view_data)

