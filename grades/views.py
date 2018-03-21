import logging

from django.shortcuts import render
from students.models import Student
from assignments.models import Task
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('gradebook')

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    students = Student.objects.all()
    tasks = Task.objects.all().prefetch_related()

    view_data = {
        "students": students,
        "tasks": tasks,
    }
    return render(request, 'dashboard.html', view_data)

