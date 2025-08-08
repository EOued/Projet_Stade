from enum import Enum
import yaml


class Var(Enum):
    VERSION = 0
    TITLE = 1


def variable(name: Var):
    with open("__VARIABLES__.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data[name.name]
