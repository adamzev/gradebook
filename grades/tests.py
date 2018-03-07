from django.test import TestCase
from django.urls import resolve
from grades.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

class SignUpTest(TestCase):
    def test_sign_up_page_returns_correct_html(self):
        response = self.client.get('/sign_up/')

        self.assertTemplateUsed(response, 'sign_up.html')

    def test_can_create_new_user(self):
        response = self.client.post('/sign_up/', data={'username': 'adam', 'password':'qwerty123!@#'})
        self.assertIn('adam', response.content.decode())
        self.assertTemplateUsed(response, 'welcome.html')