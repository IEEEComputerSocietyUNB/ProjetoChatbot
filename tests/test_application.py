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
        try:
            self.tgbot = Application(retrieve_default()['token'], False)
        except FileNotFoundError:
            pass

    @unittest.skipUnless(os.path.exists("./bot/config.ini"),
                         "Configuration file not found")
    def test_if_retrieve_default_works(self):
        self.assertEqual(type(dict(retrieve_default())), type({}))

    @unittest.skipUnless(os.path.exists("./bot/config.ini"),
                         "Configuration file not found")
    def test_if_retrieve_default_has_token(self):
        self.assertTrue('token' in list(retrieve_default()))

    @unittest.skipUnless(os.path.exists("./bot/config.ini"),
                         "Configuration file not found")
    def test_if_retrieve_without_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            retrieve_default("fail.ini")

    @patch('telegram.Bot')
    def test_info_message(self, bot):
        self.assertEqual(self.tgbot.info(bot, bot), 0)

    @patch('telegram.Bot')
    def test_start_method(self, bot):
        self.assertEqual(self.tgbot.start(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    @patch('telegram.ext.JobQueue')
    def test_reset_reminder_timer(self, comm, bot, job_queue):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.
                         reset_reminder_timer(bot, bot, job_queue), 0)

    @patch('telegram.Bot')
    def text_button(self, bot):
        self.assertEqual(self.tgbot.button(bot, bot), 0)

    def test_set_user_custom_interval(self):
        interval = 3
        chatID = "123456789"
        self.assertEqual(self.tgbot.
                         set_user_custom_interval(interval, chatID), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_ask_for_interval(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.
                         ask_for_interval(bot, bot, "Tente novamente"), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_lembrete(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.lembrete(bot, bot), 0)

    @patch('telegram.Bot')
    @patch('telegram.ext.Job')
    def test_callback_lets_talk(self, bot, job):
        self.assertEqual(self.tgbot.callback_lets_talk(bot,
                         job), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    @patch('telegram.ext.JobQueue')
    def test_text_message(self, comm, bot, job_queue):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.text_message(bot, bot, job_queue), 0)

    def test_error_method(self):
        self.assertEqual(self.tgbot.error("", "", ""), 0)

    @patch('telegram.ext.Updater')
    def test_run_method(self, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.run(), 0)


if __name__ == '__main__':
    unittest.main(exit=False)
