import os
import sys
import unittest
from telegram import Bot
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from bot.screening.screening import Screening


class TestScreening(unittest.TestCase):
    def setUp(self):
        self.screening = Screening()

    def tearDown(self):
        self.screening = None

    def test_load_jsons(self):
        """
        Check if read the jsons appropriately
        """
        self.assertEqual(self.screening.load_jsons(), 0)
        self.assertEqual(type(self.screening.initial_answers), list)
        self.assertEqual(type(self.screening.initial_questions), list)
        self.assertEqual(type(self.screening.next_steps), dict)
        self.assertEqual(type(self.screening.scales_dict), dict)

    def test_dass_screen(self):
        self.assertEqual(type(self.screening.dass_screen("DASS_21A")), list)

    def test_get_equivalent_range(self):
        self.assertEqual(
            self.screening.get_equivalent_range('SOCIODEMOGRAFICO'), 0)
        self.assertEqual(self.screening.get_equivalent_range('DASS_21A'), 1)
        self.assertEqual(self.screening.get_equivalent_range('DASS_21D'), 2)
        self.assertEqual(self.screening.get_equivalent_range('DASS_21S'), 3)

    def test_evaluate(self):
        arr = [3, 0, 0, 0, 0, 0, 0]
        self.assertEqual(
            self.screening.evaluate_initial_screen(arr), [
                "DASS-21A", "DASS-21S"])

    # def test_initial_screen(self, bot, update):
    #     self.assertEqual(self.screening.initial_screen(bot, update),0)

    # def test_build_question(self):
    #     question_index = 1
    #     self.assertEqual(self.screening.build_question(question_index), )
    # def test_build_button_markup(self):
    #     question_index = 1
    #     self.assertEqual(self.screening.build_button_markup(question_index),)

    # @patch('bot.communication.Communication')
    # @patch("telegram.Bot")
    # def test_button_clicked(self, comm, bot):
    #     self.tgbot.comm = comm
    #     self.assertEqual(self.screening.button_clicked(bot, bot), )


if __name__ == "__main__":
    unittest.main()
