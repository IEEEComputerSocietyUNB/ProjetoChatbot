import os
import json
import time
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from bot.config_reader import retrieve_default
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.watson import Watson


class Communication:

    def __init__(self, use_watson=False, train=True):
        """
        Generator for dealing with most messages the bot will receive
        from user.
        """
        self.comm = ChatBot(
            "Comms",
            response_selection_method=get_random_response,
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                },
                {
                    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                    'threshold': 0.65,
                    'default_response':
                        [
                            'Desculpa, mas não entendi sua mensagem.',
                            'Não compreendi, você pode repetir?',
                            'Como é? Não entendi',
                        ],
                }
            ],
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        )
        if train:
            self.comm.train('bot/dialogs/')
        if use_watson:
            try:
                self.watson_analyzer = Watson(retrieve_default()['user'],
                                              retrieve_default()['pass'])
                self.watson_usage = True
            except KeyError:
                # If config.ini doesn't have the user and password:
                # Alert user and end execution
                print('Watson\'s user and password '
                      'need to be in configuration file.')
                exit()
        else:
            self.watson_usage = False
        self.all_texts = ''

    def respond(self, message):
        """
        Receive message from user and returns corresponding answer.
        """
        # if string isnt empty concatenate with space
        if(self.all_texts):
            self.all_texts += ' ' + message
        else:
            self.all_texts = message

        if(len(self.all_texts) > 50 and self.watson_usage):
            user_emotion = self.watson_analyzer.get_emotion(message)
            # if relevance is bigger than an arbitrary number send it to user
            if(user_emotion[1] > 60):
                message = f'Parece que tem sentido {user_emotion[0]}. '
                message += 'Quer conversar sobre isso?\n'
                return (message)
            else:
                return self.comm.get_response(self.clean(message))
        else:
            return self.comm.get_response(self.clean(message))

    def clean(self, message):
        """
        Remove upper letters and possible abbreviations.

        Might be improved to remove other words, like adverbs
        and some pronouns.
        """
        # message = self.remove_punctuations(message)
        message = self.switch_abbreviations(message)
        message = self.remove_words(message)
        return message.lower()

    def switch_abbreviations(self, message, files=["abbreviations.json"]):
        message = " {} ".format(message)
        try:
            for file in files:
                FILE_PATH = str(os.getcwd()) + '/bot/dialogs/switches/' + file
                with open(FILE_PATH, 'r') as file:
                    common_abbr = json.load(file)
                    for word in common_abbr:
                        message = message.replace(
                            (' ' + word + ' '), (' ' + common_abbr[word] + ' ')
                        )
            message = message[1:-1]
            return message
        except FileNotFoundError:
            raise FileNotFoundError

    def remove_words(self, message, files=["articles.json", "pronouns.json"]):
        message = " {} ".format(message)
        try:
            for file in files:
                FILE_PATH = str(os.getcwd()) + '/bot/dialogs/removals/' + file
                with open(FILE_PATH, 'r') as file:
                    removals = json.load(file)

                    for word in removals:
                        message = message.replace((' ' + word + ' '), (' '))
            message = message[1:-1]
            return message
        except FileNotFoundError:
            raise FileNotFoundError
