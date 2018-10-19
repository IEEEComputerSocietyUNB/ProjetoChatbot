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
            self.tgbot = Application(
                retrieve_default("TELEGRAM")["token"],
                train=False
            )
            self.periodic_messages = Periodic_mesages_util()
        except FileNotFoundError:
            pass

    def test_set_user_custom_interval(self):
        interval = 3
        chatID = "123456789"
        self.assertEqual(self.periodic_messages.
                         set_user_custom_interval(interval, chatID), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_ask_for_interval(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.periodic_messages.
                         ask_for_interval(bot, bot), 0)

    def test_build_custom_interval_file(self):
        default_dict = {"default_interval": 3, "max_interval": 7}
        self.assertEqual(self.periodic_messages.
                         build_custom_interval_file(), default_dict)


if __name__ == '__main__':
    unittest.main(exit=False)
