import os
import time
import unittest

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

MAX_WAIT = 10

# TODO move the following to a design document
# TODO Document the core functionality: a teacher can send out the same task to students both online
# and with a printed worksheet and track the results in the same place
# TODO add feature: create an task/worksheet
# TODO select which students will do the task online and which will do it using paper
# TODO set the default setting of the above to be based on what the student did previously
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

def get_task_list(browser):
    return browser.find_element_by_id('task_list')

def login_user(browser, live_server_url, username, password):
    browser.get(live_server_url + '/users/login/')

    input_box = browser.find_element_by_id('id_username')
    input_box.send_keys(username)

    input_box = browser.find_element_by_id('id_password')
    input_box.send_keys(password)

    input_box.send_keys(Keys.ENTER)

    wait_for(lambda: browser.find_element_by_id('user')).text

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

class LogInTests(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_login(self):
        self.browser.get(self.live_server_url + '/users/login/')
        header_text = self.browser.find_elements_by_tag_name('h3')
        self.assertIn('Log in', [x.text for x in header_text])

        login_user(self.browser, self.live_server_url, 'AdamLevin', 'htgc87aa')

        wait_for(lambda: self.assertIn('AdamLevin', self.browser.find_element_by_id('user').text))


class MainFeatureTests(LiveServerTestCase):

    fixtures = ['users.json'] # contains Adam Levin but not Lizzie
    @classmethod
    def create_user(cls):
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
        cls.create_user()

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

        
        # She is offered the ability to create a new task and assign it to a class
        header_text = self.browser.find_elements_by_tag_name('h3')
        self.assertIn('Create a new task', [x.text for x in header_text])

        # She creates a new task called "Two digit addition"
        task_input_box = self.browser.find_element_by_id('new_task')
        task_input_box.send_keys('Two digit addition')

        group_select_box = Select(self.browser.find_element_by_id('group_for_task'))
        group_select_box.select_by_visible_text("All")
        task_input_box.send_keys(Keys.ENTER)
        
        wait_for(lambda: self.assertIn('Two digit addition', get_task_list(self.browser).text))
        self.assertIn('Sue', get_task_list(self.browser).text)
        self.assertIn('Little Bobbie', get_task_list(self.browser).text)

        # She enters grades for "Two digit addition" for Sue and Little Bobbie
        # Sue got a 97, little Bobbie got a 85

        student_grade_inputs = self.browser.find_elements_by_class_name('grade_for_student')

        for student_grade_input in student_grade_inputs:
            if student_grade_input.get_attribute("data-task-name") == 'Two digit addition':
                if student_grade_input.get_attribute("data-student-name") == "Sue":
                    student_grade_input.send_keys('97')
                elif student_grade_input.get_attribute("data-student-name") == "Little Bobbie":
                    student_grade_input.send_keys('85')

        student_grade_inputs[0].send_keys(Keys.ENTER)
        # Lizzie logs out
        self.browser.get(self.live_server_url + '/users/logout/')

        self.browser.get(self.live_server_url + '/dashboard/')

        
        try:
            user = self.browser.find_element_by_id('user').text
            self.assertNotIn('Lizzie', user)
            self.assertNotIn('Two digit addition', get_task_list(self.browser).text)
        except NoSuchElementException:
            pass
            ## since we are looking for these things not to be there, it is okay if they aren't


        # Adam logs in and isn't able to see any of Lizzie's assignments
        login_user(self.browser, self.live_server_url, 'AdamLevin', 'htgc87aa')
        self.browser.get(self.live_server_url + '/dashboard/')
        self.assertNotIn('Two digit addition', get_task_list(self.browser).text)
        self.browser.get(self.live_server_url + '/users/logout/')

        # Later, she logs back in and the marks for Sue and Little Bobbie are still there
        login_user(self.browser, self.live_server_url, 'Lizzie', 'qwerty12345@')

        
        wait_for(lambda: self.assertIn('Lizzie', self.browser.find_element_by_id('user').text))

        self.browser.get(self.live_server_url + '/dashboard/')
        
        student_grade_inputs = self.browser.find_elements_by_class_name('grade_for_student')

        sue_found = False
        bobbie_found = False
        for student_grade_input in student_grade_inputs:
            if student_grade_input.get_attribute("data-task-name") == 'Two digit addition':
                if student_grade_input.get_attribute("data-student-name") == "Sue":
                    sue_found = True
                    self.assertEqual(student_grade_input.value, '97')
                elif student_grade_input.get_attribute("data-student-name") == "Little Bobbie":
                    bobbie_found = True
                    self.assertEqual(student_grade_input.value, '85')

        if not sue_found or not bobbie_found:
            self.fail("Bobbie or Sue not found")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
