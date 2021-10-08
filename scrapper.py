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
POST_LINK = 'https://www.instagram.com/p/CUxJUUhJ1VS/'

browser = webdriver.Chrome('../chromedriver')
browser.implicitly_wait(5)

class LoginPage:
    def __init__(self, browser=browser, login_link=LOGIN_LINK):
        self.browser = browser
        self.browser.get(login_link)

    def login(self, username=USERNAME, password=PASSWORD):
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
    def __init__(self, generator, browser=browser, post_link=POST_LINK):
        self.browser = browser
        self.browser.get(post_link)
        self.generator = generator

    def answer_all_questions(self):
        self.show_more_comments()
        comments = self.browser.find_elements_by_class_name("Mr508")
        for comment in comments:
            question = self.parse_question(comment) 

            if self.not_answered(comment):
                print(question)
                answer = self.generator.generate_answer(question)['generated_text']
                self.reply(comment, answer)
                self.save(comment)

    def parse_question(self, comment):
        return comment.find_elements_by_tag_name("span")[1].text

    def reply(self, comment, answer):
        # i know it's a mess but it works, pwease don touch it
        self.browser.execute_script("arguments[0].scrollIntoView(true);", comment)
        sleep(5)

        buttons = comment.find_element_by_class_name("ZyFrc").find_elements_by_tag_name('button')
        for button in buttons:
            if 'Reply' in button.text:
                self.browser.execute_script("arguments[0].click();", button)
                break

        sleep(5)
        comment_box = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
        self.browser.execute_script("arguments[0].scrollIntoView(true);", comment_box)

        comment_box.send_keys(answer)
        self.browser.execute_script("arguments[0].scrollIntoView(false);", comment_box)

    def not_answered(self, comment):
        comment_text = ' '.join([r.text for r in comment.find_elements_by_tag_name("span")[:2]])
        with open('answered_questions.txt', 'r') as f:
            answered_questions = [r[:-1] for r in f.readlines()]
            if comment_text in answered_questions:
                return False
        return True

    def save(self, comment):
        comment_text = ' '.join([r.text for r in comment.find_elements_by_tag_name("span")[:2]])
        with open('answered_questions.txt', 'a+') as f:
            f.write(comment_text + '\n')

    def show_more_comments(self):
        # keep clicking 'show more comments'
        while True:
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='dCJp8 afkep']"))
                ).click()
            except:
                break
