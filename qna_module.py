import time
from transformers import pipeline, set_seed
import random


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class QNAGenerator():
    def __init__(self, model='gpt2', max_length=300):
        self.pipeline = pipeline('text-generation', model=model)
        self.max_length=max_length

    def generate_answer(self, question):
        time0 = time.time()
        prompt = self.preprocess(question)
        result = self.pipeline(prompt, max_length=self.max_length, return_full_text=False)[0]
        time1 = time.time()

        result['inference_time'] = time1 - time0
        return self.postprocess(result)

    def preprocess(self, question):
        question = question.replace('?', '') + '?'      # add exactly 1 question mark
        question = 'Question: {}\n'.format(question)    # create prompt for question answering
        question +=  'here is my answer:\n'
        return question

    def postprocess(self, result):
        
        # remove unfinished sentence
        if result['generated_text'][-1] != '.':
            result['generated_text'] = '.'.join(result['generated_text'].split('.')[:-1])
        return result 


 

