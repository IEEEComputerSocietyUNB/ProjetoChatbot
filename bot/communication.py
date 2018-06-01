from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import os
import json


class Communication:

    def __init__(self):
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
        return self.comm.get_response(self.clean(message))

    def clean(self, message):
        ABBR_PATH = str(os.getcwd())
        ABBR_PATH += '/bot/dialogs/abbreviations/abbreviations.json'
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
