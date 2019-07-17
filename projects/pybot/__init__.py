from actions import Bot

client_user_name = 'Shiv'
bot_name = '@PyBot'


def __get_user_input():
    sentence_length = len(client_user_name)
    print(' '*2 + "-"*sentence_length)
    print('| {} |'.format(client_user_name))
    print(' '*2 + "-"*sentence_length)
    user_input = input()
    return user_input


def get_request_message():
    return __get_user_input()


def __display_response(response_message):
    print("\n")
    screen_width = 150
    sentence_length = len(bot_name)
    space_length = screen_width - sentence_length
    print(' '*space_length + "-"*sentence_length)
    print(' '*(space_length - 2) + '| {} |'.format(bot_name))
    print(' '*space_length + "-"*sentence_length)

    for sentence in response_message.split('\n'):
        sentence_length = len(sentence)
        space_length = screen_width - sentence_length
        print(' '*space_length + sentence)
    print("\n")


def get_response_message(request_message):
    response_message = request_message
    return __display_response(response_message)


if __name__ == '__main__':
    bot = Bot()
    classifier = bot.load()

    # Inside a session
    while(True):
        # Read the message from client interface
        request_message = get_request_message()

        # Get the response for the requested message
        response = bot.predict(request_message, classifier)
        __display_response(response)

        # Look for the word 'quit' to end the client
        if request_message.lower() == 'quit':
            __display_response('Ok, bye!')
