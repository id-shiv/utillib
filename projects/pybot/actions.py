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

                    intent_utterance_data.append({
                        "main_intent": _file.split('.')[0],
                        "sub_intent": _intent,
                        "utterance": all_utterances,
                        "responses": _main_intents[_intent]['responses']
                        }
                    )

        self.intents = intent_utterance_data
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

        return clf

    def predict(self, request, classifier):
        X_predict = [request]

        # Run the test data into the model
        predicted = classifier.predict(X_predict)

        print(predicted)
        for intent in self.intents:
            if intent['sub_intent'] == predicted[0]:
                response = random.choice(intent['responses'])

        return response
