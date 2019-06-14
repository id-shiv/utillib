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

# List of project variables
BOT_NAME = 'Stark'
USER_NAME = os.getlogin()  # logged in user name
SCREEN_WIDTH = 150  # console width in characters
RE_TRAIN = True
RESPONSE_PROBABILITY = 0.47

# Files and Directory locations
KNOWLEDGE_BASE_DIRECTORY = 'poc/pybot_v3/knowledge_base/'
TEMP_DIRECTORY = 'poc/pybot_v3/temp/'
BOT_ACTIONS_FILE = ''
INTENTS_FILE = 'bot_profile.json'


class Knowledge:
    @staticmethod
    def load_knowledge():
        knowledge = list()
        for _file in os.listdir(KNOWLEDGE_BASE_DIRECTORY):
            # print(KNOWLEDGE_BASE_DIRECTORY + _file)
            with open(KNOWLEDGE_BASE_DIRECTORY + _file) as _knowledge_file:
                _knowledge_file_intents = json.load(_knowledge_file)['intents']
                knowledge.append(_knowledge_file_intents)
        return knowledge

    @staticmethod
    def load_intents(data_set_folder, intents_file):
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

    @staticmethod
    def load_bot_actions():
        with open(KNOWLEDGE_BASE_DIRECTORY + BOT_ACTIONS_FILE) as file:
            bot_actions = json.load(file)
        return bot_actions


class Model:
    @staticmethod
    def create_model(training, output):
        tensorflow.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        return model

    def train_model(self, training, output):
        model = self.create_model(training, output)
        model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
        model.save(TEMP_DIRECTORY + "model.tflearn")

        return model

    def load_model(self):
        with open(KNOWLEDGE_BASE_DIRECTORY + INTENTS_FILE) as file:
            data = json.load(file)
        with open(TEMP_DIRECTORY + "data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
        model = self.__create_model(training, output)
        model.load(TEMP_DIRECTORY + "model.tflearn")

        return model, words, labels, data

    @staticmethod
    def bag_of_words(s, words):
        stemmer = LancasterStemmer()
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)


class Actions:
    @staticmethod
    def __return_top_link_from_google(search_word):
        for link in search(search_word, tld="co.in", num=10, stop=1, pause=2):
            return link


class Bot:
    def __init__(self):
        model = None
        words = None
        labels = None
        training = None
        output = None
        intents = None

    @staticmethod
    def __display_response(response):
        print("\n")
        sentence_length = len(BOT_NAME)
        space_length = SCREEN_WIDTH - sentence_length
        print(' '*space_length + "-"*sentence_length)
        print(' '*(space_length - 2) + '| {} |'.format(BOT_NAME))
        print(' '*space_length + "-"*sentence_length)

        for sentence in response.split('\n'):
            sentence_length = len(sentence)
            space_length = SCREEN_WIDTH - sentence_length
            print(' '*space_length + sentence)
        print("\n")

    @staticmethod
    def __get_user_input():
        sentence_length = len(USER_NAME)
        print(' '*2 + "-"*sentence_length)
        print('| {} |'.format(USER_NAME))
        print(' '*2 + "-"*sentence_length)
        user_input = input()
        return user_input

    def __get_response(self, request):
        results = self.model.predict([Model.bag_of_words(request, self.words)])[0]
        results_index = numpy.argmax(results)
        tag = self.labels[results_index]

        print(results, results[results_index], results_index, tag)
        if results[results_index] > RESPONSE_PROBABILITY:
            for tg in self.intents["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            return random.choice(responses)
        else:
            return 'Hmmm ... Not sure of it.\nShould i google this for you?'

    def __train_model(self):
        self.words, self.labels, self.training, self.output, self.intents = Knowledge.load_intents(KNOWLEDGE_BASE_DIRECTORY, INTENTS_FILE)
        model_obj = Model()
        self.model = model_obj.train_model(self.training, self.output)

    def __load_model(self):
        self.model, self.words, self.labels, self.intents = Model.load_model()

    def start(self):
        """
        Method to start the bot
        1. Loads knowledge files
        2. Greet and converse
        3. Exit on typing 'quit'
        """
        print('\nLoading Knowledge files')
        Knowledge.load_knowledge()

        if RE_TRAIN:
            print('Training {}'.format(BOT_NAME))
            self.__train_model()
        else:
            print('Loading trained {}'.format(BOT_NAME))
            self.__load_model()

        # Start conversation
        print('\n{} is ready to converse, remember to type \'quit\' to exit chat'.format(BOT_NAME))
        # Greet user
        self.__display_response('Hello {}, how may i help you?'.format(USER_NAME))
        while True:
            request = self.__get_user_input()
            if 'quit' in request.lower():  # exit the chat on typing 'quit'
                self.__display_response('Alright {}, have a good day'.format(USER_NAME))
                break
            else:  # retrieve the response and display
                response = self.__get_response(request)
                self.__display_response(response)


bot = Bot()
bot.start()
