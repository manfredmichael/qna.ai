import os, dotenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dotenv.load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

LOGIN_LINK = 'https://www.instagram.com/accounts/login/?source=auth_switcher' 
POST_LINK = ''

browser = webdriver.Chrome('../chromedriver')
browser.implicitly_wait(5)
browser.get(LOGIN_LINK)

class LoginPage:
    def __init__(self, browser):
        self.browser = browser

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        browser.implicitly_wait(8)
try:
    login_page = LoginPage(browser)
    login_page.login(USERNAME, PASSWORD)
finally:
    sleep(10)
    # browser.close()


