import unittest
import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from linter.linter import Linter


class TestLinterClass(unittest.TestCase):
    """
    Test linter methods and help check which patterns must be verified.
    """

    def setUp(self):
        self.linter = Linter()
        self.FILE_PATH = "./bot_test/dialogs"
        os.makedirs(self.FILE_PATH)

    def tearDown(self):
        shutil.rmtree("./bot_test", ignore_errors=True)

    def test_linter_constructor(self):
        self.assertEqual(self.linter.file_count, 0)
        self.assertEqual(self.linter.directories, [])

    def test_if_linter_finds_yml(self):
        """
        Check if linter identifies yml file on test directory with files
        """
        filename = "dialogs.yml"
        FPATH = "{0}/{1}".format(self.FILE_PATH, filename)
        with open(FPATH, "w") as test_json:
            test_json.write("categories:\n- Test")
        expected_result = {"dialogs": ["dialogs.yml"]}

        self.assertEqual(
            self.linter.check_folders(path="./bot_test/"),
            expected_result
        )
        os.remove(FPATH)

    def test_if_linter_works_on_empty_folders(self):
        """
        Check if linter works on test directory without files
        """

        self.assertEqual(self.linter.check_folders(path="./bot_test/"), {})

    def test_if_linter_works_on_files_only(self):
        """
        Check if linter works on test directory with only files
        """
        os.rmdir(self.FILE_PATH)
        filename = "dialogs.yml"
        FPATH = "{0}/{1}".format("./bot_test/", filename)

        with open(FPATH, "w") as test_json:
            test_json.write("categories:\n- Test")

        self.assertEqual(self.linter.check_folders(path="./bot_test/"), {})

    # def test_if_linter_warns(self):
    #     filename = "dialogs.yml"
    #     FPATH = "{0}/{1}".format(self.FILE_PATH, filename)
    #     with open(FPATH, "w") as test_json:
    #         test_json.write("categories:\n- Test")
    #     self.assertEqual(self.linter.check_pronouns_on_dialogs(), False)


if __name__ == "__main__":
    unittest.main()
