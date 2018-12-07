from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://192.168.62.130:9000')

assert 'Django' in browser.title