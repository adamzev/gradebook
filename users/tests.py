from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.
class SignUpTest(TestCase):
    def test_sign_up_page_returns_correct_html(self):
        response = self.client.get('/sign_up/')

        self.assertTemplateUsed(response, 'sign_up.html')

    def test_user_can_be_created(self):
        all_users = User.objects.all()
        prev_count = all_users.count()
        user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

        # Update fields and then save again
        user.first_name = 'John'
        user.last_name = 'Citizen'
        user.save()
        all_users = User.objects.all()
        cur_count = all_users.count()
        self.assertEqual(prev_count + 1, cur_count)


    def test_can_create_new_user(self):
        data = {
            'username': 'adam', 
            'password':'qwerty123!@#',
        }
        response = self.client.post('/sign_up/', data=data)
        self.assertIn('adam', response.content.decode())
        self.assertTemplateUsed(response, 'welcome.html')