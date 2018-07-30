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
from bot.application import Application, retrieve_default


class TestBotBasics(unittest.TestCase):

    def setUp(self):
        self.tgbot = Application(retrieve_default()['token'])

    def test_if_retrieve_default_works(self):
        self.assertEqual(type(dict(retrieve_default())), type({}))

    def test_if_retrieve_default_has_token(self):
        self.assertTrue('token' in list(retrieve_default()))

    def test_if_retrieve_without_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            retrieve_default("fail.ini")

    def test_if_bot_is_unbchatbot(self):
        """
        Check if bot being initialized is truly the unbchatbot
        """
        self.assertEqual(self.tgbot.verify_bot(), ('unbchatbot', 330147863))

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

    @patch('telegram.Bot')
    @patch('telegram.ext.Updater')
    def test_any_message(self, bot, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.any_message(bot, self.tgbot.updater, \
                        self.tgbot.updater.job_queue), 0)

    @patch('telegram.Bot')
    @patch('telegram.ext.Updater')
    def test_callback_lets_talk(self, bot, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.callback_lets_talk(bot, self.tgbot.updater.job_queue), 0)


if __name__ == '__main__':
    unittest.main()
