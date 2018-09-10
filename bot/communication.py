from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import os
import json


class Communication:

    def __init__(self):
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
        self.comm.train('bot/dialogs/')

    def respond(self, message):
        """
        Receive message from user and returns corresponding answer.
        """
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
