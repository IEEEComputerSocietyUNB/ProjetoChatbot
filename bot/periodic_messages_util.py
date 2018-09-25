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


class Periodic_mesages_util:

    def ask_for_interval(self, bot, update, message):
        """
        Builds the keyboard and prompts it to the user with the message
        argument
        """
        # numeric keyboard
        digit_list = []
        for i in range(1, 10):
            callback_data = "{}-{}".format(str(i), str(update.message.chat_id))
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

    def set_user_custom_interval(self, interval, chatID,
                                 file='users_custom_invervals.json'):
        """
        Write the user defined interval of reminder to chat in to the
        users_custom_invervals.json file
        """
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + file
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)

            intervals_dict[chatID] = str(interval)

            with open(FILE_PATH, "w") as data_file:
                json.dump(intervals_dict, data_file)

        except FileNotFoundError:
            print("File not found error")
        return 0
