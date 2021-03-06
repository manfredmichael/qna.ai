import os, dotenv
import pickle
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


dotenv.load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

LOGIN_LINK = 'https://www.instagram.com/accounts/login/?source=auth_switcher' 
# POST_LINK = 'https://www.instagram.com/p/CUxJUUhJ1VS/'
POST_LINK = 'https://www.instagram.com/p/CUy9QhKJwa0/'
COOKIE_PATH = 'cookie.txt'

browser = webdriver.Chrome('../chromedriver')
browser.implicitly_wait(5)


class LoginPage:
    def __init__(self, browser=browser, login_link=LOGIN_LINK):
        self.browser = browser
        self.browser.get(login_link)

    def login(self, username=USERNAME, password=PASSWORD):
        try:
            sleep(3)
            self.load_cookie()
            self.browser.get('https://www.instagram.com/')
            print('Logged in with cookie')

        except Exception as e:
            print(f'Failed to log in with cookie: {e}')
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
        finally:
            # remove popups
            try:
                WebDriverWait(self.browser, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='cmbtv']/button[.='Not Now']"))
                ).click()
            except TimeoutException:
                print('no pop up found on login')
                pass

    def load_cookie(self, path=COOKIE_PATH):
         with open(path, 'rb') as cookiesfile:
             cookies = pickle.load(cookiesfile)
             for cookie in cookies:
                 self.browser.add_cookie(cookie)


class PostPage:
    def __init__(self, generator, browser=browser, post_link=POST_LINK):
        self.browser = browser
        self.browser.get(post_link)
        self.generator = generator
        try:
            self.save_cookie()
        except Exception as e:
            print(f'Error when saving cookie: {e}')

    def answer_all_questions(self):
        self.show_more_comments()
        comments = self.browser.find_elements_by_class_name("Mr508")
        for comment in comments:
            try:
                # random pause to avoid getting detected as bot
                sleep(random.random() * 3)

                name, question = self.parse_question(comment) 
                if self.not_answered(name, question):
                    print(question)
                    answer = self.generator.generate_answer(question)['generated_text']
                    self.reply(comment, answer)
                    self.save(name, question)
                    print('answered successfuly')
            except Exception as e:
                print(f'Error caught while answering comments: {e}\nquestion: {question}')

    def parse_question(self, comment):
        name = comment.find_element_by_tag_name('div').find_elements_by_tag_name("span")[-4].text
        question = comment.find_element_by_tag_name('div').find_elements_by_tag_name("span")[-3].text
        return name, question 

    def reply(self, comment, answer):
        # it's a mess but it works, please don't touch it
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

        # replace new line with shift+enter
        for part in answer.split('\n'):
            comment_box.send_keys(part)
            ActionChains(self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        try:
            comment_box.send_keys(Keys.ENTER)
        except:
            print('Don\'t need to presse enter')
        # comment_box.send_keys(answer)
        self.browser.execute_script("arguments[0].scrollIntoView(false);", comment_box)

    def not_answered(self, name, question):
        # get name + question
        comment_text = ' '.join([name, question])
        try:
            with open('answered_questions.txt', 'r') as f:
                answered_questions = [r[:-1] for r in f.readlines()]
                if comment_text in answered_questions:
                    return False
        except Exception as e:
            print(f'Error when checking answered questions: {e}')
            pass
        return True

    def save(self, name, question):
        # get name + question
        comment_text = ' '.join([name, question])
        with open('answered_questions.txt', 'a+') as f:
            f.write(comment_text + '\n')

    def show_more_comments(self):
        # keep clicking 'show more comments'
        while True:
            try:
                WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='dCJp8 afkep']"))
                ).click()
            except:
                break

    def save_cookie(self, path=COOKIE_PATH):
        with open(path, 'wb') as f:
            cookies = self.browser.get_cookies()
            pickle.dump(cookies, f)
            print(f'Saving cookies..')
