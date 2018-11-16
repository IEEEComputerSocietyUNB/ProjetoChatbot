import os
import sys
import random
import logging
import telegram

import time
import json
from datetime import timedelta
from datetime import datetime
from time import sleep

import sqlite3
import pygal
import emoji
from time import sleep
from telegram import Bot, User, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Dispatcher,\
    MessageHandler, Filters, CallbackQueryHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bot.communication import Communication
from bot.config_reader import retrieve_default
from bot.periodic_messages_util import Periodic_mesages_util
from bot.communication import Communication
from bot.dbutils import DBUtils as dbu


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
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.emotion_handler = False
        self.logger = logging.getLogger("LOG")
        self.app = Bot(token)
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        start_handler = CommandHandler("start", self.start)
        self.dispatcher.add_handler(start_handler)

        info_handler = CommandHandler("info", self.info)
        self.dispatcher.add_handler(info_handler)

        helpme_handler = CommandHandler("helpme", self.helpme)
        self.dispatcher.add_handler(helpme_handler)

        contatos_handler = CommandHandler("contatos", self.contatos)
        self.dispatcher.add_handler(contatos_handler)


        lembrete_handler = CommandHandler('lembrete', self.lembrete)
        self.dispatcher.add_handler(lembrete_handler)

        self.dispatcher.add_handler(CallbackQueryHandler(self.button))

        message_handler = MessageHandler(Filters.text, self.text_message,
                                         pass_job_queue=True)

        emotion_handler = CommandHandler("emotion", self.emotional_state)
        self.dispatcher.add_handler(emotion_handler)

        emotions_chart_handler = CommandHandler(
            "emotionchart", self.emotional_state_chart
        )
        self.dispatcher.add_handler(emotions_chart_handler)

        message_handler = MessageHandler(Filters.text, self.text_message)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_error_handler(self.error)
        self.periodic_mesages_util = Periodic_mesages_util()
        
    def send_type_action(self, bot, update):
        """
        Shows status typing when sending message
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        sleep(1)

    def start(self, bot, update):
        """
        Start command to receive /start message on Telegram.

        @bot = information about the bot
        @update = the user info.
        """
        self.send_type_action(bot, update)
        name = update.message["chat"]["first_name"]
        start_text = (
            f"Olá {name}, eu sou o Rabot."
            "\nUm robô bem simpático criado para alegrar seu dia!\n"
        )
        bot.send_message(chat_id=update.message.chat_id, text=start_text)
        start_text = (
            "Se quiser saber mais sobre mim ou meus criadores "
            "basta digitar `/info` ;)"
        )
        bot.send_message(
            chat_id=update.message.chat_id,
            text=start_text,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        start_text = "Agora vamos lá. Em que posso ajudá-lo?"
        bot.send_message(
            chat_id=update.message.chat_id,
            text=start_text,
            reply_markup=telegram.ReplyKeyboardRemove()
        )
        return 0

    def info(self, bot, update):
        """
        Info command to know more about the developers.

        @bot = information about the bot
        @update = the user info.
        """
        self.send_type_action(bot, update)
        with open(f"{os.getcwd()}/bot/dialogs/commands/info.md")\
                as info_file:
            info_text = info_file.read()
            bot.send_message(
                chat_id=update.message.chat_id,
                text=info_text,
                parse_mode=telegram.ParseMode.MARKDOWN,
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
        with open(f"{os.getcwd()}/bot/dialogs/commands/help.md") as help_file:
            helpme_text = help_file.read()
            bot.send_message(
                chat_id=update.message.chat_id,
                text=helpme_text,
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        return 0

    def contatos(self, bot, update):
        """
        Shows all contact centers to the bot user
        """

        self.send_type_action(bot, update)
        with open(f"{os.getcwd()}/bot/dialogs/contacts.md") as contatos_file:
            contatos_text = contatos_file.read()
            bot.send_message(
                chat_id=update.message.chat_id,
                text=contatos_text,
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        return 0

    def lembrete(self, bot, update, file_name='users_custom_invervals.json'):
        """
        Asks the frequency (in days) on witch the user wants to
        be reminded to chat
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + file_name
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)
        except FileNotFoundError:
            intervals_dict = self.periodic_mesages_util. \
                build_custom_interval_file()
        max_interval = intervals_dict.get("max_interval")
        self.periodic_mesages_util. \
            ask_for_interval(bot, update)

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
        except FileNotFoundError:
            intervals_dict = self.periodic_mesages_util. \
                build_custom_interval_file()

        interval = int(intervals_dict.get("default_interval"))
        chatID = update.message.chat_id
        if (intervals_dict.get(str(chatID) is not None)):
            interval = int(intervals_dict.get(str(chatID)))
        job_queue.run_repeating(self.callback_lets_talk,
                                interval=timedelta(days=interval),
                                name='reminder_job',
                                context=update)
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING

    def text_message(self, bot, update):
        self.send_type_action(bot, update)

        if not self.check_for_emotion(update):
            message = update.effective_message.text
            update.effective_message.reply_text(
                str(self.comm.respond(message))
            )
        return 0

    def check_for_emotion(self, update):
        if self.emotion_handler:
            self.emotional_state_collect_emotion(
                update,
                update.effective_message.text
            )
            if len(update.effective_message.text) <= 1:
                return True
            return False

    def emotional_state_collect_emotion(self, update, msg_text):
        """
        When the user chooses an option based on how he or she is feeling
        a certain moment. This method is called to evaluate which option
        has been choosen and then call the method responsible for storing
        the information.

        @update = the user info.
        @msg_text = the option the user has choosen
        """
        with open("bot/dialogs/emotions.json", "r") as rf:
            data = json.load(rf)
        response = random.choice(data[emoji.demojize(msg_text)]["statements"])
        response = str(response)
        emotion_type = int(data[emoji.demojize(msg_text)]["emotion_type"])

        update.effective_message.reply_text(response)
        update.effective_message.reply_text(
            "Em breve, eu te apresentarei um diário com maiores informações.",
            reply_markup=ReplyKeyboardRemove(),
        )
        self.emotion_handler = False
        self.emotional_state_store_emotion(update, emotion_type)
        return 0

    def emotional_state_store_emotion(self, update, emotion_type):
        """
        This method stores the emotion the user are feeling in a certain
        moment in a database.

        @emotion_type = a numeric value which is associated with an emotion
        """
        user_id = str(update.message.from_user.id)
        datetime_statement = time.time()

        connection = dbu.db_connect("emotions.sqlite3")
        dbu.create_emotion(
            connection,
            user_id,
            datetime_statement,
            emotion_type
        )
        connection.close()
        return 0

    def emotional_state(self, bot, update):
        """
        Asks how the user is feeling in a certain moment

        @bot = information about the bot
        @update = the user info.
        """
        self.send_type_action(bot, update)
        name = update.message["chat"]["first_name"]
        start_text = (
            f"{name}, eu gostaria de saber como você está se sentindo agora\n"
        )

        bot.send_message(chat_id=update.message.chat_id, text=start_text)
        faces_keyboard = []
        with open("bot/dialogs/emotions.json", "r") as rf:
            data = json.load(rf)
            for item in data:
                faces_keyboard.append(
                    [{"text": emoji.emojize(item, use_aliases=True)}]
                )

        # faces_keyboard = [
        #     [{"text": emoji.emojize(":laughing:", use_aliases=True)}],
        #     [{"text": emoji.emojize(":smile:", use_aliases=True)}],
        #     [{"text": emoji.emojize(
        #         ":expressionless_face:", use_aliases=True
        #     )}],
        #     [{"text": emoji.emojize(":disappointed:", use_aliases=True)}],
        #     [{"text": emoji.emojize(":angry_face:", use_aliases=True)}],
        # ]

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Qual dessas caras exprime melhor o seu estado atual?\n",
            reply_markup={
                "keyboard": faces_keyboard,
                "resize_keyboard": False,
                "one_time_keyboard": True,
            },
        )
        self.emotion_handler = True
        return 0

    def emotional_state_chart(self, bot, update):
        """
        Generate charts based on the emotional reports the user has sent

        @bot = information about the bot
        @update = the user info.
        """
        self.send_type_action(bot, update)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Vou mostrar para você o que tenho até o momento.",
        )

        # make a query to the sqlite3 database to retrieve the recorded
        # information about the user's current emotional state
        connector = dbu.db_connect("emotions.sqlite3")
        rows = dbu.select_emotions_count(
            connector,
            str(update.message.from_user.id)
        )
        if rows is None or len(rows) == 0:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Parece que você ainda não utilizou o comando /emotion"
                "para que você possa me dizer algumas informações.",
            )
            return 0
        emotions = {
            1: "Raiva",
            2: "Triste",
            3: "Normal",
            4: "Bom",
            5: "Excelente"
        }
        pie_chart = pygal.Pie(
            half_pie=True,
            legend_at_bottom=True,
            print_values=True,
            style=pygal.style.LightSolarizedStyle,
        )
        pie_chart.title = "Gráfico das suas ultimas emoções"
        for row in rows:
            pie_chart.add(emotions[row[0]], row[1])
        chart_name = f"output_pie_{str(update.message.from_user.id)}.png"
        rd = pie_chart.render_to_png(chart_name)
        bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(chart_name, "rb")
        )
        if os.path.exists(chart_name):
            os.remove(chart_name)
        return 0

    def error(self, bot, update, error):
        self.logger.warning(f'Update "{update}" caused error "{error}"')
        return 0

    def run(self):
        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()
        return 0


if __name__ == "__main__":
    # Variables set on Heroku
    TOKEN = os.environ.get("TOKEN")
    NAME = os.environ.get("NAME")
    # Port is given by Heroku
    PORT = os.environ.get("PORT")
    if TOKEN is not None:
        bot = Application(TOKEN, use_watson=False)
        bot.updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN)
        bot.updater.bot.set_webhook(f"https://{NAME}.herokuapp.com/{TOKEN}")
        bot.updater.idle()

    # Run on local system once detected that it's not on Heroku
    else:
        try:
            token = retrieve_default("TELEGRAM")["token"]
            watson = eval(retrieve_default()["IBM Watson"])
            x = Application(token=token, use_watson=watson)
            x.run()
        except FileNotFoundError:
            print("Configuration file not found.")
            sys.exit(1)
