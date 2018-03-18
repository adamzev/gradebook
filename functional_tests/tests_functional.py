import os
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

MAX_WAIT = 10
# TODO Document the core functionality: a teacher can send out the same assignment to students both online
# and with a printed worksheet and track the results in the same place
# TODO add feature: create an assignment/worksheet
# TODO select which students will do the assignment online and which will do it using paper
# TODO set the default setting of the above to be based on what the student did previously
# TODO add in classes
# TODO add in various grading systems (complete/incomplete, check, check- check+, percentage grade)

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, func):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_enter_grades_and_retrieve_them_later(self):
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
        time.sleep(1)
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
        time.sleep(1)
        student_list = self.browser.find_element_by_id('student_list').text
        self.assertIn('Sue', student_list)

        student_input_box = self.browser.find_element_by_id('new_student')
        student_input_box.send_keys('Little Bobbie')
        student_input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        student_list = self.browser.find_element_by_id('student_list').text
        self.assertIn('Sue', student_list)
        self.assertIn('Little Bobbie', student_list)

        
        # She is offered the ability to create a new assignment
        header_text = self.browser.find_elements_by_tag_name('h3')
        self.assertIn('Create a new assignment', [x.text for x in header_text])

        assignment_input_box = self.browser.find_element_by_id('new_assignment')
        assignment_input_box.send_keys('Two digit addition')
        assignment_input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        assignment_list = self.browser.find_element_by_id('assignment_list').text
        self.assertIn('Two digit addition', assignment_list)


        # She creates a new assignment called "Two digit addition"
        self.fail('Finish the test!')
        

       

        # She enters grades for "Two digit addition" for Sue and Little Bobbie
        # Sue got a 97, little Bobbie got a 85

        # Lizzie logs out

        # Later, she logs back in and the marks for Sue and Little Bobbie are still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
