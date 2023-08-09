"""
This is the main script for saving the log file of the experiment.
"""

import logging


def logger_creator(script_name, log_name, path=None):
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
    log_creator = logging.getLogger(script_name)
    log_creator.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                                  '%m-%d-%Y %H:%M:%S')

    if path is None:
        file_handler_creator = logging.FileHandler(variables.log_path + '\\' + log_name)
    else:
        file_handler_creator = logging.FileHandler(path + '\\' + log_name)
    file_handler_creator.setLevel(logging.DEBUG)
    file_handler_creator.setFormatter(formatter)
    log_creator.addHandler(file_handler_creator)
    return log_creator
