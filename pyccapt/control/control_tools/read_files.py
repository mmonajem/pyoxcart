import json


def read_json_file(json_file_path):
	"""
	Read data from a JSON file.

	This function reads and loads data from a JSON file and returns the data as a dictionary.

	Args:
		json_file_path (str): The path to the JSON file.

	Returns:
		dict: The data loaded from the JSON file as a dictionary.
	"""
	with open(json_file_path) as file:
		data = json.load(file)
		return data
