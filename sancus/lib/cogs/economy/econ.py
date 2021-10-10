import json
from functions.objects import userObject

import discord

from lib.bot import bot


class bank():

    def __init__(self, client : bot, guildid, memberID):
        self.user = None
        self.member = memberID
        self.client = client
        if str(memberID) in client.users_:
            self.user = client.users_[str(memberID)]
            self.banks = client.users_[str(memberID)]["banks"]
            
            if str(guildid) not in self.banks:
                self.banks[str(guildid)] = {"bank":0, "wallet":0}
                self.client.config.put_config_user(
                    self.member, {"banks": self.banks})
        
        else:
            self.user = {
                "id" : memberID,
                "banks" : {str(guildid): {"bank":0, "wallet":0}}
            }
            self.banks = self.user["banks"]
            user = userObject(memberID, self.banks)
            self.client.config.post_config_user(user)
            

    def get_balance(self, guildid):
        return self.banks[str(guildid)]['bank'], self.banks[str(guildid)]["wallet"]

    def add_wallet_money(self, guildid, amount):
        total = int(self.banks[str(guildid)]['wallet']) + amount
        self.banks[str(guildid)]["wallet"] = total                
        self.client.config.put_config_user(self.member, {"banks":self.banks})
        self.client.users_ = self.client.config.get_config_users()
        
    def add_bank_money(self, guildid, amount):
        total = int(self.banks[str(guildid)]['bank']) + amount
        self.banks[str(guildid)]["bank"] = total
        self.client.config.put_config_user(self.member, {"banks": self.banks})
        self.client.users_ = self.client.config.get_config_users()

    def remove_wallet_money(self, guildid, amount):
        total = int(self.banks[str(guildid)]['wallet']) - amount
        self.banks[str(guildid)]["wallet"] = total
        self.client.config.put_config_user(self.member, {"banks": self.banks})
        self.client.users_ = self.client.config.get_config_users()

    def remove_bank_money(self, guildid, amount):
        total = int(self.banks[str(guildid)]['bank']) - amount
        self.banks[str(guildid)]["bank"] = total
        self.client.config.put_config_user(self.member, {"banks": self.banks})
        self.client.users_ = self.client.config.get_config_users()
