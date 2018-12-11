from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
		self.live_server_url = 'http://192.168.62.130:9000/lists/'

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# A user has heard about a cool new online to-do app. He goes
		# to check out its homepage
		self.browser.get(self.live_server_url)
		#self.browser.get('http://192.168.62.130:9000/lists/')

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
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		
		# There is still a text box inviting him to add another item. He 
		# enters "Use peacock feathers to make a fly" (He is very methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on his list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		# He wonders whether the site will remember his list. Then he sees
		# that the site has generated a unique URL for him -- there is some
		# explanatory text to that effect.

		# He visits the URL - his to-do list is still there.

		# Satisfied, he goes back to sleep
		self.fail('Finish the test!')

	def check_for_row_in_list_table(self, row_text):
		time.sleep(5)
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')	
		self.assertIn(row_text, [row.text for row in rows])