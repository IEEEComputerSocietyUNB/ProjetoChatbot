import telegram
import os
import sys
import logging
from time import sleep
from telegram import Bot
from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler, Dispatcher, MessageHandler, \
    Filters


def retrieve_default():
    try:
        config = ConfigParser()
        config.read_file(open(str(os.getcwd())+'/bot/config.ini'))
        return(config['DEFAULT'])
    except Exception as e:
        return(e)


class Chatbot:
    """
    The chatbot per se! Yay <3
    """
    def __init__(self, token):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        self.logger = logging.getLogger("log")
        self.bot = Bot(token)
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        info_handler = CommandHandler('info', self.info)
        self.dispatcher.add_handler(info_handler)
        echo_handler = MessageHandler(Filters.text, self.echo)
        self.dispatcher.add_handler(echo_handler)
        self.dispatcher.add_error_handler(self.error)

    def verify_bot(self):
        return(self.bot.get_me().username, self.bot.get_me().id)

    def make_log(self):
        print(self.bot.getLogger())

    def start(self, bot, update):
        """
        Start command to start bot on Telegram.
        @bot = information about the bot
        @update = the user info.
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        sleep(3.5)
        name = update.message['chat']['first_name']
        start_text = \
            "Olá {}, eu sou um chatbot em desenvolvimento".format(name)
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
        info_text = "This is the info!"
        bot.send_message(
            chat_id=update.message.chat_id,
            text="*bold* _italic_ `fixed font` [link](http://google.com).",
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        print('info sent')

    def echo(self, bot, update):
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        update.effective_message.reply_text(update.effective_message.text)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def run(self):
        # Start the Bot
        print('Bot configured. Receiving messages now.')
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def run_heroku(self, TOKEN, NAME, PORT):
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN
        )
        self.updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(NAME, TOKEN)
        )
        self.updater.idle()


if __name__ == '__main__':
    # try to run with Heroku variables
    try:
        # Variables set on Heroku
        TOKEN = os.environ.get('TOKEN')
        NAME = os.environ.get('NAME')
        # Port is given by Heroku
        PORT = os.environ.get('PORT')

        bot = Chatbot(TOKEN)
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
        token = retrieve_default()['token']
        if(not token):
            print('Configuration file not found.')
            sys.exit(1)
        x = Chatbot(token)
        x.run()
