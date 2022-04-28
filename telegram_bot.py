from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram.utils.request import Request
import requests
import telegram

class TelegramBot:
    def __init__(self):
        self.token = 'YOUR_TOKEN'
        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher
        self.chat_id = "YOUR_CHAT_ID"

    def sendMessage(self, message):
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + str(self.chat_id) + '&parse_mode=Markdown&text=' + message
        requests.get(send_text)