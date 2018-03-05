from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_grades_and_retrieve_them_later(self):
        # Lizzie has heard about a new site to store her grades.
        # She checks out the homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title mentions Gradebook
        self.assertIn('Gradebook', self.browser.title)
        self.fail("Finish the test!")

        # She is invited to log in or create an account
        # She is new to the site so she creates an account

        # Now she has created an account she can log in.
        # She sees her name listed as the current user

        # She is offered to create a new assignment
        # She creates a new assignment called "Two digit addition"

        # She is offered the ability to enter students

        # She enters Sue and Little Bobbie

        # She enters grades for "Two digit addition" for Sue and Little Bobbie
        # Sue got a 97, little Bobbie got a 85

        # Lizzie logs out

        # Later, she logs back in and the marks for Sue and Little Bobbie are still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
