import logging


def getLogger(name):
    # Create file handler which logs even debug messages
    FileHandler = logging.FileHandler('{}.txt'.format(name))
    FileHandler.setLevel(logging.INFO)

    # create console handler with a higher log level
    ConsoleHandler = logging.StreamHandler()
    ConsoleHandler.setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(FileHandler)
    logger.addHandler(ConsoleHandler)

    return logger
