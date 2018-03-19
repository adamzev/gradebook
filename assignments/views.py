from django.shortcuts import render, redirect, HttpResponse
from .models import Task
from students.models import Group, Student
# Create your views here.
def new_task(request):
    if request.POST['group_for_task'] == 'all':
        group = Group.objects.create(name='all')
        students = list(Student.objects.all())
        group.Students.add(*students)
        group.save()
    
    task = Task.objects.create(name=request.POST['name'])
    task.Groups.add(group)
    task.save()
    return_page = request.POST.get('return_page', '/')
    return redirect(return_page)

def show_tasks(request):
    tasks = Task.objects.all()
    
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