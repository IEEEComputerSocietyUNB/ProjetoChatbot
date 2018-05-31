from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import os


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
        return self.comm.get_response(message)
