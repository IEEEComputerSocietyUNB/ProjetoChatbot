import os
from configparser import ConfigParser


def retrieve_default(filename='config.ini'):
    """
    Function to retrieve all informations from token file.
    Usually retrieves from config.ini
    """
    try:
        FILE_PATH = str(os.getcwd()) + '/bot/' + filename
        config = ConfigParser()
        with open(FILE_PATH) as config_file:
            config.read_file(config_file)
        return(config['DEFAULT'])
    except FileNotFoundError:
        config_information = '[DEFAULT]\ntoken=\nuser=\npass='
        with open('config.ini', mode='w') as config_file:
            config_file.write(config_information)
        raise FileNotFoundError
