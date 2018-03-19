from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from .models import Task
from students.models import Student, Group
# Create your tests here.
class TasksTest(TestCase):
    def test_task_can_be_created(self):
        all_tasks = Task.objects.all()
        prev_count = all_tasks.count()
        task = Task.objects.create(name='First HW')
        task.save()
        all_tasks = Task.objects.all()
        cur_count = all_tasks.count()
        self.assertEqual(prev_count + 1, cur_count)

    def test_task_can_be_assigned_to_custom_group(self):
        student1 = Student.objects.create(name="Mary")
        student2 = Student.objects.create(name="Sue")

        group = Group.objects.create(name="My Class")
        group.Students.add(student1, student2)

        all_tasks = Task.objects.all()
        prev_count = all_tasks.count()
        task = Task.objects.create(name='First HW')
        task.Groups.add(group)
        task.save()
        pk = task.pk
        all_tasks = Task.objects.all()
        cur_count = all_tasks.count()
        self.assertEqual(prev_count + 1, cur_count)

        task_from_db = Task.objects.get(pk=pk)

        group_from_db = task_from_db.Groups.all()[0]

        students_from_db = group_from_db.Students.all()

        self.assertIn("Mary", [student.name for student in students_from_db])


    def test_can_create_new_task_using_post(self):
        data = {
            'name': 'Hard worksheet', 
            'group_for_task': 'all'
        }
        response = self.client.post('/assignments/tasks/new/', data=data)
        response = self.client.get('/assignments/tasks/')
        self.assertIn('Hard worksheet', response.content.decode())

