from django.test import TestCase

from .models import Students

# Create your tests here.
class StudentsTest(TestCase):
    def test_student_can_be_created(self):
        all_students = Students.objects.all()
        prev_count = all_students.count()
        student = Students.objects.create(name='Grade A Student')
        student.save()
        all_students = Students.objects.all()
        cur_count = all_students.count()
        self.assertEqual(prev_count + 1, cur_count)

    def test_can_create_new_student_using_post(self):
        data = {
            'name': 'Mary Sue', 
        }
        response = self.client.post('/students/new/', data=data)
        response = self.client.get('/students/')
        self.assertIn('Mary Sue', response.content.decode())

