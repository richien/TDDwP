from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.browser = webdriver.Firefox()
		cls.browser.implicitly_wait(3)

	@classmethod
	def tearDownClass(cls):
		cls.browser.quit()
		super().tearDownClass()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# A user, Henry, has heard about a cool new online to-do app. He goes
		# to check out its homepage
		self.browser.get('%s%s' % (self.live_server_url, '/lists/'))
		
		# He notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# He is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		
		# He types "buy peacock feathers" into a text box (His hobby
		# is tying fly fishing lures)
		inputbox.send_keys('Buy peacock feathers')

		# When he hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		henry_list_url = self.browser.current_url
		self.assertRegex(henry_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		
		# There is still a text box inviting him to add another item. He 
		# enters "Use peacock feathers to make a fly" (He is very methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on his list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		# Now a new user, Francis, comes along to the site.

		## We use a new browser session to make sure that no information
		## of Henry's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the home page. There is no sign of Henry's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Francis starts a new list by entering a new item. She
		# is less interesting than Henry...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, henry_list_url)

		# Again, there is no trace of Henry's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Satisfied, they both go back to sleep
		self.fail('Finish the test!')

	def check_for_row_in_list_table(self, row_text):
		time.sleep(5)
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')	
		self.assertIn(row_text, [row.text for row in rows])
