from django.shortcuts import render, redirect
from .models import Student

# Create your views here.
def new_student(request):
    Student.objects.create(name=request.POST['name'])
    return_page = request.POST.get('return_page', '/')
    return redirect(return_page)

def show_students(request):
    students = Student.objects.all()
    
    view_data = {
        "students": students
    }

    return render(request, 'students.html', view_data)