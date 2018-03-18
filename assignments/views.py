from django.shortcuts import render, redirect
from .models import Assignment
# Create your views here.
def new_assignment(request):
    Assignment.objects.create(name=request.POST['name'])
    return_page = request.POST.get('return_page', '/')
    return redirect(return_page)

def show_assignments(request):
    assignments = Assignment.objects.all()
    
    view_data = {
        "assignments": assignments
    }

    return render(request, 'assignments.html', view_data)