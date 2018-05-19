import telegram
import os
import sys
from time import sleep
from telegram import Bot
from telegram.ext import Updater, CommandHandler, Dispatcher
from configparser import ConfigParser
import logging


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
        self.bot = Bot(token)
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        info_handler = CommandHandler('info', self.info)
        self.dispatcher.add_handler(info_handler)

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
        name = update.message['chat']['first_name']
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        sleep(2)
        start_text = \
            "Olá {}, eu sou um chatbot em desenvolvimento".format(name)
        bot.send_message(chat_id=update.message.chat_id, text=start_text)

    def info(self, bot, update):
        """
        Info command to know more about the developers.
        @bot = information about the bot
        @update = the user info.
        """
        info_text = "This is the info!"
        bot.send_message(
            chat_id=update.message.chat_id,
            text="*bold* _italic_ `fixed font` [link](http://google.com).",
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        print('info sent')

    def run(self):
        # Start the Bot
        print('Bot configured. Receiving messages now.')
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()


if __name__ == '__main__':
    token = retrieve_default()['token']
    if(not token):
        print('Configuration file not found.')
        sys.exit(1)
    x = Chatbot(token)
    x.run()
