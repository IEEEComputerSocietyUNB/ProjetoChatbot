import os
import sys
import random
import logging
import telegram
import json
from datetime import timedelta
from datetime import datetime
from time import sleep
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, \
    Dispatcher, MessageHandler, Filters
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.communication import Communication
from bot.config_reader import retrieve_default
from bot.periodic_messages_util import Periodic_mesages_util


class Application:
    """
    The chatbot per se, it contains the Communication class to deal with
    oncoming messages and also handles all Telegram related commands.
    Might soon have a sibling to deal with Facebook.
    """
    def __init__(self, token, train=True, use_watson=True):
        if train:
            self.comm = Communication(use_watson)

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

        helpme_handler = CommandHandler('helpme', self.helpme)
        self.dispatcher.add_handler(helpme_handler)

        contatos_handler = CommandHandler('contatos', self.contatos)
        self.dispatcher.add_handler(contatos_handler)

        lembrete_handler = CommandHandler('lembrete', self.lembrete)
        self.dispatcher.add_handler(lembrete_handler)

        weekly_handler = CommandHandler('resumo', 
                                        self.weekly_resume,
                                        pass_args=True)
       
        find_weekly_handler = CommandHandler('historico',
                                            self.find_weekly_resume)

        self.dispatcher.add_handler(find_weekly_handler)

        self.dispatcher.add_handler(weekly_handler)

        self.dispatcher.add_handler(CallbackQueryHandler(self.button))

        message_handler = MessageHandler(Filters.text, self.text_message,
                                         pass_job_queue=True)

        weekly_message_handler = MessageHandler(Filters.text, self.weekly_update,
                                         pass_job_queue=True)

        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(weekly_message_handler)

        self.dispatcher.add_error_handler(self.error)

        self.periodic_mesages_util = Periodic_mesages_util()

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
        start_text = f"Olá {name}, eu sou o Rabot.\n" + \
            "Um robô bem simpático criado para alegrar seu dia!\n"
        bot.send_message(chat_id=update.message.chat_id, text=start_text)
        start_text = "Se quiser saber mais sobre mim ou meus criadores " + \
            "basta digitar `/info` ;)"
        bot.send_message(
            chat_id=update.message.chat_id, text=start_text,
            parse_mode=telegram.ParseMode.MARKDOWN)
        start_text = "Agora vamos lá. Em que posso ajudá-lo?"
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
        with open(f"{os.getcwd()}/bot/dialogs/info.md") as info_file:
            info_text = info_file.read()
            bot.send_message(
                chat_id=update.message.chat_id,
                text=info_text,
                parse_mode=telegram.ParseMode.MARKDOWN
            )
            return 0
        return 1

    def helpme(self, bot, update):
        """
        Helpme command to show information about help sources
        for people in critical situations
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        with open(f"{os.getcwd()}/bot/dialogs/help.md") as help_file:
            helpme_text = help_file.read()
            bot.send_message(
                chat_id=update.message.chat_id,
                text=helpme_text,
                parse_mode=telegram.ParseMode.MARKDOWN
            )
        return 0

    def contatos(self, bot, update):
        """
        Shows all contact centers to the bot user
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )

        with open(f"{os.getcwd()}/bot/dialogs/contacts.md") as contatos_file:
            contatos_text = contatos_file.read()
            bot.send_message(
                chat_id=update.message.chat_id,
                text=contatos_text,
                parse_mode=telegram.ParseMode.MARKDOWN
            )
        return 0

    def lembrete(self, bot, update, file='users_custom_invervals.json'):
        """
        Asks the frequency (in days) on which the user wants to
        be reminded to chat
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + file
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)
                max_interval = intervals_dict.get("max_interval")
                message = "Com que frequencia você quer ser lembrado de " + \
                          "dialogar com o bot? Diga um intervalo em dias " + \
                          "inferior a {}".format(max_interval)

                self.periodic_mesages_util. \
                    ask_for_interval(bot, update, message)
        except FileNotFoundError:
            print("File not found error")

        return 0

    def weekly_resume(self, bot, update, args):
        """
        Asks about the user's week experiences
        """
        message = ' '.join(args)

        # TODO : add message and user to database

        bot.send_message(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

    def find_weekly_messages(self, bot, update):
        """
        Search database to find saved weekly resumes
        """
        # TODO
        pass

    def button(self, bot, update):
        """
        Parse the callback_query for the button pressed and call
        apropriate handler
        """
        query = update.callback_query
        # query.data is the string payload sended. Exemple: "5-7267119" where
        # the single digit prior to "-" is the interval and the nuber
        # after is the chatID from the user

        index = query.data.find("-")
        interval = int(query.data[0])
        chatID = query.data[index + 1:]
        if(interval >= 1 and interval <= 9):
            return_value = self.periodic_mesages_util. \
                set_user_custom_interval(interval, chatID)
            if(return_value == 0):
                bot.edit_message_text(text="Frequência alterada",
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id)
        return 0

    def callback_lets_talk(self, bot, job):
        bot.send_message(chat_id=job.context.message.chat_id,
                         text='Vamos conversar?')
        return 0

    def text_message(self, bot, update,
                     job_queue, file_name='users_custom_invervals.json'):
        # The user interacted with the bot so the scheduled
        # reminders to use the bot should be removed
        jobs = job_queue.get_jobs_by_name('reminder_job')
        # print(jobs)
        for job in jobs:
            job.schedule_removal()

        # starting timer for next reminder to chat
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + file_name
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)
                interval = int(intervals_dict.get("default_interval"))
                chatID = update.message.chat_id
                if (intervals_dict.get(str(chatID) is not None)):
                    interval = int(intervals_dict.get(str(chatID)))
                job_queue.run_repeating(self.callback_lets_talk,
                                        interval=timedelta(days=interval),
                                        name='reminder_job',
                                        context=update)
        except FileNotFoundError:
            print("File not found error")
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        message = update.effective_message.text
        update.effective_message.reply_text(str(self.comm.respond(message)))
        return 0

    def callback_week(self, bot, job):
        bot.send_message(chat_id=job.context.message.chat_id,
                         text='Use /resumo e me conte como foi sua semana!')

    def weekly_update(self, bot, update, job_queue):
        """ Requests weekly update from user """
        job_queue.run_repeating(self.callback_week,
                                     interval=60,
                                     first=0,
                                     name='weekly',
                                     context=update)

    def error(self, bot, update, error):
        self.logger.warning(
            f'Update "{update}" caused error "{error}"'
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
    # Variables set on Heroku
    TOKEN = os.environ.get('TOKEN')
    NAME = os.environ.get('NAME')
    # Port is given by Heroku
    PORT = os.environ.get('PORT')
    if TOKEN is not None:
        bot = Application(TOKEN, use_watson=False)
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
    else:
        try:
            token = retrieve_default()['token']
            x = Application(token, use_watson=False).run()
        except FileNotFoundError:
            print('Configuration file not found.')
            sys.exit(1)
