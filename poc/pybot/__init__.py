import os
import random
import json

import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import pickle

import warnings
warnings.simplefilter("ignore")

TEMP_DIRECTORY = 'temp/'
BOT_NAME = 'PyBot'
DATA_SET_FOLDER = 'poc/pybot/knowledge/'
INTENTS_FILE = '__intent_knowledge.json'
BOT_ACTIONS_FILE = 'bot_actions.json'
USER_NAME = os.getlogin()
RE_TRAIN = False


def __load_intents(data_set_folder, intents_file):
    stemmer = LancasterStemmer()

    with open(data_set_folder + intents_file) as file:
        data = json.load(file)

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    print(docs_x)
    print(docs_y)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open(TEMP_DIRECTORY + "data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
    
    return words, labels, training, output, data


def __load_bot_actions():
    with open(DATA_SET_FOLDER + BOT_ACTIONS_FILE) as file:
        bot_actions = json.load(file)
    return bot_actions


def __create_model(training, output):
    tensorflow.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    return model


def __train_model(training, output):
    model = __create_model(training, output)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save(TEMP_DIRECTORY + "model.tflearn")

    return model


def __load_model():
    with open(DATA_SET_FOLDER + INTENTS_FILE) as file:
        data = json.load(file)
    with open(TEMP_DIRECTORY + "data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
    model = __create_model(training, output)
    model.load(TEMP_DIRECTORY + "model.tflearn")

    return model, words, labels, data


def __bag_of_words(s, words):
    stemmer = LancasterStemmer()
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def __respond(model, question, words, labels, intents):
    results = model.predict([__bag_of_words(question, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in intents["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    return random.choice(responses)


def __display_bot_response(response):
    screen_width = 150
    for sentence in response.split('\n'):
        sentence_length = len(sentence)
        space_length = screen_width - sentence_length
        print(' '*space_length + sentence)


def start():
    print('Starting {} ...'.format(BOT_NAME))
    print('Loading {} knowledge base ...'.format(BOT_NAME))
    # nltk.download('punkt')
    if RE_TRAIN:
        words, labels, training, output, intents = __load_intents(DATA_SET_FOLDER, INTENTS_FILE)
        model = __train_model(training, output)
    else:
        model, words, labels, intents = __load_model()
    print('Knowledge base loaded, {} is now ready to converse'.format(BOT_NAME))

    print('\n\n')
    message = 'Hello {}, How may i help you'.format(USER_NAME)
    __display_bot_response(message)

    response = '1'
    while response == '1':
        question = input()
        bot_response = __respond(model, question, words, labels, intents)
        __display_bot_response(bot_response)
        for response, action in __load_bot_actions().items():
            if bot_response == response:
                __display_bot_response('1. Yes')
                __display_bot_response('2. No')
                perform_action = input()
                if perform_action.lower() == 'yes' or perform_action == '1':
                    __display_bot_response('Performing {}'.format(action))
        
        print("\n")
        __display_bot_response('Need help?')
        __display_bot_response('1. Yes')
        __display_bot_response('2. Share feedback?')
        __display_bot_response('Enter anything else to close the chat')
        response = input()
        if response == '1' or response.lower() == 'yes':
            __display_bot_response('Sure, what is it?')
            if response not in ['1', '2', '3']:
                __display_bot_response('You did not choose from the options')

    if response == '2':
        __display_bot_response('Type in your feedback here')
        feedback = input()
        __display_bot_response('Thank you {} for your feedback, have a great day'.format(USER_NAME))
    else:
        __display_bot_response('Alright {}, have a great day'.format(USER_NAME))
    print('\n')


start()
