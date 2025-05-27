import json
from default import SETTINGS_FILE, TEAMS_FILE, FIELDS_FILE

settings_config = None
teams_config = None
fields_config = None


def open_file(fileIndex: int):

    filename = [SETTINGS_FILE, TEAMS_FILE, FIELDS_FILE][fileIndex]
    with open(filename, "r") as file:
        return json.load(file)


def load():
    global settings_config
    global teams_config
    global fields_config
    settings_config = open_file(0)
    teams_config = open_file(1)
    fields_config = open_file(2)
