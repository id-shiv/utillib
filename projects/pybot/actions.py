import os
import json
import re
import random

import pandas as pd
import numpy as np

import textblob
import nltk
from nltk.corpus import words
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier

nltk.download('stopwords')
nltk.download('words')

INTENTS_PATH = 'projects/pybot/knowledge_base/'


def __get_words_features(sentence, remove_stopwords=False):
    if remove_stopwords:
        # Load stop words
        stop_words = stopwords.words('english')
        sentence = " ".join(word for word in sentence.split(' ') if word not in stop_words)
    sentence = textblob.Sentence(sentence)
    return sentence.word_counts


def __ngrams(sentence, n):
    # Convert to lowercases
    sentence = sentence.lower()

    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', sentence)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def __load_intents(remove_stopwords=False):
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

    return intent_utterance_data


def __intents_to_dataframe(intents):
    # columns = list(set([word.lower() for word in words.words()])) + \
    #                 ['sub_intent', 'main_intent']
    columns = ['sub_intent', 'main_intent']
    intents_data_frame = pd.DataFrame(columns=columns)

    for intent in intents:
        row = dict()
        row['sub_intent'] = intent['sub_intent']
        row['main_intent'] = intent['main_intent']

        # print(__get_words_features(intent['utterance']))
        for word in intent['utterance'].split(' '):
            if len(word) > 1 and word.strip() != '':
                row[word] = 1.0

        for bi_gram in __ngrams(intent['utterance'], 2):
            row[bi_gram] = 1.0

        row_dataframe = pd.DataFrame([row], columns=row.keys())
        intents_data_frame = intents_data_frame.append(row_dataframe, sort=False)

    intents_data_frame = intents_data_frame.reset_index(drop=True)
    intents_data_frame = intents_data_frame.replace(np.NaN, 0)
    return intents_data_frame


def __split_X_y(intents):
    y = intents['sub_intent']
    X = intents.drop('sub_intent', axis=1)
    X = X.drop('main_intent', axis=1)
    return X, y


def __model(X, y):
    clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    clf.fit(X, y)
    return clf


def __predict(request, X, model):
    X_predict = list()
    for feature in X.columns:
        feature_found = False
        for word in request.split(' '):
            if feature == word.strip().lower():
                X_predict.append(1)
                feature_found = True
                break
        if not feature_found:
            X_predict.append(0)

    pred = model.predict([X_predict])

    probability_classes = model.predict_proba([X_predict])[0]
    # gets a dictionary of {'class_name': probability}
    prob_per_class_dictionary = dict(zip(model.classes_, probability_classes))

    return pred, prob_per_class_dictionary


def load():
    intents = __load_intents(remove_stopwords=False)

    intents_data = __intents_to_dataframe(intents)

    X, y = __split_X_y(intents_data)

    classifier = __model(X, y)

    return intents, X, classifier


def predict(request, intents, X, classifier):
    y_predict, predict_score = __predict(request, X, classifier)
    # print(y_predict, predict_score)

    # print(y_predict, predict_score)
    for _intent in intents:
        if _intent['sub_intent'] == y_predict[0]:
            response = random.choice(_intent['responses'])
    return response
