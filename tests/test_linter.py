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

    def tearDown(self):
        self.linter = None

    def test_if_linter_opens_all_yml(self):
        """
        Check if linter identifies all yml files on test directory
        """
        FILE = "test.yaml"
        FILE_PATH = "bots/dialog/tests"
        os.makedirs(FILE_PATH)
        FPATH = FILE_PATH + "/" + FILE
        with open(FPATH, "w") as file:
            file.write("Hello World")
        self.assertEqual(self.linter.check_files(path=FILE_PATH), 1)
        os.remove(FPATH)
        os.removedirs(FILE_PATH)


if __name__ == '__main__':
    unittest.main()
