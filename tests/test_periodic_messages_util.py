import unittest
import os
import sys
from telegram import Bot
from unittest.mock import patch
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)

from bot.periodic_messages_util import Periodic_mesages_util
from bot.application import Application, retrieve_default


class TestBotPeriodicMessagesUtil(unittest.TestCase):

    def setUp(self):
        try:
            self.tgbot = Application(retrieve_default()['token'], False)
            self.periodic_messages = Periodic_mesages_util()

        except FileNotFoundError:
            pass

    def test_set_user_custom_interval(self):
        interval = 3
        chatID = "123456789"
        self.assertEqual(self.periodic_messages.
                         set_user_custom_interval(interval, chatID), 0)

    def test_nonexistent_set_user_custom_interval(self):
        interval = 3
        chatID = "987654321"
        self.assertEqual(self.periodic_messages.
                         set_user_custom_interval(interval, chatID), 0)

    def test_set_user_custom_interval_wrong_file(self):
        interval = 3
        chatID = "123456789"
        file_name = "another_file_name.json"
        self.assertEqual(self.periodic_messages.
                         set_user_custom_interval(interval, chatID, file_name), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_ask_for_interval(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.periodic_messages.
                         ask_for_interval(bot, bot, "Tente novamente"), 0)


if __name__ == '__main__':
    unittest.main(exit=False)
