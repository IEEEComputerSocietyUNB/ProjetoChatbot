import unittest
import os
import sys
import logging
from telegram import Bot
from unittest.mock import patch
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.application import Application
from bot.config_reader import retrieve_default


class TestBotBasics(unittest.TestCase):

    def setUp(self):
        try:
            self.tgbot = Application(retrieve_default()['token'], False)
        except FileNotFoundError:
            pass

    @patch('telegram.Bot')
    def test_info_message(self, bot):
        self.assertEqual(self.tgbot.info(bot, bot), 0)

    @patch('telegram.Bot')
    def test_start_method(self, bot):
        self.assertEqual(self.tgbot.start(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_text_message(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.text_message(bot, bot), 0)

    def test_error_method(self):
        self.assertEqual(self.tgbot.error("", "", ""), 0)

    @patch('telegram.ext.Updater')
    def test_run_method(self, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.run(), 0)


if __name__ == '__main__':
    unittest.main()
