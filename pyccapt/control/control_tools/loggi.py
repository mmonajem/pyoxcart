import logging


def logger_creator(script_name, variables, log_name, path=None):
	"""
	Create and configure a logger object for logging.

	This function uses the native Python logging library to create a logger object
	that can be used to log statements of different levels.

	Args:
		script_name (str): The name of the script using the logger.
		variables (object): An object containing relevant variables.
		log_name (str): The name of the log file.
		path (str, optional): The path to the log directory. Defaults to None.

	Returns:
		logging.Logger: The configured logger object.
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
