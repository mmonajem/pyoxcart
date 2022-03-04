"""
This is the main script is load the GUI base on the configuration file.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

import logging

from apt_pycontrol.tools import variables


def get_logging():
    """
    The function is used to instantiate and configure logger object for logging.
    The function use python native logging library.

    Attributes:
        Does not accept any arguments
    Returns:
        Returns the logger object which could be used log statements of following level:
            1. INFO: "Useful information"
            2. WARNING: "Something is not right"
            3. DEBUG: "A debug message"
            4. ERROR: "A Major error has happened."
            5. CRITICAL "Fatal error. Cannot continue"
    """

    # Gets or creates a logger
    logger = logging.getLogger(__name__)
    # set log level
    logger.setLevel(logging.INFO)
    # define file handler and set formatter
    # Reads file path from imported "variables" file
    file_handler = logging.FileHandler(variables.path + '\\logfile.log', mode='w')
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)
    # add file handler to logger
    logger.addHandler(file_handler)
    return logger
