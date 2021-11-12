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
    ###Getting Version
    config = configparser.ConfigParser()
    with open("sancus/data/config.ini", 'r') as configFile:
        config.read_file(configFile)
    Version = config.get("DEFAULT", "version")

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

if __name__ == "__main__":
    main()