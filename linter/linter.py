import os
from os import listdir
from os.path import isdir, isfile, join

class Linter:
    def __init__(self):
        self.file_count = 0
        self.directories = []

    def check_folders(self, path="bot/dialogs"):
        """Checks for specified dialog folders"""
        all_folders = [
            folder for folder in listdir(path) if isdir(join(path, folder))
        ]
        yml_paths = {}
        for folder in all_folders:
            full_path = "{0}/{1}".format(path, folder)
            all_files = [
                file for file in listdir(full_path) \
                    if isfile(join(full_path, file))
            ]
            only_yml = [f for f in all_files if f[-3:] == "yml"]
            yml_paths[folder] = only_yml
        return yml_paths

    # def check_pronouns_on_dialogs(self, folder):
    #     pass

    # def check_switched_words_on_dialogs(self):
    #     pass
    #
    # def check_for_special_characters(self):
    #     pass
    #
    # def check_for_everything(self):
    #     pass
