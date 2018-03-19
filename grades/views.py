from django.shortcuts import render
from students.models import Student
from assignments.models import Assignment

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def dashboard(request):
    students = Student.objects.all()
    assignments = Assignment.objects.all()
    
    assignments_for_view = []
    for assignment in assignments:
        assignment.groups = assignment.Groups.all()
        assignment.students = []
        for group in assignment.groups:
            
            assignment.students += group.Students.all()
        assignments_for_view.append(assignment)

    
    view_data = {
        "students": students,
        "assignments": assignments_for_view,
    }
    return render(request, 'dashboard.html', view_data)

