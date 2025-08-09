from enum import Enum
import yaml
from utils.utils import resource_path


class Var(Enum):
    VERSION = 0
    TITLE = 1


def variable(name: Var):
    with open(resource_path("__VARIABLES__.yaml"), "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data[name.name]
