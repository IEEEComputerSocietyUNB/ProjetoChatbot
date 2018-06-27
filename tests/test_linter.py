import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from linter.linter import Linter


class TestLinter(unittest.TestCase):
    """
    Test linter methods and help check which patterns must be verified.
    """

    def setUp(self):
        self.linter = Linter()
        self.FILE = "test.yml"
        self.FILE_PATH = "./bot_test/dialog/tests"
        os.makedirs(self.FILE_PATH)

    def tearDown(self):
        self.linter = None
        os.removedirs(self.FILE_PATH)

    def test_if_linter_finds_one_yml(self):
        """
        Check if linter identifies one yml file on test directory
        """
        FILE_TOPIC = "/test"
        os.makedirs(self.FILE_PATH + FILE_TOPIC)
        FPATH = "{0}/{1}/{2}".format(self.FILE_PATH, FILE_TOPIC, self.FILE)

        with open(FPATH, "w") as file_test:
            file_test.write("Hello World")
        self.assertEqual(self.linter.check_files(path=self.FILE_PATH), 1)

        os.remove(FPATH)
        os.rmdir(self.FILE_PATH + FILE_TOPIC)

    def test_if_linter_finds_one_yml(self):
        """
        Check if linter identifies all yml files on test directory
        """
        FILE_TOPIC = "/test"
        os.makedirs(self.FILE_PATH + FILE_TOPIC)
        FPATH = []
        FPATH.append("{0}/{1}/{2}".format(self.FILE_PATH, FILE_TOPIC, self.FILE))
        FPATH.append("{0}/{1}/{2}".format(self.FILE_PATH, FILE_TOPIC , "file.yml"))

        for item in FPATH:
            with open(item, "w") as file_test:
                file_test.write("Hello World")
        self.assertEqual(self.linter.check_files(path=self.FILE_PATH), 2)

        for item in FPATH:
            os.remove(item)
        os.rmdir(self.FILE_PATH + FILE_TOPIC)


if __name__ == '__main__':
    unittest.main()
