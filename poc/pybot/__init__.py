import os
import random
import json

from googlesearch import search

import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import pickle

import warnings
warnings.simplefilter("ignore")

TEMP_DIRECTORY = 'poc/pybot/knowledge/'  # this directory is used to dump model and data
BOT_NAME = 'PyBot'
DATA_SET_FOLDER = 'poc/pybot/knowledge/'
INTENTS_FILE = '__intent_knowledge.json'
BOT_ACTIONS_FILE = 'bot_actions.json'
USER_NAME = os.getlogin()
RE_TRAIN = True
RESPONSE_PROBABILITY = 0.49


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
    results = model.predict([__bag_of_words(question, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    # print(results, results[results_index], results_index, tag)
    if results[results_index] > RESPONSE_PROBABILITY:
        for tg in intents["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        return random.choice(responses)
    else:
        return 'Hmmm ... Not sure of it.\nShould i google this for you?'


def __display_bot_response(response):
    print("\n")
    screen_width = 150
    sentence_length = len(BOT_NAME)
    space_length = screen_width - sentence_length
    print(' '*space_length + "-"*sentence_length)
    print(' '*(space_length - 2) + '| {} |'.format(BOT_NAME))
    print(' '*space_length + "-"*sentence_length)

    for sentence in response.split('\n'):
        sentence_length = len(sentence)
        space_length = screen_width - sentence_length
        print(' '*space_length + sentence)
    print("\n")


def __get_user_input():
    sentence_length = len(USER_NAME)
    print(' '*2 + "-"*sentence_length)
    print('| {} |'.format(USER_NAME))
    print(' '*2 + "-"*sentence_length)
    user_input = input()
    return user_input


def __return_top_link_from_google(search_word):
    for link in search(search_word, tld="co.in", num=10, stop=1, pause=2): 
        return link


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
        question = __get_user_input()
        bot_response = __respond(model, question, words, labels, intents)

        has_action = False
        for response, action in __load_bot_actions().items():
            if bot_response == response:
                has_action = True
                message = bot_response + '\n1. Yes\n2. No'
                __display_bot_response(message)
                perform_action = __get_user_input()
                if perform_action.lower() == 'yes' or perform_action == '1':
                    __display_bot_response('I am performing required actions, please wait ...')
                    if action == 'google':
                        top_link = __return_top_link_from_google(question)
                        __display_bot_response('Ok! so this is what i found: {}'.format(top_link))

        if not has_action:
            __display_bot_response(bot_response)
        else:
            has_action = False

        message = '1. Continue\n2. Share feedback?\nEnter anything else to close the chat'
        __display_bot_response(message)
        response = __get_user_input()
        if response == '1':
            __display_bot_response('Sure, what is it?')
        if response not in ['1', '2', '3']:
            __display_bot_response('You did not choose from the options')

    if response == '2':
        __display_bot_response('Type in your feedback here')
        feedback = __get_user_input()
        __display_bot_response('Thank you {} for your feedback, have a great day'.format(USER_NAME))
    else:
        __display_bot_response('Alright {}, have a great day'.format(USER_NAME))
    print('\n')


start()
