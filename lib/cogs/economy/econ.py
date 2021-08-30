import json

import discord

from lib.bot import bot


def open_econ():
    with open("./data/econ.json") as f:
        return json.load(f)


def save_econ(data):
    with open("./data/econ.json", 'w') as f:
        json.dump(data, f, indent=4)


def bank_add_user(userID):
    data = open_econ()

    if str(userID) not in data['bank']:
        data['bank'][userID] = {
            'bank': 0,
            'wallet': 0
        }

    save_econ(data)


def shop_add_user(userID):
    data = open_econ()

    if str(userID) not in data['shop']:
        data['shop'][userID] = {
            'inventory': {},
            'amount': 0
        }

    save_econ(data)


class bank():

    def __init__(self, memberID):
        self.member = memberID
        self.user = bot.oldConfig.user(str(memberID))

    def get_balance(self):
        return self.user['bank'], self.user['wallet']

    def add_wallet_money(self, amount):
        total = int(self.user['wallet']) + amount
        bot.oldConfig.set_user(self.member, 'wallet', total)

    def add_bank_money(self, amount):
        total = int(self.user['bank']) + amount
        bot.oldConfig.set_user(self.member, 'bank', total)

    def remove_wallet_money(self, amount):
        total = int(self.user['wallet']) - amount
        bot.oldConfig.set_user(self.member, 'wallet', total)

    def remove_bank_money(self, amount):
        total = int(self.user['bank']) + - amount
        bot.oldConfig.set_user(self.member, 'bank', total)
