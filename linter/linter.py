import os

class Linter:
    def __init__(self):
        self.file_count = 0
        self.directories = []

    def check_files(self, path="./bot/dialogs", idfile="dialogs.json"):
        def find_id_file():
            with open("{}/{}".format(path, idfile), 'r') as current_file:
                topics = current_file.read()
                print(topics)
                # self.directories.append
        #
        # number_of_files = 0
        # for item in os.listdir():
        #     if
        find_id_file()
        return 0
