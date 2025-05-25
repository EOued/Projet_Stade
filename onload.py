import json
from default import SETTINGS_FILE, TEAMS_FILE

settings_config = None
teams_config = None


def open_file(openSettings: bool = False):
    filename = SETTINGS_FILE if (openSettings) else TEAMS_FILE
    with open(filename, "r") as file:
        return json.load(file)


def onload():
    global settings_config
    global teams_config
    settings_config = open_file(True)
    teams_config = open_file()
