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
        self.FILE_PATH = "./bot_test/dialogs"
        os.makedirs(self.FILE_PATH)

    def tearDown(self):
        self.linter = None
        os.removedirs(self.FILE_PATH)

    # def test_if_linter_finds_yml(self):
    #     """
    #     Check if linter identifies json file on test directory with files
    #     """
    #     filename = "dialogs.json"
    #     FPATH = "{0}/{1}".format(self.FILE_PATH, filename)
    #     with open(FPATH, "w") as test_json:
    #         test_json.write("[\"test\"]")
    #
    #     self.assertEqual(self.linter.check_files(path=self.FILE_PATH), 0)
    #     os.remove(FPATH)


if __name__ == '__main__':
    unittest.main()
