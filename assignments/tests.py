from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from .models import Assignment
from students.models import Student, Group
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

    def test_assignment_can_be_assigned_to_custom_group(self):
        student1 = Student.objects.create(name="Mary")
        student2 = Student.objects.create(name="Sue")

        group = Group.objects.create(name="My Class")
        group.Students.add(student1, student2)

        all_assignments = Assignment.objects.all()
        prev_count = all_assignments.count()
        assignment = Assignment.objects.create(name='First HW')
        assignment.Groups.add(group)
        assignment.save()
        pk = assignment.pk
        all_assignments = Assignment.objects.all()
        cur_count = all_assignments.count()
        self.assertEqual(prev_count + 1, cur_count)

        assignment_from_db = Assignment.objects.get(pk=pk)

        group_from_db = assignment_from_db.Groups.all()[0]

        students_from_db = group_from_db.Students.all()

        self.assertIn("Mary", [student.name for student in students_from_db])


    def test_can_create_new_assignment_using_post(self):
        data = {
            'name': 'Hard worksheet', 
            'group_for_assignment': 'all'
        }
        response = self.client.post('/assignments/new/', data=data)
        response = self.client.get('/assignments/')
        self.assertIn('Hard worksheet', response.content.decode())

