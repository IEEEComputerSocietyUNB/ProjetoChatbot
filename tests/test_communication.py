import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.communication import Communication


class TestBotDialogs(unittest.TestCase):

    def setUp(self):
        self.comm = Communication()

    def test_if_comm_answers_greetings(self):
        """
        Check if communication answers greetings appropriately
        """
        self.assertEqual(self.comm.respond("Oi"), "Olá, tudo bom?")

    # def test_if_message_cleaning_works(self):
    #     self.assertEqual(self.comm.clean_message("Olá"), "ola")


if __name__ == '__main__':
    unittest.main()
