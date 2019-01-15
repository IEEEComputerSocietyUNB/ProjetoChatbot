import unittest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from bot.communication import Communication, switch_abbreviations, remove_words
from bot.watson import Watson


class TestBotCommunication(unittest.TestCase):
    def setUp(self):
        self.comm = Communication(train=False, use_watson=False)

    def tearDown(self):
        self.comm = None

    def test_if_comm_answers(self):
        """
        Check if communication method answers appropriately
        """
        self.comm = Communication()
        self.assertEqual(self.comm.respond("Olá"), "Olá, tudo bom?")

    def test_if_comm_removes_accents_and_upper_letters(self):
        """
        Check if communication method cleans.
        """
        # Remove upper letters
        self.assertEqual(self.comm.clean("ABCDEF"), "abcdef")

    def test_if_comm_raises_error_when_abbr_is_not_a_list(self):
        with self.assertRaises(FileNotFoundError):
            switch_abbreviations("teste", directory="fail.txt")

    def test_if_comm_raises_error_when_abbr_not_found(self):
        with self.assertRaises(FileNotFoundError):
            switch_abbreviations("teste", directory=["fail.txt"])

    def test_comm_switches_abbreviations(self):
        self.assertEqual(
            switch_abbreviations("vc está aki"), "você está aqui"
        )

    def test_if_comm_raises_error_when_rm_is_not_a_list(self):
        with self.assertRaises(FileNotFoundError):
            remove_words("teste", directory="fail")

    def test_if_comm_raises_error_when_rm_not_found(self):
        with self.assertRaises(FileNotFoundError):
            remove_words("teste", directory=["fail"])

    def test_comm_removes_pronouns_and_articles(self):
        self.assertEqual(
            remove_words("conte uma piada"),
            "conte piada"
        )

    def test_if_comm_clean_returns_clean_messages(self):
        self.assertEqual(self.comm.clean("cadê vc"), "cadê você")
        self.assertEqual(self.comm.clean("vc é um chato"), "você é chato")


if __name__ == "__main__":
    unittest.main()
