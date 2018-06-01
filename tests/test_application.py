import unittest
import os
import sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.application import Application, retrieve_default


class TestBotBasics(unittest.TestCase):

    def setUp(self):
        self.tgbot = Application(retrieve_default()['token'])

    def test_if_retrieve_default_works(self):
        self.assertEqual(type(dict(retrieve_default())), type({}))

    def test_if_retrieve_default_has_token(self):
        self.assertTrue('token' in list(retrieve_default()))

    def test_if_retrieve_without_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            retrieve_default("fail.ini")

    def test_if_bot_is_unbchatbot(self):
        """
        Check if bot being initialized is truly the unbchatbot
        """
        self.assertEqual(self.tgbot.verify_bot(), ('unbchatbot', 330147863))


if __name__ == '__main__':
    unittest.main()