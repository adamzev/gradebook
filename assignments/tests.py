""" Tests the assignment views and models """
import logging

from django.test import TestCase

from students.models import Group, Student
from users.models import User

from .models import Assignment, Task

logger = logging.getLogger(__name__)
# Create your tests here.
def create_user():
    """ Creates a user with the name myusername and pasword, mypassword """
    return User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

class TasksTest(TestCase):
    """ Tests regarding the Task model """
    def test_task_can_be_created(self):
        user = create_user()
        all_tasks = Task.objects.all()
        prev_count = all_tasks.count()
        task = Task.objects.create(name='First HW', creator=user)
        task.save()
        all_tasks = Task.objects.all()
        cur_count = all_tasks.count()
        self.assertEqual(prev_count + 1, cur_count)

    def test_task_can_be_assigned_to_custom_group(self):
        user = create_user()
        student1 = Student.objects.create(name="Mary")
        student2 = Student.objects.create(name="Sue")

        group = Group.objects.create(name="My Class")
        group.Students.add(student1, student2)

        all_tasks = Task.objects.all()
        prev_count = all_tasks.count()
        task = Task.objects.create(name='First HW', creator=user)
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
        create_user()
        self.client.login(username='myusername', password='mypassword')
        data = {
            'name': 'Hard worksheet', 
            'group_for_task': 'all'
        }
        response = self.client.post('/assignments/tasks/new/', data=data)
        response = self.client.get('/assignments/tasks/')
        self.assertIn('Hard worksheet', response.content.decode())

    def test_student_can_get_grade_for_task(self):
        user = create_user()
        student1 = Student.objects.create(name="Mary")
        student_pk = student1.pk
        task1 = Task.objects.create(name='Algebra Quiz', creator=user)
        assignment1 = Assignment(student=student1, task=task1, grade=85, completed=True)
        assignment1.save()
        student1_from_db = Student.objects.get(pk=student_pk)

        task = student1_from_db.tasks.first()

        self.assertEqual(task.assignments.first().grade, 85)

    def test_grade_can_be_updated_using_post(self):
        user = create_user()
        self.client.login(username="myusername", password="mypassword")
        student1 = Student.objects.create(name="Mary")


        task = Task.objects.create(name='Second HW', creator=user)
        task.save()

        assign = Assignment.objects.create(student=student1, task=task)
        pk = assign.pk
        assign = None
        data = {
            'grade': '85'
        }
        self.client.post(f'/assignments/{pk}', data=data)
        assign_from_db = Assignment.objects.get(pk=pk)
        self.assertEqual(assign_from_db.grade, 85)

    def test_invalid_grade_not_updated(self):
        user = create_user()
        self.client.login(username="myusername", password="mypassword")
        student1 = Student.objects.create(name="Mary")
        task = Task.objects.create(name='Second HW', creator=user)
        task.save()
        assign = Assignment.objects.create(student=student1, task=task)
        pk = assign.pk
        data = {
            'grade': '-12'
        }
        self.client.post(f'/assignments/{pk}', data=data)
        assign_from_db = Assignment.objects.get(pk=pk)
        self.assertEqual(assign_from_db.grade, None)
