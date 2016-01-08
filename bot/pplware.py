import tgbot
import requests
import os
import urllib
import json
import feedparser
from twx.botapi import InputFileInfo, InputFile, ChatAction
from tgbot import TGCommandBase



def _latestnews():
    d = feedparser.parse('http://pplware.sapo.pt/feed/')
    return d['items'][0]['link']

class Pplware(tgbot.TGPluginBase):

    def list_commands(self):
        return [
            TGCommandBase('latest', self.latest, 'Get latest news from pplware'),
            TGCommandBase('alertlateston', self.alertlateston, 'Turn on latest news alert',),
            TGCommandBase('alertlatestoff', self.alertlatestoff, 'Turn off latest news alert',),
        ]

    def alertlateston(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        self.save_data(message.chat.id, 'alert', obj=True)
        bot.send_message(message.chat.id, '/alertlatestoff to trun it off')

    def alertlatestoff(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        self.save_data(message.chat.id, 'alert', obj=False)
        bot.send_message(message.chat.id, '/alertlateston to trun it on')

    def latest(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        msg = _latestnews()
        self._cron_alertlatest(bot)
        bot.send_message(message.chat.id, msg).wait()

    def cron_go(self, bot, action, param):
        if action == 'alert':
            self._cron_alertlatest(bot)

    def _cron_alertlatest(self, bot):
        msg = _latestnews()
        lmsg =  self.read_data("latest")
        if lmsg != msg:
            self.save_data("latest", obj=msg)
            self._send_to_users(bot, msg, 'alert')

    def _send_to_users(self, bot, msg, typ):
        for chat in self.iter_data_key_keys(key1="user"):
            if self.read_data(chat, typ):
                bot.send_message(chat, msg).wait()
