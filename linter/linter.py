import os

class Linter:
    def __init__(self):
        self.file_count = 0
        self.directories = []

    def check_folders(self, path="./bot/dialogs", idfile="dialogs.json"):
        """Checks for specified dialog and removal folders on dialogs.json"""
        # def find_id_file():
        #     with open("{0}/{1}".format(path, idfile), 'r') as current_file:
        #         topics = current_file.read()
        #         print(topics)
        #         # self.directories.append
        # #
        # # number_of_files = 0
        # # for item in os.listdir():
        # #     if
        # find_id_file()
        return 0

    def check_removed_words_on_dialogs(self):
        pass

    def check_switched_words_on_dialogs(self):
        pass

    def check_for_special_characters(self):
        pass

    def check_for_everything(self):
        pass
