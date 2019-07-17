import os
import json

import textblob
import pandas as pd
import numpy as np

# import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
# nltk.download('stopwords')
# nltk.download('words')
from sklearn.ensemble import RandomForestClassifier


INTENTS_PATH = 'projects/pybot/knowledge_base/'


def load():
    data_set_columns = words.words() + ['sub_intent', 'main_intent']

    intent_utterance_data = list()
    for _file in os.listdir(INTENTS_PATH):
        _main_intent_file = INTENTS_PATH + _file
        with open(_main_intent_file) as _main_intent_file_obj:
            _main_intents = json.load(_main_intent_file_obj)
            for _intent in _main_intents:
                for _utterance in _main_intents[_intent]['utterances']:
                    intent_utterance_data.append({
                        "main_intent": _file.split('.')[0],
                        "sub_intent": _intent,
                        "utterance": _utterance
                        }
                    )

    # Create a dataframe from the list
    data_set = pd.DataFrame(intent_utterance_data, columns=data_set_columns)
    print(data_set.shape)

    # # populate row for intent of unknown
    # intent_utterance_data = dict()
    # for word_in_vocabulary in words.words():
    #     if word_in_vocabulary in data_set_columns:
    #         intent_utterance_data[word_in_vocabulary] = -1
    #     else:
    #         intent_utterance_data[word_in_vocabulary] = 1
    # intent_utterance_data['sub_intent'] = 'unknown'
    # intent_utterance_data['main_intent'] = 'unknown'
    # no_idea = pd.DataFrame([intent_utterance_data])

    # data_set = data_set.append(no_idea)
    data_set = data_set.reset_index(drop=True)
    data_set = data_set.replace(np.NaN, -1)
    print(data_set)

    request = "need latest configuration of ST002"

    y = data_set['main_intent']
    X = data_set.drop('main_intent', axis=1)
    X = X.drop('sub_intent', axis=1)

    classifier = model(X, y)
    predict(request, X, classifier)

    y = data_set['sub_intent']
    X = data_set.drop('sub_intent', axis=1)
    X = X.drop('main_intent', axis=1)

    classifier = model(X, y)
    y_predict, predict_score = predict(request, X, classifier)


def model(X, y):
    clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    clf.fit(X, y)
    return clf


def predict(request, X, model):
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

    print(prob_per_class_dictionary)
    print(pred)
    return pred, prob_per_class_dictionary
    

def _get_words_features(message, remove_stopwords=False):
    if remove_stopwords:
        # Load stop words
        stop_words = stopwords.words('english')
        message = " ".join(word for word in message.split(' ') if word not in stop_words)
    sentence = textblob.Sentence(message)
    return sentence.word_counts


load()