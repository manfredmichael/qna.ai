from qna_module import QNAGenerator
from scrapper import LoginPage, PostPage
from time import sleep


MODEL = 'gpt2'
MAX_LENGTH = 180 

def main():
    login = LoginPage()
    login.login()
    while True:
        try:
            generator = QNAGenerator(model=MODEL,
                                     max_length=MAX_LENGTH)
            print('Answering questions..')
            post = PostPage(generator)
            post.answer_all_questions()
        except Exception as e:
            print(f'error caught on main script:{e}')
        finally:
            print('Done..')
            sleep(240)

if __name__ == '__main__':
    main()

