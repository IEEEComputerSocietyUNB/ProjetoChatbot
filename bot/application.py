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
from configparser import ConfigParser
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, \
    Dispatcher, MessageHandler, Filters
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
        raise FileNotFoundError


class Application:
    """
    The chatbot per se, it contains the Communication class to deal with
    oncoming messages and also handles all Telegram related commands.
    Might soon have a sibling to deal with Facebook.
    """
    def __init__(self, token, train=True):
        if train:
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

        helpme_handler = CommandHandler('helpme', self.helpme)
        self.dispatcher.add_handler(helpme_handler)

        contatos_handler = CommandHandler('contatos', self.contatos)
        self.dispatcher.add_handler(contatos_handler)

        lembrete_handler = CommandHandler('lembrete', self.lembrete)
        self.dispatcher.add_handler(lembrete_handler)

        self.dispatcher.add_handler(CallbackQueryHandler(self.button))

        message_handler = MessageHandler(Filters.text, self.text_message,
                                         pass_job_queue=True)
        self.dispatcher.add_handler(message_handler)

        self.dispatcher.add_error_handler(self.error)

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

    def ask_for_interval(self, bot, update, message):
        """
        Builds the keyboard and prompts it to the user with the message
        argument
        """
        # numeric keyboard
        digit_list = []
        for i in range(1, 10):
            callback_data = "{}-{}".format(str(i),str(update.message.chat_id))
            button = InlineKeyboardButton(str(i), callback_data=callback_data)
            digit_list.append(button)

        keyboard = [digit_list[0:3],
                    digit_list[3:6],
                    digit_list[6:9]
                    ]

        bot.send_message(
            chat_id=update.message.chat_id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            one_time_keyboard=True
        )
        return 0

    def lembrete(self, bot, update):
        """
        Asks the frequency (in days) on witch the user wants to
        be reminded to chat
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + \
                "users_custom_invervals.json"
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)
                max_interval = intervals_dict.get("max_interval")
                message = "Com que frequencia você quer ser lembrado de " + \
                          "dialogar com o bot? Diga um intervalo em dias " + \
                          "inferior a {}".format(max_interval)

                self.ask_for_interval(bot, update, message)
        except FileNotFoundError:
            print("File not found error")

        return 0

    def set_user_custom_interval(self, interval, chatID):
        """
        Write the user defined interval of reminder to chat in to the
        users_custom_invervals.json file
        """
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + \
                "users_custom_invervals.json"
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)

            intervals_dict[chatID] = str(interval)

            FILE_PATH = str(os.getcwd()) + '/bot/' + \
                "users_custom_invervals.json"
            with open(FILE_PATH, "w") as data_file:
                json.dump(intervals_dict, data_file)

        except FileNotFoundError:
            print("File not found error")
        return 0

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
            if(self.set_user_custom_interval(interval, chatID) == 0):
                bot.edit_message_text(text="Frequência alterada",
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id)

        else:
            self.ask_for_interval(bot, update, "Tente novamente")

        return 0

    def reset_reminder_timer(self, bot, update, job_queue):
        """
        Remove previus scheduled reminder and sets a new one
        """
        # Removing previus job
        jobs = job_queue.get_jobs_by_name('reminder_job')
        # print(jobs)
        for job in jobs:
            job.schedule_removal()

        # starting timer for next reminder to chat
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + \
                "users_custom_invervals.json"
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

        return 0

    def callback_lets_talk(self, bot, job):
        bot.send_message(chat_id=job.context.message.chat_id,
                         text='Vamos conversar?')
        return 0

    def text_message(self, bot, update, job_queue):
        self.reset_reminder_timer(bot, update, job_queue)
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        message = update.effective_message.text
        update.effective_message.reply_text(str(self.comm.respond(message)))
        return 0

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
            x = Application(token).run()
        except FileNotFoundError:
            print('Configuration file not found.')
            sys.exit(1)
