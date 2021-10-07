from time import sleep
from selenium import webdriver

browser = webdriver.Chrome()
browser.implicitly_wait(5)

browser.get('https://www.instagram.com/')

login_link = browser.find_element_by_xpath("//a[text()='Log in']")
login_link.click()

sleep(5)

browser.close()
