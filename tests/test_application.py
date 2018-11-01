import unittest
import os
import sys
import logging
from telegram import Bot
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from bot.application import Application
from bot.config_reader import retrieve_default


class TestBotBasics(unittest.TestCase):
    def setUp(self):
        try:
            self.tgbot = Application(
                retrieve_default("TELEGRAM")["token"],
                train=False
            )
        except FileNotFoundError:
            pass

    @patch("telegram.Bot")
    def test_info_message(self, bot):
        self.assertEqual(self.tgbot.info(bot, bot), 0)

    @patch("telegram.Bot")
    def test_start_method(self, bot):
        self.assertEqual(self.tgbot.start(bot, bot), 0)

    @patch('telegram.Bot')
    def text_button(self, bot):
        self.assertEqual(self.tgbot.button(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_contatos(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.contatos(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_helpme(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.helpme(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_lembrete(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.lembrete(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_find_weekly_resume(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.find_weekly_resume(bot, bot), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    def test_lembrete_wrong_file(self, comm, bot):
        self.tgbot.comm = comm
        file_name = "another_file_name.json"
        self.assertEqual(self.tgbot.lembrete(bot, bot, file_name), 0)

    @patch('telegram.Bot')
    @patch('telegram.ext.Job')
    def test_callback_lets_talk(self, bot, job):
        self.assertEqual(self.tgbot.callback_lets_talk(bot,
                         job), 0)

    @patch('telegram.Bot')
    @patch('telegram.ext.Job')
    def test_callback_week(self, bot, job):
        self.assertEqual(self.tgbot.callback_week(bot,
                         job), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    @patch('telegram.ext.JobQueue')
    def test_weekly_update(self, comm, bot, job_queue):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.weekly_update(bot, bot, job_queue), 0)

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    @patch('telegram.ext.JobQueue')
    def test_text_message(self, comm, bot, job_queue):
        self.tgbot.comm = comm
        self.assertEqual(self.tgbot.text_message(bot, bot, job_queue), 0)

    @patch("bot.communication.Communication")
    @patch("telegram.Bot")
    def test_text_message(self, comm, bot):
        self.tgbot.comm = comm
        file_name = "another_file_name.json"
        self.assertEqual(self.tgbot.
                         text_message(bot, bot, job_queue, file_name), 0)

    def test_error_method(self):
        self.assertEqual(self.tgbot.error("", "", ""), 0)

    @patch("telegram.ext.Updater")
    def test_run_method(self, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.run(), 0)


if __name__ == "__main__":
    unittest.main()
