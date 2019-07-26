import os
import json
import random

import pandas as pd

import nltk
from nltk.corpus import words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

nltk.download('stopwords')
nltk.download('words')

INTENTS_PATH = 'projects/pybot/knowledge_base/'


class Bot:
    def __init__(self):
        self.intents = None
        self.features = None
        self.current_context = None
        self.intent = None
        self.response = None
        self.classifier = None

        self.conversation_context = None
        self.request_to_previous_context = False
        self.all_mandatory_slots_filled = True

    def __load_intents(self, remove_stopwords=False):
        intent_utterance_data = list()
        for _file in os.listdir(INTENTS_PATH):
            _main_intent_file = INTENTS_PATH + _file
            with open(_main_intent_file) as _main_intent_file_obj:
                _main_intents = json.load(_main_intent_file_obj)
                for _intent in _main_intents:
                    all_utterances = ''
                    for _utterance in _main_intents[_intent]['utterances']:
                        all_utterances = all_utterances + " " + _utterance

                    if remove_stopwords:
                        # Load stop words
                        stop_words = stopwords.words('english')
                        all_utterances = " ".join(word for word in all_utterances.split(' ') if word not in stop_words)

                    try:
                        _slots = _main_intents[_intent]['slots']
                    except:
                        _slots = None

                    try:
                        _action = _main_intents[_intent]['action']
                    except:
                        _action = None

                    intent_utterance_data.append({
                        "main_intent": _file.split('.')[0],
                        "sub_intent": _intent,
                        "utterance": all_utterances,
                        "responses": _main_intents[_intent]['responses'],
                        "slots": _slots,
                        "action": _action
                        }
                    )

        self.intents = intent_utterance_data
        self.conversation_context = intent_utterance_data
        return intent_utterance_data

    def load(self):
        intents = self.__load_intents()

        documents = list()
        labels = list()

        for intent in intents:
            if intent['sub_intent'] == 'unknown':
                documents.append(" ".join([word for word in words.words()]))
                labels.append('unknown')
            else:
                document = intent['utterance'].strip().lower()
                documents.append(document)
                labels.append(intent['sub_intent'])

        dataframe = pd.DataFrame({'utterance': documents, 'sub_intent': labels})
        X = dataframe['utterance'].values
        y = dataframe['sub_intent'].values

        clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                        ('tfidf', TfidfTransformer(use_idf=True)),
                        ('clf', SGDClassifier(loss='hinge',
                                              penalty='l2',
                                              alpha=1e-3,
                                              random_state=42,
                                              verbose=1)), ])

        # Fit the model to the training data
        clf.fit(X, y)

        self.classifier = clf

    def predict(self, request):
        X_predict = [request]

        # Run the test data into the model
        predicted = self.classifier.predict(X_predict)

        for intent in self.intents:
            if intent['sub_intent'] == predicted[0]:
                response = random.choice(intent['responses'])
                self.response = response
                self.current_context = intent['main_intent']
                self.intent = intent['sub_intent']
                self.slots = intent['slots']

    def respond(self, request):
        # Process request
        #print('\n')
        #print('Request Processing')
        #print(self.current_context)
        #print(self.intent)

        for _intent_index, _intent in enumerate(self.conversation_context):
            if (_intent['main_intent'] == self.current_context) and (_intent['sub_intent'] == self.intent):
                if _intent['slots']:
                    for _slot_index, _slot in enumerate(_intent['slots']):
                        try:
                            if _slot['current_status'] == 'request_info':
                                _modified_slot = _slot
                                _modified_slot['value'] = request
                                _slot['current_status'] = None
                                self.conversation_context[_intent_index]['slots'][_slot_index] = _modified_slot

                                self.request_to_previous_context = True
                        except:
                            modified_slot = _slot
                            modified_slot['current_status'] = 'request_info'
                            self.conversation_context[_intent_index]['slots'][_slot_index] = modified_slot

                            break
        
        if not self.request_to_previous_context:
            self.predict(request)

        # Process response
        #print('\n')
        #print('Response Processing')
        #print(self.current_context)
        #print(self.intent)
        response = self.response

        for _intent_index, _intent in enumerate(self.conversation_context):
            if (_intent['main_intent'] == self.current_context) and (_intent['sub_intent'] == self.intent):
                if _intent['slots']:
                    for _slot_index, _slot in enumerate(_intent['slots']):
                        try:
                            if _slot['value']:
                                modified_slot = _slot
                                modified_slot['current_status'] = None
                                self.conversation_context[_intent_index]['slots'][_slot_index] = modified_slot
                                
                                # print(_slot_index)
                                # print(len(_intent['slots']))
                                if _slot_index == (len(_intent['slots']) - 1):
                                    #print('all mandatory slots filled')
                                    self.all_mandatory_slots_filled = True
                        except:
                            response = random.choice(_slot['responses'])
                            modified_slot = _slot
                            modified_slot['current_status'] = 'request_info'
                            self.conversation_context[_intent_index]['slots'][_slot_index] = modified_slot

                            self.all_mandatory_slots_filled = False
                            break

        if self.all_mandatory_slots_filled:
            for _intent_index, _intent in enumerate(self.conversation_context):
                if (_intent['main_intent'] == self.current_context) and (_intent['sub_intent'] == self.intent):
                    if _intent['action']:
                        try:
                            to_replace = _intent['action']['value'].split('<')[1].split('>')[0]
                        except:
                            # print('nothing to replace')
                            pass
                        else:
                            replace_with = None
                            for _slot in _intent['slots']:
                                if _slot['identifier'] == to_replace:
                                    replace_with = _slot['value']
                            response = response + '\n' + _intent['action']['value'].replace('<' + to_replace + '>', replace_with)

                    for _slot_index, _slot in enumerate(_intent['slots']):
                        modified_slot = _slot
                        modified_slot['current_status'] = None
                        modified_slot['value'] = None
                        self.conversation_context[_intent_index]['slots'][_slot_index] = modified_slot
            self.current_context = None
            self.intent = None
            self.request_to_previous_context = False
            self.all_mandatory_slots_filled = False

        return response
