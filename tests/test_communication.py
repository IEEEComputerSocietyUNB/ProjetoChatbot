import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.communication import Communication


class TestBotCommunication(unittest.TestCase):

    def setUp(self):
        self.comm = Communication()

    def test_if_comm_answers(self):
        """
        Check if communication method answers appropriately
        """
        self.assertEqual(self.comm.respond("Oi"), "Olá, tudo bom?")

    def test_if_comm_removes_accents_and_upper_letters(self):
        """
        Check if communication method cleans
        """
        # Remove upper letters
        self.assertEqual(self.comm.clean("ABCDEF"), "abcdef")

    def test_if_comm_removes_abbreviation(self):
        self.assertEqual(self.comm.clean("cadê vc"), "cadê você")
        self.assertEqual(self.comm.clean("vc é um chato"), "você é um chato")

    def test_if_comm_raises_error_when_abbr_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.comm.clean("teste", file="fail.txt")


if __name__ == '__main__':
    unittest.main()
