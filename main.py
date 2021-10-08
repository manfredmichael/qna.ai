from qna_module import QNAGenerator

MODEL = 'gpt2'
MAX_LENGTH = 180 

def main():
    generator = QNAGenerator(model=MODEL,
                             max_length=MAX_LENGTH)
    while True:
        question = input('Type your question: ')
        result = generator.generate_answer(question)
        print('{} - {}'.format(result['inference_time'], result['generated_text']))
    pass

if __name__ == '__main__':
    main()

