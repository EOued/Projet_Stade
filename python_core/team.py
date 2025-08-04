from python_core.default import FieldPortion
from python_core.field import Field


class Team:
    def __init__(
        self,
        name: str,
        fieldportion: FieldPortion,
        priority: int,
        periods: list[list[tuple[int, int]]],
    ):
        self.name: str = name
        self.fieldportion: FieldPortion = (
            fieldportion
            if isinstance(fieldportion, FieldPortion)
            else FieldPortion(fieldportion)
        )
        self.priority = priority
        self.periods = periods
        self.locked_periods = [0, 0, 0, 0, 0, 0, 0]
        self.fields = [{}, {}, {}, {}, {}, {}, {}]

    def reset(self):
        self.fields = [{}, {}, {}, {}, {}, {}, {}]
        self.locked_periods = [0, 0, 0, 0, 0, 0, 0]

    def add_field(self, day, field, period):
        if field not in self.fields[day]:
            self.fields[day][field] = 0
        self.fields[day][field] ^= period
        self.locked_periods[day] ^= period

    def print(self):
        """
        Prints the team.
        """
        print(f'"{self.name}":')
        print(f"\tField portion: {self.fieldportion.name}")
        print(f"\tPriority: {self.priority}")
        return
