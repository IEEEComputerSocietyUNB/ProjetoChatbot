import unittest
import os
from bot.bot import Chatbot
from bot.bot import retrieve_token


class TestBotBasics(unittest.TestCase):

    def setUp(self):
        self.bot = Chatbot(retrieve_token())

    def test_nothing(self):
        """
        Check if testing is really ocurring
        """
        pass

    def test_if_bot_is_unbchatbot(self):
        """
        Check if bot being initialized is truly the unbchatbot
        """
        self.assertEqual(self.bot.verify_bot(), ('unbchatbot', 330147863))

    def test_if_bot_logging_works(self):
        """
        Check for bot logging
        """
        # self.assertEqual(self.bot.make_log(), 'test')
        pass

    def test_if_start_command_works(self):
        """
        Check for start command veracity
        """
        pass


# class TestGreetingDialogs(unittest.TestCase):


if __name__ == '__main__':
    unittest.main()
