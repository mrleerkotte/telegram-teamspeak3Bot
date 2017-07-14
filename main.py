#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
import re
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from TeamspeakActions import TeamspeakActions

config = configparser.ConfigParser()
config.sections()

config.read('teamspeakBot.conf')

telegram_api_token = config['Telegram']['telegram_api_token']
teamspeak_query_user = config['Teamspeak']['teamspeak_query_user']
teamspeak_query_pass = config['Teamspeak']['teamspeak_query_pass']
teamspeak_query_server = config['Teamspeak']['teamspeak_query_server']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def telegram_help(bot, update):
    update.message.reply_text('Help!')


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    query = update.inline_query.query

    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Get Clients",
                                            input_message_content=InputTextMessageContent(
                                                TeamspeakActions.get_clients(teamspeak_query_user, teamspeak_query_pass,
                                                                             teamspeak_query_server),
                                                parse_mode=ParseMode.MARKDOWN)))

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Get Banlist",
                                            input_message_content=InputTextMessageContent(
                                                TeamspeakActions.get_bans(teamspeak_query_user, teamspeak_query_pass,
                                                                          teamspeak_query_server),
                                                parse_mode=ParseMode.MARKDOWN)))

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Kick all clients",
                                            input_message_content=InputTextMessageContent(
                                                "*He'j het verstaand in'n tuk zit'n ofzo? Grapjas*",
                                                parse_mode=ParseMode.MARKDOWN)))

    update.inline_query.answer(results, cache_time=0)


def error(bot, update, telegram_error):
    logger.warning('Update "%s" caused telegram_error "%s"' % (update, telegram_error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_api_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("telegram_help", telegram_help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def translate(m_string, char):
    return m_string.translate(None, "i")


if __name__ == '__main__':
    main()
