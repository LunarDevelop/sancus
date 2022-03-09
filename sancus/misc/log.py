import logging
import os
import dotenv
import discord

dotenv.load_dotenv('.env')


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError(
            '{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError(
            '{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError(
            '{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


addLoggingLevel('JOIN EVENT', 11, "join")
addLoggingLevel('LEAVE EVENT', 12, "leave")


class CustomFormatter(logging.Formatter):

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
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        11: cyan + format + reset,
        12: brightMagenta + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(
            log_fmt,  datefmt='%d-%b-%y %H:%M:%S')
        return formatter.format(record)


def logger(
    name: str,
    level=logging.WARNING,
    file: bool = False,
    fileName: str = "latest",
    fileMode: str = 'w'
) -> logging:

    log = logging.getLogger(name)
    log.setLevel(level)

    c_handler = logging.StreamHandler()
    c_handler.setFormatter(CustomFormatter())
    log.addHandler(c_handler)

    # Create formatters and add it to handlers
    if file:
        f_handler = logging.FileHandler(f'logs/{fileName}.log', fileMode)
        f_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S')
        f_handler.setFormatter(f_format)
        f_handler.setLevel(level)
        log.addHandler(f_handler)

    return log
