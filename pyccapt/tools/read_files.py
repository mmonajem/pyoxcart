import json


def read_json_file(jsonFile):
    with open(jsonFile) as file:
        data = json.load(file)
        return data


