import telegram
import os
import sys
import logging
import random
from time import sleep
from telegram import Bot
from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler, Dispatcher, MessageHandler, \
    Filters
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.communication import Communication


def retrieve_default(file='config.ini'):
    """
    Function to retrieve all informations from token file.
    Usually retrieves from config.ini
    """
    try:
        FILE_PATH = str(os.getcwd()) + '/bot/' + file
        config = ConfigParser()
        with open(FILE_PATH) as file:
            config.read_file(file)
        return(config['DEFAULT'])
    except FileNotFoundError:
        print("File not found error")
        raise FileNotFoundError


class Application:
    """
    The chatbot per se, it contains the Communication class to deal with
    oncoming messages and also handles all Telegram related commands.
    Might soon have a sibling to deal with Facebook.
    """
    def __init__(self, token):
        self.comm = Communication()
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        self.logger = logging.getLogger("log")
        self.app = Bot(token)
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        info_handler = CommandHandler('info', self.info)
        self.dispatcher.add_handler(info_handler)

        helpme_handler = CommandHandler('helpme', self.helpme)
        self.dispatcher.add_handler(helpme_handler)

        contatos_handler = CommandHandler('contatos', self.contatos)
        self.dispatcher.add_handler(contatos_handler)

        message_handler = MessageHandler(Filters.text, self.text_message)
        self.dispatcher.add_handler(message_handler)

        self.dispatcher.add_error_handler(self.error)

    def verify_bot(self):
        """
        Method to check if bot is as expected
        """
        return(self.app.get_me().username, self.app.get_me().id)

    def start(self, bot, update):
        """
        Start command to receive /start message on Telegram.
        @bot = information about the bot
        @update = the user info.
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        sleep(3.5)
        name = update.message['chat']['first_name']
        start_text = "Olá {},".format(name) + "Eu sou o Rabot.\n" + \
            "Estou aqui para alegrar o seu dia!\n" + "Em que posso ajudá-lo?"
        bot.send_message(chat_id=update.message.chat_id, text=start_text)
        return 0

    def info(self, bot, update):
        """
        Info command to know more about the developers.
        @bot = information about the bot
        @update = the user info.
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        info_text = "Saiba mais sobre mim acessando minha",\
            "página de desenvolvimento!\n",\
            "https://github.com/ComputerSocietyUNB/ProjetoChatbot"
        bot.send_message(
            chat_id=update.message.chat_id,
            text=info_text,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        print('info sent')
        return 0

    def helpme(self, bot, update):
        """
        Helpme command to show information about help sources
        for people in critical situations
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        helpme_text = "Você quer conversar com alguém? Existem muitas opções",\
            "e eu posso te indicar algumas. Que tal entrar em contato com", \
            "algumas pessoas?",\
            "CVV: https://www.cvv.org.br/quero-conversar/",\
            "UnB/CAEP: 3107-1680",\
            "Unip:     3349-0046",\
            "Instituto Brasiliense de Análise de Comportamento: ", \
            "3242-5250 ou 3443-4086",\
            "Quer ver mais? Digite /contatos"
        bot.send_message(
            chat_id=update.message.chat_id,
            text=helpme_text,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

    def contatos(self, bot, update):
        """
        Shows all contact centers to the bot user
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )

        contatos_text = "Lista completa de contatos para", \
            "Psicologia Gratuita ou de Baixo Custo:\n", \
            "CVV: https://www.cvv.org.br/quero-conversar/\n",\
            "UnB/CAEP: 3107-1680\n",\
            "Unip: 3349-0046\n",\
            "Instituto Brasiliense de Análise de Comportamento:", \
            "3242-5250 ou 3443-4086\n",\
            "Centro de Orientação Médico ou Psicopedagógico:", \
            "3325-4995 ou 3326-3201\n",\
            "Associação Brasiliense de Psicodrama e Sociodrama:", \
            "3245-6390 ou 3346-6832\n",\
            "UNICEUB: 3966-1687 ou 3966-1626\n",\
            "Universidade Católica de Brasília: 3356-9328\n",\
            "Escola Lacaniana de Psicanalise de Brasília:", \
            "99976-5818 ou 3242-5615 ou 3345-0169\n",\
            "IGTB - Instituto de Gestalt-Terapia de Brasília:", \
            "3033-7094 ou 9967-7569\n",\
            "Instituto São Paulo de Análise Comportamento:", \
            "3425-2717 ou 3327-7338\n",\
            "Clínica Social do IMPI: 3364-2745\n",\
            "Clínica Social INTERPSI/CBP: 98118-0548 ou 99982-3224\n",\
            "IBNeuro - Instituto Brasileiro de Neuropsicológica:", \
            "3226-3002 ou 3225-9185\n",\
            "Clínica Social de Taguatinga: 3967-3060\n",\
            "SOBRAP: Instituto Brasileiro de Psicanálise, Dinâmica", \
            "de Grupo e Psicodrama: 3323-5366"

        bot.send_message(
            chat_id=update.message.chat_id,
            text=contatos_text,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

    def text_message(self, bot, update):
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        message = update.effective_message.text
        update.effective_message.reply_text(str(self.comm.respond(message)))
        return 0

    def error(self, bot, update, error):
        self.logger.warning(
            'Update "{0}" caused error "{1}"'.format(update, error)
        )
        return 0

    def run(self):
        # Start the Bot
        print('Bot configured. Receiving messages now.')
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()
        return 0


if __name__ == '__main__':
    # try to run with Heroku variables
    try:
        # Variables set on Heroku
        TOKEN = os.environ.get('TOKEN')
        NAME = os.environ.get('NAME')
        # Port is given by Heroku
        PORT = os.environ.get('PORT')

        bot = Application(TOKEN)
        bot.updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN
        )
        bot.updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(NAME, TOKEN)
        )
        bot.updater.idle()

    # Run on local system once detected that it's not on Heroku
    except Exception as inst:
        try:
            token = retrieve_default()['token']
            x = Application(token)
            x.run()
        except FileNotFoundError:
            print('Configuration file not found.')
            sys.exit(1)
