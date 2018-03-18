from django.shortcuts import render
from students.models import Student
from assignments.models import Assignment

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def dashboard(request):
    students = Student.objects.all()
    assignments = Assignment.objects.all()
    
    view_data = {
        "students": students,
        "assignments": assignments,
    }
    return render(request, 'dashboard.html', view_data)
