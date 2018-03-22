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
    tasks = Task.objects.filter(creator=request.user).prefetch_related()

    view_data = {
        "students": students,
        "tasks": tasks,
    }
    return render(request, 'dashboard.html', view_data)

