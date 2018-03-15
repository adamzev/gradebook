import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_grades_and_retrieve_them_later(self):
        # Lizzie has heard about a new site to store her grades.
        # She checks out the homepage
        self.browser.get('http://localhost:8080')

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
        time.sleep(15)
        user = self.browser.find_element_by_id('user')
        time.sleep(1)
        self.assertIn('Lizzie', user)
        # Now she has created an account she can log in.
        # She sees her name listed as the current user

        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Create a new assignment', header_text)
        # She is offered to create a new assignment
        # She creates a new assignment called "Two digit addition"
        self.fail('Finish the test!')
        # She is offered the ability to enter students

        # She enters Sue and Little Bobbie

        # She enters grades for "Two digit addition" for Sue and Little Bobbie
        # Sue got a 97, little Bobbie got a 85

        # Lizzie logs out

        # Later, she logs back in and the marks for Sue and Little Bobbie are still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
