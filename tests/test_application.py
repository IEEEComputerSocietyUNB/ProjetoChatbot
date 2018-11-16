import unittest
import os
import sys
import logging
from telegram import Bot
from telegram.ext import Updater
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bot.application import Application
from bot.config_reader import retrieve_default
from bot.dbutils import DBUtils as dbu
import emoji
import random
import time


class TestBotBasics(unittest.TestCase):
    def setUp(self):
        try:
            self.tgbot = Application(
                retrieve_default("TELEGRAM")["token"],
                train=False
            )
        except FileNotFoundError:
            self.fail('Config.ini not found')

    @patch("telegram.Bot")
    def test_info_message(self, bot):
        self.assertEqual(self.tgbot.info(bot, bot), 0)

    @patch("telegram.Bot")
    def test_start_method(self, bot):
        self.assertEqual(self.tgbot.start(bot, bot), 0)

    @patch('telegram.Bot')
    def test_button(self, bot):
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
    def test_lembrete_wrong_file(self, comm, bot):
        self.tgbot.comm = comm
        file_name = "another_file_name.json"
        self.assertEqual(self.tgbot.lembrete(bot, bot, file_name), 0)

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

    @patch('bot.communication.Communication')
    @patch('telegram.Bot')
    @patch('telegram.ext.JobQueue')
    def test_text_message_wrong_file(self, comm, bot, job_queue):
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

    @patch('telegram.ext.Updater')
    @patch('telegram.Bot')
    def test_emotions_method(self, bot, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.emotional_state(bot, updater), 0)

    @patch('telegram.ext.Updater')
    @patch('telegram.Bot')
    def test_emotional_state_method(self, bot, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.emotional_state(bot, updater), 0)
        self.assertTrue(self.tgbot.emotion_handler)

    @patch('telegram.ext.Updater')
    @patch('telegram.Bot')
    def test_emotional_state_chart_method(self, bot, updater):
        self.tgbot.updater = updater
        self.assertEqual(self.tgbot.emotional_state_chart(bot, updater), 0)

    def test_database_creation(self):
        self.assertTrue(dbu.db_connect('test.sqlite3') is not None)

    @patch('telegram.Bot')
    def test_if_emotion_is_stored(self, bot):

        database_file = 'bot/test.sqlite3'
        emotions_list = [1, 2, 3, 4, 5]
        conn = dbu.db_connect('bot/test.sqlite3')
        user_id = str(random.randint(0, 100))
        dbu.create_emotion(conn,
                           user_id,
                           time.time(),
                           random.choice(emotions_list))
        self.assertTrue(conn is not None)
        conn = dbu.db_connect('bot/test.sqlite3')
        rows = dbu.select_emotions_count(conn, user_id)
        self.assertTrue(len(rows) > 0)

        if(os.path.exists(database_file)):
            os.remove(database_file)

    @patch('telegram.ext.Updater')
    def test_emotional_state_collect_emotion(self, update):
        emotions = [emoji.emojize(':laughing:', use_aliases=True),
                    emoji.emojize(':smile:', use_aliases=True),
                    emoji.emojize(':expressionless_face:', use_aliases=True),
                    emoji.emojize(':disappointed:', use_aliases=True),
                    emoji.emojize(':angry_face:', use_aliases=True)]
        face = random.choice(emotions)
        self.assertEqual(self.tgbot.emotional_state_collect_emotion(update,
                                                                    face), 0)


if __name__ == "__main__":
    unittest.main()
