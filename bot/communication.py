from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os


class Communication:

    def __init__(self):
        self.comm = ChatBot(
            "Comms",
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                },
                {
                    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                    'threshold': 0.65,
                    'default_response':
                        'Desculpa, mas não entendi sua mensagem.',
                }
            ],
            # read_only=True
        )

        self.comm.set_trainer(ListTrainer)

        # TODO create function to deal with training
        print(os.getcwd())
        self.comm.train([
            "Oi",
            "Olá, tudo bom?"
        ])

    def respond(self, message):
        return self.comm.get_response(message)
