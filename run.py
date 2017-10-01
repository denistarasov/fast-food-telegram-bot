from telegram.ext import CommandHandler
from telegram.ext import Updater
import logging
import os
from construct_map import construct_map

TOKEN = ""


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


# def echo(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def send_constructed_map(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=construct_map(update.message.text))


logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                        filename='main.log',
                        level=logging.DEBUG)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
# from telegram.ext import CommandHandler
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# from telegram.ext import MessageHandler, Filters
# echo_handler = MessageHandler(Filters.text, echo)
# dispatcher.add_handler(echo_handler)
from telegram.ext import MessageHandler, Filters
construct_map_handler = MessageHandler(Filters.text, send_constructed_map)
dispatcher.add_handler(construct_map_handler)

# caps_handler = CommandHandler('caps', caps, pass_args=True)
# dispatcher.add_handler(caps_handler)

updater.start_polling()
