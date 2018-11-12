import os
import sys
import unittest
from telegram import Bot
from unittest.mock import patch

from bot.screening import Screening

class TestScreening(unittest.TestCase):
    def setUp():
        self.screening = Screening()

    def tearDown(self):
        self.screening = None

    def test_build_question(self):
        question_index = 1
        self.assertEqual(self.screening.build_question(question_index), )
    def test_build_button_markup(self):
        question_index = 1
        self.assertEqual(self.screening.build_button_markup(question_index), )

    @patch('bot.communication.Communication')
    @patch("telegram.Bot")
    def test_button_clicked(self, comm, bot):
        self.tgbot.comm = comm
        self.assertEqual(self.screening.button_clicked(bot, bot), )
        
