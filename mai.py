from time import time
from transformers import pipeline, set_seed

# set_seed(42)

generator = pipeline('text-generation', model='gpt2')
while True:
    print('-------------------------')
    question = input('type your question: ')
    print('-------------------------')

    question2 = "Question: {}\n".format(question.replace('?', '') + '?')

    time0 = time()
    result = question2 + 'here is my answer:\n'
    # result = generator(question, max_length=50, return_full_text=False)[0]['generated_text']
    for i in range(1):
        result += generator(result, max_length=300, return_full_text=False)[0]['generated_text']

    total_time = time() - time0
    print(f'inference time: {total_time}')
    print('=========================')
    if result[-1] != '.':
        result = '.'.join(result.split('.')[:-1])
    print(result)
