import os

# List of project variables
BOT_NAME = 'Stark' 
USER_NAME = os.getlogin() # logged in user name
SCREEN_WIDTH = 150 # console width in characters

KNOWLEDGE_BASE_DIRECTORY = 'poc/pybot_v3/knowledge_base/'
TEMP_DIRECTORY = 'poc/pybot_v3/temp'


class Bot:
    @staticmethod
    def __display_bot_response(response):
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
    def start_bot():
        Bot.__display_bot_response('Hello ' + USER_NAME)


Bot.start_bot()
