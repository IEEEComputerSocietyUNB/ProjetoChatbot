import os
import json
import time
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from bot.config_reader import retrieve_default

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from bot.watson import Watson


class Communication:
    def __init__(self, use_watson=False, train=True):
        """
        Generator for dealing with most messages the bot will receive
        from user.
        """
        self.comm = ChatBot(
            "Comms",
            response_selection_method=get_random_response,
            logic_adapters=[
                {"import_path": "chatterbot.logic.BestMatch"},
                {
                    "import_path": "chatterbot.logic.LowConfidenceAdapter",
                    "threshold": 0.65,
                    "default_response": [
                        "Desculpa, mas não entendi sua mensagem.",
                        "Não compreendi, você pode repetir?",
                        "Como é? Não entendi",
                    ],
                },
            ],
            trainer="chatterbot.trainers.ChatterBotCorpusTrainer",
        )
        if train:
            self.comm.train("bot/dialogs/")
        if use_watson:
            try:
                self.watson_analyzer = Watson(
                    retrieve_default("WATSON")["user"],
                    retrieve_default("WATSON")["pass"],
                )
                self.watson_usage = True
            except KeyError:
                # If config.ini doesn't have the user and password:
                # Alert user and end execution
                print("Watson's user and password"
                      "need to be in configuration file.")
                exit()
        else:
            self.watson_usage = False
        self.all_texts = ""

    def respond(self, message):
        """
        Receive message from user and returns corresponding answer.
        """
        # if string isnt empty concatenate with space
        if self.all_texts:
            self.all_texts += " " + message
        else:
            self.all_texts = message

        if len(message) > 50 and self.watson_usage:
            analysis = self.watson_analyzer.get_analysis(message)

            # Get top 1 categorie
            top_score = analysis["categories"][0]["score"]
            top_label = analysis["categories"][0]["label"]

            # Print the leaf from category tree
            toplabel_index = top_label.rindex("/") + 1
            leaf_category = top_label[toplabel_index:]
            return f"Hmm, você está falando sobre {leaf_category}"
        else:
            return self.comm.get_response(self.clean(message))

    def clean(self, message):
        """
        Remove upper letters and possible abbreviations.

        Might be improved to remove other words, like adverbs
        and some pronouns.
        """
        # message = self.remove_punctuations(message)
        message = self.switch_abbreviations(message)
        message = self.remove_words(message)
        return message.lower()

    def switch_abbreviations(self, message, files=["abbreviations.json"]):
        message = f" {message} "
        try:
            for file in files:
                FILE_PATH = f"{str(os.getcwd())}/bot/dialogs/switches/{file}"
                with open(FILE_PATH, "r") as file:
                    common_abbr = json.load(file)
                    for word in common_abbr:
                        message = message.replace(
                            (f" {word} "), (f" {common_abbr[word]} ")
                        )
            message = message[1:-1]
            return message
        except FileNotFoundError:
            raise FileNotFoundError

    def remove_words(self, message, files=["articles.json", "pronouns.json"]):
        message = f" {message} "
        try:
            for file in files:
                FILE_PATH = f"{str(os.getcwd())}/bot/dialogs/removals/{file}"
                with open(FILE_PATH, "r") as file:
                    removals = json.load(file)

                    for word in removals:
                        message = message.replace((f" {word} "), (" "))
            message = message[1:-1]
            return message
        except FileNotFoundError:
            raise FileNotFoundError
