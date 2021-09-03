import os
from time import sleep
import json
import configparser

from functions.consoleColours import *

###Getting Version
config = configparser.ConfigParser()
with open("sancus/data/config.ini", 'r') as configFile:
    config.read_file(configFile)
Version = config.get("DEFAULT", "version")


updateAsk = input("Do you want to update your packages?\n ")
if updateAsk.lower() in ["yes", "y"]:
    os.system("py update.script.py")

###Launching bot
try:
    print(f"{colours.PURPLE}Starting bot.......{colours.ENDC}")
    from lib.bot import bot
    bot.run(Version)

except ModuleNotFoundError:
    print(f"{colours.WARNING}Module not detected, \n{colours.OKCYAN} Installing modlues now {colours.ENDC}")
    os.system("py install-script.py")
    print(f"{colours.PURPLE}Starting bot.......{colours.ENDC}")
    from lib.bot import bot
    bot.run(Version)

except TypeError as error:
    print(colours.FAIL, error, colours.ENDC)

except:
    try:
        print(f"{colours.WARNING}Trying to start bot, attepmt #2.......{colours.ENDC}")
        from lib.bot import bot
        bot.run(Version)

    except:
        print(colours.FAIL, "Failed to start", colours.ENDC)

from lib.bot import bot
bot.run(Version)