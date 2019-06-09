from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import os

BOT_NAME = 'PyBot'
KNOWLEDGE_FOLDER = 'poc/pybotv2/knowledge_base/'

bot = ChatBot(BOT_NAME)
trainer = ListTrainer(bot)


for _file in os.listdir(KNOWLEDGE_FOLDER):
    with open(KNOWLEDGE_FOLDER + _file, 'r') as knowledge:
        trainer.train(knowledge.readlines())

while True:
    request = input('You : ')
    response = bot.get_response(request)
    print('{} : {}'.format(BOT_NAME, response))

    if 'bye' in str(response):
        print(BOT_NAME + 'bye')
        break