from qna_module import QNAGenerator
from scrapper import LoginPage, PostPage
from time import sleep


MODEL = 'gpt2'
MAX_LENGTH = 180 

def main():
    login = LoginPage()
    login.login()
    generator = QNAGenerator(model=MODEL,
                             max_length=MAX_LENGTH)
    while True:
        try:
            post = PostPage(generator)
            post.answer_all_questions()
        finally:
            sleep(600)

if __name__ == '__main__':
    main()

