import logging
import os
import sys
from bot.bot import Chatbot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN')
    NAME = os.environ.get('NAME')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Initialize bot
    bot = Chatbot(TOKEN)

    # Add handlers #TODO: remove handlers and leave them on bot.py
    bot.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    bot.dispatcher.add_error_handler(error)

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
