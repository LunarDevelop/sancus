import os
from time import sleep
import json
import configparser

import sys, os

sys.path.append(os.path.join(os.getcwd(),"sancus"))
sys.path.append(os.getcwd())

from functions.consoleColours import *

class main():
    
    from functions.mongoDbAPI import connectionDb
    Version = connectionDb().get_config_config()["version"]


    from lib.bot import bot
    bot.run(Version)

if __name__ == "__main__":
    main()