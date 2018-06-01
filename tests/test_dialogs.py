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
    """
    Tests on dialogs are needed to verify that the bot has no weird dialog.
    Important due to seriousness of emotional triggers.
    """

    def setUp(self):
        self.comm = Communication()

    def test_if_comm_answers_greetings(self):
        """
        Check if communication answers greetings appropriately
        """
        self.assertEqual(self.comm.respond("oi"), "Olá, tudo bom?")

    def test_if_comm_answers_greetings2(self):
        """
        Check if communication answers greetings appropriately
        """
        self.assertEqual(self.comm.respond("Olá"), "Olá, tudo bom?")


if __name__ == '__main__':
    unittest.main()
