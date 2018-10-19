import os
import sys
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)


class Periodic_mesages_util:

    def __init__(self):
        self.default_message= "Com que frequencia você quer ser lembrado " + \
                                "de dialogar com o bot? Diga um intervalo  " + \
                                "em dias inferior a {max_interval}"

    def ask_for_interval(self, bot, update):
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
            text=self.default_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            one_time_keyboard=True
        )
        return 0

    def set_user_custom_interval(self, interval, chatID,
                                 file_name='users_custom_invervals.json'):
        """
        Write the user defined interval of reminder to chat in to the
        users_custom_invervals.json file
        """
        try:
            FILE_PATH = str(os.getcwd()) + '/bot/' + file_name
            with open(FILE_PATH) as data_file:
                intervals_dict = json.load(data_file)
        except FileNotFoundError:
            intervals_dict = self.build_custom_interval_file()

        intervals_dict[chatID] = str(interval)
        with open(FILE_PATH, "w") as data_file:
            json.dump(intervals_dict, data_file)

        return 0

    def build_custom_interval_file(self,
                                   file_name='users_custom_invervals.json'):
        default_dict = {"default_interval": 3, "max_interval": 7}
        FILE_PATH = str(os.getcwd()) + '/bot/' + file_name
        with open(FILE_PATH, "w") as data_file:
            json.dump(default_dict, data_file)
        return default_dict
