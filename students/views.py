from django.shortcuts import render, redirect
from .models import Students

# Create your views here.
def new_student(request):
    Students.objects.create(name=request.POST['name'])
    return_page = request.POST.get('return_page', '/')
    return redirect(return_page)

def show_students(request):
    students = Students.objects.all()
    
    page_data = {
        "students": students
    }

    return render(request, 'students.html', page_data)