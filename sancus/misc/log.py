import logging as pyLogging
import os
import dotenv
import discord

dotenv.load_dotenv('.env')


class CustomFormatter(pyLogging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    green = "\033[92m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        pyLogging.DEBUG: grey + format + reset,
        pyLogging.INFO: green + format + reset,
        pyLogging.WARNING: yellow + format + reset,
        pyLogging.ERROR: red + format + reset,
        pyLogging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = pyLogging.Formatter(
            log_fmt,  datefmt='%d-%b-%y %H:%M:%S')
        return formatter.format(record)


def logging(name: str, level = pyLogging.WARNING, file : bool = False) -> pyLogging:

    logger = pyLogging.getLogger(name)
    logger.setLevel(level)

    c_handler = pyLogging.StreamHandler()
    c_handler.setFormatter(CustomFormatter())
    logger.addHandler(c_handler)


    # Create formatters and add it to handlers
    if file:
        f_handler = pyLogging.FileHandler('logs/latest.log', 'w')
        f_format = pyLogging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S')
        f_handler.setFormatter(f_format)    
        f_handler.setLevel(pyLogging.WARNING)
        logger.addHandler(f_handler)
    
    return logger
