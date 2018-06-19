import telegram
import os
import sys
import logging
import random
from datetime import timedelta
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
        self.job_queue = self.updater.job_queue

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        info_handler = CommandHandler('info', self.info)
        self.dispatcher.add_handler(info_handler)

        any_message_handler = MessageHandler(Filters.all, self.any_message, pass_job_queue=True)
        self.dispatcher.add_handler(any_message_handler)

        text_message_handler = MessageHandler(Filters.text, self.text_message)
        self.dispatcher.add_handler(text_message_handler, group=1)

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

    def text_message(self, bot, update):
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        message = update.effective_message.text
        update.effective_message.reply_text(str(self.comm.respond(message)))

    def any_message(self, bot, update, job_queue):
        #starting timer for next reminder to chat
        job_queue.run_repeating(self.callback_lets_talk, timedelta(days=3),
                                context=update)

    def callback_lets_talk(self, bot, job):
        bot.send_message(chat_id=job.context.message.chat_id,
                         text='Vamos conversar ?')

    def error(self, bot, update, error):
        self.logger.warning(
            'Update "{0}" caused error "{1}"'.format(update, error)
        )

    def run(self):
        # Start the Bot
        print('Bot configured. Receiving messages now.')
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    # def run_heroku(self, TOKEN, NAME, PORT):
    #     self.updater.start_webhook(
    #         listen="0.0.0.0",
    #         port=int(PORT),
    #         url_path=TOKEN
    #     )
    #     self.updater.bot.set_webhook(
    #         "https://{}.herokuapp.com/{}".format(NAME, TOKEN)
    #     )
    #     self.updater.idle()


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
