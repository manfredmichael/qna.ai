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
POST_LINK = 'https://www.instagram.com/p/CUuxjg1P-sZ/'

browser = webdriver.Chrome('../chromedriver')
browser.implicitly_wait(5)

class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get(LOGIN_LINK)

    def login(self, username, password):
        # wait until login page show up
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )

        # login
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        
        # remove popups
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='cmbtv']/button[.='Not Now']"))
            ).click()
        finally:
            pass


class PostPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get(POST_LINK)

    def answer_all_questions(self):
        self.show_more_comments()
        comments = self.browser.find_elements_by_class_name("Mr508")
        for comment in comments:
            question = self.parse_question(comment)
            print(question)

    def parse_question(self, comment):
        question = comment.find_elements_by_tag_name("span")[1].text

    def show_more_comments(self):
        # keep clicking 'show more comments'
        while True:
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='dCJp8 afkep']"))
                ).click()
            except:
                break


try:
    login = LoginPage(browser)
    login.login(USERNAME, PASSWORD)
    post = PostPage(browser)
    post.answer_all_questions()
finally:
    sleep(10)
    browser.close()
