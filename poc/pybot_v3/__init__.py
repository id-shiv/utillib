import os
import json

# List of project variables
BOT_NAME = 'Stark'
USER_NAME = os.getlogin()  # logged in user name
SCREEN_WIDTH = 150  # console width in characters
RE_TRAIN = True

# Files and Directory locations
KNOWLEDGE_BASE_DIRECTORY = 'poc/pybot_v3/knowledge_base/'
TEMP_DIRECTORY = 'poc/pybot_v3/temp/'


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


class Bot:
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

    @staticmethod
    def __get_response(request):
        response = request
        return response

    @staticmethod
    def __train_model():
        pass

    @staticmethod
    def __load_model():
        pass

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
