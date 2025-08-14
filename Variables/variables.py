from enum import Enum, auto
from types import NoneType
import yaml
from utils.utils import resource_path


class Var(Enum):
    VERSION = auto()
    AV_LANGUAGES = auto()
    LANGUAGE_NAME = auto()
    TITLE = auto()
    TEAMS = auto()
    FIELDS = auto()
    FILE = auto()
    OPEN = auto()
    SAVE = auto()
    SAVEAS = auto()
    EXECUTE = auto()


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
        print(_variable(name))
        return _variable(name)[Languages[language].value][language]
