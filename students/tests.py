from django.test import TestCase

from .models import Student
from users.models import User

def create_user():
    return User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Create your tests here.
class StudentsTest(TestCase):
    def test_student_can_be_created(self):
        all_students = Student.objects.all()
        prev_count = all_students.count()
        student = Student.objects.create(name='Grade A Student')
        student.save()
        all_students = Student.objects.all()
        cur_count = all_students.count()
        self.assertEqual(prev_count + 1, cur_count)

    def test_can_create_new_student_using_post(self):
        create_user()
        self.client.login(username='myusername', password='mypassword')
        data = {
            'name': 'Mary Sue', 
        }
        response = self.client.post('/students/new/', data=data)
        response = self.client.get('/students/')
        self.assertIn('Mary Sue', response.content.decode())

    def test_student_info_not_accessable_or_created_without_login(self):
        create_user()
        data = {
            'name': 'Mary Sue', 
        }
        response = self.client.post('/students/new/', data=data)
        response = self.client.get('/students/')
        self.assertNotIn('Mary Sue', response.content.decode())
        self.client.login(username='myusername', password='mypassword')
        response = self.client.get('/students/')
        self.assertNotIn('Mary Sue', response.content.decode())