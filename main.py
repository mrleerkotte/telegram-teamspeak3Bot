#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

import logging
import configparser
from teamspeakActions import teamspeakActions
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

config = configparser.ConfigParser()
config.sections()

config.read('teamspeakBot.conf')

TELEGRAM_API_TOKEN = config['Telegram']['TELEGRAM_API_TOKEN']
TEAMSPEAK_QUERY_USER = config['Teamspeak']['TEAMSPEAK_QUERY_USER']
TEAMSPEAK_QUERY_PASS = config['Teamspeak']['TEAMSPEAK_QUERY_PASS']
TEAMSPEAK_QUERY_SERVER = config['Teamspeak']['TEAMSPEAK_QUERY_SERVER']


def start(bot, update):
    keyboard = [[InlineKeyboardButton("TS Clients", callback_data='1')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    teamspeakClients = teamspeakActions.getClients(TEAMSPEAK_QUERY_USER, TEAMSPEAK_QUERY_PASS, TEAMSPEAK_QUERY_SERVER)

    bot.editMessageText(text="%s" % teamspeakClients,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        parse_mode=ParseMode.MARKDOWN)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Create the Updater and pass it your bot's token.
updater = Updater(token=TELEGRAM_API_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
