import json

def read_json_file(jsonFile):
    with open(jsonFile) as file:
        data = json.load(file)
        return data

def read_text_file(textFile):
    pass

def read_csv_file(csvFile):
    pass