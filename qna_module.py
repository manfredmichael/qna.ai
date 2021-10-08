from transformers import pipeline, set_seed
from googletrans import Translator
import time
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
        self.translator = Translator()

    def generate_answer(self, question):
        try:
            language = self.translator.detect(question).lang
        except:
            language = None

        time0 = time.time()
        prompt = self.preprocess(question, language)
        result = self.pipeline(prompt, max_length=self.max_length, return_full_text=False)[0]
        time1 = time.time()

        result['inference_time'] = time1 - time0
        return self.postprocess(result, language)

    def preprocess(self, question, language):
        try:
            question = self.translator.translate(question, dest=language).text
        except:
            print('Failed to translate question')
        question = question.replace('?', '') + '?'      # add exactly 1 question mark
        question = 'Question: {}\n'.format(question)    # create prompt for question answering
        question +=  'here is my answer:\n'
        return question

    def postprocess(self, result, language):
        
        # remove unfinished sentence

        try:
            result['generated_text'] = self.translator.translate(result['generated_text'], dest=language).text
        except:
            print('Failed to translate answer')
        if result['generated_text'][-1] != '.':
            result['generated_text'] = '.'.join(result['generated_text'].split('.')[:-1])
        return result 


 

