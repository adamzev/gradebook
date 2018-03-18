from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from .models import Assignment

# Create your tests here.
class AssignmentsTest(TestCase):
    def test_assignment_can_be_created(self):
        all_assignments = Assignment.objects.all()
        prev_count = all_assignments.count()
        assignment = Assignment.objects.create(name='First HW')
        assignment.save()
        all_assignments = Assignment.objects.all()
        cur_count = all_assignments.count()
        self.assertEqual(prev_count + 1, cur_count)

    def test_can_create_new_student_using_post(self):
        data = {
            'name': 'Hard worksheet', 
        }
        response = self.client.post('/assignments/new/', data=data)
        response = self.client.get('/assignments/')
        self.assertIn('Hard worksheet', response.content.decode())

