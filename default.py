from enum import Enum

GAMEFORMAT = ["Whole Field", "Half Field", "Quarter Field"]
FIELDTYPE = ["Natural Field", "Synthetic Field"]

SETTINGS_FILE = "settings.json"
TEAMS_FILE = "teams.json"
FIELDS_FILE = "fields.json"

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class FieldPortion(Enum):
    WHOLE = 0
    HALF = 1
    QUARTER = 2

class FieldType(Enum):
    NATURAL = 0
    SYNTHETIC = 1
    QUARTER = 2
