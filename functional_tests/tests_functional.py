import os
import time
import unittest

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

MAX_WAIT = 10
# TODO Document the core functionality: a teacher can send out the same assignment to students both online
# and with a printed worksheet and track the results in the same place
# TODO add feature: create an assignment/worksheet
# TODO select which students will do the assignment online and which will do it using paper
# TODO set the default setting of the above to be based on what the student did previously
# TODO add in classes
# TODO add in various grading systems (complete/incomplete, check, check- check+, percentage grade)
def wait_for(func):
    start_time = time.time()
    while True:
        try:
            return func()
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.1)

def create_pre_authenticated_session(username, password):
    user = User.objects.create(username=username, password=password)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key

def get_student_list(browser):
    return browser.find_element_by_id('student_list')

def get_assignment_list(browser):
    return browser.find_element_by_id('assignment_list')

class NewUserTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_can_sign_up(self):
        # Lizzie has heard about a new site to store her grades.
        # She checks out the homepage
        self.browser.get(self.live_server_url)

        # She notices the page title mentions Gradebook
        self.assertIn('Gradebook', self.browser.title)

        # She is invited to log in or create an account
        # She is new to the site so she creates an account

        account_link = self.browser.find_element_by_link_text('Create account')
        account_link.click()

        self.assertIn('Sign up', self.browser.title)

        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('Lizzie')

        # She enters and confirms her new password
        passwordbox = self.browser.find_element_by_id('id_password1')
        passwordbox.send_keys('qwerty12345@')
        passwordbox = self.browser.find_element_by_id('id_password2')
        passwordbox.send_keys('qwerty12345@')

        passwordbox.send_keys(Keys.ENTER)
        user = wait_for(lambda: self.browser.find_element_by_id('user')).text
        self.assertIn('Lizzie', user)
        # Now she has created an account she can log in.
        # She sees her name listed as the current user
    
    def test_user_can_login(self):
        self.fail("write test")


class LoggedInUserTests(LiveServerTestCase):
    @classmethod
    def login_user(cls):
        '''
        cls.browser.get(cls.live_server_url)
        session_key = create_pre_authenticated_session('Lizzie', 'qwerty12345@')
        cls.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
        cls.browser.refresh()

        '''
        cls.browser.get(cls.live_server_url)


        account_link = cls.browser.find_element_by_link_text('Create account')
        account_link.click()

        inputbox = cls.browser.find_element_by_id('id_username')
        inputbox.send_keys('Lizzie')

        # She enters and confirms her new password
        passwordbox = cls.browser.find_element_by_id('id_password1')
        passwordbox.send_keys('qwerty12345@')
        passwordbox = cls.browser.find_element_by_id('id_password2')
        passwordbox.send_keys('qwerty12345@')

        passwordbox.send_keys(Keys.ENTER)
        wait_for(lambda: cls.browser.find_element_by_id('user'))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.login_user()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()



    def test_can_enter_grades_and_retrieve_them_later(self):
        # Lizzie has heard about a new site to store her grades.
        # She checks out the homepage

        self.browser.get(self.live_server_url + '/dashboard/')

        # She notices the page title mentions Gradebook
        #self.assertIn('Gradebook', self.browser.title)

        user = self.browser.find_element_by_id('user').text
        self.assertIn('Lizzie', user)
        # Now she has created an account she can log in.
        # She sees her name listed as the current user

        # She is offered the ability to enter students
        header_text = self.browser.find_elements_by_tag_name('h3')

        self.assertIn('Enter a new student', [x.text for x in header_text])

        # She enters Sue and Little Bobbie
        student_input_box = self.browser.find_element_by_id('new_student')
        student_input_box.send_keys('Sue')
        student_input_box.send_keys(Keys.ENTER)

        wait_for(lambda: self.assertIn('Sue', get_student_list(self.browser).text))

        student_input_box = self.browser.find_element_by_id('new_student')
        student_input_box.send_keys('Little Bobbie')
        student_input_box.send_keys(Keys.ENTER)

        wait_for(lambda: self.assertIn('Little Bobbie', get_student_list(self.browser).text))

        
        # She is offered the ability to create a new assignment and assign it to a class
        header_text = self.browser.find_elements_by_tag_name('h3')
        self.assertIn('Create a new assignment', [x.text for x in header_text])

        # She creates a new assignment called "Two digit addition"
        assignment_input_box = self.browser.find_element_by_id('new_assignment')
        assignment_input_box.send_keys('Two digit addition')

        group_select_box = Select(self.browser.find_element_by_id('group_for_assignment'))
        group_select_box.select_by_visible_text("All")
        assignment_input_box.send_keys(Keys.ENTER)
        
        wait_for(lambda: self.assertIn('Two digit addition', get_assignment_list(self.browser).text))
        self.assertIn('Sue', get_assignment_list(self.browser).text)
        self.assertIn('Little Bobbie', get_assignment_list(self.browser).text)

        # She enters grades for "Two digit addition" for Sue and Little Bobbie
        # Sue got a 97, little Bobbie got a 85

        student_grade_inputs = self.browser.find_element_by_class('grade_for_student')

        for student_grade_input in student_grade_inputs:
            if student_grade_input.get_attribute("data-assignment-name") == 'Two digit addition':
                if student_grade_input.get_attribute("data-student-name") == "Sue":
                    student_grade_input.send_keys('97')
                elif student_grade_input.get_attribute("data-student-name") == "Little Bobbie":
                    student_grade_input.send_keys('85')

        student_grade_inputs[0].send_keys(Keys.ENTER)

        self.fail('Finish the test!')




        # Lizzie logs out

        # Later, she logs back in and the marks for Sue and Little Bobbie are still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
