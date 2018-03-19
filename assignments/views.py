from django.shortcuts import render, redirect, HttpResponse
from .models import Assignment
from students.models import Group, Student
# Create your views here.
def new_assignment(request):
    if request.POST['group_for_assignment'] == 'all':
        group = Group.objects.create(name='all')
        students = list(Student.objects.all())
        group.Students.add(*students)
        group.save()
    
    assignment = Assignment.objects.create(name=request.POST['name'])
    assignment.Groups.add(group)
    assignment.save()
    return_page = request.POST.get('return_page', '/')
    return redirect(return_page)

def show_assignments(request):
    assignments = Assignment.objects.all()
    
    assignments_for_view = []
    for assignment in assignments:
        assignment.groups = assignment.Groups.all()
        assignment.students = []
        for group in assignment.groups:
            
            assignment.students += group.Students.all()
        assignments_for_view.append(assignment)

    view_data = {
        "assignments": assignments_for_view
    }

    return render(request, 'assignments.html', view_data)