import logging as pyLogging
import os
import dotenv
import discord

dotenv.load_dotenv('.env')

pyLogging.addLevelName(pyLogging.DEBUG+5, "GuildLogging")

GUILDLOGGING = pyLogging.DEBUG+5


class CustomFormatter(pyLogging.Formatter):

    green = "\033[92m"
    black = "\u001b[30m"
    red = "\u001b[31m"
    bold_red = "\x1b[31;1m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"
    grey = "\x1b[38;20m"
    
    brightBlack = "\u001b[30;1m"
    brightRed = "\u001b[31;1m"
    brightGreen = "\u001b[32;1m"
    brightYellow = "\u001b[33;1m"
    brightBlue = "\u001b[34;1m"
    brightMagenta = "\u001b[35;1m"
    brightCyan = "\u001b[36;1m"
    brightWhite = "\u001b[37;1m"
    
    reset = "\u001b[0m"
    
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        pyLogging.DEBUG: grey + format + reset,
        pyLogging.INFO: green + format + reset,
        pyLogging.WARNING: yellow + format + reset,
        pyLogging.ERROR: red + format + reset,
        pyLogging.CRITICAL: bold_red + format + reset,
        GUILDLOGGING: cyan + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = pyLogging.Formatter(
            log_fmt,  datefmt='%d-%b-%y %H:%M:%S')
        return formatter.format(record)


def logging(
    name: str, 
    level=pyLogging.WARNING, 
    file: bool = False, 
    fileName: str = "latest", 
    fileMode: str = 'w'
    ) -> pyLogging:

    logger = pyLogging.getLogger(name)
    logger.setLevel(level)

    c_handler = pyLogging.StreamHandler()
    c_handler.setFormatter(CustomFormatter())
    logger.addHandler(c_handler)

    # Create formatters and add it to handlers
    if file:
        f_handler = pyLogging.FileHandler(f'logs/{fileName}.log', fileMode)
        f_format = pyLogging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S')
        f_handler.setFormatter(f_format)
        f_handler.setLevel(level)
        logger.addHandler(f_handler)

    return logger
