import os
from time import sleep
import json
import configparser

import sys, os

try:
    sys.path.insert(0, os.path.join(os.getcwd(),"sancus"))
except:pass

from functions.consoleColours import *

class main():
    
    from functions.mongoDbAPI import connectionDb
    Version = connectionDb().get_config_config()["version"]


    from lib.bot import bot
    bot.run(Version)

if __name__ == "__main__":
    main()