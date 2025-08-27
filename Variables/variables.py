from enum import Enum, auto
from types import NoneType
from pathlib import Path
import yaml, sys, os

Var = Enum(
    "Var",
    [
        "VERSION",
        "AV_LANGUAGES",
        "LANGUAGE_NAME",
        "TITLE",
        "TEAMS",
        "FIELDS",
        "FILE",
        "OPEN",
        "SAVE",
        "SAVEAS",
        "EXTRACTPDF",
        "EXECUTE",
        "IDENTIFIER",
        "TYPE",
        "PERIOD",
        "PORTION",
        "PRIORITY",
        "DAY",
        "HOUR",
        "DURATION",
        "START",
        "END",
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "SUNDAY",
        "NAME",
        "NATURAL",
        "SYNTHETIC",
        "WHOLE",
        "HALF",
        "QUARTER",
        "ADD",
        "DELETE",
        "FIRST_FIT",
        "BEST_FIT",
        "WORST_FIT",
        "AM",
        "PM",
        "INSERT_BEFORE",
        "INSERT_AFTER",
        "SUPRESS",
        "EXECUTE_NO_DATA",
        "EXECUTE_SAVE_DATA",
        "EXECUTE_PERIOD_FAIL",
        "EXECUTE_SUCCESS",
        "LOAD_FILE_MODIFIED",
        "BAD_SCHEDULE",
    ],
    start=0,
)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundle_dir = Path(sys._MEIPASS)
    else:
        bundle_dir = Path(__file__).parent.parent
    return os.path.join(bundle_dir, relative_path)


def _variable(name: Var):
    with open(resource_path("__VARIABLES__.yaml"), "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data[name.name]


Languages = Enum("Languages", _variable(Var.AV_LANGUAGES), start=0)
print(Languages.__members__)


def variable(name: Var, language: str | NoneType = None):
    if language is None:
        return _variable(name)
    else:
        return _variable(name)[Languages[language].value][language]
