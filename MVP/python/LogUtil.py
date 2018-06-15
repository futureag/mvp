'''Wrapper for the Python Logger to add standard MVP customization
'''
import logging
from logging.handlers import TimedRotatingFileHandler

def get_logger(name="MvpLogger"):
    """Create and return a logger

    Builds a Python logger to:
      log everything to the screen
      WARNING to a rotating file

    Args:
        name: The name given to the logger
    Returns:
        logger: the logger object
    Raises:
        None
    """
    fname = "/home/pi/MVP/logs/mvp.log"
    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    # build logger
    logger = logging.getLogger('mvp.'+name)
    logger.setLevel(logging.DEBUG)

    # Rotating File handler - only send WARNING and above
    file_handler = TimedRotatingFileHandler(fname, when="d", interval=30, backupCount=3)
    file_handler.setLevel(logging.WARNING)
    formater = logging.Formatter(fmt)
    file_handler.setFormatter(formater)

    # Screen handler - display all (DEBUG, defaults above)
    screen_handler = logging.StreamHandler()
    screen_formater = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    screen_handler.setFormatter(screen_formater)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)

    return logger


def test():
    """Test of the logger
    A light weight test, less complex that PyUnit

    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    print "Test MvpLogger"
    print "Getting logger"
    logger = get_logger()
    print "Testing output"
    logger.debug("Something happening here")
    logger.info("Just thought you might like to know")
    logger.warning("Will Robinson ...")

if __name__ == "__main__":
    test()
