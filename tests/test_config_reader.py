import os
import sys
import unittest
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.config_reader import retrieve_default


class TestConfigBasics(unittest.TestCase):
    @unittest.skipUnless(os.path.exists("./bot/config.ini"),
                         "Configuration file not found")
    def test_if_retrieve_default_works(self):
        self.assertEqual(type(dict(retrieve_default())), type({}))

    @unittest.skipUnless(os.path.exists("./bot/config.ini"),
                         "Configuration file not found")
    def test_if_retrieve_default_has_token(self):
        self.assertTrue('token' in list(retrieve_default()))

    @unittest.skipUnless(os.path.exists("./bot/config.ini"),
                         "Configuration file not found")
    def test_if_retrieve_without_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            retrieve_default("fail.ini")


if __name__ == '__main__':
    unittest.main()
