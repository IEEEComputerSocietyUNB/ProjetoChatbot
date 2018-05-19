import logging
import os
import sys
from bot.bot import Chatbot
from telegram.ext import Updater, CommandHandler, MessageHandler,


if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN')
    NAME = os.environ.get('NAME')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Initialize bot
    bot = Chatbot(TOKEN)

    # Start the webhook
    bot.updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN
    )
    bot.updater.bot.set_webhook(
        "https://{}.herokuapp.com/{}".format(NAME, TOKEN)
    )
    bot.updater.idle()
