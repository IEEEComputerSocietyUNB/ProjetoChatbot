from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import os
import json


class Communication:

    def __init__(self):
        """
        Generator for dealing with most messages the bot will receive
        from user
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
        Method that receives message from user and returns
        corresponding answer
        """
        return self.comm.get_response(self.clean(message))

    def clean(self, message, file='abbreviations.json'):
        """
        Method to remove upper letters and possible abbreviations.
        Might be improved to remove other words, like adverbs
        and some pronouns
        """
        ABBR_PATH = str(os.getcwd())
        ABBR_PATH += '/bot/dialogs/abbreviations/' + file
        try:
            with open(ABBR_PATH, 'r') as file:
                commom_abbr = json.load(file)
                for word in commom_abbr:
                    message = message.replace(
                        (' ' + word), (' ' + commom_abbr[word])
                    )
                    message = message.replace(
                        (word + ' '), (commom_abbr[word] + ' ')
                    )
        except FileNotFoundError:
            raise FileNotFoundError
        return message.lower()
